import dataset
import types

class Transactioner:
    def __init__(self):
        self.__transaction = None
        self.__db_url = None
        self.__dataset_kwargs = None

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
        if isinstance(v, types.MethodType): self.__transaction = v
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

