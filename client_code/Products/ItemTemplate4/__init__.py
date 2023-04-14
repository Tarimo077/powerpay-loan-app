from ._anvil_designer import ItemTemplate4Template
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ...EditProduct import EditProduct
from .. import Products

class ItemTemplate4(ItemTemplate4Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.refresh_data_bindings()

    # Any code you write here will run before the form opens.

  def check_prods(self,prod, **properties):
    pro = prod
    s = False
    for customer in app_tables.customers.search(products=q.any_of([prod])):
      alert('The product cannot be deleted as it is linked to an active customer')
      self.__init__()
      s = True
    return s
      
  def edit_click(self, **event_args):
    """This method is called when the button is clicked"""
    product_id = self.product_id.text
    product_desc = self.product_description.text
    product_name = self.product_name.text
    prod_img = self.image_1.source
    my_list = {'name': product_name, 'id': product_id, 'desc': product_desc, 'img': prod_img}
    new_form = EditProduct(my_list)
    alert(
      content = new_form,
      large=True
    )
    self.refresh_data_bindings()

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    product_id = self.product_id.text
    product_desc = self.product_description.text
    product_name = self.product_name.text
    c = confirm("Do you wish to delete product " + product_name + "? This action cannot be undone")
    if c == True:
      x = app_tables.products.get(product_id=product_id, product_name=product_name)
      if x is not None:
        y = self.check_prods(product_id)
        if y == False:
          x.delete()
          alert("Product deleted")
          open_form('Products')
        else:
          pass
      else: 
        pass
    self.refresh_data_bindings()


