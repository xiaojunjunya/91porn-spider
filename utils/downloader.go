package downloader

import (
	"context"
	"github.com/vbauerster/mpb/v5"
	"github.com/vbauerster/mpb/v5/decor"
	"golang.org/x/net/proxy"
	"html"
	"io"
	"net"
	"net/http"
	"os"
	"path"
	"sync"
	"time"
	_ "net/url"
)

type Worker struct {
	Workers chan int
	Tasks chan *Task
	Wg sync.WaitGroup
	Process *mpb.Progress
	Trans *http.Transport
	SaveDir string
	TempDir string
}

type Task struct {
	Title string
	Url string
}

type progress struct {
	contentLength     float64
	totalWrittenBytes float64
	downloadLevel     float64
}

func (dl *progress) Write(p []byte) (n int, err error) {
	n = len(p)
	dl.totalWrittenBytes = dl.totalWrittenBytes + float64(n)
	currentPercent := (dl.totalWrittenBytes / dl.contentLength) * 100
	if (dl.downloadLevel <= currentPercent) && (dl.downloadLevel < 100) {
		dl.downloadLevel++
	}
	return
}

func IsExist(path string) bool {
	_, err := os.Stat(path)
	return err == nil || os.IsExist(err)
}

func New(workersNum int,socks5Proxy string,saveDir string)(*Worker){
	if !IsExist(saveDir){
		os.Mkdir(saveDir,755)
	}
	if !IsExist( path.Join(saveDir,"tmp") ){
		os.Mkdir(path.Join(saveDir,"tmp"),755)
	}
	var trans *http.Transport
	if socks5Proxy!=""{
		// setup a http client
		dialer, _ := proxy.SOCKS5("tcp", socks5Proxy, nil, proxy.Direct)
		dc := dialer.(interface {
			DialContext(ctx context.Context, network, addr string) (net.Conn, error)
		})

		trans = &http.Transport{
			DialContext: dc.DialContext,
			IdleConnTimeout:       60 * time.Second,
			TLSHandshakeTimeout:   10 * time.Second,
			ExpectContinueTimeout: 1 * time.Second,
		}
	}else {
		trans = &http.Transport{
			IdleConnTimeout:       60 * time.Second,
			TLSHandshakeTimeout:   10 * time.Second,
			ExpectContinueTimeout: 1 * time.Second,
		}
	}
	return &Worker{
		Workers: make(chan int,workersNum),
		Tasks: make(chan *Task,workersNum),
		Trans: trans,
		SaveDir: saveDir,
		TempDir: path.Join(saveDir,"tmp"),
		Process: mpb.New(mpb.WithWidth(64)),
		Wg: sync.WaitGroup{},
	}
}

func (w *Worker)DownloadFile(title string,url string) error {
	tmppath := w.TempDir + "/" + title + ".tmp"
	savePath := w.SaveDir + "/" +title + ".mp4"
	if IsExist(savePath){
		return nil
	}
	out, err := os.Create( tmppath )
	if err != nil {
		return err
	}
	client := &http.Client{
		Transport: w.Trans,
	}
	resp, err := client.Get(url)
	if err != nil {
		out.Close()
		return err
	}
	defer resp.Body.Close()
	if resp.StatusCode == http.StatusNotFound {
		return http.ErrMissingFile
	}
	//fileSize, _ := strconv.Atoi(resp.Header.Get("Content-Length"))
	// 创建一个进度条
	prog := &progress{
		contentLength: float64(resp.ContentLength),
	}
	// create progress bar
	bar := w.Process.AddBar(
		int64(prog.contentLength),
		mpb.PrependDecorators(
			decor.Name(title + " ",decor.WC{W: len(title)/2+1, C: decor.DidentRight}),
			decor.CountersKibiByte("% .2f/% .2f"),
			decor.Percentage(decor.WCSyncSpace),
			//decor.OnComplete(
			//	decor.AverageETA(decor.ET_STYLE_GO, decor.WC{W: 4}), "done",
			//),
		),
		mpb.AppendDecorators(
			decor.EwmaETA(decor.ET_STYLE_GO, 90),
			decor.Name(" ] "),
			decor.EwmaSpeed(decor.UnitKiB, "% .2f", 60),
		),
	)
	reader := bar.ProxyReader(resp.Body)
	defer reader.Close()
	mw := io.MultiWriter(out, prog)
	if _, err = io.Copy(mw, reader); err != nil {
		out.Close()
		return err
	}
	out.Close()
	if err = os.Rename(tmppath, savePath); err != nil {
		return err
	}
	//prcs.Wait()
	return nil
}

func (w *Worker)Push(title string,url string)  {
	w.Wg.Add(1)
	go func(title string,url string) {
		w.Workers <- 1
		defer func() {
			w.Wg.Done()
			<- w.Workers
		}()
		url = html.UnescapeString(url)

		w.DownloadFile(title,url)
	}(title,url)
}

func (w *Worker)Wait()  {
	w.Wg.Wait()
	w.Process.Wait()
}