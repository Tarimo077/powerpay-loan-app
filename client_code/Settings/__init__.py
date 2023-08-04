from ._anvil_designer import SettingsTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from anvil_extras import popover
from ..UserPopover import UserPopover
import random
from ..OTP import OTP

class Settings(SettingsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.current_pwd.text = ""
    self.new_pwd.text = ""
    usr = anvil.server.call('getusername')
    self.usr = usr
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
    self.phone_num = self.phone.text
    self.username_label.popover(UserPopover(), 
                          placement = 'bottom', 
                          trigger='stickyhover', 
                          delay={ "show": 100, "hide": 100 },
                          max_width='700px'
                         )

  def link_1_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Home', 0)

  def link_3_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Customers')

  def request_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Request')

  def home_link_copy_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Transactions', True)

  def home_link_copy_2_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Support')

  def link_1_copy_click(self, **event_args):
    """This method is called when the link is clicked"""
    c = confirm('Are you sure you want to logout?', buttons=[("Yes", True),("No", False)])
    if(c==True):
      open_form('Login')
    else:
      pass

  def save_click(self, **event_args):
    """This method is called when the button is clicked"""
    if len(str(self.phone.text)) != 12:
      alert("Invalid phone number")
      return
    if self.f_name.text == " " or self.s_name.text == " " or self.email.text == " " or self.phone.text == " ":
      alert("Kindly fill in all fields")
    else:
      first_name = self.f_name.text
      second_name = self.s_name.text
      email = self.email.text
      phone = self.phone.text
      name = first_name + " " + second_name
      e = app_tables.users.get(username=self.usr)
      pwd = e['password']
      e.delete()
      app_tables.users.add_row(email=email, password=pwd, phone=phone, username=name)
      anvil.server.call('strusr', name)
      self.usr = name
      self.phone_num = phone
      alert('Your information has been updated')
      self.__init__()

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.current_pwd.text == " ":
      alert("Kindly input the current password")
      return
    if self.new_pwd.text == " ":
      alert("Kindly input the new password")
      return
    r = app_tables.users.get(username=self.usr)
    if self.current_pwd.text == r['password']:
      #lets open OTP page
      # Generate a random 4-digit OTP
      otp = "{:04d}".format(random.randint(0, 9999))
      print("OTP IS: "+ str(otp))
      data = {
        "mobile": str(self.phone_num),
        "message": "Greetings " + self.usr + ". Your OTP is " + str(otp)
      }
      anvil.server.call('sendsms', data)
      new_pwd = self.new_pwd.text 
      nw_frm = OTP(otp, self.phone_num, new_pwd)
      alert_instance = alert(
        content=nw_frm,
        large=False,
        title=None,
        dismissible=False,
        buttons=[('Cancel', 0)],
        role='outlined')
    else:
      alert("Wrong current password")
      self.current_pwd.text = ""
      self.new_pwd.text = ""

      







