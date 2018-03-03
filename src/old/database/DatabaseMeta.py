#!python3
#encoding:utf-8
from database.init.DbInitializer import DbInitializer
from database.init.AccountsDbInitializer import AccountsDbInitializer as Accounts
from database.init.ApisDbInitializer import ApisDbInitializer as Apis
from database.init.GnuLicensesDbInitializer import GnuLicensesDbInitializer as GnuLicenses
from database.init.LanguagesDbInitializer import LanguagesDbInitializer as Languages
from database.init.LicensesDbInitializer import LicensesDbInitializer as Licenses
from database.init.OtherRepositoriesDbInitializer import OtherRepositoriesDbInitializer as OtherRepositories
from database.init.RepositoriesDbInitializer import RepositoriesDbInitializer as Repositories
from database.init.ContributionsDbInitializer import ContributionsDbInitializer as Contributions
from collections import OrderedDict

class DatabaseMeta(type):
    def __new__(cls, name, bases, attrs):
        # 単一DB
        attrs['_{0}__Initializers'.format(name)] = OrderedDict() # Database.__Initializers 実装
        for initer in [Apis(), Accounts(), Languages(), GnuLicenses(), Licenses(), OtherRepositories()]:
            attrs['_{0}__Initializers'.format(name)][initer.DbId] = initer # Database.__Initializers['Accounts'] = database.init.AccountsDbInitializer.AccountsDbInitializer()
            #attrs[initer.DbId] = property(lambda cls: initer.Db)
        return type.__new__(cls, name, bases, attrs)

    def __init__(cls, name, bases, attrs):
        #import copy
        # 単一DB
        for initer in attrs['_{0}__Initializers'.format(name)].values():
            initer.Initialize()
            setattr(cls, initer.DbId, initer.Db)
            #setattr(cls, initer.DbId, property(lambda cls: initer.Db))
            #setattr(cls, initer.DbId, property(lambda cls: copy.copy(initer.Db)))
            #setattr(cls, initer.DbId, property(lambda cls: copy.deepcopy(initer.Db)))
        
        if 0 == attrs['_{0}__Initializers'.format(name)]['Accounts'].Db['Accounts'].count(): raise Exception('登録ユーザがひとつもありません。UserRegister.pyで登録してから再実行してください。')

        # ユーザ単位DB（AccountsDB生成後でないと作れない）
        attrs['_{0}__InitializersByMultiUsers'.format(name)] = OrderedDict()
        accountsDb = attrs['_{0}__Initializers'.format(name)]['Accounts'].Db
        for initer in [cls(accountsDb) for cls in [Repositories]]:
            initer.Initialize()
            setattr(cls, initer.DbId, initer.Db)
            #setattr(cls, initer.DbId, property(lambda cls: initer.Db))
            #setattr(cls, initer.DbId, property(lambda cls: copy.copy(initer.Db)))
            #setattr(cls, initer.DbId, property(lambda cls: copy.deepcopy(initer.Db)))
        for initer in [cls(accountsDb) for cls in [Contributions]]:
            #initer.Initialize() # データ取得してしまう。将来的には外部ツール化すべき
            setattr(cls, initer.DbId, initer.Db)

    # Singleton
    _instance = None
    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance

