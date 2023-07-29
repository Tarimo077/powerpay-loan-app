from ._anvil_designer import CustomerDetailsTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class CustomerDetails(CustomerDetailsTemplate):
  def __init__(self, arr, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.item = arr

    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Customers')

