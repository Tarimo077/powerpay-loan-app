from ._anvil_designer import RequestTemplate
from anvil import *
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import json
from .ItemTemplate6 import ItemTemplate6

class Request(RequestTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    dt = {
      "data": 'GET'
    }
    response = anvil.server.call('req', dt)
    text = response.get_bytes().decode('utf-8')
    my_array = json.loads(text)
    self.repeating_panel_1.items = my_array
    myobj = ItemTemplate6()
    for x in my_array:
      actve = x["active"]
      dev = x["deviceID"]
      ItemTemplate6.get_rws(self,actve,dev)

    # Any code you write here will run before the form opens.

  def send_click(self, **event_args):
    """This method is called when the button is clicked"""    
    keys_to_extract = ['deviceID', 'active']
    key_res = []
    val_res = []
    for my_object in my_array:
      extracted_keys = {}
      for key, value in my_object.items(): 
        if key in keys_to_extract:
          key_res.append(str(key)+":"+str(value))
          #val_res.append(value)
        #    extracted_keys[key] = value
