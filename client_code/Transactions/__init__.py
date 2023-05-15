from ._anvil_designer import TransactionsTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import json

class Transactions(TransactionsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    res = anvil.server.call('getcashin')
    text = res.get_bytes().decode('utf-8')
    my_array = json.loads(text)
    amounts = []
    refs = []
    times = []
    latest_trans = []
    for x in my_array:
      amounts.append(x['amount'])
      refs.append(x['id'])
      times.append(x['transtime'])
    amnt = 0
    for y in amounts:
      amnt = amnt + y
      
    latest_trans = my_array[-5:]
    self.moneyin.text = "KSH "+str(amnt)
    self.repeating_panel_1.items = latest_trans

    # Any code you write here will run before the form opens.

  def home_link_copy_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Transactions')

  def home_link_copy_2_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Support')

  def home_link_copy_3_click(self, **event_args):
    """This method is called when the link is clicked"""
    c = confirm('Are you sure you want to logout?')
    if(c==True):
      open_form('Login')
    else:
      pass

  def home_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Home', 0)

  def customers_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Customers')

  def request_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Request')






