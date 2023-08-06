# -*- coding: utf-8 -*-
#-----------------------------------------------------------------
# Copyright (C) 2020, the Loge development team
#
# This file is part of Loge
# Loge is distributed under the terms of GNU General Public License
# The full license can be found in 'license.txt'
# Loge development team can be found in 'development.txt'
#-----------------------------------------------------------------

'''
---------------------------------------------------------------------
Browser module.
Browser is a window where results of processing script are visible.
---------------------------------------------------------------------
'''

from PyQt5.QtWidgets import QTextBrowser

class Browser(QTextBrowser):

    def scroll_to_relposition(self, relposition):
        absmaximum = self.verticalScrollBar().maximum()
        absposition = relposition * absmaximum
        self.verticalScrollBar().setValue(absposition)