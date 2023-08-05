#!/usr/bin/env python
# -*- coding: utf-8 -*-

#    Virtual-IPM is a software for simulating IPMs and other related devices.
#    Copyright (C) 2017  The IPMSim collaboration <http://ipmsim.gitlab.io/IPMSim>
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import absolute_import, unicode_literals

import logging
import sys

import virtual_ipm.log as log
from virtual_ipm.frontends.gui import MainWindow
import virtual_ipm.frontends.gui.pyqt45 as pyqt45

QtCore = pyqt45.QtCore
Widgets = pyqt45.Widgets


def main():
    log.to_console(level=logging.INFO)

    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_X11InitThreads)
    app = Widgets.QApplication(sys.argv)

    view = MainWindow()
    view.show()

    return app.exec_()

if __name__ == '__main__':
    sys.exit(main())
