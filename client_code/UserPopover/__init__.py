from ._anvil_designer import UserPopoverTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import datetime

class UserPopover(UserPopoverTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    usr = anvil.server.call('getusername')
    self.user.text = usr
    current_time = datetime.datetime.now().strftime("%I:%M:%S %p")
    self.timeLabel.text = current_time
    current_date = datetime.datetime.now()
    formatted_date = current_date.strftime("%B %d, %Y")
    self.dateLabel.text = formatted_date
    
    

    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    c = confirm('Are you sure you want to logout?', buttons=[("Yes", True),("No", False)])
    if(c==True):
      open_form('Login')
    else:
      pass

  def link_3_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Settings')

  def timer_1_tick(self, **event_args):
    """This method is called Every [interval] seconds. Does not trigger if [interval] is 0."""
    current_time = datetime.datetime.now().strftime("%I:%M:%S %p")
    self.timeLabel.text = current_time
    current_date = datetime.datetime.now()
    formatted_date = current_date.strftime("%B %d, %Y")
    self.dateLabel.text = formatted_date




