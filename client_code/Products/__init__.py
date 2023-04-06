from ._anvil_designer import ProductsTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..EditProduct import EditProduct

class Products(ProductsTemplate):
  def __init__(self, user_tag, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.refresh_data_bindings()
    self.item = user_tag
    self.user.text = user_tag
    self.products_panel.items = app_tables.products.search(tables.order_by('product_id'))
    

    # Any code you write here will run before the form opens.

  def home_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Home', self.item)

  def products_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Products', self.item)

  def customers_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Customers', self.item)

  def search_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    search_text = self.search.text
    self.products_panel.items = app_tables.products.search(product_name=q.ilike(search_text+"%"))

  def add_product_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('AddProduct', self.item)

  def request_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Request', self.item)




    


    

