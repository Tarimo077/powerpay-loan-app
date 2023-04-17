from ._anvil_designer import ChatTemplate
from anvil import *
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import json

class Chat(ChatTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.item = False

    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    prompt = self.text_box_1.text
    self.text_box_1.text = ""
    self.item = False
    m = self.makeLabels(prompt)
    self.linear_panel_1.add_component(m)
    response = anvil.server.call('getChat', prompt)
    self.item = True
    n = self.makeLabels(response)
    self.linear_panel_1.add_component(n)

  def makeLabels(self, prompt, **event_args):
    if(self.item==False):
      c = Label(align="right", text=prompt, spacing_above="medium")
    else:
      text = prompt.get_bytes().decode('utf-8')
      c = Label(align="left", text=text, spacing_above="medium", bold=True, icon="fa:magic")
    return c

  def text_box_1_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    self.button_1_click()

    
    

