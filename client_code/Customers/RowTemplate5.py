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
    # Any code you write here will run before the form opens.
    if self.label_1.text == 'Active':
      self.status.background = "#8cfe00"
    else:
      self.status.background = "#79747E"


  def see_more_click(self, **event_args):
    """This method is called when the button is clicked"""
    data = Customers().item
    for x in data:
      if self.item['id'] == x['id']:
        arr = x
    open_form('CustomerDetails', arr)
    


