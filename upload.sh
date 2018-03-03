#!/bin/bash
user=ytyaru0
desc="GitHubの草SVGを作成するツール。"
url=http://ytyaru.hatenablog.com/entry/2000/00/00/000000
target=$(cd $(dirname $0) && pwd)

. /home/pi/root/script/sh/pyenv.sh
. /home/pi/root/env/py/auto_github/bin/activate

script=/tmp/work/GitHub.Uploader.Pi3.Https.201802210700/src/Uploader.py
python3 ${script} "${target}" -u  "${user}" -d "${desc}" -l "${url}"

