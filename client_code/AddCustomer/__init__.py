from ._anvil_designer import AddCustomerTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import datetime
import json

class AddCustomer(AddCustomerTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    #self.my_column_data = [row['product_name'] for row in app_tables.products.search()]
    #self.product_list.items = self.my_column_data
    self.slctlist = []
    self.db_list = []
    # Any code you write here will run before the form opens.
    res = anvil.server.call('getInfluxdb_devs')
    text = res.get_bytes().decode('utf-8')
    my_array = json.loads(text)
    sorted_items = sorted(my_array, key=lambda x: x['deviceID'])
    my_items = []
    for x in sorted_items:
      x = str(x['deviceID'])
      my_items.append(x)

    self.deviceList.items = my_items

  def addcustomer_click(self, **event_args):
    """This method is called when the button is clicked"""
    name = self.cname.text
    contact1 = self.contact.text
    id_num1 = self.id_num.text
    id_len = len(str(id_num1))
    contact_len = len(str(contact1))
    b = app_tables.customers.get(id_num=self.id_num.text,contact=self.contact.text)
    if name.strip() == '':
    # One or more fields are empty
      alert('Please fill in a name')
      return

    if id_len != 8:
    # The id field contains non-numeric characters
      alert('Please enter a valid ID')
      return
    if contact_len != 12:
    # The id field contains non-numeric characters
      alert('Please enter a valid contact')
      return
    if self.file_loader_1.file is None:
      alert('Kindly upload customer image')
      return
    if b is not None:
      alert('There already exists a customer with that id number and contact')
      return
    if self.deviceList.selected_value is None:
      alert('Kindly select a device ID')
      return
    else:
      current_date = datetime.date.today()
      dev = int(self.deviceList.selected_value)
      d = app_tables.customers.get(device_id=dev)
      if d is None:
        dt = {
          'name': name,
          'contact': contact1,
          'id_num': id_num1
        }
        ans = anvil.server.call('checkoldcustomers', dt)
        ans = ans.get_bytes().decode('utf-8')
        ans = json.loads(ans)
        if ans==True:
          a = confirm("Customer "+name+" was removed from the system in the past.Do you wish to reinstate them as a customer?")
          if a==True:
            app_tables.customers.add_row(name=name, id_num=id_num1, contact=contact1,
                                   dob=self.dob.date, image=self.file_loader_1.file,
                                   active_date=current_date, device_id=dev)
            reste = anvil.server.call('removeoldcustomers', dt)
            alert('Customer ' + name + ' has been added to the system')
            open_form('Customers')
          else:
            pass
        else:
          app_tables.customers.add_row(name=name, id_num=id_num1, contact=contact1,
                                   dob=self.dob.date, image=self.file_loader_1.file,
                                   active_date=current_date, device_id=dev)
          alert('Customer ' + name + ' has been added to the system')
          open_form('Customers')         
      else:
        alert('Customer '+d['name']+" has already been assigned that device")
        

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Home')

  def link_3_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Customers')

  def request_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Request')

    






      
    


