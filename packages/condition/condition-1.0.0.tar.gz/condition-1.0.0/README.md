# Condition
[![PyPI version](https://badge.fury.io/py/condition.svg)](https://badge.fury.io/py/condition)
[![PyPI](https://img.shields.io/pypi/pyversions/condition.svg)](https://pypi.org/project/condition/)
[![Docs](https://readthedocs.org/projects/condition/badge/?version=latest)](https://condition.readthedocs.io/en/latest/?badge=latest)
[![pipeline status](https://gitlab.com/wyzhao/condition/badges/master/pipeline.svg)](https://gitlab.com/wyzhao/condition/commits/master)
[![coverage report](https://gitlab.com/wyzhao/condition/badges/master/coverage.svg)](https://gitlab.com/wyzhao/condition/commits/master)

## Project Description

This project provides a pythonic way to construct a condition object. The condition
object can later used to query pandas Dataframe, filter pyarrow partitions or 
to generate where conditions in SQL. 
It takes care of formating and syntax for you.

#### A Quick Example


```python 

>>> from condition import *
>>> import pandas as pd
>>> fl = FieldList('A B C date value'.split())
>>> cond = ((fl.date >= pd.to_datetime('20000101')) 
...             & (fl.date <= pd.to_datetime('20010131'))
...             & (fl.A == 'a1 a3'.split()) \
...             & (fl.B == 'b1')) \
...             | (fl.C != 'c3 c5'.split())
>>> cond # show as sql where condition

        (
                (date >= '2000-01-01 00:00:00'
                and date <= '2001-01-31 00:00:00'
                and A in ('a1','a3')
                and B = 'b1')
        or C not in ('c3','c5'))

>>> cond.to_df_query()
"(((date >= '2000-01-01 00:00:00')&(date <= '2001-01-31 00:00:00')&(A in ('a1','a3'))&(B == 'b1'))|(C not in ('c3','c5')))"
>>> cond.to_pyarrow_filter()
[[('date', '>=', Timestamp('2000-01-01 00:00:00')),
  ('date', '<=', Timestamp('2001-01-31 00:00:00')),
  ('A', 'in', {'a1', 'a3'}),
  ('B', '=', 'b1')],
 [('C', 'not in', {'c3', 'c5'})]]
```


#### SQL Generation

```python 

>>> from condition.sql import render_sql
>>> sql = """
...     select *
...     from my_table
...     where {{where_condition}}
... """
>>> print(render_sql(sql, cond))

    select *
    from my_table
    where 
        (
                (date >= '2000-01-01 00:00:00'
                and date <= '2001-01-31 00:00:00'
                and A in ('a1','a3')
                and B = 'b1')
        or C not in ('c3','c5'))
```


Please see [Usage Examples](https://condition.readthedocs.io/en/latest/usage.html) for detailed examples.

## Installation
This project is distributed via `pip`. To get started:

```
pip install condition
```

To install jinja2 package used by condition.sql, do the following

```
pip install condition[sql]
```

To install all packages for development, do the following

```
pip install condition[dev]
```

