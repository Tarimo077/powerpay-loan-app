from ._anvil_designer import RequestTemplate
from anvil import *
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import json

class Request(RequestTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def send_click(self, **event_args):
    """This method is called when the button is clicked"""    
    data = self.data.text
    dt = {
      "data": data
    }
    response = anvil.server.call('req', dt)
    text = response.get_bytes().decode('utf-8')
    self.display.text = text

