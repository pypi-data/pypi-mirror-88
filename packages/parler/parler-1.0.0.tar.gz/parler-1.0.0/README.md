# Parler Python API
Parler Social Media Python API

### Install
```sh
$ pip install parler
```

### Authentication
After you login to Parler.com you can get the `MST` and `JST` tokens:

`Open DevTools -> Storage -> Cookies`

### Usage
```python
from parler import Parler

mst = 'XXX' # see authentication section
jst = 'YYY'

client = Parler(mst, jst)

print(client.getFeed());
```

### Methods
```sh
$ python
Python 3.7.3 (default, May 31 2019, XX:XX:XX)
[GCC 5.4.0 2016XXXX] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>> import parler
>>> help(parler)
```
