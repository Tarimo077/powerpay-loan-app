from ._anvil_designer import SupportTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Support(SupportTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    name = self.name.text
    email = self.email.text
    feedback = self.feedback.text
    if(name==''):
      alert('Name is empty')
      return
    if(email==''):
      alert('Email is empty')
      return
    if(feedback==''):
      alert('Feedback is empty')
      return
    data = {
      'name': name,
      'email': email,
      'feedback': feedback
    }
    anvil.server.call('getSupport', data)
    alert('Thank you for your feedback')
    self.name.text = ''
    self.email.text = ''
    self.feedback.text = ''

  def home_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Home')

  def customers_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Customers')

  def request_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Request')

  def home_link_copy_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Support')





    

