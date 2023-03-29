from ._anvil_designer import CustomersTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Customers(CustomersTemplate):
  def __init__(self, user_tag, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.refresh_data_bindings()
    self.item = user_tag
    self.user.text = user_tag
    self.repeating_panel_1.items = app_tables.customers.search(tables.order_by('name'))

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

  def search_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    search_text = self.search.text
    self.repeating_panel_1.items = app_tables.customers.search(name=q.ilike(search_text+'%'))

  def addcustomer_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('AddCustomer', self.item)



    






