from ._anvil_designer import IntroTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Intro(IntroTemplate):
  def __init__(self, b, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.b = b     
    # Any code you write here will run before the form opens.

  def radio_button_1_clicked(self, **event_args):
    """This method is called when this radio button is selected"""
    st = self.radio_button_1.selected
    if(st==True):
      q = app_tables.users.get(username=self.b)
      username = q['username']
      password = q['password']
      q.delete()
      app_tables.users.add_row(username=username, password=password, intro=False)

