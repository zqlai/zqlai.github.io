Title: build Django on Godady virtual host 
Category: life
Tags: Django, Godady 
Authors: zqlai


just get a Godady virtual host, WITHOUT pip tool, only python2.6

let's begin

1. download source of python3.7.0 and unzip it
```
cd python_source_dir
./configure
make
make install
```

when `make install`, an error came out:
```
      from _ctypes import Union, Structure, Array
      ImportError: No module named '_ctypes'
```

Googling it, seems that we need install libffi-dev, then
```
download source and
./configure make make install DESTDIR=~/software
setup the LD_LIBRARY_PATH in the .bashrc and source it
```
