from ._anvil_designer import SettingsTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Settings(SettingsTemplate):
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
    # Any code you write here will run before the form opens.
    d = app_tables.users.get(username=usr)
    self.f_name.text = words[0]
    self.s_name.text = words[1]
    self.email.text = d['email']
    self.phone.text = d['phone']
