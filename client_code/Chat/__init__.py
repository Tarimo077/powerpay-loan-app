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
    m, y = self.makeLabels(prompt)
    self.linear_panel_1.add_component(m)
    self.linear_panel_1.add_component(y)
    response = anvil.server.call('getChat', prompt)
    self.item = True
    n, b = self.makeLabels(response)
    self.linear_panel_1.add_component(n)
    self.linear_panel_1.add_component(b)

  def makeLabels(self, prompt, **event_args):
    if(self.item==False):
      s = Label(align="right", text="You:\n", spacing_above="medium", icon="fa:comments", spacing_below="small", role="usr")
      c = Label(align="right", text=prompt+" ", spacing_above="small", font_size=15, border=" 3px solid #8fce00")
    else:
      text = prompt.get_bytes().decode('utf-8')
      s = Label(align="left", text="PPBot:\n", spacing_above="medium", icon="fa:magic", spacing_below="small", role="bot")
      c = Label(align="left", text=" "+text, spacing_above="small", font_size=15, border=" 3px solid #ffa500")
    return s,c

  def text_box_1_pressed_enter(self, **event_args):
    """This method is called when the user presses Enter in this text box"""
    self.button_1_click()

    
    

