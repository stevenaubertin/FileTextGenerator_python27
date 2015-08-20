# -*- coding: utf-8 -*-

"""
@package RandomFileTextGenerator
random fileText generator using http://randomtextgenerator.com/
Copyright (C) 2015 Steven Aubertin

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>
"""

__author__ = 'Steven Aubertin <stevenaubertin@gmail.com>'
__copyright__ = "Copyright (C) All Rights Reserved 2015"
__file__ = 'randomFileTextGenerator.py'
__license__ = "Public Domain"
__name__ = 'Random file text generator'
__version__ = '2.0'

import urllib2
import os
import sys
import getopt
import contextlib
from bs4 import BeautifulSoup


def about():
    print """
            RandomFileTextGenerator Copyright (C) 2015  Steven Aubertin
            This program comes with ABSOLUTELY NO WARRANTY;
            This is free software, and you are welcome to redistribute it
            under certain conditions;
            For more details, visit http://www.gnu.org/licenses/
            IMPORTANT :
            To use this program, you will need the library beautifulsoup4
            (pip install beautifulsoup4 or easy_install beautilfulsoup4)

            -Update Steven Aubertin 06/29/2015
                * Fix file(s) naming
                * FIX files creation
                * Fix proper file closing
                * Fix file size
                * FIX encoding errors
                * Add arguments options
                * Add return code
        """.format(sys.argv[0])


def print_usage():
    print """usage : {0}
            [-o <output files, default file.txt separated by space ex. a.txt b.txt c.txt>]
            [-a <about, print about message>]
            [-s <size in bytes, default 1024>]
            [-c <file count, default 1>]
            [-v <verbose, default False>]
            [-h <help, print this usage message>]
            [-r <replace all files>]

            *Note that if count is smaller than the number of output files.
            The number of output files will be used.
            """.format(sys.argv[0])


def read_url(url):
    if url:
        reader_resp_content = None

        reader_req = urllib2.Request(url)
        with contextlib.closing(urllib2.urlopen(reader_req)) as reader_resp:
            reader_resp_content = reader_resp.read()

        try:
            return reader_resp_content.decode('utf-8')
        except:
            pass

        try:
            iso_string = reader_resp_content.decode('iso-8859-1')
            print 'UTF-8 decoding failed, but ISO-8859-1 decoding succeeded'
            return iso_string
        except Exception, e:
            print e
            raise
    else:
        print "Invalid url in read_url"


def create_filenames(params):
    file_counts = len(params["outputfiles"])
    count = params["count"]
    files = params["outputfiles"]

    if file_counts < count:
        j = 0
        for i in xrange(0, count-file_counts):
            index = i % file_counts
            if index == 0:
                j += 1
            f = params["outputfiles"][index]
            files.append('{0}{1}{2}'.format(os.path.splitext(f)[0], j, os.path.splitext(f)[1]))

    return files


def replace_existing_file(filename, params, MAX_TRY=3):
    replace = False

    for i in xrange(0, MAX_TRY):
        try:
            user_input = str(raw_input("File {0} already exists would you like to replace? [y/n]".format(filename))).lower()
            if user_input == 'y':
                with open(filename, 'w') as f:
                        pass
                replace = True
                break
            elif user_input == 'n':
                break
        except:
            pass

    return replace


def create_files(params):
    files = create_filenames(params)

    if params["replace_all"]:
        for f in files:
            try:
                if os.path.exists(f):
                    os.remove(f)
                    if params["verbose"]:
                        print 'File {0} removed.'.format(f)
            except:
                if params["verbose"]:
                    print 'Unable to remove file {0}.'.format(f)

    for filename in files:
        try:
            if os.path.exists(filename) and not replace_existing_file(filename, params):
                continue

            with open(filename, "a") as text_file:
                size = os.stat(filename).st_size
                while size < params["size"]:
                    page = read_url(params["url"])
                    soup = BeautifulSoup(page)
                    text = soup.find('textarea').text
                    try:
                        content = str(text)
                    except:
                        content = text.encode('utf-8')
                    i = 0
                    while size < params["size"]:
                        if i < len(content):
                            text_file.write(content[i])
                            size += 1
                            i += 1
                        else:
                            # Not finish but require more content
                            break

            if params["verbose"]:
                print 'File {0} created with size of {1}.'.format(filename, os.stat(filename).st_size)
        except Exception, e:
            if params["verbose"]:
                print e


def main(argv):
    #Default parameters
    params = {
        "outputfiles":["file.txt"],
        "size":1024,
        "count":1,
        "url":"http://randomtextgenerator.com/",
        "verbose":False,
        "replace_all":False
    }

    #Parsing arguments
    try:
        opts, argvs = getopt.getopt(
            argv,
            "havro:c:s:", ["outputfiles=", "count=", "size="]
        )
    except getopt.GetoptError:
        print_usage()
        return 2

    if len(opts) == 0:
        about()
        print_usage()
        return 0

    for opt, arg in opts:
        if opt == '-h':
            print_usage()
            return 0
        elif opt == '-a':
            about()
            return 0
        elif opt == '-v':
            params["verbose"] = True
        elif opt in ("-o", "--outputfiles"):
            params["outputfiles"] = arg.split(' ')
        elif opt in ("-c", "--count"):
            params["count"] = int(arg)
        elif opt in ("-s", "--size"):
            params["size"] = int(arg)
        elif opt in ('-r', '--replace'):
            params["replace_all"] = True

    #Create files
    create_files(params)
    return 0

#Starting point of script
sys.exit(main(sys.argv[1:]))






