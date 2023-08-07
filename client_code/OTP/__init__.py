from ._anvil_designer import OTPTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class OTP(OTPTemplate):
  def __init__(self, otp, num, pwd, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.otpz = str(otp)
    self.phone.text = str(num)
    self.phone_nm = num
    self.pwd = pwd
    # Any code you write here will run before the form opens.

  def otp_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    if len(str(self.otp.text)) == 4:
      otpstr = str(self.otp.text)
      if otpstr == self.otpz:
        z = app_tables.users.get(phone=self.phone_nm)
        username = z['username']
        email = z['email']
        z.delete()
        app_tables.users.add_row(email=email, username=username, phone=self.phone_nm, password=self.pwd)
        self.raise_event("x-close-alert")
        alert("\t\tSuccess\n\n\t  Password updated")
        open_form('Settings')
      else:
        self.error.text = "Wrong OTP. Enter OTP again"
        self.otp.text = ""
    else:
      pass
        
      

