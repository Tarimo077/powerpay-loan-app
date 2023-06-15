from ._anvil_designer import ItemTemplate1Template
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ...CustomerProfile import CustomerProfile
from datetime import datetime, timezone, timedelta

class ItemTemplate1(ItemTemplate1Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    #selected_products = []
    
    #formatted_date = dob.strftime("%d %B %Y")
    
    
    #product_ids = customer_row['products']
    #for product_id in product_ids:
     # product_row = app_tables.products.get(product_id=product_id)
      #selected_products.append(product_row['product_name'])

    #separator = ', '
    #my_string = separator.join(selected_products)
    #self.products.text = my_string
    
    #name = self.cname.text
    #id_num = self.id_num.text
    #contact = self.contact.text
    #self.item = {'name': name, 'id_num': id_num, 'contact': contact}

    # Any code you write here will run before the form opens.

  def edit_click(self, **event_args):
    """This method is called when the button is clicked"""
    name = self.cname.text
    id_num = self.id_num.text
    contact = self.contact.text
    dob = self.dob.text
    img = self.image_1.source
    device_id = self.device.text
    #products = []
    #products = self.products.text
    my_list = {'name': name, 'id_num': id_num, 'contact': contact, 'dob': dob, 'img': img, 'device_id': device_id}
    new_form = CustomerProfile(my_list)
    #open_form(new_form)
    alert(
      content=new_form,
      large=True,
    )
    self.refresh_data_bindings()

  def delete_click(self, **event_args):
    """This method is called when the button is clicked"""
    name = self.cname.text
    id_num = self.id_num.text
    contact = self.contact.text
    dt = {
      'name': name,
      'contact': contact,
      'id_num': id_num
    }
    c = confirm("Do you wish to delete customer " + self.cname.text + "? This action cannot be undone")
    if c == True:
      x = app_tables.customers.get(contact=contact, name=name, id_num=id_num)
      if x is not None:
        x.delete()
        res = anvil.server.call('deletedCustomers', dt)
        alert("Customer deleted")
        open_form('Customers')
    else:
      open_form('Customers')

      

    

