"""
@package RandomFileTextGenerator
random fileText generator using http://randomtextgenerator.com/
Copyright (C) 2015 Remi Carpentier

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
__author__ = 'Remi Carpentier, Quebec, Canada <carpentieremi@hotmail.com>'
__copyright__ = "Copyright (C) All Rights Reserved 2015"
__file__ = 'randomFileTextGenerator.py'
__license__ = "Public Domain"
__name__ = 'Random file text generator'
__version__ = '1.0'

import urllib2
import os
from bs4 import BeautifulSoup

url = "http://randomtextgenerator.com/"
print """
    RandomFileTextGenerator Copyright (C) 2015  Remi Carpentier
    This program comes with ABSOLUTELY NO WARRANTY;
    This is free software, and you are welcome to redistribute it
    under certain conditions;
    For more details, visit http://www.gnu.org/licenses/
    IMPORTANT :
    To use this program, you will need the library beautifulsoup4
    (pip install beautifulsoup4 or easy_install beautilfulsoup4)
    """
fileName = raw_input("ENTER a name for your file or PRESS ENTER to use 'file' by default : ")
if not fileName:
    fileName = "file"
nb = input("ENTER the number of files you want (Files name will be numbered) : ")
grosseur = input("ENTER a length for one file in bits (this will be approximate) : ")

def read_url(url):
    reader_req = urllib2.Request(url)
    reader_resp = urllib2.urlopen(reader_req)
    reader_resp_content = reader_resp.read()
    reader_resp.close()

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
i = 0
safe_guard = 0
while i < nb:
    j = safe_guard
    safe_guard = 0
    try:
        textName = fileName+str(i)+".txt"
        text_file = open(textName, "a")
        while (os.stat(textName).st_size < grosseur):
            text = read_url(url)
            soup = BeautifulSoup(text)
            text_file.write(str(soup.find('textarea').text))
            j = j + 1
        text_file.close()
        i = i + 1
    except:
        safe_guard = j
        pass
