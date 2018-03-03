from db.transact.Transactioner import Transactioner

class MyDbTransactioner:
    def __init__(self):
        self.__db_url = 'sqlite:///test.db'
        self.__dataset_kwargs = None
    @property
    def DbUrl(self): return self.__db_url
    @property
    def DbKwargs(self): return self.__dataset_kwargs

    def CreateTable(self, db, table_name, **name_types):
        if table_name in db.tables: self.DropTable(db, table_name)
        columns = ', '.join(k+' '+v for k,v in name_types.items())
        sql = f'create table {table_name} ({columns});'
        print(sql)
        db.query(sql)
    def DropTable(self, db, table_name):
        sql = f'drop table {table_name};'
        print(sql)
        db.query(sql)
    def Insert(self, db, table_name, **kv):
        columns = ','.join([k for k in kv.keys()])
        values = ','.join(self.__GetInsertValues(kv.values()))
        sql = f'insert into {table_name} ({columns}) values ({values});'
        print(sql)
        db.query(sql)
    def __GetInsertValues(self, values):
        vals = []
        for v in values:
            if isinstance(v, int): vals.append(str(v))
            else: vals.append(f"'{v}'")
        return vals

