#! /usr/bin/env python
__author__ = 'Tser'
__email__ = '807447312@qq.com'
__project__ = 'xiaobaiauto2'
__script__ = 'chinese_chromedriver_installer.py'
__create_time__ = '2020/7/17 1:04'

from typing import Optional
from urllib.request import urlretrieve, urlopen
from winreg import HKEY_CURRENT_USER, OpenKey, EnumValue
from re import findall, IGNORECASE
from zipfile import ZipFile
from os import remove, path
import platform, sys, subprocess

def back(a,b,c):
    '''''回调函数
    @a:已经下载的数据块
    @b:数据块的大小
    @c:远程文件的大小
    '''
    per = 100.0*a*b/c
    if per > 100:
        per = 100
    print(end='\r')
    print('当前已下载%.2f%%' % per, end='')

def get_osname():
    if sys.platform == 'win32':
        ''' windows '''
        return 'windows'
    elif sys.platform == 'darwin':
        ''' Mac OS '''
        return 'macos'
    elif sys.platform == 'linux2':
        if 'ubuntu' in platform.platform().lower():
            ''' ubuntu '''
            return 'ubuntu'
        elif 'redhat' in platform.platform().lower():
            ''' redhat/centos '''
            return 'centos'
        else:
            return 'other'
    else:
        return 'other'

def download(url: Optional[str] = '', **kwargs):
    '''
    下载文件
    :param url:
    :param filename:
    :param file
    :param path:
    :param unzip: bool 默认False
    :param del_src: bool 默认False
    :param kwargs:
    :return:
    '''
    if url != '':
        urlretrieve(url, kwargs.get('filename'), back)
    if kwargs.get('unzip'):
        if kwargs.get('path') not in [None, '']:
            ZipFile(kwargs.get('filename')).extractall(path=kwargs.get('path'))
        elif kwargs.get('path') in [None, ''] and kwargs.get('file') not in [None, '']:
            ZipFile(kwargs.get('filename')).extract(kwargs.get('file'))
    if kwargs.get('del_src'):
        remove(kwargs.get('filename'))

def chromedriver_download(version: Optional[str] = '87'):
    '''
    自动下载chromedriver驱动文件
    :param version: 87,88等chrome浏览器版本号（整数）
    :return:
    '''
    TAOBAO_MIRROR_DOWNLOAD_URL = 'https://npm.taobao.org/mirrors/chromedriver/'
    name = get_osname()
    if name == 'windows':
        filename = 'chromedriver_win32.zip'
        try:
            if version == '':
                chrome_current_version = EnumValue(OpenKey(HKEY_CURRENT_USER, 'Software\Google\Chrome\BLBeacon'), 0)[1]
                cur_version = chrome_current_version.split('.')[0]
            else:
                cur_version = version
            res = urlopen(TAOBAO_MIRROR_DOWNLOAD_URL).read().decode('utf-8')
            LAST_VERSION = findall(f'/mirrors/chromedriver/{cur_version}([0-9\.]+)/">', res, IGNORECASE)[0]
            DOWNLOAD_URL = f'{TAOBAO_MIRROR_DOWNLOAD_URL}{cur_version}{LAST_VERSION}/{filename}'
            download(DOWNLOAD_URL, filename=filename, file='chromedriver.exe', unzip=True, del_src=True)
        except Exception as e:
            raise ('是不是没安装Chrome浏览器呢？' + str(e))
    elif name == 'macos':
        filename = 'chromedriver_mac64.zip'
        if version == '':
            cur_version = ''
        else:
            cur_version = version
        try:
            res = urlopen(TAOBAO_MIRROR_DOWNLOAD_URL).read().decode('utf-8')
            if cur_version == '':
                LAST_VERSION = findall(f'/mirrors/chromedriver/([0-9\.]+)/">', res, IGNORECASE)[-1]
            else:
                LAST_VERSION = findall(f'/mirrors/chromedriver/{cur_version}([0-9\.]+)/">', res, IGNORECASE)[0]
                LAST_VERSION = cur_version + LAST_VERSION
            DOWNLOAD_URL = f'{TAOBAO_MIRROR_DOWNLOAD_URL}{LAST_VERSION}/{filename}'
            download(DOWNLOAD_URL, filename=filename, path='/usr/local/bin', unzip=True, del_src=True)
        except Exception as e:
            pass

