import inspect
import types
from db.transact.Transactioner import Transactioner

import pathlib
import importlib
class AccesserMeta(type):
    def __new__(cls, name, bases, attrs):
        for name, transact in cls.__GetTransactioners():
            accesser = cls.__Create(transact)
            attrs[name] = accesser
        return type.__new__(cls, name, bases, attrs)

    @classmethod
    def __GetTransactioners(cls):
        path_this = pathlib.Path(__file__).parent
        path_transact = path_this / 'transact'
        path_transacts = path_transact.glob('?*Transactioner.py') # 正規表現は使えない。ワイルドカードのみ。
        for path in path_transacts:
            filename = path.name.rstrip('.py')
            module = importlib.import_module(f'db.transact.{filename}')
            cls = getattr(module, filename)
            yield filename.rstrip('Transactioner'), cls()

    @classmethod
    def __Create(cls, target_class):
        attrs = {}
        # target_classの自作公開メソッドをすべて取得
        for method_info in inspect.getmembers(target_class, inspect.ismethod):
            method_name = method_info[0]
            method = method_info[1]
            if not isinstance(method, types.MethodType): continue
            if method_name.startswith('_'): continue
            t = Transactioner()
            t.TransactionMethod = method
            t.DbUrl = target_class.DbUrl
            t.DbKwargs = target_class.DbKwargs
            attrs[method_name] = t.Transact
        accesserType = type(target_class.__class__.__name__ + 'Accesser', (object,), attrs)
        return accesserType()

    __instance = None
    def __call__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super().__call__(*args, **kwargs)
        return cls.__instance

