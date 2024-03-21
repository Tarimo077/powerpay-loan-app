from ._anvil_designer import IndexTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Index(IndexTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def energyTab_tab_click(self, tab_index, tab_title, **event_args):
    """This method is called when a tab is clicked"""
    self.energyTab.background = "#0800FF"
    self.energyTab.foreground = "#FFFFFF"
    self.energyTab.bold = True
    self.cookingTab.bold = False
    self.deviceTab.bold = False
    self.cookingTab.background = "FFFFFF"
    self.cookingTab.foreground = "#0800FF"
    self.deviceTab.background = "FFFFFF"
    self.deviceTab.foreground = "#0800FF"

  def cookingTab_tab_click(self, tab_index, tab_title, **event_args):
    """This method is called when a tab is clicked"""
    self.cookingTab.background = "#0800FF"
    self.cookingTab.foreground = "#FFFFFF"
    self.cookingTab.bold = True
    self.energyTab.bold = False
    self.deviceTab.bold = False
    self.energyTab.border
    self.energyTab.background = "FFFFFF"
    self.energyTab.foreground = "#0800FF"
    self.deviceTab.background = "FFFFFF"
    self.deviceTab.foreground = "#0800FF"

  def deviceTab_tab_click(self, tab_index, tab_title, **event_args):
    """This method is called when a tab is clicked"""
    self.deviceTab.background = "#0800FF"
    self.deviceTab.foreground = "#FFFFFF"
    self.deviceTab.bold = True
    self.cookingTab.bold = False
    self.energyTab.bold = False
    self.cookingTab.background = "FFFFFF"
    self.cookingTab.foreground = "#0800FF"
    self.energyTab.background = "FFFFFF"
    self.energyTab.foreground = "#0800FF"
