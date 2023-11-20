from ._anvil_designer import RowTemplate5Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from . import Customers

class RowTemplate5(RowTemplate5Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.see_more.tooltip = "click here to see more details about " + str(self.item['name'])
    # Any code you write here will run before the form opens.
    if self.label_1.text == 'On Track':
      self.status.background = "#8cfe00"
      self.label_1.tooltip = str(self.item['name'] + " is on track with payments")
      self.status.tooltip = str(self.item['name'] + " is on track with payments")
    elif self.label_1.text == 'None':
      self.status.background = "#79747E"
      self.label_1.tooltip = str(self.item['name'] + " has no active loans")
      self.status.tooltip = str(self.item['name'] + " has no active loans")
    elif self.label_1.text == 'Initiated':
      self.status.background = "#ffa500"
      self.label_1.tooltip = str(self.item['name'] + " has initiated a loan process")
      self.status.tooltip = str(self.item['name'] + " has initiated a loan process")
    else:
      self.status.background = "#0080FF"
      self.label_1.tooltip = str(self.item['name'] + " has completed their loan")
      self.status.tooltip = str(self.item['name'] + " has completed their loan")
      

  def see_more_click(self, **event_args):
    """This method is called when the button is clicked"""
    data = Customers().item
    for x in data:
      if self.item['id'] == x['id']:
        arr = x
    open_form('CustomerDetails', arr)
    


