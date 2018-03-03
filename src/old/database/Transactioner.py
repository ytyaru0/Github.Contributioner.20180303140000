import dataset
from log.Log import Log
import types

class Transactioner:
    def __init__(self):
        self.__transaction = None
        self.__db_url = None
        self.__dataset_kwargs = None
    """
    def __init__(self, transaction, db_url, **dataset_kwargs):
        self.__transaction = None
        self.__db_url = None
        self.__dataset_kwargs = None
        self.TransactionMethod = transaction
        self.DbUrl = db_url
        self.DbKwargs = dataset_kwargs
    """

    def Transact(self, *args, **kwargs):
        with dataset.connect(self.__db_url, self.__dataset_kwargs) as db:
            db.begin()
            res = self.__transaction(db, *args, **kwargs)
            db.commit()
            return res

    @property
    def TransactionMethod(self): return self.__transaction
    @TransactionMethod.setter
    def TransactionMethod(self, v):
        if v is None: return
        if isinstance(v, types.FunctionType): self.__transaction = v
        else: raise Exception('メソッドを指定してください。第一引数はdataset.Databaseです。（他の引数は任意）')

    @property
    def DbUrl(self): return self.__db_url
    @DbUrl.setter
    def DbUrl(self, v):
        if v is None: return
        if isinstance(v, str): self.__db_url = v
        else: raise Exception('strを指定してください。dataset.connect()のDB接続文字列になります。')

    @property
    def DbKwargs(self): return self.__dataset_kwargs
    @DbKwargs.setter
    def DbKwargs(self, v):
        if v is None: return
        if isinstance(v, dict): self.__dataset_kwargs = v
        else: raise Exception('dictを指定してください。dataset.connect()のキーワード引数になります。')


if __name__ == '__main__':

    def CreateTable(db, table_name, name_types):
        columns = ', '.join(k+' '+v for k,v in name_types.items())
        #for k, v in name_types.items():
        #    k + ' ' + v
        #db.query('create table {table_name} (Id integer, Name text);')
        sql = f'create table {table_name} ({columns});'
        Log().debug(sql)
        db.query(sql)
    def Insert(db, table_name, **kv):
        columns = ','.join([k for k in kv.keys()])
        values = ','.join(GetInsertValues(kv.values()))
        #db.query(f'insert into {table_name} ({columns}) values ({values});')
        sql = f'insert into {table_name} ({columns}) values ({values});'
        Log().debug(sql)
        db.query(sql)
    def GetInsertValues(values):
        values = []
        for v in values:
            if isinstance(v, int): values.append(str(v))
            else: values.append(f"'{v}'")
        return values

    #t = Transactioner(CreateTable, 'sqlite:///test.db')
    t = Transactioner()
    t.DbUrl = 'sqlite:///test.db'

    t.TransactionMethod = CreateTable
    nt = {'Id': 'integer', 'Name': 'text'}
    t.Transact('MyTable', nt)

    t.TransactionMethod = Insert
    nv = {'Id': 0, 'Name': 'A'}
    t.Transact('MyTable', nt)
