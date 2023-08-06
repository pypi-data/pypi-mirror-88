# -*- coding: utf-8 -*-
#-----------------------------------------------------------------
# Copyright (C) 2017-2020, the Loge development team
#
# This file is part of Loge
# Loge is distributed under the terms of GNU General Public License
# The full license can be found in 'license.txt'
# Loge development team can be found in 'development.txt'
#-----------------------------------------------------------------

import os

from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtCore import pyqtSlot

from loge.core.core_utils import APP_PATH


class Tree(QtWidgets.QTreeView):
	def __init__(self, parent=None):
		super(Tree, self).__init__(parent)
		#---
		self.setMaximumWidth(200)
		self.clicked.connect(self.on_treeView_clicked)
		#---
		self.core = None

	def assing_core (self, core):
		self.core = core
		
	def reload(self):
		#---Dir to show
		if self.core.Script.script_path:
			dir_to_show = os.path.dirname(self.core.Script.script_path)
		else:
			dir_to_show=APP_PATH
		#---Link the tree to a model
		model = QtWidgets.QFileSystemModel()
		model.setRootPath(dir_to_show)
		model.setNameFilters( ["*.py"] )
		self.setModel(model)
		#---Set the tree's index to the root of the model
		indexRoot = model.index(model.rootPath())
		self.setRootIndex(indexRoot)
		#---Hide tree size and date columns
		self.hideColumn(1)
		self.hideColumn(2)
		self.hideColumn(3)
		#---Hide tree header
		self.setHeaderHidden(True)

	@pyqtSlot(QtCore.QModelIndex)
	def on_treeView_clicked(self, index):
		indexItem = self.model().index(index.row(), 0, index.parent())
		#---
		fileName = str(self.model().fileName(indexItem))
		filePath = str(self.model().filePath(indexItem))
		#---
		if os.path.isfile(filePath):
			if os.path.splitext(filePath)[1] == '.py':
				self.core.file_open(filePath, browser_path_update=False)
