#!/usr/bin/env python
# Copyright 2009 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "HS" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/hs_license

import os.path as op
import sys
sys.path.insert(0, op.abspath('..')) # for all cross-toolkit modules
import os
import shutil
from optparse import OptionParser

from core.app import Application as MoneyGuruApp

def main(dev):
    if not dev:
        print "Building help index"
        help_path = op.abspath('../help/moneyguru_help')
        os.system('open /Developer/Applications/Utilities/Help\\ Indexer.app --args {0}'.format(help_path))
    
    print "Building mg_cocoa.plugin"
    if op.exists('py/build'):
        shutil.rmtree('py/build')
    if op.exists('py/dist'):
        shutil.rmtree('py/dist')
    
    os.chdir('py')
    if dev:
        os.system('python -u setup.py py2app -A')
    else:
        os.system('python -u setup.py py2app')
    os.chdir('..')

    print 'Generating Info.plist'
    contents = open('InfoTemplate.plist').read()
    contents = contents.replace('{version}', MoneyGuruApp.VERSION)
    open('Info.plist', 'w').write(contents)
    
    print "Building the XCode project"
    os.system('xcodebuild')

if __name__ == '__main__':
    usage = "usage: %prog [options]"
    parser = OptionParser(usage=usage)
    parser.add_option('--dev', action='store_true', dest='dev', default=False,
        help="If this flag is set, will configure for dev builds.")
    (options, args) = parser.parse_args()
    main(options.dev)
