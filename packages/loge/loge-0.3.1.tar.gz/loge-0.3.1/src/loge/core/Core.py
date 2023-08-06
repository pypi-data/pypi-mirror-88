# -*- coding: utf-8 -*-
#-----------------------------------------------------------------
# Copyright (C) 2017-2020, the Loge development team
#
# This file is part of Loge
# Loge is distributed under the terms of GNU General Public License
# The full license can be found in 'license.txt'
# Loge development team can be found in 'development.txt'
#-----------------------------------------------------------------

import subprocess
import idlelib
import traceback
import os

from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QMessageBox, QDialog, QInputDialog
from PyQt5.QtPrintSupport import QPrintDialog
from PyQt5.QtGui import QCursor

from loge.core.Script import Script
from loge.core.Shell import Shell
from loge.core.core_utils import abspath, get_html_from_memo, get_html_from_code, get_html_from_markdownfile

class Core():
    
    def __init__(self):
        self.Script = Script()
        self.Shell = Shell()
        self.Gui = None
        #---
        self.watcher = None
        self.timer = None
        #---
        self.set_watcher()
        self.set_timer()
        self.Shell.assign_code(self.Script)
        #---
        self.scrolls_data = {}

    def set_watcher(self):
        self.watcher = QtCore.QFileSystemWatcher()
        self.watcher.fileChanged.connect(self.script_changed)
        self.Script.set_watcher(self.watcher)

    def set_timer(self):
        # -- Timer --
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.TimerAction)

    def watcher_clicked(self,checked):
        if self.Script.script_path :
            if self.Gui.main_window.actions['watch_script'].isChecked():
                self.Script.activate_watcher()
            else:
                self.Script.deactivate_watcher()
        else:
            QMessageBox.information(None, 'Info', 'Please create or open script first')
            self.Gui.main_window.actions['watch_script'].setChecked(False)

    def script_changed(self,file):
        self.Script.reloadcode()
        self.refresh()

    #------------------------ 

    def refresh(self, waitcursor = True, silenceErrorMassage = False):
        successruned = False        
        message = None
        error_trace = None
        if waitcursor:
            QApplication.setOverrideCursor(QCursor(QtCore.Qt.WaitCursor))
        try:
            self.Script.parse()
            self.Shell.run_parsed()
            self.Gui.browser_reload(self.Shell.report_html)
            successruned = True
        except Exception as e:
            message = 'Some problem - ' + str(e)
            error_trace = str(traceback.format_exc())
        finally:
            QApplication.restoreOverrideCursor()
            self.Gui.warning_browser.hide()
            self.Gui.browser.setStyleSheet("background-color: White;")
        if not successruned and message:
            if silenceErrorMassage:
                self.Gui.warning_browser.show()
                self.Gui.warning_browser.setTextColor(QtCore.Qt.red)
                self.Gui.warning_browser.setText(message + '\n' + error_trace)
                self.Gui.browser.setStyleSheet("background-color: rgb(255, 240, 240);")
            else:
                QMessageBox.information(None, message, error_trace)
        #---
        apptitle=''
        if self.Script.script_path:
            apptitle = ' - ' + os.path.basename(self.Script.script_path)
        if self.Script.saveLock:
            apptitle += '  (read only)'
        apptitle = self.Gui.get_app_main_title() + apptitle
        self.Gui.set_app_title(apptitle)
        #---
        return successruned
    
    def synchronizeEditorToScript(self):
        if self.Script.code_oryginal != self.Gui.editor.toPlainText():
            self.Gui.editor.setPlainText(self.Script.code_oryginal)

    def synchronizeScriptToEditorAndRefresh(self):
        self.Script.code_oryginal = self.Gui.editor.toPlainText() 
        self.refresh(silenceErrorMassage=True)

    def reload_script_file(self):
        if self.Script.script_path :
            self.Script.reloadcode()
            self.synchronizeEditorToScript()
            self.refresh()
        else:
            QMessageBox.information(None, 'Info', 'Please create or open script first')

    #------------------------ 

    def file_new(self):
        template_path = abspath('templates/x_newtemplate.py')
        self.Shell.delete_tmpfile() #Cleaning Loge tmp files
        self.file_save_if_changed()#save current file if changed
        self.Script.newFile(template_path, 'Save new script as', 'newScript.py')
        self.synchronizeEditorToScript()
        self.refresh()
        #--File browser update
        self.Gui.file_browser.reload()
            
    def file_open(self, file_path = None, saveLock = False, browser_path_update=True):
        self.Shell.delete_tmpfile() #cleaning Loge tmp files
        self.scrolls_archive_positions()#archive scroll position
        self.file_save_if_changed()#save current file if changed
        self.Script.openFile(file_path, saveLock)
        self.synchronizeEditorToScript()
        self.refresh()
        self.scrols_load_position_from_archive()#load scroll position
        #--File browser update
        if browser_path_update:
            self.Gui.file_browser.reload()
        #--Timer
        self.TimerFromCode()

    def file_openreadonly(self, file_path = None):
        self.file_open(file_path = None, saveLock = True)

    def file_save(self):
        if self.Script.script_path :
            self.Script.code_oryginal = self.Gui.editor.toPlainText()
            if self.Script.savecode():
                self.Gui.main_window.showStatusInfo('Saved to '+ self.Script.script_path)
        else:
            self.file_saveas()

    def file_saveas(self):
        self.scrolls_archive_positions()#archive scroll position
        self.Script.saveAs()
        self.refresh()
        #--File browser update
        self.Gui.file_browser.reload()
    
    def file_save_if_changed(self):
        if self.Script.code_has_changed():
            # - ask if save changes
            dialogReply = QMessageBox.question( None, 'Loge', "Do you want save changes?", 
                                                QMessageBox.Yes | QMessageBox.No, 
                                                QMessageBox.No)
            if dialogReply == QMessageBox.Yes:
                self.file_save()

    def scrolls_archive_positions(self):
        if self.Script.script_path:
            scroll_editor = self.Gui.editor.verticalScrollBar().value()
            scroll_browser = self.Gui.browser.verticalScrollBar().value()
            #---
            self.scrolls_data[self.Script.script_path] = [scroll_editor, scroll_browser]

    def scrols_load_position_from_archive(self):
        if self.Script.script_path in self.scrolls_data:
            scroll_editor = self.scrolls_data[self.Script.script_path][0]
            self.Gui.editor.verticalScrollBar().setValue(scroll_editor)
            #---
            scroll_browser = self.scrolls_data[self.Script.script_path][1]
            self.Gui.browser.verticalScrollBar().setValue(scroll_browser)
        else:
            self.Gui.editor.verticalScrollBar().setValue(0)
            self.Gui.browser.verticalScrollBar().setValue(0)
            
    def scrolls_synchronize(self):
        if self.Gui.main_window.actions['editor_scroll_synchro'].isChecked():
            self.Gui.browser.scroll_to_relposition(self.Gui.editor.get_scroll_relposition())
        
    def show_file_browser(self):
        if self.Gui.main_window.actions['file_browser'].isChecked():
            self.Gui.file_browser.show()
            self.Gui.file_browser.reload()
        else:
            self.Gui.file_browser.hide()

    #------------------------ 

    def file_edit(self):
        if self.Script.saveLock:
            QMessageBox.information(None, 'Info', 'File open read only. Use save as option')
            return False
        if self.Gui.main_window.actions['file_edit'].isChecked():
            self.Gui.main_window.splitter_editor.show()
            self.Gui.toolbar_editor.setVisible(True)
            self.synchronizeEditorToScript()
        else:
            self.Gui.main_window.splitter_editor.hide()
            self.Gui.toolbar_editor.setVisible(False)

    #------------------------ 

    def show_python_source(self):
        html_page = get_html_from_code(self.Script.code_oryginal)
        self.Gui.set_browser_content(html_page)

    def show_html(self):
        html_page = get_html_from_code(self.Shell.report_html)
        self.Gui.set_browser_content(html_page)

    def show_markdown(self):
        html_page = get_html_from_code(self.Shell.report_markdown)
        self.Gui.set_browser_content(html_page)

    def show_loge(self):
        self.Gui.set_browser_content(self.Shell.report_html)

    def show_syntax(self):
        html_page = get_html_from_memo('x_syntax.md')
        self.Gui.set_browser_content(html_page)

    #------------------------
    def PreviewMarkdown(self):
        #---asking for file path
        filename = self.Script.open_markdown()
        if not filename == '':
            #---
            html_page = get_html_from_markdownfile(filename)
            self.Gui.set_browser_content(html_page)

    def SaveMarkdown(self):
        if self.Script.script_path :
            initname = os.path.basename(self.Script.script_path).replace('.py', '.md')
            self.Shell.save_report_markdown(self.Script.savedir, initname)
        else:
            QMessageBox.information(None, 'Info', 'Please create or open script first')

    #------------------------ 
            
    def startpage(self):
        html_page = get_html_from_memo('x_startpage.md')
        self.Gui.set_browser_content(html_page)

    def help(self):
        html_page = get_html_from_memo('x_help.md')
        self.Gui.set_browser_content(html_page)

    def about(self):
        html_page = get_html_from_memo('x_about.md')
        self.Gui.set_browser_content(html_page)

    #------------------------ 

    def file_print(self):
        dialog = QPrintDialog()
        if dialog.exec_() == QDialog.Accepted:
            self.Gui.get_browser_document().print_(dialog.printer())
    
    #------------------------ 

    def tutorial(self):
        tutorial_path = abspath('memos/x_tutorial.py')
        savedir = self.Script.savedir #coping current savedir
        #--opening oryginal tutorial
        self.Shell.delete_tmpfile()
        self.Script.openFile(tutorial_path)
        #---saving temporary tutorial copy
        tutorial_tmppath = os.path.join(self.Shell.tmpdir, 'tmp_tutorial.py')
        self.Script.saveAs(tutorial_tmppath)
        #---opening temporary tutorial copy
        self.Shell.delete_tmpfile()
        self.Script.openFile(tutorial_tmppath)
        self.Script.savedir = savedir #back to previouse savedir
        self.refresh()
        self.file_edit()

    #------------------------ 

    def floatprecision(self):
        if self.Script.script_path :
            #---asking for precision as int number
            value = QInputDialog.getInt(    None, 
                                            'Float display precysion', 'Set the precison:',
                                            value = self.Shell.float_display_precison,
                                            min = 1, max = 9, step = 1)[0]
            #---
            self.Shell.float_display_precison = value
            self.refresh()
        else:
            QMessageBox.information(None, 'Info', 'Please create or open script first')

    #-----------------------

    def TimerButtonClicked(self):
        if self.Script.script_path:
            if self.Gui.toolbar_timer.timerButton.isChecked():
                self.TimerStart()
            if not self.Gui.toolbar_timer.timerButton.isChecked():
                self.TimerStop()
        else:
            self.TimerStop()
            QMessageBox.information(None, 'Info', 'Please create or open script first')

    def TimerAction(self):
        if self.Script.script_path:
            if self.Gui.toolbar_timer.timerButton.isChecked():
                self.Gui.toolbar_timer.timerPulse.setChecked(not(self.Gui.toolbar_timer.timerPulse.isChecked()))
                self.refresh(False)

    #---------------------
    def TimerStart(self):
        timespace = int(self.Gui.toolbar_timer.timerSpinBox.value() * 1000)
        self.timer.start(timespace)
        self.Gui.toolbar_timer.timerButton.setChecked(True)
        self.Gui.toolbar_timer.timerSpinBox.setEnabled(False)
        self.Gui.toolbar_timer.timerPulse.setEnabled(True)
        self.refresh(False)
                
    def TimerStop(self):
        self.timer.stop()
        self.Gui.toolbar_timer.timerButton.setChecked(False)
        self.Gui.toolbar_timer.timerSpinBox.setEnabled(True)
        self.Gui.toolbar_timer.timerPulse.setChecked(False)
        self.Gui.toolbar_timer.timerPulse.setEnabled(False)

    def TimerFromCode(self):
        parameters = self.Script.getTimerParameters()
        if parameters:
            self.Gui.toolbar_timer.timerButton.setChecked(parameters[0])
            self.Gui.toolbar_timer.timerSpinBox.setValue(parameters[1])
            if parameters[0]:
                self.TimerStart()
        else:
            self.TimerStop()
            self.Gui.toolbar_timer.timerButton.setChecked(False)
            self.Gui.toolbar_timer.timerSpinBox.setValue(2.0)
