import requests
from lxml import etree
import os
import time
from tqdm import tqdm
import re
import execjs
import random
import socket # 内置库
import socks # 需要安装：pip install pysocks

# 代理服务器IP（域名）
socks5_proxy_host = '127.0.0.1'
# 代理服务器端口号
socks5_proxy_port = 10808

# 设置代理
socks.set_default_proxy(socks.SOCKS5,socks5_proxy_host,socks5_proxy_port)
socket.socket = socks.socksocket


def random_ip():
    a=random.randint(1,255)
    b=random.randint(1,255)
    c=random.randint(1,255)
    d=random.randint(1,255)
    return(str(a)+'.'+str(b)+'.'+str(c)+'.'+str(d))

def add_header():
    return {"Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
                  "Proxy-Connection": "keep-alive",
                  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36',
	  'X-Forwarded-For':random_ip()
                  }

def links(url):
    res = requests.get(url, headers=add_header(),timeout=20)
    #print(res.text)
    data = etree.HTML(res.text)
    link_list = data.xpath('//*[@class="well well-sm videos-text-align"]/a/@href')
    print("link_list",link_list)
    return link_list

def url_parse(url):
    res = requests.get(url, headers=add_header(), timeout=20)
    data = etree.HTML(res.text)
    true_url = data.xpath('//*/div//source/@src')[0]
    return true_url

