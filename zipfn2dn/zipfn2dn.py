#!/bin/env python
# encoding: utf-8
'''
default.zipfn2dn -- project zip filename to its' containing root directory name

default.zipfn2dn is a description

It defines classes_and_methods

@author:     togashix
        
@copyright:  2013 organization_name. All rights reserved.
        
@license:    license

@contact:    togashix@gmail.com
@deffield    updated: Updated
'''

import sys
import os

from argparse import ArgumentParser
from argparse import RawDescriptionHelpFormatter

__all__ = []

DEBUG = 0
TESTRUN = 0
PROFILE = 0

class CLIError(Exception):
    '''Generic exception to raise and log different fatal errors.'''
    def __init__(self, msg):
        super(CLIError).__init__(type(self))
        self.msg = "E: %s" % msg
    def __str__(self):
        return self.msg
    def __unicode__(self):
        return self.msg

def main(argv=None): # IGNORE:C0111
    '''Command line options.'''
    
    if argv is None:
        argv = sys.argv
    else:
        sys.argv.extend(argv)

    program_name = os.path.basename(sys.argv[0])
    program_shortdesc = __import__('__main__').__doc__.split("\n")[1]
    program_license = '''%s

  Created by togashix.
  Copyright 2013 togashix. All rights reserved.
  
  Licensed under the Apache License 2.0
  http://www.apache.org/licenses/LICENSE-2.0
  
  Distributed on an "AS IS" basis without warranties
  or conditions of any kind, either express or implied.

USAGE
''' % (program_shortdesc)

    try:
        # Setup argument parser
        parser = ArgumentParser(description=program_license, formatter_class=RawDescriptionHelpFormatter)
        parser.add_argument("-f", "--file", dest="input_filename", help="input filename")
        parser.add_argument("-W", "--overwrite", dest="overwrite", action="store_true", help="the input file will be overwritten")
        #parser.add_argument("-e", "--zip-encoding", dest="zip_encoding", help="zip encoding")
        #parser.add_argument("-E", "--fs-encoding", dest="fs_encoding", help="filesystem encoding")
        
        # Process arguments
        args = parser.parse_args()
        
        input_filename = args.input_filename
        overwrite = args.overwrite
        
        if input_filename == None:
            raise CLIError("no input is specified.")
        
        book_title = os.path.basename(input_filename)
        book_title = ".".join(book_title.split(".")[:-1])
        
        import tempfile
        output_handle, output_filename = tempfile.mkstemp(".tmp", "zipfn2dn_")
        try:
            import zipfile
            infile = zipfile.ZipFile(input_filename)
            outfile = zipfile.ZipFile(output_filename, "w")
            print input_filename
            print output_filename
            try:
                zis = infile.infolist()
                for zi in zis:
                    fn = zi.filename.split("/")
                    if len(fn) > 1:
                        fn[0] = book_title
                        fn = "/".join(fn)
                    else:
                        fn = zi.filename
                    file_bytes = infile.read(zi.filename)
                    zi.filename = fn
                    zi.orig_filename = fn
                    print zi.filename
                    outfile.writestr(zi, file_bytes)
            finally:
                if outfile:
                    outfile.close()
                    del outfile
                if infile: infile.close()
            
            if overwrite:
                finally_name = input_filename
            else:
                finally_name = input_filename + '.zip'
            
            if os.path.exists(finally_name):
                os.unlink(finally_name)
            from distutils import file_util
            file_util.copy_file(output_filename, finally_name)
        finally:
            if os.path.exists(output_filename):
                os.close(output_handle)
                os.unlink(output_filename)
            pass
    except KeyboardInterrupt:
        ### handle keyboard interrupt ###
        return 0
    except Exception, e:
        if DEBUG or TESTRUN:
            raise(e)
        indent = len(program_name) * " "
        sys.stderr.write(program_name + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help")
        return 2

if __name__ == "__main__":
    if DEBUG:
        sys.argv.append("-h")
        #sys.argv.append("-v")
        #sys.argv.append("-r")
    if TESTRUN:
        import doctest
        doctest.testmod()
    if PROFILE:
        import cProfile
        import pstats
        profile_filename = 'default.zipfn2dn_profile.txt'
        cProfile.run('main()', profile_filename)
        statsfile = open("profile_stats.txt", "wb")
        p = pstats.Stats(profile_filename, stream=statsfile)
        stats = p.strip_dirs().sort_stats('cumulative')
        stats.print_stats()
        statsfile.close()
        sys.exit(0)
    sys.exit(main())
