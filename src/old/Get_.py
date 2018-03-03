#!python3
#encoding: utf-8
import argparse
import pathlib
from log.Log import Log

import requests
from bs4 import BeautifulSoup
import dataset
import datetime
import os.path
from database.Database import Database as Db

class Main(object):
    def Run(self):
        parser = argparse.ArgumentParser(
            description='GitHub Repository Uploader.',
        )
        parser.add_argument('path_dir_pj')
        parser.add_argument('-n', '--username', action='append')
        parser.add_argument('-d', '--path_dir_db')
        parser.add_argument('-id', '--path_dir_input_db')
        parser.add_argument('-od', '--path_dir_output_db')
        parser.add_argument('-u', '--url', action='append')
        parser.add_argument('-y', '--yaml')
        self.__args = parser.parse_args()

        usernames = self.__GetUsernames()
        Log.debug('対象ユーザ:', usernames)
        path_out = GetDirOutputDb()
        path_out.mkdir(parents=True, exist_ok=True)

    def __GetUsernames(self):
        if None is not self.__args.username: return self.__args.username
        elif None is self.__args.path_dir_db:
            path_db = self.__GetDirInputDb()
            #path_db = self.__GetPathDbAccount()
            if not path_db.isfile(): raise Main.ArgumentError(f'指定パスにDBが存在しません。: {path_db}')
            db_account = dataset.connect('sqlite:///' + str(path_db))
            return [a['Username'] for a in db_account['Accounts'].find()]
        else: 

    def __GetDirInputDb(self):
        if None is not self.__args.path_dir_db: return pathlib.Path(self.__args.path_dir_db)
        elif None is not self.__args.path_dir_input_db: return pathlib.Path(self.__args.path_dir_input_db)
        else:
            if None is self.__args.username:
                raise Main.ArgumentError(f'ユーザ名か入力DBディレクトリのパスを指定してください。')
                
    def __GetDirOutputDb(self):
        if None is not self.__args.path_dir_db: return pathlib.Path(self.__args.path_dir_db)
        elif None is not self.__args.path_dir_output_db: return pathlib.Path(self.__args.path_dir_output_db)
        else: pathlib.Path(__file__).parent / 'res/db/'
                
    """
    def __GetDirInputDb(self):
        if None is self.__args.path_dir_db:
            if None is self.__args.path_dir_input_db and None is self.__args.path_dir_output_db:
                raise Main.ArgumentError(f'DBパスが存在しません。: {path_db}')
                
    def __GetPathDbAccount(self):
        path_db = pathlib.Path(self.__args.path_dir_db).resolve()
        return path_db / 'Github.Accounts.sqlite3'

    def __GetPathDirDb(self):
        path_dir_db = pathlib.Path(self.__args.path_dir_db).resolve()
        if path_dir_db.isdir(): Main.ArgumentError(f'指定ディレクトリが存在しません。: {path_dir_db}')
        return path_dir_db

    def __Getyaml(self):
        if None is not self.__args.yaml: raise NotImplementedError()
        
    """

    class ArgumentError(RuntimeError):
        def __init__(*args, **kwargs):
            message = '起動引数エラー。'
            if 0 < len(args): message += str(args[0]) 
            super().__init__(message)
            #super().__init__(args, kwargs)

    """
    ContributionDBの生成と更新を実行する。
    DBが存在しなければDBファイルとテーブルを作成する。
    DBが存在すればレコードを更新する。
    @param {string} usernameは対象ユーザ名。
    """
    def Run(self, username):
        self.__Create(username)
        self.__Insert(self.__GetContributionsSince(self.__GetContributionsSVG(username), self.__GetLastDateFromDB()))
    def __Create(self, username):
        # DB用に空ファイルを作成する
        path_file_db = self.__GetDbFilePath(username)
        if os.path.isfile(path_file_db):
            self.__db = self.__OpenDb(username)
            return
        with open(path_file_db, 'w') as f:
            pass
        # テーブルを作成する
        self.__db = self.__OpenDb(username)
        sql = """
create table "Contributions"(
    "Id"                integer primary key,
    "Date"              text not null,
    "Count"             integer not null check(0 <= "Count")
);
"""
        self.__db.query(sql)
    """
    DBファイルパスを返す。
    @param {str} usernameは対象ユーザ名。
    """
    def __GetDbFilePath(self, username):
        return os.path.join(self.__path_dir_db, 'GitHub.Contributions.{username}.sqlite3'.format(username=username))
    """
    ContributionDBファイルを開く。
    """
    def __OpenDb(self, username):
        path_file_db = self.__GetDbFilePath(username)
        if os.path.isfile(path_file_db):
            return dataset.connect('sqlite:///' + path_file_db)
        else:
            return None
    """
    DBから最終日を取得する。
    @return {soup.find} HTML内のSVG要素。
    """
    def __GetLastDateFromDB(self):
        if None is self.__db:
            return None
        sql = 'select MAX("Date") LastDate from Contributions;'
        return self.__db.query(sql).next()['LastDate']
    """
    GitHub個人ページからSVG要素を取得し返す。
    @param {string} usernameは対象ユーザ名。
    @return {soup.find} HTML内のSVG要素。
    """
    def __GetContributionsSVG(self, username):
        last_date = self.__GetLastDateFromDB()
        if None is last_date or None is not last_date and last_date < "{0:%Y-%m-%d}".format(datetime.datetime.now()):
            print('************************{0}'.format(username))
            url = 'https://github.com/{username}'.format(username=username)
            file_name = '{username}_contributions'.format(username=username)
            r = requests.get(url)
            r.raise_for_status()
            soup = BeautifulSoup(r.text, 'html.parser') # html.parser, lxml
            return soup.find("svg", attrs={"class": "js-calendar-graph-svg"})
        else:
            return None
    """
    指定した日付と同じかそれより未来のみを対象としたContributionsを取得する。
    @param {soup.find} svgはHTML内のSVG要素。
    @param {string} sinceは日付。yyyy-MM-dd書式。Noneや空文字ならすべての日付を対象とする。
    @return {dict} 指定した日付とそれ以降におけるSVGのContributions。
    """
    def __GetContributionsSince(self, svg, since):
        if None is svg:
            return None
        contributions = []
        for rect in svg.find_all('rect'):
            date = rect.get('data-date')
            if not since or (since and since <= date):
                contributions.append({"Date": date, "Count": rect.get('data-count')})
        return contributions
    """
    指定した日付と同じかそれより未来のみを対象としたContributionsを取得する。
    @param {dict} 
    """
    def __Insert(self, contributions):
        if None is contributions:
            return
        self.__db.begin()
        # 指定した日付と同日なら更新する
        self.__db['Contributions'].update(contributions[0], 'Date')
        # 指定した日付以降なら挿入する
        for c in contributions[1:]:
            self.__db['Contributions'].insert(c)
        self.__db.commit()


if __name__ == '__main__':
    username = 'ytyaru'
    path_dir_db = os.path.abspath(os.path.dirname(__file__))
    m = Main(path_dir_db)
    m.Run(username)

