from ._anvil_designer import RowTemplate8Template
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime, timezone, timedelta

class RowTemplate8(RowTemplate8Template):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
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
    self.item['last status change'] = formatted_time_str
    self.button_2.tooltip = 'Click to see ' + self.item['deviceID'] + ' data'
    #self.time.text = formatted_time_str
    #self.devid.text = self.item['deviceID']
      #self.item['last status change'] = formatted_time_str
      #myobj = RowTemplate7(self.item)
    #myobj.item = self.item
    if(self.item['active']==True):
      self.item['active'] = 'Yes'
      self.statusChange.text = 'Deactivate'
      self.statusChange.background = '#DB4437'
      self.statusChange.tooltip = 'Deactivate ' + self.item['deviceID']
    else:
      self.item['active'] = 'No'
      self.statusChange.text = 'Activate'
      self.statusChange.background = '#0080FF'
      self.statusChange.tooltip = 'Activate ' + self.item['deviceID']
    # Any code you write here will run before the form opens.

    # Any code you write here will run before the form opens.

  def statusChange_click(self, **event_args):
    """This method is called when the button is clicked"""
    status = self.item['active']
    if(status == 'Yes'):
      status = True
      strconc = 'deactivate'
    else:
      status = False
      strconc = 'activate'
    dt = {
      'selectedDev' : self.item['deviceID'],
      'status' : status
    }

    c = confirm('Are you sure you want to ' + strconc + ' ' + self.item['deviceID'], buttons=[("Yes", True),("No", False)])
    if(c==True):
      anvil.server.call('changeStatus', dt)
      open_form('Request')
      alert(self.item['deviceID'] + ' ' + strconc + 'd', buttons=None)
    else:
      pass

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('DeviceData', self.item['deviceID'])



