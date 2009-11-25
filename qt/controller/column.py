# -*- coding: utf-8 -*-
# Created By: Virgil Dupras
# Created On: 2009-11-25
# $Id$
# Copyright 2009 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "HS" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/hs_license

DATE_EDIT = 'date_edit'
DESCRIPTION_EDIT = 'description_edit'
PAYEE_EDIT = 'payee_edit'
ACCOUNT_EDIT = 'account_edit'

class Column(object):
    def __init__(self, attrname, title, defaultWidth, editor=None):
        self.index = None # Is set when the column list is read
        self.attrname = attrname
        self.title = title
        self.defaultWidth = defaultWidth
        self.editor = editor
    