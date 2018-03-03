# `==`と`is`

pythonでは2種類の比較演算子を使う。

演算子|例|対象
------|--|----
`==`|`1 == 5`, `'A' == 'A'`|値(str,int)
`is`|`some_instance is None`|参照(None,type。`id()`値)

使い分けたほうが安全。[参考](https://www.python-izm.com/tips/difference_eq_is/)

さらに、`==`と`is`では左辺と右辺の意味が異なる。

* `is` の場合、`対象 is 期待値`という順序になる。
* `==` の場合、特に無い。

英語では`主語 is 補語`になるため、順序が固定されてしまう。

* `対象 is 期待値`よりも`期待値 == 対象`のほうが見やすい。
* 場合によっては

C言語では、左辺がNULL

* `NULL == instance`
* `instance == NULL`


# キー確認

kvがmastersと同じキーを*すべて*持っているか確認したい

masters = {'k1':'v1', 'k2':'v2'}
kv = {'k1':'v', 'k3': 0}

## OK

```python
for k in kv:
    if k not in masters.keys(): raise Exception()
```
```
kvのkeyAは、masterに含まれていない。これはエラーですわ。
```

## NG

```python
for m in masters:
    if m not in kv.keys(): raise Exception()
```
```
masterのkeyAは、kvに含まれていない。これはエラーですわ。
```

結果に問題はないが、主語がmasterになることに違和感。調べたいのはkvのほうなのだから、kvを主語にすべき。








masters = {'k1':'v1', 'k2':'v2'}
kv = {'k1':'v', 'k3': 0}
for k in kv:
    if k not in masters.keys(): raise Exception()


masters = {'k1':'v1', 'k2':'v2'}
kv = {'k1':'v', 'k2': 0}
for k in kv:
    if k not in masters.keys(): raise Exception()

masters = {'k1':'v1', 'k2':'v2'}
kv = {'k1':'v', 'k2': 0}
for m in masters:
    if m not in kv.keys(): raise Exception()

