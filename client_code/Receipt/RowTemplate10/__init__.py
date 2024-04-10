from ._anvil_designer import RowTemplate10Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class RowTemplate10(RowTemplate10Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.qty.text = self.item['qty']
    self.desc.text = self.item['desc']
    self.amnt.text = self.item['amnt']

    # Any code you write here will run before the form opens.

  def amnt_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    self.item['amnt'] = self.amnt.text

  def desc_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    self.item['desc'] = self.desc.text

  def qty_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    self.item['qty'] = self.qty.text
