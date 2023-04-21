from ._anvil_designer import CustomersTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Customers(CustomersTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.refresh_data_bindings()
    self.repeating_panel_1.items = app_tables.customers.search(tables.order_by('name'))

    # Any code you write here will run before the form opens.

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Home', 0)

  def link_3_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Customers')

  def search_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    search_text = self.search.text
    self.repeating_panel_1.items = app_tables.customers.search(name=q.ilike(search_text+'%'))

  def addcustomer_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('AddCustomer')

  def request_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Request')

  def home_link_copy_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Support')

  def home_link_copy_2_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Login')






    






