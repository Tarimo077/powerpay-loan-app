from ._anvil_designer import ChatTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Chat(ChatTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.

    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    prompt = self.text_box_1.text
    self.text_area_1.text += prompt
    response = anvil.server.call('getChat', prompt)
    self.text_area_1.text += response
    

