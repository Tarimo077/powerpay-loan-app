from ._anvil_designer import CustomerProfileTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class CustomerProfile(CustomerProfileTemplate):
  def __init__(self, my_list, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.item = my_list
    self.cname.text = my_list['name']
    self.id_num.text = my_list['id_num']
    self.contact.text = my_list['contact']
    self.dob.date = my_list['dob']
    self.db_name = my_list['name']
    self.db_contact = my_list['contact']
    self.db_id = my_list['id_num']
    self.db_products = my_list['products']
    self.productdisplay.text = self.db_products
    self.slct_list = []
    self.my_column_data = [row['product_name'] for row in app_tables.products.search()]
    self.products.items = self.my_column_data
    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    name = self.cname.text
    id_num = self.id_num.text
    contact = self.contact.text
    date_of_birth = self.dob.date
    id_len = len(str(id_num))
    contact_len = len(str(contact))
    prods = []
    prods_num= []
    my_string = self.productdisplay.text
    prods = my_string.split(",")
    prods = list(prods)
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
      
    else:
      row = app_tables.customers.get(name= self.db_name, contact=self.db_contact,id_num=self.db_id)
      for prod in prods:
        rw = app_tables.products.get(product_name=prod)
        r = rw['product_id']
        prods_num.append(r)        

      rw_dt = row['active_date']
      row.delete()
      app_tables.customers.add_row(name=name, contact=contact,
                                   image=self.file_loader_1.file,
                                   dob=date_of_birth, id_num=id_num, products=prods_num, active_date=rw_dt)
      alert("Customer has been updated. Press OK to return to page")
      self.refresh_data_bindings()

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""

  def additem_click(self, **event_args):
    """This method is called when the button is clicked"""
    x = self.products.selected_value
    self.slct_list.append(x)
    separator = ','
    my_string = separator.join(self.slct_list)
    self.productdisplay.text = my_string
    self.products.selected_value = None
    self.my_column_data = [x for x in self.my_column_data if x not in self.slct_list]
    self.products.items = self.my_column_data

    
      

    

      
    
    

