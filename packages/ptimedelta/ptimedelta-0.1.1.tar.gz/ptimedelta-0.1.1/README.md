# ptimedelta

Convert time periods represented by strings to timedelta objects and vice versa. 

## Features
1. Supports Python2.7, Python3+.

## Warning
Project under a development.

## Installation
```shell script
$ pip install ptimedelta
```

## Examples
```pydocstring
>>> import ptimedelta as ptd
>>> ptd.to_timedelta("12m34s")
datetime.timedelta(seconds=754)
>>> ptd.to_seconds("3h23m4s", as_int=True)
12184
```
