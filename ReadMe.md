# このソフトウェアについて

GitHubの草SVGを作成するツール。

Githubアップローダから別案件化させた。その`Github.Accounts.sqlite3`に依存する。

# 概要

1. 草データを取得する
    * GithubサイトのユーザページにあるContributionsのSVGから [例](https://github.com/ytyaru)
1. 1をsqlite3のDBに保存する
1. 2を元にして全ての年における草SVGを作成する

# コマンド概要

コマンド|説明
--------|----
Get.py|草データの入手
Make.py|草データからSVGファイル作成
__Backup.py|草データとSVGの保存やアップロード

https://github.com/users/<username>/contributions
[["2013/01/27",2],["2013/01/28",2],["2013/01/29",0],["2013/01/30",0],["2013/01/31",0],...]

## 引数

### Get.py

```python
$ python Get.py -n -d -u -y
```

引数|名前|説明
----|----|----
`-n`|username|対象Githubユーザ `https://github.com/users/<username>/contributions`
`-d`|path_dir_db|入出力DBディレクトリパス
`-id`|path_dir_in_db|入力DBディレクトリパス `Github.Accounts.sqlite3`
`-od`|path_dir_out_db|出力DBディレクトリパス `Github.Contributions.{user}.sqlite3`
`-u`|url|アップロードURL
`-y`|yaml|yamlファイルパス。またはフロースタイル`{d:{k:v}, a:[1,2]}`

* 優先
    * `-y`引数があればそちらを優先する。他は`-d`,`-id`,`-od`,`-u`の指定があっても無視する。
    * `-n`引数があれば`-d`,`-y`の設定は無視して`-n`指定されたユーザのみ対象とする
* 必須
    * 対象ユーザ
        * `-u`, `-y`, `-d`のいずれかによる指定
* デフォルト値
    * DB出力ディレクトリ
        * カレントディレクトリ

#### 例

指定ユーザの草を取得する。

```python
$ python Get.py --user Githubユーザ名
```

ユーザ指定の略記と複数。
```python
$ python Get.py -n user1 -n user2 -n user3
```

https://github.com/users/<username>/contributions
[["2013/01/27",2],["2013/01/28",2],["2013/01/29",0],["2013/01/30",0],["2013/01/31",0],...]

DBの指定。`Github.Accounts.sqlite3`にある全ユーザを対象とする。草データ出力先にもなる。

```python
$ python Get.py -d /tmp
```

`-id`でAccountsDBパス指定、`-od`で草DBパス指定。
```python
$ python Get.py -id /tmp/in/ -od /tmp/out/
```

アップロード先の指定。（`-u`複数指定可能）

```python
$ python Get.py -u https://github.com/...
```

yamlファイルパス指定。

```python
$ python Get.py -y config.yml
```

フロースタイルyamlデータ指定。

```python
$ python Get.py -y {Path:/tmp/, Url:https://github.com/...}
```

### Make.py

```python
$ python Make.py -n -i -o -u -y
```

引数|名前|説明
----|----|----
`-n`|username|対象Githubユーザ
`-i`,`-d`|path_dir_db|DBディレクトリパス
`-o`,`-s`|path_dir_output|SVG出力ディレクトリパス
`-u`|url|アップロードURL
`-y`|yaml|yamlファイルパス。またはフロースタイル`{d:{k:v}, a:[1,2]}`

* 優先
    * `-y`引数があればそちらを優先する。他は`-d`,`-i`,`-o`,`-u`の指定があっても無視する。
    * `-n`引数があれば`-d`,`-y`の設定は無視して`-n`指定されたユーザのみ対象とする
* 必須
    * 入力DBパス
        * `-i`, `-d`, `-y`のいずれかによる指定
* デフォルト値
    * DB出力ディレクトリ
        * カレントディレクトリ

#### 例

指定ユーザの草SVGを作成する。

```python
$ python Make.py --user Githubユーザ名
```

ユーザ指定の略記と複数。
```python
$ python Make.py -n user1 -n user2 -n user3
```

DBの指定。`-i`,`-d`どちらでも可。`Github.Accounts.sqlite3`にある全ユーザを対象とする。

```python
$ python Make.py -i /tmp/db/
```

SVGファイル出力先の指定。`-o`,`-s`どちらでも可。

```python
$ python Make.py -o /tmp/svg/
```

アップロード先の指定。（`-u`複数指定可能）

```python
$ python Make.py -u https://github.com/...
```

yamlファイルパス指定。

```python
$ python Make.py -y config.yml
```

フロースタイルyamlデータ指定。

```python
$ python Make.py -y {Path:/tmp/, Url:https://github.com/...}
```

### Backup.py

これは別案件にすべきか。

```python
$ python Backup.py サブコマンド
```

サブコマンド。バックアップ方法ごとに存在する。

方法|略記|説明
----|----|----
FileSystem|fs|ファイルシステムによる書き込み。
FileSystem.zip|zip|ファイルシステムによる書き込み。zip圧縮。
Github.Repository|hub,github|Github Repositories APIによる create と`git push`
Github.Pages|pages,gitpages|`docs/`にファイル出力した上で`Github.Repository`パターン
Bitbucket|bb,bitbucket|
GitLab|gl,lab,gitlab|
GoogleDrive|google|
Dropbox|drop|

#### 方法1: FileSystem

CUIでなくPythonインタフェースにすべき。書き出すべきデータがメモリ上にしか存在しないため。

```python
from abc import ABCMeta, abstractmethod
class Backupper(meta=ABCMeta):
    @abstractmethod
    def Backup(*args, **kwargs): pass

class FileSystem(Backupper):
    def Backup(*args, **kwargs):
        if 'files' not in kwargs: raise Exception('引数filesがありません。')
```

ディレクトリ構成をdict型で持たせる。
```python
files = {
    '/': {
        'tmp': {
            'some.txt': some_str,
            'sub': {}
        }
    }
}
```
値がdict型ならディレクトリ、文字列型かバイナリ型ならファイル。

面倒すぎる。pathとデータを渡して、必要なディレクトリは自動生成がいい。ファイルがないディレクトリを作りたければデータを省略する。


```python
from abc import ABCMeta, abstractmethod
class Backupper(meta=ABCMeta):
    @abstractmethod
    def Backup(*args, **kwargs): pass
class FileSystem(Backupper):
    def Backup(path, data=None):
        if isinstance(data, str):
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open('w', encoding='utf-8') as f: f.write(data)
        elif isinstance(data, (bytes, bytearray)):
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open('wb') as f: f.write(data)
        else:
            path.mkdir(parents=True, exist_ok=True)
```

引数が不定のインタフェースって……。

#### 方法2: Github.Repository

```python
$ python Backup.py github パス -u -d -l
```

引数|名前|説明
----|----|----
[0]|ローカルリポジトリパス（`.git`を配置したいディレクトリ。リモートリポジトリ名にもなる）
`-u`|アップロードしたいGithubユーザ
`-d`|リポジトリの説明文
`-l`|リポジトリのURL

#### 方法3: Github.Pages

```python
$ python Backup.py pages パス -u -d -l
```

引数|名前|説明
----|----|----
[0]|ローカルリポジトリパス（`.git`を配置したいディレクトリ。リモートリポジトリ名にもなる）
`-u`|アップロードしたいGithubユーザ
`-d`|リポジトリの説明文
`-l`|リポジトリのURL

なお、`docs/`ディレクトリ必須。その配下に1つ以上のファイル必須。

# 設定

最小。
```yaml
Default:
    Path: /.../github/contributions/
    Url: https://github.com/{user}/{repo}.git
```

ファイル種別ごと。
```yaml
Default:
    Path:
        Db: /.../db/
        Svg: /.../svg/
    Url
        Db: https://github.com/{user}/MyContributions/res/db/
        Svg: https://github.com/{user}/MyContributions/res/svg/
```

複雑な指定。
```yaml
Default:
    Path:
        Db:
            - /.../db/
            - /.../db2/
        Svg:
            - /.../svg/
            - /.../svg2/
    Upload:
        Github:
            # 全ユーザの草データを所定リポジトリにpushする
            - https://github.com/MyUser/MyContributions.git
            # ユーザ名を`{user}`とすることで各ユーザごとにリポジトリを作成できる
            - https://github.com/{user}/MyContributions.git
            # ユーザとリポジトリを個別に指定できる
            - user: abc
              repo: https://github.com/xyz/MyContributions.git
            # ユーザとリポジトリを個別に指定できる（`{user}`とすると指定したユーザ名になる）
            - user: ytyaru
              repo: https://github.com/{user}/MyContributions.git
            - user: defg
              repo: https://github.com/{user}/Kusa.git
            # 上記すべて1つずつ実行する（重複していても）

```


# 開発環境

* [Raspberry Pi](https://ja.wikipedia.org/wiki/Raspberry_Pi) 3 Model B
    * [Raspbian](https://www.raspberrypi.org/downloads/raspbian/) GNU/Linux 8.0 (jessie)
        * [pyenv](http://ytyaru.hatenablog.com/entry/2019/01/06/000000)
            * Python 3.6.4

# ライセンス

このソフトウェアはCC0ライセンスである。

[![CC0](http://i.creativecommons.org/p/zero/1.0/88x31.png "CC0")](http://creativecommons.org/publicdomain/zero/1.0/deed.ja)

利用ライブラリは以下。

Library|License|Copyright
-------|-------|---------
[requests](http://requests-docs-ja.readthedocs.io/en/latest/)|[Apache-2.0](https://opensource.org/licenses/Apache-2.0)|[Copyright 2012 Kenneth Reitz](http://requests-docs-ja.readthedocs.io/en/latest/user/intro/#requests)
[dataset](https://dataset.readthedocs.io/en/latest/)|[MIT](https://opensource.org/licenses/MIT)|[Copyright (c) 2013, Open Knowledge Foundation, Friedrich Lindenberg, Gregor Aisch](https://github.com/pudo/dataset/blob/master/LICENSE.txt)
[bs4](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)|[MIT](https://opensource.org/licenses/MIT)|[Copyright © 1996-2011 Leonard Richardson](https://pypi.python.org/pypi/beautifulsoup4),[参考](http://tdoc.info/beautifulsoup/)
[pytz](https://github.com/newvem/pytz)|[MIT](https://opensource.org/licenses/MIT)|[Copyright (c) 2003-2005 Stuart Bishop <stuart@stuartbishop.net>](https://github.com/newvem/pytz/blob/master/LICENSE.txt)
[PyYAML](https://github.com/yaml/pyyaml)|[MIT](https://opensource.org/licenses/MIT)|[Copyright (c) 2006 Kirill Simonov](https://github.com/yaml/pyyaml/blob/master/LICENSE)
[pyotp](https://github.com/pyotp/pyotp)|[MIT](https://opensource.org/licenses/MIT)|[Copyright (C) 2011-2017 Mark Percival m@mdp.im, Nathan Reynolds email@nreynolds.co.uk, Andrey Kislyuk kislyuk@gmail.com, and PyOTP contributors](https://github.com/pyotp/pyotp/blob/master/LICENSE)
[SQLAlchemy](https://www.sqlalchemy.org/)|[MIT](https://opensource.org/licenses/MIT)|[Mike Bayer](https://pypi.python.org/pypi/SQLAlchemy/1.2.2)
[furl](https://github.com/gruns/furl)|[Unlicense](http://unlicense.org/)|[gruns/furl](https://github.com/gruns/furl/blob/master/LICENSE.md)

以下、依存ライブラリ。

Library|License|Copyright
-------|-------|---------
[alembic](https://github.com/zzzeek/alembic)|[MIT](https://opensource.org/licenses/MIT)|[Copyright (C) 2009-2018 by Michael Bayer.](https://github.com/zzzeek/alembic/blob/master/LICENSE)
[banal](https://github.com/pudo/banal)|[MIT](https://opensource.org/licenses/MIT)|[Copyright (c) 2017 Friedrich Lindenberg](https://github.com/pudo/banal/blob/master/LICENSE)
[certifi](https://github.com/certifi/python-certifi)|[MPL2.0](https://www.mozilla.org/en-US/MPL/2.0/)|[MPL2.0](https://github.com/certifi/python-certifi/blob/master/LICENSE)
[chardet](https://github.com/chardet/chardet)|[LGPL2.1](https://www.gnu.org/licenses/old-licenses/lgpl-2.1.ja.html)|[Copyright (C) 1991, 1999 Free Software Foundation, Inc.](https://github.com/chardet/chardet/blob/master/LICENSE)
[idna](https://github.com/kjd/idna)|All rights reserved.|[Copyright (c) 2013-2017, Kim Davies. All rights reserved.](https://github.com/kjd/idna/blob/master/LICENSE.rst)
[mako](https://github.com/zzzeek/mako)|[MIT](https://opensource.org/licenses/MIT)|[Copyright (C) 2006-2016 the Mako authors and contributors see AUTHORS file.](https://github.com/zzzeek/mako/blob/master/LICENSE)
[normality](https://github.com/pudo/normality)|[MIT](https://opensource.org/licenses/MIT)|[Copyright (c) 2013, Open Knowledge Foundation, Friedrich Lindenberg, Gregor Aisch](https://github.com/pudo/normality/blob/master/LICENSE)
[dateutil](https://pypi.python.org/pypi/python-dateutil/2.6.1)|[Simplified BSD](https://opensource.org/licenses/BSD-2-Clause)|[© Copyright 2016, dateutil.](https://dateutil.readthedocs.io/en/stable/)
[python-editor](https://github.com/fmoo/python-editor)|[Apache License 2.0](https://opensource.org/licenses/Apache-2.0)|[fmoo/python-editor](https://github.com/fmoo/python-editor/blob/master/LICENSE)
[six](https://pypi.python.org/pypi/six)|[MIT](https://opensource.org/licenses/MIT)|[Copyright (c) 2010-2018 Benjamin Peterson](https://github.com/benjaminp/six/blob/master/LICENSE)

