# Unit Name: moneyguru.custom_date_range_panel_test
# Created By: Virgil Dupras
# Created On: 2009-02-18
# $Id$
# Copyright 2009 Hardcoded Software (http://www.hardcoded.net)

from datetime import date

from ..base import TestCase
from ...model.date import MonthRange

class DateRangeOnOctober2007AndPanelLoaded(TestCase):
    def setUp(self):
        self.create_instances()
        self.document.date_range = MonthRange(date(2007, 10, 1))
        self.document.select_custom_date_range()
        self.clear_gui_calls()
    
    def test_dates(self):
        # the dates, when loading the panel, are the dates of the current date range
        self.assertEqual(self.cdrpanel.start_date, '01/10/2007')
        self.assertEqual(self.cdrpanel.end_date, '31/10/2007')
    
    def test_set_start_later_than_end(self):
        # when start_date is set later than end_date, end_date is set to the same date.
        self.cdrpanel.start_date = '04/11/2007'
        self.assertEqual(self.cdrpanel.end_date, '04/11/2007')
    
    def test_set_end_earlier_than_start(self):
        # when end_date is set earlier than start_date, start_date is set to the same date.
        self.cdrpanel.end_date = '04/09/2007'
        self.assertEqual(self.cdrpanel.start_date, '04/09/2007')
    