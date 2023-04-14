from ._anvil_designer import AddCustomerTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import datetime

class AddCustomer(AddCustomerTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.my_column_data = [row['product_name'] for row in app_tables.products.search()]
    self.product_list.items = self.my_column_data
    self.slctlist = []
    self.db_list = []
    # Any code you write here will run before the form opens.

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
    else:
      for x in self.slctlist:
        product_row = app_tables.products.get(product_name=x)
        r = product_row['product_id']
        self.db_list.append(r)
      current_date = datetime.date.today()
      app_tables.customers.add_row(name=name, id_num=id_num1, contact=contact1,
                                   dob=self.dob.date, image=self.file_loader_1.file, products=self.db_list,
                                   active_date=current_date)
      alert('Customer ' + name + ' has been added to the system')
      open_form('Customers')

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Home')

  def link_2_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Products')

  def link_3_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Customers')

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    slct = self.product_list.selected_value
    self.slctlist.append(slct)
    self.product_list.selected_value = None
    sepa = ''
    my_str = sepa.join(self.slctlist)
    self.items_selected.text = my_str
# Remove any elements from list1 that are also in list2:
    self.my_column_data = [x for x in self.my_column_data if x not in self.slctlist]
    self.product_list.items = self.my_column_data
    






      
    


