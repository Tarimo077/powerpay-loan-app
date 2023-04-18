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
    sorted_items = sorted(my_array, key=lambda x: x['deviceID'])
    self.repeating_panel_1.items = sorted_items
    active_devs = 0
    inactive_devs = 0
    for obj in my_array:
      if obj["active"]:
        active_devs += 1
      else:
        inactive_devs += 1

    self.activeDevs.text = "   "+str(active_devs)
    self.inactiveDevs.text = "   "+str(inactive_devs)
    #my_obj = ItemTemplate6()
    #usr = self.item
    #my_obj.getItem(usr)
      #ItemTemplate6.get_rws(self,actve,dev)
      

    # Any code you write here will run before the form opens.

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Home')

  def link_2_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Products')

  def link_3_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Customers')

  def request_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Request')
    
  def repeating_panel_1_show(self, **event_args):
    """This method is called when the RepeatingPanel is shown on the screen"""
    self.refresh_data_bindings()





