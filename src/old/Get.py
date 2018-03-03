#!python3
#encoding: utf-8
import argparse
import pathlib
from log.Log import Log
import dataset
"""
import requests
from bs4 import BeautifulSoup
import dataset
import datetime
import os.path
from database.Database import Database as Db
"""
class Main(object):
    def Run(self):
        parser = argparse.ArgumentParser(
            description='GitHub Repository Uploader.',
        )
        #parser.add_argument('path_dir_pj')
        parser.add_argument('-n', '--username', action='append')
        parser.add_argument('-d', '--path_dir_db')
        parser.add_argument('-id', '--path_dir_input_db')
        parser.add_argument('-od', '--path_dir_output_db')
        parser.add_argument('-u', '--url', action='append')
        parser.add_argument('-y', '--yaml')
        self.__args = parser.parse_args()
        print(self.__args)

        # 起動引数チェック
        usernames = self.__GetUsernames()
        Log().debug(f'対象ユーザ: {usernames}')
        path_out = self.__GetDirOutputDb()
        Log().debug(f'出力パス: {path_out}')
        path_out.mkdir(parents=True, exist_ok=True)
        self.__Getyaml()

        # 草DB作成

        # 草データ取得
        data = None
        try:
            data = FromApi()
        except RateLimitError as e:
            data = FromSvg()
        finally:
            if data is None: raise NotGetError()
        Insert(data)

    def __GetUsernames(self):
        if self.__args.username is not None: return self.__args.username
        elif self.__args.path_dir_db is not None:
            path_db = self.__GetDirInputDb()
            path_db_account = self.__GetPathDbAccount(path_db)
            if not path_db_account.is_file(): raise Main.ArgumentError(f'指定パスにDBが存在しません。: {path_db_account}')
            db_account = dataset.connect('sqlite:///' + str(path_db_account))
            return [a['Username'] for a in db_account['Accounts'].find()]
        else: raise Main.ArgumentError(f'ユーザ名か入力DBディレクトリのパスを指定してください。')

    def __GetPathDbAccount(self, path_db):
        return pathlib.Path(path_db / 'Github.Accounts.sqlite3').resolve()

    def __GetDirInputDb(self):
        if None is not self.__args.path_dir_db: return pathlib.Path(self.__args.path_dir_db)
        elif None is not self.__args.path_dir_input_db: return pathlib.Path(self.__args.path_dir_input_db)
        else:
            if None is self.__args.username:
                raise Main.ArgumentError(f'ユーザ名か入力DBディレクトリのパスを指定してください。')
                
    def __GetDirOutputDb(self):
        if self.__args.path_dir_db is not None: return pathlib.Path(self.__args.path_dir_db)
        elif self.__args.path_dir_output_db is not None: return pathlib.Path(self.__args.path_dir_output_db)
        else: return pathlib.Path(pathlib.Path(__file__).parent / 'res/db/').resolve()
            
    def __Getyaml(self):
        if None is not self.__args.yaml: raise NotImplementedError('YAML読込は未実装です。')
    
    class ArgumentError(Exception):
        def __init__(self, *args, **kwargs):
            message = '起動引数エラー。'
            if 0 < len(args): message += str(args[0]) 
            super().__init__(message)


if __name__ == '__main__': Main().Run()

