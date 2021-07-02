import subprocess
from pathlib import Path
from typing import Optional
import urllib.request
from zipfile import ZipFile
import re
import shutil

PYTHON_EMBEDDED_URL = 'https://www.python.org/ftp/python/3.9.6/python-3.9.6-embed-amd64.zip'
GET_PIP_URL = 'https://bootstrap.pypa.io/get-pip.py'


def abort(ret):
    print('')
    print('build error!')
    print(f'return code {ret.returncode}')
    print('press enter to continue')
    input()
    exit()


def exec(cmd: str, cwd: Optional[Path] = None):
    print('')
    print(f'実行 [{cmd}] [{cwd}]')
    ret = subprocess.run(cmd, cwd=cwd, shell=True)
    if ret.returncode != 0:
        abort(ret)


def download(url: str, savepath: Path):
    print('')
    print(f'ダウンロード [{url}] [{savepath}]')
    with urllib.request.urlopen(url) as f_remote:
        with open(savepath, 'wb') as f_file:

            maxbytes = 1024 * 1024
            readbytes = 0
            while True:
                buf = f_remote.read(maxbytes)
                if len(buf) == 0:
                    break
                f_file.write(buf)
                readbytes += len(buf)
                print(f'    [{readbytes / 1024 / 1024}MB]')

    print('完了')


if __name__ == '__main__':
    cwd = Path(__file__).parent.resolve()
    dist = cwd / 'dist'
    tmp = cwd / 'tmp'
    pythondir = tmp / 'python'

    dist.mkdir(exist_ok=True)
    tmp.mkdir(exist_ok=True)
    pythondir.mkdir(parents=True, exist_ok=True)

    # ダウンロード・解凍
    if not (tmp / 'python.zip').exists():
        download(PYTHON_EMBEDDED_URL, tmp / 'python.zip')
    if not (tmp / 'get-pip.py').exists():
        download(GET_PIP_URL, tmp / 'get-pip.py')

    # pythonインストール
    if not (pythondir / 'python.exe').exists():
        with ZipFile(tmp / 'python.zip') as z:
            z.extractall(pythondir)
        exec('python.exe ' + str(tmp / 'get-pip.py'), pythondir)

        # python39._pthの修正
        with open(pythondir / 'python39._pth', 'r') as f_from:
            buf = f_from.read()
            buf = re.sub(r'^ *# *import site *$', 'import site', buf, flags=re.MULTILINE)
            with open(pythondir / 'python39._pth', 'w') as f_to:
                f_to.write(buf)

    # ファイルのコピー（server）
    if (tmp / 'server').exists():
        shutil.rmtree(tmp / 'server')
    (tmp / 'server').mkdir(exist_ok=True)

    for p in (cwd / 'server').glob('*.py'):
        shutil.copy(p, tmp / 'server')
    shutil.copy(cwd / 'server' / 'requirements.txt', tmp / 'server')
    exec('python.exe -m pip install -r  ' + str(tmp / 'server' / 'requirements.txt'), pythondir)

    # ファイルのコピー・ビルド（client）
    if (tmp / 'client').exists():
        shutil.rmtree(tmp / 'client')

    exec('npm run electron:build', cwd / 'client')
    shutil.copytree(cwd / 'client' / 'dist_electron' / 'win-unpacked', tmp / 'client')

    # 本ディレクトリに移動
    if dist.exists():
        shutil.rmtree(dist)
    shutil.move(tmp / 'client', dist)
    shutil.move(tmp / 'server', dist / 'server')
    shutil.copytree(pythondir, dist / 'python')

    print('build success!')
    print('press enter to continue')
    input()
    exit()
