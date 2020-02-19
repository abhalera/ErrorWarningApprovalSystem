import os
# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Feb 11 2020)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class frameMain
###########################################################################

class frameMain ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Error Warning Approval System", pos = wx.DefaultPosition, size = wx.Size( 1262,790 ), style = wx.DEFAULT_FRAME_STYLE )
		
		self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )
		
		self.m_menubarMain = wx.MenuBar( 0 )
		self.m_menuFile = wx.Menu()
		self.m_menuItemNew = wx.MenuItem( self.m_menuFile, wx.ID_ANY, u"&New", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuFile.Append( self.m_menuItemNew )
		
		self.m_menuItemOpen = wx.MenuItem( self.m_menuFile, wx.ID_ANY, u"&Open", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuFile.Append( self.m_menuItemOpen )
		
		self.m_menuItemClose = wx.MenuItem( self.m_menuFile, wx.ID_ANY, u"&Close", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuFile.Append( self.m_menuItemClose )
		
		self.m_menuItemSave = wx.MenuItem( self.m_menuFile, wx.ID_ANY, u"Save", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuFile.Append( self.m_menuItemSave )
		
		self.m_menuItemSaveAll = wx.MenuItem( self.m_menuFile, wx.ID_ANY, u"Save All", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuFile.Append( self.m_menuItemSaveAll )
		
		self.m_menuFile.AppendSeparator()
		
		self.m_menuItemQuit = wx.MenuItem( self.m_menuFile, wx.ID_ANY, u"&Quit", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuFile.Append( self.m_menuItemQuit )
		
		self.m_menubarMain.Append( self.m_menuFile, u"&File" ) 
		
		self.m_menuEdit = wx.Menu()
		self.m_menuItemCopy = wx.MenuItem( self.m_menuEdit, wx.ID_ANY, u"Copy", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuEdit.Append( self.m_menuItemCopy )
		
		self.m_menuItemPaste = wx.MenuItem( self.m_menuEdit, wx.ID_ANY, u"Paste", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuEdit.Append( self.m_menuItemPaste )
		
		self.m_menuEdit.AppendSeparator()
		
		self.m_menuItemPreferences = wx.MenuItem( self.m_menuEdit, wx.ID_ANY, u"Preferences", wx.EmptyString, wx.ITEM_NORMAL )
		self.m_menuEdit.Append( self.m_menuItemPreferences )
		
		self.m_menubarMain.Append( self.m_menuEdit, u"Edit" ) 
		
		self.SetMenuBar( self.m_menubarMain )
		
		self.m_toolBarMain = self.CreateToolBar( wx.TB_HORIZONTAL|wx.RAISED_BORDER, wx.ID_ANY ) 
		self.m_toolNew = self.m_toolBarMain.AddTool( wx.ID_ANY, u"tool", wx.Bitmap( os.environ["EWAS_ROOT"] + "/wxformbuilder/" + u"iconfinder_New_1493292.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, u"New", u"New", None ) 
		
		self.m_toolOpen = self.m_toolBarMain.AddTool( wx.ID_ANY, u"tool", wx.Bitmap( os.environ["EWAS_ROOT"] + "/wxformbuilder/" + u"iconfinder_Close_1493281.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, u"Open", u"Open", None ) 
		
		self.m_toolSave = self.m_toolBarMain.AddTool( wx.ID_ANY, u"tool", wx.Bitmap( os.environ["EWAS_ROOT"] + "/wxformbuilder/" + u"iconfinder_3floppy_unmount_18268.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, u"Save", u"Save", None ) 
		
		self.m_toolSaveAll = self.m_toolBarMain.AddTool( wx.ID_ANY, u"tool", wx.Bitmap( os.environ["EWAS_ROOT"] + "/wxformbuilder/" + u"iconfinder_save_all_18901.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, u"Save All", u"Save All", None ) 
		
		self.m_toolClose = self.m_toolBarMain.AddTool( wx.ID_ANY, u"tool", wx.Bitmap( os.environ["EWAS_ROOT"] + "/wxformbuilder/" + u"iconfinder_Delete_1493279.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, u"Close", u"Close", None ) 
		
		self.m_toolBarMain.AddSeparator()
		
		self.m_toolCut = self.m_toolBarMain.AddTool( wx.ID_ANY, u"tool", wx.Bitmap( os.environ["EWAS_ROOT"] + "/wxformbuilder/" + u"iconfinder_Cut_1493291.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, u"Cut", u"Cut", None ) 
		
		self.m_toolCopy = self.m_toolBarMain.AddTool( wx.ID_ANY, u"tool", wx.Bitmap( os.environ["EWAS_ROOT"] + "/wxformbuilder/" + u"iconfinder_Copy_1493280.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, u"Copy", u"Copy", None ) 
		
		self.m_tool10 = self.m_toolBarMain.AddTool( wx.ID_ANY, u"tool", wx.Bitmap( os.environ["EWAS_ROOT"] + "/wxformbuilder/" + u"iconfinder_Paste_1493290.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.m_toolBarMain.AddSeparator()
		
		self.m_toolPreferences = self.m_toolBarMain.AddTool( wx.ID_ANY, u"tool", wx.Bitmap( os.environ["EWAS_ROOT"] + "/wxformbuilder/" + u"iconfinder_Options_1493287.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, u"Preferences", u"Preferences", None ) 
		
		self.m_toolReport = self.m_toolBarMain.AddTool( wx.ID_ANY, u"tool", wx.Bitmap( os.environ["EWAS_ROOT"] + "/wxformbuilder/" + u"iconfinder_start_60207.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, u"Run", u"Run", None ) 
		
		self.m_toolBarMain.Realize() 
		
		self.m_statusBarMain = self.CreateStatusBar( 1, 0|wx.SUNKEN_BORDER, wx.ID_ANY )
		bSizerMainContents = wx.BoxSizer( wx.HORIZONTAL )
		
		bSizerSidebar = wx.BoxSizer( wx.VERTICAL )
		
		m_radioBoxErrorWarningChoices = [ u"Erorrs Only", u"Warnings Only", u"Both" ]
		self.m_radioBoxErrorWarning = wx.RadioBox( self, wx.ID_ANY, u"E/W Filter", wx.DefaultPosition, wx.DefaultSize, m_radioBoxErrorWarningChoices, 3, wx.RA_SPECIFY_ROWS )
		self.m_radioBoxErrorWarning.SetSelection( 0 )
		bSizerSidebar.Add( self.m_radioBoxErrorWarning, 0, wx.ALL, 5 )
		
		m_radioBoxReportingVerbosityChoices = [ u"1", u"2", u"3", u"4", u"5" ]
		self.m_radioBoxReportingVerbosity = wx.RadioBox( self, wx.ID_ANY, u"Reporting Verbosity", wx.DefaultPosition, wx.DefaultSize, m_radioBoxReportingVerbosityChoices, 5, wx.RA_SPECIFY_ROWS )
		self.m_radioBoxReportingVerbosity.SetSelection( 0 )
		bSizerSidebar.Add( self.m_radioBoxReportingVerbosity, 0, wx.ALL, 5 )
		
		self.m_textCtrlXLSX = wx.TextCtrl( self, wx.ID_ANY, u"Enter filename to dump XLSX", wx.DefaultPosition, wx.DefaultSize, 0 )
		bSizerSidebar.Add( self.m_textCtrlXLSX, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		bSizerMainContents.Add( bSizerSidebar, 1, wx.EXPAND, 5 )
		
		self.m_notebookMain = wx.Notebook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		
		bSizerMainContents.Add( self.m_notebookMain, 10, wx.EXPAND |wx.ALL, 5 )
		
		
		self.SetSizer( bSizerMainContents )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.Bind( wx.EVT_MENU, self.NewRun, id = self.m_menuItemNew.GetId() )
		self.Bind( wx.EVT_MENU, self.OpenRun, id = self.m_menuItemOpen.GetId() )
		self.Bind( wx.EVT_MENU, self.CloseRun, id = self.m_menuItemClose.GetId() )
		self.Bind( wx.EVT_MENU, self.SaveRun, id = self.m_menuItemSave.GetId() )
		self.Bind( wx.EVT_MENU, self.SaveAllRun, id = self.m_menuItemSaveAll.GetId() )
		self.Bind( wx.EVT_MENU, self.QuitApplication, id = self.m_menuItemQuit.GetId() )
		self.Bind( wx.EVT_MENU, self.Copy, id = self.m_menuItemCopy.GetId() )
		self.Bind( wx.EVT_MENU, self.Paste, id = self.m_menuItemPaste.GetId() )
		self.Bind( wx.EVT_MENU, self.Preferences, id = self.m_menuItemPreferences.GetId() )
		self.Bind( wx.EVT_TOOL, self.NewRun, id = self.m_toolNew.GetId() )
		self.Bind( wx.EVT_TOOL, self.OpenRun, id = self.m_toolOpen.GetId() )
		self.Bind( wx.EVT_TOOL, self.SaveRun, id = self.m_toolSave.GetId() )
		self.Bind( wx.EVT_TOOL, self.SaveAllRun, id = self.m_toolSaveAll.GetId() )
		self.Bind( wx.EVT_TOOL, self.CloseRun, id = self.m_toolClose.GetId() )
		self.Bind( wx.EVT_TOOL, self.Preferences, id = self.m_toolPreferences.GetId() )
		self.Bind( wx.EVT_TOOL, self.Run, id = self.m_toolReport.GetId() )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def NewRun( self, event ):
		event.Skip()
	
	def OpenRun( self, event ):
		event.Skip()
	
	def CloseRun( self, event ):
		event.Skip()
	
	def SaveRun( self, event ):
		event.Skip()
	
	def SaveAllRun( self, event ):
		event.Skip()
	
	def QuitApplication( self, event ):
		event.Skip()
	
	def Copy( self, event ):
		event.Skip()
	
	def Paste( self, event ):
		event.Skip()
	
	def Preferences( self, event ):
		event.Skip()
	
	
	
	
	
	
	
	def Run( self, event ):
		event.Skip()
	

