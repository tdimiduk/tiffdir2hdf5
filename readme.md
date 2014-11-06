tiffdir2hdf5
============

Set of scripts to manage converting timeseries tiffs into a compressed hdf5 file.

For timeseries (video) images where many of the pixels do not change, you can get good compression even losslessly (of order one third the size).

``` shell
tiffdir2hdf5.py directory
```

and its inverse

``` shell
hdf52tiffdir.py file.h5
```
