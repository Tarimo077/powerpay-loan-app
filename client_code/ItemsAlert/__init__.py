from ._anvil_designer import ItemsAlertTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class ItemsAlert(ItemsAlertTemplate):
  def __init__(self, billTo, contact, receiptNum, dt, amnt, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.amnt = amnt
    self.billTo = billTo
    self.contact = contact
    self.receiptNum = receiptNum
    self.dt = dt
    self.drop_down_1.items = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20']
    self.drop_down_1.selected_value = '1'

    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.raise_event("x-close-alert")
    list = []
    self.amnt = int(self.amnt.replace(',', ''))
    v = int(self.amnt)/(int(self.drop_down_1.selected_value))
    for x in range(int(self.drop_down_1.selected_value)):
      y = {"qty": 1, "desc": '', "amnt": v}
      list.append(y)
    open_form('Receipt',True,  self.billTo, self.contact, self.receiptNum, self.dt, list)
