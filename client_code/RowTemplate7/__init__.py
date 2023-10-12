from ._anvil_designer import RowTemplate7Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class RowTemplate7(RowTemplate7Template):
  def __init__(self, myobj, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.item = myobj
    print("my item: " + str(self.item))
    if(self.item['active']==True):
      self.change_state.text = "Deactivate"
      self.change_state.background = "#ffa500"
      self.change_state.tooltip = "Turn Device Off"
    else:
      self.change_state.text = "Activate"
      self.change_state.background = "#8fce00"
      self.change_state.tooltip = "Turn Device On"

    # Any code you write here will run before the form opens.
