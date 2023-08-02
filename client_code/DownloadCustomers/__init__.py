from ._anvil_designer import DownloadCustomersTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.media

class DownloadCustomers(DownloadCustomersTemplate):
  def __init__(self, arr, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.arr = arr
    # Any code you write here will run before the form opens.

  def pin_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    text_len = len(str(self.pin.text))
    if(text_len==4):
      text = self.pin.text
      if(text==1234):
        self.raise_event("x-close-alert")
        sheet = anvil.server.call('download_customers', self.arr)
        anvil.media.download(sheet)
      else:
        alert('Wrong PIN')
        self.pin.text = ''
    else:
      pass
