from ._anvil_designer import PasswordTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Password(PasswordTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.
  

  def pin_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    text_len = len(str(self.pin.text))
    if(text_len==4):
      text = self.pin.text
      if(text==1234):
        self.raise_event("x-close-alert")
        open_form('Transactions', False)
      else:
        alert('Wrong PIN')
        self.pin.text = ''
    else:
      pass
      

