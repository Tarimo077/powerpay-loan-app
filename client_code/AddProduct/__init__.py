from ._anvil_designer import AddProductTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class AddProduct(AddProductTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    # Any code you write here will run before the form opens.

  def link_1_copy_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Home')

  def link_2_copy_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Products')

  def link_3_copy_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Customers')

  def add_product_click(self, **event_args):
    """This method is called when the button is clicked"""
    product_id = self.product_id.text
    product_id_1 = str(product_id)
    product_name = self.product_name.text
    product_desc = self.product_desc.text
    img = self.file_loader_1.file

    if product_id_1.strip() == '' or product_name.strip() == '' or product_desc.strip() == '':
      alert('Kindly fill in all fields')
      return
    if img is None:
      alert('Kindly upload product image')
      return
    else:
      z = app_tables.products.get(product_id=product_id, product_name=product_name)
      if z is None:
        app_tables.products.add_row(image=img, product_id=product_id,
                                    product_name=product_name, product_description=product_desc)
        alert(product_name+' has been added to the system with product id '+str(product_id))
        open_form('Products')
      else:
        alert('There already exists a Product with that id and name')
        self.product_id.text = ''
        self.product_name.text = ''
        return
      

    




