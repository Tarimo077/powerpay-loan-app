from ._anvil_designer import CustomersTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import json
from datetime import datetime

class Customers(CustomersTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.refresh_data_bindings()
    usr = anvil.server.call('getusername')
    print('Logged in as '+usr)
    #self.repeating_panel_1.items = app_tables.customers.search(tables.order_by('name'))
    rxt = anvil.server.call('getcustomers')
    rxt = rxt.get_bytes().decode('utf-8')
    rxt = json.loads(rxt)
    my_arr = []
    for g in rxt:
      dat = g['date']
      datetime_obj = datetime.strptime(dat, "%Y-%m-%d %H:%M:%S")
      formatted_date = datetime_obj.strftime("%d %B %Y %I:%M %p")
      data = {
        'id' : int(g['id']),
        'email' : g['email'],
        'name' : g['name'],
        'contact' : g['contact'],
        'age' : g['age'],
        'date' : formatted_date,
        'county': g['county'],
        'sub_county': g['sub_county'],
        'gender' : g['gender'],
        'salary' : g['salary'],
        'kplc_meter' : g['kplc_meter']
      }
      my_arr.append(data)
    # Sort the my_arr list by the 'id' field
    sorted_arr = sorted(my_arr, key=lambda item: item['id'])
    self.repeating_panel_1.items = sorted_arr
    self.item = sorted_arr  

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
    leng = len(search_text)
    filtered_objects = [obj for obj in self.item if obj['name'][:leng].lower() == search_text.lower()]
    self.repeating_panel_1.items = filtered_objects

  def addcustomer_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('AddCustomer')

  def request_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Request')

  def home_link_copy_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form("Transactions", True)

  def home_link_copy_2_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Support')

  def link_1_copy_click(self, **event_args):
    """This method is called when the link is clicked"""
    c = confirm('Are you sure you want to logout?')
    if(c==True):
      open_form('Login')
    else:
      pass











    






