from ._anvil_designer import SupportTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from ..UserPopover import UserPopover
from anvil_extras import popover

class Support(SupportTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    usr = anvil.server.call('getusername')
    words = usr.split()
# Extract the first character of each word and convert it to uppercase
    initials = [word[0].upper() for word in words]
# Join the initials together
    initials_string = ''.join(initials)
    self.username_label.text = initials_string
    self.username_label.popover(UserPopover(), 
                          placement = 'bottom', 
                          trigger='stickyhover', 
                          delay={ "show": 100, "hide": 100 },
                          max_width='700px'
                         )
    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    name = self.name.text
    email = self.email.text
    feedback = self.feedback.text
    if(name==''):
      alert('Name is empty', buttons=None)
      return
    if(email==''):
      alert('Email is empty', buttons=None)
      return
    if(feedback==''):
      alert('Feedback is empty', buttons=None)
      return
    data = {
      'name': name,
      'email': email,
      'feedback': feedback
    }
    anvil.server.call('getSupport', data)
    alert('Thank you for your feedback', buttons=None)
    self.name.text = ''
    self.email.text = ''
    self.feedback.text = ''

  def home_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Home', 0)

  def customers_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Customers')

  def request_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Request')

  def home_link_copy_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Transactions', True)

  def home_link_copy_2_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Support')

  def home_link_copy_3_click(self, **event_args):
    """This method is called when the link is clicked"""
    c = confirm('Are you sure you want to logout?', buttons=[("Yes", True),("No", False)])
    if(c==True):
      open_form('Login')
    else:
      pass










    

