from ._anvil_designer import ItemTemplate6Template
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import Request
import anvil.server
import json


class ItemTemplate6(ItemTemplate6Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

  def get_rws(self, actve, dev, **properties):
    self.active.text = actve
    self.devid.text = dev
      
    
    
    

    # Any code you write here will run before the form opens.
