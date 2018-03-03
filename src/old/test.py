from database.Transactioner import Transactioner
from log.Log import Log

if __name__ == '__main__':
    def CreateTable(db, table_name, **name_types):
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
        vals = []
        for v in values:
            if isinstance(v, int): vals.append(str(v))
            else: vals.append(f"'{v}'")
        print(vals)
        return vals

    #t = Transactioner(CreateTable, 'sqlite:///test.db')
    t = Transactioner()
    t.DbUrl = 'sqlite:///test.db'

    t.TransactionMethod = CreateTable
    nt = {'Id': 'integer', 'Name': 'text'}
    t.Transact('MyTable', **nt)

    t.TransactionMethod = Insert
    nv = {'Id': 0, 'Name': 'A'}
    t.Transact('MyTable', **nv)
