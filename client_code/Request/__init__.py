from ._anvil_designer import RequestTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import json
from ..UserPopover import UserPopover
from anvil_extras import popover
from ..AddDevice import AddDevice

class Request(RequestTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    usr = anvil.server.call('getusername')
    if usr == "Jeff Tarimo" or usr == "Brian Olasya":
      self.outlined_button_1.visible = True
    else:
      self.outlined_button_1.visible = False
    words = usr.split()
# Extract the first character of each word and convert it to uppercase
    initials = [word[0].upper() for word in words]
# Join the initials together
    initials_string = ''.join(initials)
    self.username_label.text = initials_string    
    response = anvil.server.call('req')
    text = response.get_bytes().decode('utf-8')
    my_array = json.loads(text)
    sorted_items = sorted(
    my_array,
    key=lambda x: (
        float('inf') if x['deviceID'] == 'OfficeFridge1' else
        int(x['deviceID'].split('device')[-1]) if x['deviceID'].startswith('device') else
        int(x['deviceID'][-6:]) if x['deviceID'].startswith('JD') else
        float('inf') - 1
    )
)
    #sorted_items = sorted(my_array, key=lambda x: x['deviceID'])
    self.repeating_panel_1.items = sorted_items
    anvil.server.call('strDevArr', sorted_items)
    self.item = sorted_items
    active_devs = 0
    inactive_devs = 0
    for obj in my_array:
      if obj["active"] == 'Yes' or obj["active"]:
        active_devs += 1
      else:
        inactive_devs += 1

    self.activeDevs.text = "   "+str(active_devs)
    self.inactiveDevs.text = "   "+str(inactive_devs)
    self.username_label.popover(UserPopover(), 
                          placement = 'bottom', 
                          trigger='stickyhover', 
                          delay={ "show": 100, "hide": 100 },
                          max_width='700px'
                         )
    #my_obj = ItemTemplate6()
  
    #usr = self.item
    #my_obj.getItem(usr)
      #ItemTemplate6.get_rws(self,actve,dev)
    #RowTemplate8(self.item)
      

    # Any code you write here will run before the form opens.

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Index')

  def link_3_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Customers')

  def request_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Request')
    
  def repeating_panel_1_show(self, **event_args):
    """This method is called when the RepeatingPanel is shown on the screen"""
    self.refresh_data_bindings()

  def home_link_copy_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Transactions', True)

  def link_1_copy_click(self, **event_args):
    """This method is called when the link is clicked"""
    c = confirm('Are you sure you want to logout?', buttons=[("Yes", True),("No", False)])
    if(c):
      open_form('Login')
    else:
      pass

  def outlined_button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    nw_frm = AddDevice()
    alert_instance = alert(
        content=nw_frm,
        large=True,
        title=None,
        dismissible=False,
        buttons=[('Cancel', 0)],
        role='outlined'
      )
    if alert_instance==0:
      nw_frm.raise_event("x-close-alert")









