from ._anvil_designer import LoginTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil_extras.animation import animate, Transition
import anvil.js

class Login(LoginTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.password.hide_text = True
    dom_node = anvil.js.get_dom_node(self)
    dom_node.style.background = f"url('_/theme/background_loan_app.jpg')"
    dom_app_bar = anvil.js.get_dom_node(self).querySelector(".app-bar")
    dom_app_bar.style.background = f"url('_/theme/background_loan_app.jpg')"
    self.rich_text_1.background = "white" #"#C7B8B4"
    self.image_1.background = None
    self.eye.tooltip = 'view password'
    self.pass_state = False
    slide_in_up = Transition(translateY=["100%", 0])
    slide_in_down = Transition(translateY=["-100%", 0])
    zoom_in = Transition(scale=[.3, 1])
    fade_in = Transition(opacity=[0, 1])
    fly_in_down = slide_in_down | zoom_in | fade_in
    animate(self.image_1, fly_in_down, duration=3000)
    # Any code you write here will run before the form opens.

  def login_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.timer_1.interval = 0
    self.login.background = '#DB4437'
    username = self.username.text
    password = self.password.text
    d = app_tables.users.get(email=username,password=password)
    if username == '':
      alert('Fill in username')
      self.password.text = ''
      self.login.background = '#0080FF'
      return
    if password == '':
      alert('Fill in password')
      self.login.background = '#0080FF'
      return
    if d is None:
      alert('Wrong username or password.\n If the problem persists contact \n\tPowerpay Support team.', buttons=None)
      self.login.background = '#0080FF'
      self.password.text = ''
      return
    else:
      self.item = d['username']
      #anvil.server.session['usr'] = username
      #print(anvil.server.session.get('usr'))
      anvil.server.call('strusr', d['username'])
      anvil.server.call('strInit', False)
      open_form('Index')
      e = ':slightly_smiling_face:'
      em = anvil.server.call('emojiPass', e)
      tx = '\t\t\tHi '+d['username']+em+' \n\n\tWelcome To The Powerpay \n\t\t\t\t\t\tApp'
      alert(tx, buttons=None)

  def eye_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.pass_state == False:
      self.password.hide_text = False
      self.eye.icon = 'fa:eye-slash'
      self.pass_state = True
      self.eye.background = '#DB4437'
      self.eye.tooltip = 'hide password'
      
    else:
      self.password.hide_text = True
      self.eye.icon = 'fa:eye'
      self.pass_state = False
      self.eye.background = '#0080FF'
      self.eye.tooltip = 'view password'

  def timer_1_tick(self, **event_args):
    """This method is called Every [interval] seconds. Does not trigger if [interval] is 0."""
    slide_in_up = Transition(translateY=["100%", 0])
    slide_in_down = Transition(translateY=["-100%", 0])
    zoom_in = Transition(scale=[.3, 1])
    fade_in = Transition(opacity=[0, 1])
    fly_in_down = slide_in_down | zoom_in | fade_in
    animate(self.image_1, fly_in_down, duration=5000)

      
