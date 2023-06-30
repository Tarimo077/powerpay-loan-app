from ._anvil_designer import HomeTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import plotly.graph_objects as go
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
from datetime import datetime, timedelta
import json
import anvil.js
from anvil_extras.animation import animate, fade_in, Transition
import time


class Home(HomeTemplate):
  def __init__(self, boo, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    #res = anvil.server.call('getoldcustomers')
    #text = res.get_bytes().decode('utf-8')
    #old_customers = json.loads(text)
    self.boo = boo
    usr = anvil.server.call('getusername')
    self.username_label.tooltip = "Logged in as "+usr
    words = usr.split()


# Extract the first character of each word and convert it to uppercase
    initials = [word[0].upper() for word in words]

# Join the initials together
    initials_string = ''.join(initials)
    self.username_label.text = initials_string
    bounce = Transition(translateY=[0, 0, "-15px", "-15px", 0, "-15px", 0, "-15px", 0], offset=[0, 0.2, 0.4, 0.43, 0.53, 0.7, 0.8, 0.9, 1])
    shake = Transition(translateX=[0] + ["10px", "-10px"] * 4 + [0])
    animate(self.image_4, shake, duration=5000)
    animate(self.home_customer_img, shake, duration=5000)
    animate(self.image_2, bounce, duration=5000)
    animate(self.image_3, bounce, duration=5000)  
    
  def home_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Home', 0)

  def customers_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Customers')

  def request_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Request')

  def home_link_copy_2_click(self, **event_args):
    """This method is called when the link is clicked"""
    c = confirm('Are you sure you want to logout?', buttons=[("Yes", True),("No", False)])
    if(c==True):
      open_form('Login')
    else:
      pass

  def home_link_copy_3_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Support')

  def transactions_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Transactions', True)

  def outlined_button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Customers')

  def outlined_button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Request')

  def outlined_button_4_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Support')

  def outlined_button_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Transactions', True)

  def timer_1_tick(self, **event_args):
    """This method is called Every [interval] seconds. Does not trigger if [interval] is 0."""
    bounce = Transition(translateY=[0, 0, "-30px", "-30px", 0, "-15px", 0, "-15px", 0], offset=[0, 0.2, 0.4, 0.43, 0.53, 0.7, 0.8, 0.9, 1])
    shake = Transition(translateX=[0] + ["10px", "-10px"] * 4 + [0])
    animate(self.image_4, shake, duration=5000)
    animate(self.home_customer_img, shake, duration=5000)
    animate(self.image_2, bounce, duration=5000)
    animate(self.image_3, bounce, duration=5000)



      
    




















    
