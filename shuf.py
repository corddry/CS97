#!/usr/bin/python

"""
Shuffle lines randomly
Jack Corddry


Based off of randline.py:
Copyright 2005, 2007 Paul Eggert.
Copyright 2010 Darrell Benjamin Carbajal.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation; either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

Please see <http://www.gnu.org/licenses/> for a copy of the license.

$Id: randline.py,v 1.4 2010/04/05 20:04:43 eggert Exp $
"""

import random, sys
from optparse import OptionParser

class randline:
    
    def __init__(self, lines):
       self.lines = lines
       self.chosen = []

    def chooseline(self):
##        if isEmpty():
##            parser.error("ERROR IN CODE: no more lines to shuffle!")
        choice = random.choice(self.lines)
        while choice in self.chosen:
            choice = random.choice(self.lines)
        self.chosen.append(choice)
        return choice
    def reset(self):
        self.chosen = []
    def isEmpty(self):
        return len(self.chosen) == len(self.lines)
        # return self.chosen == self.lines

def main():
    version_msg = "%prog 1.0"
    usage_msg = """Usage: %prog [OPTION]... [FILE]
  or:  %prog -e [OPTION]... [ARG]...
Write a random permutation of the input lines to standard output.

With no FILE, or when FILE is -, read standard input.
""" ##CHANGE THIS
    
    parser = OptionParser(version=version_msg,
                          usage=usage_msg)
    parser.add_option("-n", "--head-count",
                      action="store", dest="COUNT",
                      help="output at most COUNT lines")
    parser.add_option("-e", "--echo",
                      action="store_true",# dest="doEcho", default=False,
                      help="treat each ARG as an input line")
    parser.add_option("-r", "--repeat",
                      action="store_true",# dest="doRepeat", default=False,
                      help="output lines can be repeated")
    options, args = parser.parse_args(sys.argv[1:])

    if not (options.COUNT is None):
        doHC = True
    else:
        doHC = False
        COUNT = -1

    if doHC:
        try:
            COUNT = int(options.COUNT)
        except:
            parser.error("invalid COUNT: {0}".
                         format(options.COUNT)) 
        if COUNT < 0:
            parser.error("negative COUNT: {0}".
                         format(COUNT))
    if options.echo:
        lines = []
        for line in args:
            lines.append(line + "\n")
    elif (len(args) == 0) or (args[0] == "-"):
        lines = sys.stdin.readlines()
    
    elif len(args) != 1:
        parser.error("wrong number of operands")
    else:
        try:
            input_file = args[0]
            f = open(input_file, 'r')
            lines = f.readlines()
            f.close()
        except IOError as error:
            parser.error("I/O error({0}): {1}".
                         format(error.errno, error.strerror))
            
    generator = randline(lines)
    loops = 0
    while (not generator.isEmpty()) and (loops != COUNT):
        sys.stdout.write(generator.chooseline())
        if options.repeat:
            generator.reset()
        loops += 1
 ##   for index in range(numlines):#####################change numlines
 ##       sys.stdout.write(generator.chooseline())
    

if __name__ == "__main__":
    main()
