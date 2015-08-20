RandomFileTextGenerator
==============

This python script allow the user to create random text file(s) of specific sizes.
--------------
Usage :
            
    [-o output files, default file.txt separated by space ex. a.txt b.txt c.txt]
    [-a <about, print about message>]
    [-s <size in bytes, default 1024>]
    [-c <file count, default 1>]
    [-v <verbose, default False>]
    [-h <help, print this usage message>]
    [-r <replace all files>]

Examples:

    python RandomFileTextGenerator.py -o "a.txt b.txt c.txt"
*Will generate 3 files named, by default files will be named file.txt file1.txt ...*

    python RandomFileTextGenerator.py -s 2048
*To change the file size use -s by default the size is 1024 bytes*

    python RandomFileTextGenerator.py -r
*To remplace existing file(s) use -r*

    python RandomFileTextGenerator.py -c 666
*Will generate 666 files of the default name [file.txt,..., file665.txt] of the default (1024 bytes) size*

    python RandomFileTextGenerator.py -o "a.txt b.txt c.txt" -c 5 -s 1024 -r
*Will replace any existing file (with the same name) and create 1ko (1024 bytes) files wich will be named “a.txt a1.txt b.txt b1.txt c.txt"*
