from ._anvil_designer import ItemTemplate6Template
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import json
from datetime import datetime, timezone, timedelta
from ..RowTemplate7 import RowTemplate7


class ItemTemplate6(ItemTemplate6Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.refresh_data_bindings()
    self.init_components(**properties)
    time_text = self.item['time']
# Convert the time string to a datetime object
    time_obj_utc = datetime.fromisoformat(time_text.replace("Z", "+00:00"))

# Convert the datetime object to the server's timezone
    time_obj_server_tz = time_obj_utc.astimezone(timezone.utc).astimezone()

# Convert the datetime object to Kenyan time
    tz_offset = timedelta(hours=3)
    time_obj_kenya = time_obj_server_tz # + tz_offset

# Format the datetime object as a string in the desired format
    formatted_time_str = time_obj_kenya.strftime("%d %B %Y %I:%M%p").replace("AM", " AM").replace("PM", " PM")
    formatted_time_str = formatted_time_str.replace("th ", "").replace("st ", "").replace("nd ", "").replace("rd ", "")
    #self.time.text = formatted_time_str
    #self.devid.text = self.item['deviceID']
    self.item['last status change'] = formatted_time_str
    myobj = RowTemplate7(self.item)
    #myobj.item = self.item
    if(self.item['active']==True):
      self.item['active'] = 'Yes'
    else:
      self.item['active'] = 'No'
    # Any code you write here will run before the form opens.
  

  def change_state_click(self, **event_args):
    """This method is called when the button is clicked"""
    if(self.item['active']==True):
      act = True
    else:
      act=False
    data = {
      "selectedDev": self.devid.text,
      "status": act
    }
    if(self.item['active']==True):
      c = confirm(title='Deactivate Device', large=True, content='Do you wish to deactivate '+str(self.devid.text),
                  buttons=[("Yes", True),("No", False)])
      if(c==True):
        res = anvil.server.call('changeStatus', data)
        alert(str(self.devid.text) + ' has been deactivated', buttons=None) 
        open_form('Request')        
      else:
        self.refresh_data_bindings()
    else:
      c = confirm(title='Activate Device', large=True, content='Do you wish to activate '+str(self.devid.text),
                  buttons=[("Yes", True),("No", False)])
      if(c==True):
        res = anvil.server.call('changeStatus', data)
        alert(str(self.devid.text) + ' has been activated', buttons=None)
        open_form('Request')
      else:
        self.refresh_data_bindings()

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('DeviceData', self.item['deviceID'])

    
        
      