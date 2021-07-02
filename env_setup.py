import subprocess
from pathlib import Path
from typing import Optional


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


if __name__ == '__main__':
    cwd = Path(__file__).parent.resolve()
    venv = cwd / 'server' / 'venv' / 'Scripts'

    exec('npm install', cwd / 'client')

    exec('python -m venv venv', cwd / 'server')
    exec(str(venv / 'pip') + ' install -r requirements.txt', cwd / 'server')

    print('build success!')
    print('press enter to continue')
    input()
    exit()