def tesseract_download():
    TESSERACT_DOWNLOAD_URL = 'https://api.256file.com/download/56476_tesseract.exe'
    urlretrieve(TESSERACT_DOWNLOAD_URL, 'tesseract.exe', back)

def update_keyword_db():
    KEYWORD_DB_DOWNLOAD_URL = ''
    urlretrieve(KEYWORD_DB_DOWNLOAD_URL, 'xiaobaiauto2.db', back)
    # popen('xiaobaiauto2.db', )

def _shell(cmd: Optional[str] = ''):
    ''' subprocess '''
    name = get_osname()
    if cmd == '' and name == 'windows':
        args = ["powershell",
                "Set-ExecutionPolicy RemoteSigned -scope CurrentUser",
                "iex (new-object net.webclient).downloadstring('https://get.scoop.sh')",
                "iwr -useb get.scoop.sh | iex"]
    else:
        args = ['powershell', cmd]
    try:
        sp = subprocess.Popen(args, stdout=subprocess.PIPE)
        return sp.stdout.read()
    except Exception as e:
        return False

def jdk_install(version: Optional[str] = '8'):
    '''
    下载并安装openjdk
    windows: scoop install oraclejdk{version}
    mac os: brew cask install adoptopenjdk{version}
    ubuntu: apt install openjdk-{version}-jre
    centos: yum install java-1.{version}.0-openjdk
    '''
    name = get_osname()
    if name == 'windows':
        ''' windows '''
        _shell()
        _shell(cmd=f'scoop install oraclejdk{version}')
    elif name == 'macos':
        ''' Mac OS '''
        _shell(cmd='/bin/zsh -c "$(curl -fsSL https://gitee.com/cunkai/HomebrewCN/raw/master/Homebrew.sh)"')
        _shell(cmd=f'brew cask install adoptopenjdk{version}')
    elif name == 'ubuntu':
        ''' ubuntu/debian '''
        _shell(cmd=f'apt install openjdk-{version}-jre')
    elif name == 'centos':
        ''' redhat/centos '''
        _shell(cmd=f'yum install java-1.{version}.0-openjdk')

def jmeter_install(version: Optional[str] = '5.3', dest_dir: Optional[str] = '.'):
    ''' 下载并配置环境变量 '''
    src_list = [
        'https://mirror.bit.edu.cn/apache/jmeter/binaries/',
        'https://mirrors.bfsu.edu.cn/apache/jmeter/binaries/',
        'https://mirrors.tuna.tsinghua.edu.cn/apache/jmeter/binaries/'
    ]
    filename = f'apache-jmeter-{version}.zip'
    name = get_osname()
    download(src_list[0] + filename, filename=filename, path=dest_dir, unzip=True, del_src=True)
    if name == 'windows':
        if dest_dir != '.' and path.isdir(dest_dir):
            # try:
            #     _shell(cmd=f'setx /M JMETER_HOME {dest_dir + f"/apache-jmeter-{version}"}')
            # except Exception as e:
            _shell(cmd=f'setx JMETER_HOME {dest_dir + f"/apache-jmeter-{version}"}')
        elif dest_dir == '.':
            _shell(cmd=f'setx JMETER_HOME {path.abspath(path.curdir) + f"/apache-jmeter-{version}"}')
        _shell(cmd='setx "path" "%path%;%JMETER_HOME%/bin;"')
    elif name == 'macos':
        try:
            with open('~/.bash_profile', 'a') as f:
                if dest_dir != '.' and path.isdir(dest_dir):
                    f.write(f'\nexport JMETER_HOME={dest_dir + f"/apache-jmeter-{version}"}\nexport PATH=$PATH:$JMETER_HOME/bin:')
                elif dest_dir == '.':
                    f.write(f'\nexport JMETER_HOME={path.abspath(path.curdir) + f"/apache-jmeter-{version}"}\nexport PATH=$PATH:$JMETER_HOME/bin:')
                f.flush()
                f.close()
        except OSError as e:
            if dest_dir != '.' and path.isdir(dest_dir):
                _shell(f'export JMETER_HOME={dest_dir + f"/apache-jmeter-{version}"}')
            elif dest_dir == '.':
                _shell(f'export JMETER_HOME={path.abspath(path.curdir) + f"/apache-jmeter-{version}"}')
            _shell('export PATH=$PATH:$JMETER_HOME/bin:')