def relink(link):
    res = requests.get(link, headers=add_header(), timeout=20).text
    data = etree.HTML(res)
    cname = data.xpath('//*[@class="login_register_header"]/text()')[0]
    name = "".join(cname.split())
    print(name)
    n = re.findall('document\.write\(strencode\((.*?)\)',res)
    a = list(n[0].replace('"','').split(','))
    ctx = execjs.compile(""";var encode_version = 'sojson.v5', lbbpm = '__0x33ad7',  __0x33ad7=['QMOTw6XDtVE=','w5XDgsORw5LCuQ==','wojDrWTChFU=','dkdJACw=','w6zDpXDDvsKVwqA=','ZifCsh85fsKaXsOOWg==','RcOvw47DghzDuA==','w7siYTLCnw=='];(function(_0x94dee0,_0x4a3b74){var _0x588ae7=function(_0x32b32e){while(--_0x32b32e){_0x94dee0['push'](_0x94dee0['shift']());}};_0x588ae7(++_0x4a3b74);}(__0x33ad7,0x8f));var _0x5b60=function(_0x4d4456,_0x5a24e3){_0x4d4456=_0x4d4456-0x0;var _0xa82079=__0x33ad7[_0x4d4456];if(_0x5b60['initialized']===undefined){(function(){var _0xef6e0=typeof window!=='undefined'?window:typeof process==='object'&&typeof require==='function'&&typeof global==='object'?global:this;var _0x221728='ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=';_0xef6e0['atob']||(_0xef6e0['atob']=function(_0x4bb81e){var _0x1c1b59=String(_0x4bb81e)['replace'](/=+$/,'');for(var _0x5e3437=0x0,_0x2da204,_0x1f23f4,_0x3f19c1=0x0,_0x3fb8a7='';_0x1f23f4=_0x1c1b59['charAt'](_0x3f19c1++);~_0x1f23f4&&(_0x2da204=_0x5e3437%0x4?_0x2da204*0x40+_0x1f23f4:_0x1f23f4,_0x5e3437++%0x4)?_0x3fb8a7+=String['fromCharCode'](0xff&_0x2da204>>(-0x2*_0x5e3437&0x6)):0x0){_0x1f23f4=_0x221728['indexOf'](_0x1f23f4);}return _0x3fb8a7;});}());var _0x43712e=function(_0x2e9442,_0x305a3a){var _0x3702d8=[],_0x234ad1=0x0,_0xd45a92,_0x5a1bee='',_0x4a894e='';_0x2e9442=atob(_0x2e9442);for(var _0x67ab0e=0x0,_0x1753b1=_0x2e9442['length'];_0x67ab0e<_0x1753b1;_0x67ab0e++){_0x4a894e+='%'+('00'+_0x2e9442['charCodeAt'](_0x67ab0e)['toString'](0x10))['slice'](-0x2);}_0x2e9442=decodeURIComponent(_0x4a894e);for(var _0x246dd5=0x0;_0x246dd5<0x100;_0x246dd5++){_0x3702d8[_0x246dd5]=_0x246dd5;}for(_0x246dd5=0x0;_0x246dd5<0x100;_0x246dd5++){_0x234ad1=(_0x234ad1+_0x3702d8[_0x246dd5]+_0x305a3a['charCodeAt'](_0x246dd5%_0x305a3a['length']))%0x100;_0xd45a92=_0x3702d8[_0x246dd5];_0x3702d8[_0x246dd5]=_0x3702d8[_0x234ad1];_0x3702d8[_0x234ad1]=_0xd45a92;}_0x246dd5=0x0;_0x234ad1=0x0;for(var _0x39e824=0x0;_0x39e824<_0x2e9442['length'];_0x39e824++){_0x246dd5=(_0x246dd5+0x1)%0x100;_0x234ad1=(_0x234ad1+_0x3702d8[_0x246dd5])%0x100;_0xd45a92=_0x3702d8[_0x246dd5];_0x3702d8[_0x246dd5]=_0x3702d8[_0x234ad1];_0x3702d8[_0x234ad1]=_0xd45a92;_0x5a1bee+=String['fromCharCode'](_0x2e9442['charCodeAt'](_0x39e824)^_0x3702d8[(_0x3702d8[_0x246dd5]+_0x3702d8[_0x234ad1])%0x100]);}return _0x5a1bee;};_0x5b60['rc4']=_0x43712e;_0x5b60['data']={};_0x5b60['initialized']=!![];}var _0x4be5de=_0x5b60['data'][_0x4d4456];if(_0x4be5de===undefined){if(_0x5b60['once']===undefined){_0x5b60['once']=!![];}_0xa82079=_0x5b60['rc4'](_0xa82079,_0x5a24e3);_0x5b60['data'][_0x4d4456]=_0xa82079;}else{_0xa82079=_0x4be5de;}return _0xa82079;};if(typeof encode_version!=='undefined'&&encode_version==='sojson.v5'){function strencode(_0x50cb35,_0x1e821d){var _0x59f053={'MDWYS':'0|4|1|3|2','uyGXL':function _0x3726b1(_0x2b01e8,_0x53b357){return _0x2b01e8(_0x53b357);},'otDTt':function _0x4f6396(_0x33a2eb,_0x5aa7c9){return _0x33a2eb<_0x5aa7c9;},'tPPtN':function _0x3a63ea(_0x1546a9,_0x3fa992){return _0x1546a9%_0x3fa992;}};var _0xd6483c=_0x59f053[_0x5b60('0x0','cEiQ')][_0x5b60('0x1','&]Gi')]('|'),_0x1a3127=0x0;while(!![]){switch(_0xd6483c[_0x1a3127++]){case'0':_0x50cb35=_0x59f053[_0x5b60('0x2','ofbL')](atob,_0x50cb35);continue;case'1':code='';continue;case'2':return _0x59f053[_0x5b60('0x3','mLzQ')](atob,code);case'3':for(i=0x0;_0x59f053[_0x5b60('0x4','J2rX')](i,_0x50cb35[_0x5b60('0x5','Z(CX')]);i++){k=_0x59f053['tPPtN'](i,len);code+=String['fromCharCode'](_0x50cb35[_0x5b60('0x6','s4(u')](i)^_0x1e821d['charCodeAt'](k));}continue;case'4':len=_0x1e821d[_0x5b60('0x7','!Mys')];continue;}break;}}}else{alert('');};""")
    html = ctx.call('strencode',a[0],a[1])
    print(html)
    print(re.findall(r"source src=\'(.*?)\'",html))
    url = re.findall(r"source src=\'(.*?)\'",html)[0]
    return url,name

def load(url, name):
    res = requests.get(url, stream=True,timeout=30)
    if os.path.exists('//192.168.123.253/视频/91porn/2020.6.16/%s.mp4' % (name)) == True:
   #if os.path.exists('D:\91\%s.mp4' % (name)) == True:
        print('文件已存在')
        pass
    else:
        file_size = int(res.headers['content-length'])
        pdar = tqdm(ncols=70,total=file_size, desc=name, unit='it', unit_scale=True)
        with open(r'//192.168.123.253/视频/91porn/2020.6.16/%s.mp4' % (name), 'wb')as f:
       #with open(r'D:\91\%s.mp4' % (name), 'wb')as f:
            for chunk in res.iter_content(chunk_size=1024):
                f.write(chunk)
                pdar.update(1024)
        pdar.close()


def main():
        for i in range(1,2):
            try:
                #url = "http://www.91porn.com/v.php?category=mf&viewtype=basic&page={}".format(i)
                url = "http://www.91porn.com/v.php?category=top&viewtype=basic&page={}".format(i)
                print(url)
                for link in links(url):
                    url2,name = relink(link)
                    load(url2,name)
                time.sleep(1)
            except Exception as e:
                print (e)
                pass

if __name__ == '__main__':
    main()
