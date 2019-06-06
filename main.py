from PyQt5 import QtWidgets, QtCore,QtGui
from typing import Union
from copy import copy
from design import *
import clipboard
import sys

class mywindow(QtWidgets.QMainWindow, Ui_MainWindow):
	def __init__(self,app):
		super(mywindow, self).__init__()
		self.setupUi(self)
		self.actionexit.triggered.connect(sys.exit)
		self.actionOpen.triggered.connect(self.openFile)
		self.actionSave.triggered.connect(self.save_file)
		self.actionSave_as.triggered.connect(self.save_file_as)
		self.actionSize.triggered.connect(self.change_size)
		self.actionChange_font_family.triggered.connect(self.change_font_family)
		self.actionColor.triggered.connect(self.change_color)
		self.actionBackground_color.triggered.connect(self.change_bgcolor)
		self.actionBack_Color.triggered.connect(self.change_abgcolor)
		self.textBrowser.cursorPositionChanged.connect(self.show_info)
		self.textBrowser.textChanged.connect(self.edited)
		self.show_info()
	def save_file_as(self):
		filename = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File')
		print(filename)
		try:
			with open(filename[0], 'w') as f:
				f.write(self.textBrowser.toPlainText())
				f.close()
		except FileNotFoundError:
			return 1
		self.mainwindow.setWindowTitle(filename[0].split('/')[-1])
	def save_file(self):
		try:
			with open(self.filenames[0], 'w') as f:
				f.write(self.textBrowser.toPlainText())
				f.close()
			self.mainwindow.setWindowTitle(self.mainwindow.windowTitle()[:len(self.mainwindow.windowTitle())-9])
		except:
			self.save_file_as()
	def show_info(self):
		self.label.setText(self.cursorr())
		self.label_2.setText(self.all_info())
	def all_info(self):
		text = self.textBrowser.toPlainText()
		vowels = ['а', 'е', 'и', 'і', 'о', 'у', 'я', 'ю', 'є', 'ї', 'a', 'e', 'i', 'u', 'y']
		consonant = ['б', 'в', 'г', 'г', 'д', 'дь', 'ж', 'дж', 'з', 'зь', 'де', 'де', 'й', 'к', 'л', 'ль',
		'м', 'н', 'н', 'п', 'р', 'рь', 'с', 'сь', 'т', 'ть', 'ф', 'X', 'ц', 'ць', 'ч', 'ш','b', 'c', 'd', 'f', 'g', 'h', 'j',
		'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z']
		count_vow, count_con = [0,0]
		for x in text:
			for y in vowels:
				if y == x.lower():
					count_vow+=1
			for y in consonant:
				if x.lower() == y:
					count_con+=1
		return f"Vowels {count_vow}, Consonant {count_con}, All charapters {len(text)}"
	def edited(self):
		title = self.mainwindow.windowTitle()
		if title[len(title)-9:] != " - Edited":
			self.mainwindow.setWindowTitle(title+" - Edited")
	def cursorr(self, *c, **kwargs):
		all_pos = self.textBrowser.textCursor().anchor()
		pos = self.textBrowser.textCursor().positionInBlock()
		col = self.textBrowser.textCursor().columnNumber()
		return f"Line {self.get_lines(self.textBrowser.toPlainText(),all_pos)+1}, Column {pos+1}"
	def get_lines(self,text, pos):
		original = copy(text)
		cur_pos = len(original) - pos
		text = text.split('\n')
		i = 0
		for x in text:
			if pos - len(x) <=0:
				break
			pos -=len(x)
			i += 1
		return i
	def openFile(self):
		dlg = QtWidgets.QFileDialog()
		dlg.setFileMode(QtWidgets.QFileDialog.AnyFile)
		try:
			files = copy(self.filenames)
		except AttributeError:
			files = []
		if dlg.exec_():
			self.filenames = dlg.selectedFiles()
		if files == self.filenames:
			return False
		try:
			with open(self.filenames[0], 'rb') as file:
				try:
					self.textBrowser.setText(str(file.read().decode('utf-8')))
				except UnicodeDecodeError:
					file.seek(0)
					text = str(file.read())
					self.textBrowser.setText(text[2:len(text)-1])
				self.mainwindow.setWindowTitle(self.filenames[0].split('/')[-1])
		except IsADirectoryError:
			return
		self.show_info()
	def change_size(self):
		msg = QtWidgets.QMessageBox()
		msg.setObjectName("lay")
		msg.setStyleSheet("#lay{background-color:#FFF;}")
		self.scroll = QtWidgets.QSlider(QtCore.Qt.Horizontal)
		self.scroll.setFixedSize(200, 20)
		self.scroll.setMinimum(0)
		self.scroll.setMaximum(101)
		self.scroll.setProperty("value", self.font_size)
		self.scroll.sliderMoved.connect(self.__value_changed__)
		self.scroll.setOrientation(QtCore.Qt.Horizontal)
		self.labe = QtWidgets.QLabel(text=str(self.font_size))
		self.labe.setStyleSheet("margin:0;padding:0;")
		self.labe.setAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter)
		msg.layout().addWidget(self.labe, 0, 1)
		msg.layout().addWidget(self.scroll, 0, 0)
		msg.exec()
	def __value_changed__(self):
		self.labe.setText(str(self.scroll.value()))
		self.font_size = self.scroll.value()
		font = self.textBrowser.font()
		font.setPointSize(self.font_size)
		self.textBrowser.setFont(font)
	def change_font_family(self):
		msg = QtWidgets.QMessageBox()
		msg.setObjectName("lay")
		msg.setStyleSheet("#lay{background-color:#FFF;}")
		self.chose_color = QtWidgets.QFontComboBox()
		self.chose_color.setCurrentText(self.font_family)
		self.chose_color.currentIndexChanged.connect(self.__change_font__)
		msg.layout().addWidget(self.chose_color, 0, 0,1,0)
		msg.exec()
	def __change_font__(self):
		self.font_family = self.chose_color.currentText()
		font = self.textBrowser.font()
		font.setFamily(self.chose_color.currentText())
		self.textBrowser.setFont(font)
	def change_color(self):
		self.color = QtWidgets.QColorDialog()
		self.color.currentColorChanged.connect(self.__change_font_color__)
		self.color.exec()
	def __change_font_color__(self):
		self.textBrowser.setTextColor(self.color.currentColor())
	def change_bgcolor(self):
		self.color = QtWidgets.QColorDialog()
		self.color.currentColorChanged.connect(self.__change_bg_color__)
		self.color.exec()
	def __change_bg_color__(self):
		self.textBrowser.setTextBackgroundColor(self.color.currentColor())
	def change_abgcolor(self):
		self.color = QtWidgets.QColorDialog()
		self.color.currentColorChanged.connect(self.__change_abg_color__)
		self.color.exec()
	def __change_abg_color__(self):
		self.textBrowser.setStyleSheet(f"background-color: #{self.to_hex(self.color.currentColor().getRgb())};")
		print(f"background-color: #{self.to_hex(self.color.currentColor().getRgb())};")
	def to_hex(self, color):
		res = []
		color = list(color)
		for x in range(0,3):
			res.append("")
			while color[x]/16 > 0:
				y = color[x]%16
				color[x] //=16
				if y == 10:
					y="A"
				elif y == 11:
					y="B"
				elif y == 12:
					y="C"
				elif y == 13:
					y="D"
				elif y == 14:
					y="E"
				elif y == 15:
					y="F"
				res[x]+=str(y)
			res[x] = res[x][::-1]
		return f"{res[0]}{res[1]}{res[2]}"
app = QtWidgets.QApplication([])
application = mywindow(app)
application.show()
sys.exit(app.exec())
