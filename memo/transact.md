
def CreateTable(db, table_name, **name_types): pass

t = Transactioner('sqlite:///test.db')
t.Transact(CreateTable, 'MyTable', **nt)


MyTableTransactioner().CreateTable('MyTable', **nt)

class MyTableTransactioner(Transactioner):
    def __init__(self, db):
        self.__db = db
    def CreateTable(table_name, **name_types):
        columns = ', '.join(k+' '+v for k,v in name_types.items())
        sql = f'create table {table_name} ({columns});'
        Log().debug(sql)
        self.__db.query(sql)
class Transactioner:
    def __init__(self, sactor):
        self.__sactor = sactor
    def Transact(self, *args, **kwargs):
        with dataset.connect(self.__db_url, self.__dataset_kwargs) as db:
            db.begin()
            res = self.__transaction(db, *args, **kwargs)
            db.commit()
            return res


import Transactioner
class MyTableTransactioner(DbUrlSetter):
    DB_URL = 'MyDb.db'
    @connect(DB_URL)
    @transact
    def CreateTable(db, table_name, **name_types):
        columns = ', '.join(k+' '+v for k,v in name_types.items())
        sql = f'create table {table_name} ({columns});'
        Log().debug(sql)
        self.__db.query(sql)

`DB_URL`の値をmetaclassで動的に作成すればいい？

class Transactioner:
    def __init__(self, sactor):
        self.__sactor = sactor
    def Transact(self, *args, **kwargs):
        with dataset.connect(self.__db_url, self.__dataset_kwargs) as db:
            db.begin()
            res = self.__transaction(db, *args, **kwargs)
            db.commit()
            return res




class MyClassTransactioner(Transactioner):
    @Transact
    def CreateTable(db, table_name, **name_types):
        columns = ', '.join(k+' '+v for k,v in name_types.items())
        sql = f'create table {table_name} ({columns});'
        Log().debug(sql)
        self.__db.query(sql)
            



