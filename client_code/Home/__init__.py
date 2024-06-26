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
from anvil_extras import popover
import time
from AnvilAugment import augment
import anvil.js.window as js_window
from ..UserPopover import UserPopover

popover.dismiss_on_outside_click(True)


class Home(HomeTemplate):
  def __init__(self, boo, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.index_side_panel.visible = False
    augment.set_event_handler(self.home_rich_customers, 'hover', self.mouse_hover_customers)
    augment.set_event_handler(self.rich_text_2, 'hover', self.mouse_hover_devices)
    augment.set_event_handler(self.rich_text_4, 'hover', self.mouse_hover_support)
    augment.set_event_handler(self.rich_text_3, 'hover', self.mouse_hover_transactions)
    self.username_label.popover(UserPopover(), 
                          placement = 'bottom', 
                          trigger='stickyhover', 
                          delay={ "show": 100, "hide": 100 },
                          max_width='700px'
                         )
    #res = anvil.server.call('getoldcustomers')
    #text = res.get_bytes().decode('utf-8')
    #old_customers = json.loads(text)
    self.boo = boo
    usr = anvil.server.call('getusername')
    words = usr.split()
# Extract the first character of each word and convert it to uppercase
    initials = [word[0].upper() for word in words]
# Join the initials together
    initials_string = ''.join(initials)
    self.username_label.text = initials_string
    #bounce = Transition(translateY=[0, 0, "-15px", "-15px", 0, "-15px", 0, "-15px", 0], offset=[0, 0.2, 0.4, 0.43, 0.53, 0.7, 0.8, 0.9, 1])
    #shake = Transition(translateX=[0] + ["10px", "-10px"] * 4 + [0])
    #animate(self.image_4, shake, duration=5000)
    #animate(self.home_customer_img, shake, duration=5000)
    #animate(self.image_2, bounce, duration=5000)
    #animate(self.image_3, bounce, duration=5000)   
    

  def mouse_hover_customers(self, **event_args):
    if 'enter' in event_args['event_type']:
      bounce = Transition(translateY=[0, 0, "-15px", "-15px", 0, "-15px", 0, "-15px", 0], offset=[0, 0.2, 0.4, 0.43, 0.53, 0.7, 0.8, 0.9, 1])
      shake = Transition(translateX=[0] + ["10px", "-10px"] * 4 + [0])
      rotate = Transition(rotate=[0, "360deg"])
      animate(self.home_customer_img, shake, duration=4000)
      self.home_rich_customers.background = '#DB4437'
    else: 
      self.home_rich_customers.background = '#0080FF'

  def mouse_hover_devices(self, **event_args):
    if 'enter' in event_args['event_type']:
      bounce = Transition(translateY=[0, 0, "-15px", "-15px", 0, "-15px", 0, "-15px", 0], offset=[0, 0.2, 0.4, 0.43, 0.53, 0.7, 0.8, 0.9, 1])
      shake = Transition(translateX=[0] + ["10px", "-10px"] * 4 + [0])
      rotate = Transition(rotate=[0, "360deg"])
      self.rich_text_2.background = '#DB4437'
      animate(self.image_2, bounce, duration=2000)
      time.sleep(2)
      animate(self.image_2, rotate, duration=2000)
    else: 
      self.rich_text_2.background = '#0080FF'

  def mouse_hover_support(self, **event_args):
    if 'enter' in event_args['event_type']:
      bounce = Transition(translateY=[0, 0, "-15px", "-15px", 0, "-15px", 0, "-15px", 0], offset=[0, 0.2, 0.4, 0.43, 0.53, 0.7, 0.8, 0.9, 1])
      shake = Transition(translateX=[0] + ["10px", "-10px"] * 4 + [0])
      rotate = Transition(rotate=[0, "360deg"])
      animate(self.image_3, bounce, duration=4000)
      self.rich_text_4.background = '#DB4437'
    else: 
      self.rich_text_4.background = '#0080FF'

  def mouse_hover_transactions(self, **event_args):
    if 'enter' in event_args['event_type']:
      bounce = Transition(translateY=[0, 0, "-15px", "-15px", 0, "-15px", 0, "-15px", 0], offset=[0, 0.2, 0.4, 0.43, 0.53, 0.7, 0.8, 0.9, 1])
      shake = Transition(translateX=[0] + ["10px", "-10px"] * 4 + [0])
      rotate = Transition(rotate=[0, "360deg"])
      animate(self.image_4, shake, duration=4000)
      self.rich_text_3.background = '#DB4437'
    else: 
      self.rich_text_3.background = '#0080FF'
    
  def home_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Index')

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

  def transactions_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Transactions', True)

  def outlined_button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Index')

  def outlined_button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Request')

  def outlined_button_4_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Support')

  def outlined_button_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Transactions', True)






      
    




















    
