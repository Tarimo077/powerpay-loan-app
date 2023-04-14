from ._anvil_designer import EditProductTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class EditProduct(EditProductTemplate):
  def __init__(self, my_list, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.item = my_list
    self.product_id.text = my_list['id']
    self.product_name.text = my_list['name']
    self.product_desc.text = my_list['desc']
    self.db_name = my_list['name']
    self.db_id = my_list['id']
    self.db_desc = my_list['desc']

    # Any code you write here will run before the form opens.

  def text_box_1_pressed_enter(self, my_list, **event_args):
    """This method is called when the user presses Enter in this text box"""
    pass

  def file_loader_1_change(self, file, **event_args):
    """This method is called when a new file is loaded into this FileLoader"""
    pass

  def edit_click(self, **event_args):
    """This method is called when the button is clicked"""
    product_id = self.product_id.text
    product_name = self.product_name.text
    product_desc = self.product_desc.text
    product_image = self.file_loader_1.file

    if product_id.strip() == '' or product_name.strip() == '' or product_desc.strip() == '':
      alert('Kindly fill in all fields')
      return
    if self.file_loader_1.file is None:
      alert('Kindly upload the product image')
      return
    else:
      row = app_tables.products.get(product_id=self.db_id, product_name=self.db_name)
      row.delete()
      app_tables.products.add_row(image=self.file_loader_1.file, product_id=product_id,
                                  product_name=product_name, product_description=product_desc)
      alert("Product has been updated. Press OK to return to page")
      open_form('Products')



