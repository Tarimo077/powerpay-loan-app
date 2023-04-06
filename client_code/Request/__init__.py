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
  def __init__(self,user_tag, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.item = user_tag
    self.user.text = user_tag
    dt = {
      "data": 'GET'
    }
    response = anvil.server.call('req', dt)
    text = response.get_bytes().decode('utf-8')
    my_array = json.loads(text)
    self.repeating_panel_1.items = my_array
      #ItemTemplate6.get_rws(self,actve,dev)
      

    # Any code you write here will run before the form opens.

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Home', self.item)

  def link_2_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Products', self.item)

  def link_3_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Customers', self.item)

  def request_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Request', self.item)




