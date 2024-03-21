from ._anvil_designer import IndexTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..EnergySummary import EnergySummary
from ..CookingSummary import CookingSummary
from ..EmissionSummary import EmissionSummary

class Index(IndexTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    e = EnergySummary()
    self.containerHolder.add_component(e, full_width_row=True)

    # Any code you write here will run before the form opens.

  def energyTab_tab_click(self, tab_index, tab_title, **event_args):
    """This method is called when a tab is clicked"""
    self.energyTab.background = "#0800FF"
    self.energyTab.foreground = "#FFFFFF"
    self.energyTab.enabled = False
    self.cookingTab.enabled = True
    self.deviceTab.enabled = True
    self.energyTab.bold = True
    self.cookingTab.bold = False
    self.deviceTab.bold = False
    self.cookingTab.background = "FFFFFF"
    self.cookingTab.foreground = "#0800FF"
    self.deviceTab.background = "FFFFFF"
    self.deviceTab.foreground = "#0800FF"
    self.containerHolder.clear()
    e = EnergySummary()
    self.containerHolder.add_component(e, full_width_row=True)

  def cookingTab_tab_click(self, tab_index, tab_title, **event_args):
    """This method is called when a tab is clicked"""
    self.cookingTab.background = "#0800FF"
    self.cookingTab.foreground = "#FFFFFF"
    self.energyTab.enabled = True
    self.cookingTab.enabled = False
    self.deviceTab.enabled = True
    self.cookingTab.bold = True
    self.energyTab.bold = False
    self.deviceTab.bold = False
    self.energyTab.border
    self.energyTab.background = "FFFFFF"
    self.energyTab.foreground = "#0800FF"
    self.deviceTab.background = "FFFFFF"
    self.deviceTab.foreground = "#0800FF"
    self.containerHolder.clear()
    c = CookingSummary()
    self.containerHolder.add_component(c, full_width_row=True)

  def deviceTab_tab_click(self, tab_index, tab_title, **event_args):
    """This method is called when a tab is clicked"""
    self.deviceTab.background = "#0800FF"
    self.deviceTab.foreground = "#FFFFFF"
    self.energyTab.enabled = True
    self.cookingTab.enabled = True
    self.deviceTab.enabled = False
    self.deviceTab.bold = True
    self.cookingTab.bold = False
    self.energyTab.bold = False
    self.cookingTab.background = "FFFFFF"
    self.cookingTab.foreground = "#0800FF"
    self.energyTab.background = "FFFFFF"
    self.energyTab.foreground = "#0800FF"
    self.containerHolder.clear()
    d = EmissionSummary()
    self.containerHolder.add_component(d)
