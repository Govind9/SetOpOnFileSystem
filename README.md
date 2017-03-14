#SetOpOnFileSystem

###Prerequisite:
    boost library

###Building:

```g++ -std=c++11 -Os -Wall -pedantic set.cpp -lboost_system -lboost_filesystem -o main```


###Running:

``` ./main <directory1> <op> <directory2> ```

where operations or op would be:

* `-i` for intersection
* `-u` for union
* `-d` for difference
* `-sd` for symmetric difference


