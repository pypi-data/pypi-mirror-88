#! /usr/bin/env python3
from PySide2 import QtWidgets, QtCore, QtGui

class Backend(QtCore.QObject):
	def __init__(self, parent):
		super().__init__(parent)
		self.orientation = ""

	@QtCore.Slot(str)
	def getOrientation(self, value):
		self.orientation = value
		
	@QtCore.Slot(result=str)
	def setOrientation(self):
		return self.orientation

	def resetOrientation(self):
		self.orientation = ""