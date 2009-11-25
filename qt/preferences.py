# -*- coding: utf-8 -*-
# Created By: Virgil Dupras
# Created On: 2009-11-17
# $Id$
# Copyright 2009 Hardcoded Software (http://www.hardcoded.net)
# 
# This software is licensed under the "HS" License as described in the "LICENSE" file, 
# which should be included with this package. The terms are also available at 
# http://www.hardcoded.net/licenses/hs_license

import os.path as op

from qtlib.preferences import Preferences as PreferencesBase

# About the hidden columns prefernce:
# Rather than keeping a list of visible columns, we keep a list of hidden column. This is because
# not all columns are optionally visible, so we either need to know which columns are optionally
# visible, or only store information about hidden columns. The second way is simpler, so that's
# what we do.

class Preferences(PreferencesBase):
    def _load_values(self, settings, get):
        self.registration_code = get('RegistrationCode', self.registration_code)
        self.registration_email = get('RegistrationEmail', self.registration_email)
        self.recentDocuments = get('RecentDocuments', self.recentDocuments)
        self.recentDocuments = filter(op.exists, self.recentDocuments)
        self.networthColumnWidths = get('NetworthColumnWidths', self.networthColumnWidths)
        self.profitColumnWidths = get('ProfitColumnWidths', self.profitColumnWidths)
        self.transactionColumnWidths = get('TransactionColumnWidths', self.transactionColumnWidths)
        self.entryColumnWidths = get('EntryColumnWidths', self.entryColumnWidths)
        self.scheduleColumnWidths = get('ScheduleColumnWidths', self.scheduleColumnWidths)
        self.budgetColumnWidths = get('BudgetColumnWidths', self.budgetColumnWidths)
        self.networthHiddenColumns = set(get('NetworthHiddenColumns', self.networthHiddenColumns))
        self.profitHiddenColumns = set(get('ProfitHiddenColumns', self.profitHiddenColumns))
        self.transactionHiddenColumns = set(get('TransactionHiddenColumns', self.transactionHiddenColumns))
        self.entryHiddenColumns = set(get('EntryHiddenColumns', self.entryHiddenColumns))
        self.scheduleHiddenColumns = set(get('ScheduleHiddenColumns', self.scheduleHiddenColumns))
        self.networthGraphVisible = get('NetworthGraphVisible', self.networthGraphVisible)
        self.networthPieChartsVisible = get('NetworthPieChartsVisible', self.networthPieChartsVisible)
        self.profitGraphVisible = get('ProfitGraphVisible', self.profitGraphVisible)
        self.profitPieChartsVisible = get('ProfitPieChartsVisible', self.profitPieChartsVisible)
        self.entryGraphVisible = get('EntryGraphVisible', self.entryGraphVisible)
        self.netWorthExpandedPaths = get('NetWorthExpandedPaths', self.netWorthExpandedPaths)
        self.profitLossExpandedPaths = get('ProfitLossExpandedPaths', self.profitLossExpandedPaths)
    
    def reset(self):
        self.registration_code = ''
        self.registration_email = ''
        self.recentDocuments = []
        self.netWorthExpandedPaths = [[0], [1]] # Asset and Liability nodes
        self.profitLossExpandedPaths = [[0], [1]] # Income and Expense nodes
        self.networthColumnWidths = None
        self.profitColumnWidths = None
        self.transactionColumnWidths = None
        self.entryColumnWidths = None
        self.scheduleColumnWidths = None
        self.budgetColumnWidths = None
        self.networthHiddenColumns = set(['delta', 'delta_perc'])
        self.profitHiddenColumns = set(['delta', 'delta_perc'])
        self.transactionHiddenColumns = set(['payee', 'checkno'])
        self.entryHiddenColumns = set(['payee', 'checkno'])
        self.scheduleHiddenColumns = set(['payee', 'checkno'])
        self.networthGraphVisible = True
        self.networthPieChartsVisible = True
        self.profitGraphVisible = True
        self.profitPieChartsVisible = True
        self.entryGraphVisible = True
    
    def _save_values(self, settings, set_):
        set_('RegistrationCode', self.registration_code)
        set_('RegistrationEmail', self.registration_email)
        set_('RecentDocuments', self.recentDocuments)
        set_('NetworthColumnWidths', self.networthColumnWidths)
        set_('ProfitColumnWidths', self.profitColumnWidths)
        set_('TransactionColumnWidths', self.transactionColumnWidths)
        set_('EntryColumnWidths', self.entryColumnWidths)
        set_('ScheduleColumnWidths', self.scheduleColumnWidths)
        set_('BudgetColumnWidths', self.budgetColumnWidths)
        set_('NetworthHiddenColumns', self.networthHiddenColumns)
        set_('ProfitHiddenColumns', self.profitHiddenColumns)
        set_('TransactionHiddenColumns', self.transactionHiddenColumns)
        set_('EntryHiddenColumns', self.entryHiddenColumns)
        set_('ScheduleHiddenColumns', self.scheduleHiddenColumns)
        set_('NetworthGraphVisible', self.networthGraphVisible)
        set_('NetworthPieChartsVisible', self.networthPieChartsVisible)
        set_('ProfitGraphVisible', self.profitGraphVisible)
        set_('ProfitPieChartsVisible', self.profitPieChartsVisible)
        set_('EntryGraphVisible', self.entryGraphVisible)
        set_('NetWorthExpandedPaths', self.netWorthExpandedPaths)
        set_('ProfitLossExpandedPaths', self.profitLossExpandedPaths)
    
