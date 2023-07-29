from ._anvil_designer import CustomersTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import json
from datetime import datetime
from ..UserPopover import UserPopover
from anvil_extras import popover
import anvil.js
import anvil.media

class Customers(CustomersTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.refresh_data_bindings()
    self.drop_down_1.items = ['name', 'date']
    self.drop_down_1.selected_value = self.drop_down_1.items[0]
    usr = anvil.server.call('getusername')
    words = usr.split()
# Extract the first character of each word and convert it to uppercase
    initials = [word[0].upper() for word in words]
# Join the initials together
    initials_string = ''.join(initials)
    self.username_label.text = initials_string
    #self.repeating_panel_1.items = app_tables.customers.search(tables.order_by('name'))
    rxt = anvil.server.call('getcustomers')
    rxt = rxt.get_bytes().decode('utf-8')
    rxt = json.loads(rxt)
    leng = len(rxt)
    self.customers_no.text = str(leng)
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
        'kplc_meter' : g['kplc_meter'],
        'index': 0,
        'status': 'None'
      }
      my_arr.append(data)
    r = anvil.server.call('getloans')
    r = r.get_bytes().decode('utf-8')
    r = json.loads(r)
    thearray = []
    for h in r:
      original_datetime_str = h['last_payment']
      # Parse the original datetime string into a datetime object
      original_datetime_obj = datetime.strptime(original_datetime_str, '%Y-%m-%dT%H:%M:%S.%f%z')
# Format the datetime object back to the desired string format
      formatted_datetime_str = original_datetime_obj.strftime('%Y-%m-%dT%H:%M:%S')
      datetime_obj = datetime.strptime(dat, "%Y-%m-%d %H:%M:%S")
      formatted_date = datetime_obj.strftime("%d %B %Y %I:%M %p")
      madata = {
        'id': int(h['id']),
        'status': h['status'],
        'vendor': h['vendor'],
        'last_payment': formatted_date,
        'installments' : h['installments'],
        'payment_period': h['payment_period'],
        'deposit': h['deposit'],
        'product': h['product']
      }
      thearray.append(madata)
      
    # Sort the my_arr list by the 'id' field
    sorted_arr = sorted(my_arr, key=lambda item: item['id'])
    anotherOne = []
    for obj2 in thearray:
      id_to_check = obj2['id']
    # Check if the id exists in arr1
      if any(obj1['id'] == id_to_check for obj1 in sorted_arr):
        # Append the matching id to arr3
        anotherOne.append(id_to_check)
    index = 1
    self.loans = anotherOne
    for m in sorted_arr:
      m['index'] = index
      index = index + 1
    for e in sorted_arr:
      e['index'] = str(e['index'])
      if (e['id'] in anotherOne):
        e['status'] = 'Active'
    self.repeating_panel_1.items = sorted_arr
    nm = len(sorted_arr)
    if nm == 1:
      self.result_label.text = 'showing '+str(nm)+' result'
    else:      
      self.result_label.text = 'showing '+str(nm)+' results'
    self.item = sorted_arr
    self.arr = sorted_arr
    # Any code you write here will run before the form opens.
    self.username_label.popover(UserPopover(), 
                          placement = 'bottom', 
                          trigger='stickyhover', 
                          delay={ "show": 100, "hide": 100 },
                          max_width='700px'
                         )

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
    index = 1
    for w in filtered_objects:
      w['index'] = index
      index = index + 1
    for e in filtered_objects:
      e['index'] = str(e['index'])
    self.repeating_panel_1.items = filtered_objects
    nm = len(self.repeating_panel_1.items)
    if nm == 1:
      self.result_label.text = 'showing '+str(nm)+' result'
    else:
      self.result_label.text = 'showing '+str(nm)+' results'
    

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
    c = confirm('Are you sure you want to logout?', buttons=[("Yes", True),("No", False)])
    if(c==True):
      open_form('Login')
    else:
      pass

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('CustomerAnalytics', self.item)

  def drop_down_1_change(self, **event_args):
    """This method is called when an item is selected"""
    x = self.drop_down_1.selected_value
    nm = len(self.repeating_panel_1.items)
    self.result_label.text = 'showing '+str(nm)+' results'
    if x == 'date':
      for e in self.item:
        e['index'] = str(e['index'])
      self.repeating_panel_1.items = self.item
      nm = len(self.repeating_panel_1.items)
      if nm == 1:
        elf.result_label.text = 'showing '+str(nm)+' result'
      else:
        self.result_label.text = 'showing '+str(nm)+' results'
      self.search.text = ''
      self.search.visible = False
      self.from_date.visible = True
      self.to_date.visible = True
      self.calender_from.visible = True
      self.calender_to.visible = True
      
    else:
      for e in self.item:
        e['index'] = str(e['index'])
      self.repeating_panel_1.items = self.item
      nm = len(self.repeating_panel_1.items)
      if nm == 1:
        self.result_label.text = 'showing '+str(nm)+' result'
      else:
        self.result_label.text = 'showing '+str(nm)+' results'
      self.search.visible = True
      self.from_date.visible = False
      self.to_date.visible = False
      self.calender_from.visible = False
      self.calender_to.visible = False
      self.query.visible = False
      self.calender_from.date = None
      self.calender_to.date = None

  def calender_to_change(self, **event_args):
    """This method is called when the selected date changes"""
    if self.calender_to.date and self.calender_from.date is not None:
      self.query.visible = True
    else:
      self.query.visible = False

  def query_click(self, **event_args):
    """This method is called when the button is clicked"""
    frm = str(self.calender_from.date)
    to = str(self.calender_to.date)
    frm = datetime.strptime(frm, "%Y-%m-%d")
    to = datetime.strptime(to, "%Y-%m-%d")
    nw_arr = []
    for z in self.item:
      dt = datetime.strptime(z['date'], "%d %B %Y %I:%M %p")
      if dt <= to and dt >= frm:
        nw_arr.append(z)
      else:
        pass
    index = 1
    for y in nw_arr:
      y['index'] = index
      index = index + 1
    for e in nw_arr:
      e['index'] = str(e['index'])
    self.repeating_panel_1.items = nw_arr
    nm = len(self.repeating_panel_1.items)
    if nm == 1:
      self.result_label.text = 'showing '+str(nm)+' result'
    else:
      self.result_label.text = 'showing '+str(nm)+' results'
    

  def calender_from_change(self, **event_args):
    """This method is called when the selected date changes"""
    if self.calender_to.date and self.calender_from.date is not None:
      self.query.visible = True
    else:
      self.query.visible = False

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    sheet = anvil.server.call('download_customers', self.arr)
    anvil.media.download(sheet)

    



        
    


      
      
      













    






