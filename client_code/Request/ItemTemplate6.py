from ._anvil_designer import ItemTemplate6Template
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from .. import Request
import anvil.server
import json
from datetime import datetime, timezone, timedelta


class ItemTemplate6(ItemTemplate6Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    if(self.item['active']==True):
      self.active.text = 'Yes'
    else:
      self.active.text = 'No'
    self.devid.text = self.item['deviceID']
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
    self.time.text = formatted_time_str
    if(self.active.text=='Yes'):
      self.change_state.text = "Deactivate"
      self.change_state.background = "#ffa500"
    else:
      self.change_state.text = "Activate"
      self.change_state.background = "#8fce00"
    # Any code you write here will run before the form opens.

  def change_state_click(self, **event_args):
    """This method is called when the button is clicked"""
    if(self.active.text=='Yes'):
      act = True
    else:
      act=False
    data = {
      "selectedDev": self.devid.text,
      "status": act
    }
    if(self.active.text=='Yes'):
      c = confirm(title='Deactivate Device', large=True, content='Do you wish to deactivate device '+str(self.devid.text))
      if(c==True):
        res = anvil.server.call('changeStatus', data)
        alert('Device '+ str(self.devid.text) + ' has been deactivated')
        self.refresh_data_bindings()
      else:
        self.refresh_data_bindings()
    else:
      c = confirm(title='Activate Device', large=True, content='Do you wish to activate device '+str(self.devid.text))
      if(c==True):
        res = anvil.server.call('changeStatus', data)
        alert('Device '+ str(self.devid.text) + ' has been activated')
        self.refresh_data_bindings()
      else:
        self.refresh_data_bindings()
        
      