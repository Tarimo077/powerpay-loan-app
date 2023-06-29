from ._anvil_designer import LoginTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil_extras.animation import animate, fade_in, Transition

class Login(LoginTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.password.hide_text = True
    self.eye.tooltip = 'view password'
    self.pass_state = False

    # Any code you write here will run before the form opens.

  def login_click(self, **event_args):
    """This method is called when the button is clicked"""
    bounce = Transition(translateY=[0, 0, "-30px", "-30px", 0, "-15px", 0, "-15px", 0], offset=[0, 0.2, 0.4, 0.43, 0.53, 0.7, 0.8, 0.9, 1])
    shake = Transition(translateX=[0] + ["10px", "-10px"] * 4 + [0])
    animate(self.image_1, bounce, duration=2000)    
    self.login.background = '#ffa500'
    username = self.username.text
    password = self.password.text
    d = app_tables.users.get(username=username,password=password)
    if username == '':
      alert('Fill in username')
      self.password.text = ''
      self.login.background = '#8fce00'
      return
    if password == '':
      alert('Fill in password')
      self.login.background = '#8fce00'
      return
    if d is None:
      alert('Wrong username or password. If the problem persists contact Powerpay Support team.')
      self.login.background = '#8fce00'
      self.password.text = ''
      return
    else:
      self.item = username
      #anvil.server.session['usr'] = username
      #print(anvil.server.session.get('usr'))
      anvil.server.call('strusr', username)
      open_form('Home', username)
      alert('Hi '+username+', welcome to Powerpay Loan App')

  def eye_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.pass_state == False:
      self.password.hide_text = False
      self.eye.icon = 'fa:eye-slash'
      self.pass_state = True
      self.eye.background = '#ffa500'
      self.eye.tooltip = 'hide password'
      
    else:
      self.password.hide_text = True
      self.eye.icon = 'fa:eye'
      self.pass_state = False
      self.eye.background = '#8fce00'
      self.eye.tooltip = 'view password'

      

      
