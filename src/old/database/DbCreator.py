#!/usr/bin/env python
# -*- coding: utf-8 -*-

from abc import ABCMeta, abstractmethod
import os.path
from setting.Config import Config
import dataset
import glob

# 抽象クラス
class DbInitializer(metaclass=ABCMeta):
    def __init__(self):
        self._path_dir_root = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
        #self.__setting = setting.Setting.Setting()
        self._path_dir_this = os.path.abspath(os.path.dirname(__file__))
        self.__db = None

    def Initialize(self):
        self._CreateDb()
        self._ConnectDb()
        self.Db.query('PRAGMA foreign_keys = false')
        self._CreateTable()
        self._InsertInitData()
        self.Db.query('PRAGMA foreign_keys = true')

    #@abstractmethod
    def _CreateDb(self):
        #print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
        #print(self.DbFilePath)
        if not os.path.isfile(self.DbFilePath):
            with open(self.DbFilePath, 'w') as f: pass

    def _ConnectDb(self):
        self.__class__.Db = dataset.connect('sqlite:///' + self.DbFilePath, engine_kwargs={'pool_pre_ping':True})

    # テーブル作成（CreateTable文）
    #@abstractmethod
    def _CreateTable(self):
        self.__CreateTableBySql()
        self.__CreateTableByPy()

    # 初期値の挿入（Insert文）
    #@abstractmethod
    def _InsertInitData(self):
        self.__InsertBySql()
        self.__InsertByTsv()
        self.__InsertByPy()

    @property
    def DbId(self): return self.__class__.__name__.replace(super().__thisclass__.__name__, '')
    @property
    def DbFileName(self): return 'Github.' + self.DbId + '.sqlite3'
    #def DbFileName(self): return 'GitHub.' + self.DbId + '.sqlite3'
    @property
    def DbFilePath(self):
        #print(dir(self.__setting))
        #return os.path.join(self.__setting.PathDb, self.DbFileName)
        #print(Config()['Path']['Db'])
        #print(Config().PathDb)
        #print(self.DbFileName)
        #return os.path.join(Config().PathDb, self.DbFileName)
        return os.path.join(Config()['Path']['Db'], self.DbFileName)
        
    @property
    def Db(self): return self.__class__.Db
        # sqlite3.ProgrammingError: SQLite objects created in a thread can only be used in that same thread.The object was created in thread id 1972434016 and this is thread id 1995735040
        #try:
        #except sqlite3.ProgrammingError as e:
        #    self.__ConnectDb()
        #return self.__class__.Db

    # SQLファイルによるテーブル作成
    def __CreateTableBySql(self):
        for path_sql in self.__GetCreateTableSqlFilePaths():
            self.__ExecuteSqlFile(dbname, path_sql)

    # Pythonコードによるテーブル作成
    def __CreateTableByPy(self):
        self.__ActionByPy(action='create')

    # SQLファイルによる挿入
    def __InsertBySql(self):
        for path_sql in self.__GetCreateTableSqlFilePaths():
            self.__ExecuteSqlFile(dbname, path_sql)

    # TSVファイルによる挿入
    def __InsertByTsv(self):
        for path_tsv in self.__GetInsertTsvFilePaths():
            table_name = os.path.splitext(table_name)[0]
            loader = database.TsvLoader.TsvLoader()
            loader.ToSqlite3(path_tsv, self.DbFilePath, table_name)

    # Pythonコードによる挿入
    def __InsertByPy(self):
        self.__ActionByPy(action='insert')

    # Pythonコードによる処理実行
    def __ActionByPy(self, action='insert'):
        path, namespace, module_name, class_name, method_name = self.__GetIds_ActionByPy(action)
        if os.path.isdir(path):
            # モジュール読込
            import importlib
            module = importlib.import_module(namespace_insert_py + module_name)
            # クラスのインスタンス生成
            #cls = module[module_name](self.DbFilePath)
            cls = getattr(module, class_name)
            ##############################################################
            # 引数は何にするか。現状、DbPath, dataset.connect(), client。これをビジネスロジック化によりclient渡し不要にしたい。
            #ins = cls(self.DbFilePath)
            ins = cls(self.Db)
            ##############################################################
            # メソッドの取得と実行
            #method = getattr(cls, method_name)
            method = getattr(ins, method_name)
            method()

    def __GetIds_ActionByPy(self, action='insert'):
        self.__CheckActionName(action)
        path_root = os.path.abspath(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))))
        path_l_py = 'database/init/{0}/{1}/py/'.format(self.DbId, action)
        path_py = os.path.join(path_root, path_l_py)
        namespace = path_l_py.replace('/', '.')
        module_name = action[0].upper() + action[1:] + 'r' # Create[r], Inserte[r], Delete[r]
        class_name = module_name
        method_name = module_name[:-1] # Create, Insert, Delete
        return path_py, namespace, module_name, class_name, method_name

    def __CheckActionName(self, action):
        valid_names = {'create', 'insert'}
        if action not in valid_names: raise Exception('引数actionは{0}のいずれかのみ有効。: {1}'.format(valid_names, action))

    # パス取得（テーブル作成用SQLファイル）
    def __GetCreateTableSqlFilePaths(self):
        path = os.path.join(self._path_dir_this, self.DbId, 'create', 'table', 'sql')
        for path_sql in glob.glob(os.path.join(path + '*.sql')): yield path_sql

    # パス取得（初期値挿入用TSVファイル）
    def __GetInsertTsvFilePaths(self):
        path = os.path.join(self._path_dir_this, self.DbId, 'insert', 'tsv')
        for path_tsv in glob.glob(os.path.join(path + '*.tsv')): yield path_tsv

    # パス取得（初期値挿入用SQLファイル）
    def __GetInsertSqlFilePaths(self):
        path = os.path.join(self._path_dir_this, self.DbId, 'insert', 'sql')
        for path_tsv in glob.glob(os.path.join(path + '*.sql')): yield path_tsv

    # SQLファイル発行
    def __ExecuteSqlFile(self, sql_path):
        with open(sql_path, 'r') as f:
            sql = f.read()
            self.__class__.Db.query(sql)

