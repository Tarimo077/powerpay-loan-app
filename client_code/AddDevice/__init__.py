from ._anvil_designer import AddDeviceTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import json


class AddDevice(AddDeviceTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.deviceName.text is None:
      alert("Kindly enter device name")
      return
    else:
      ale = alert("Are you sure you want to add device "+"'"+self.deviceName.text+"'", buttons=[("Yes", True), ("No", False)], dismissible=False, title=None)
      if ale:
        dt = {
          "device": self.deviceName.text
        }
        anvil.server.call('addDevice', dt)
        self.raise_event("x-close-alert")
        open_form('Request')
      else:
        self.raise_event("x-close-alert")
        open_form("Request")
        
