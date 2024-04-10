from ._anvil_designer import ReceiptTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class Receipt(ReceiptTemplate):
  def __init__(self, x, billTo, contact, receiptNum, dt, list, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    totl = 0
    for i in list:
       totl = totl + i['amnt']
    vat = (0.16 * totl)
    subtotal = totl - vat
    self.vat.text = '{:,}'.format(vat)
    self.subTotal.text = '{:,}'.format(subtotal)
    self.totalAmnt.text = '{:,}'.format(totl)
    if x == False:
      self.button_1.remove_from_parent()
      self.outlined_button_1.remove_from_parent()
    self.repeating_panel_1.items = list
    self.billTo.text = billTo
    self.contact.text = contact
    self.date.text = dt
    self.receiptNum.text = "RECEIPT NO: " + receiptNum
    self.billTo1 = billTo
    self.contac = contact
    self.date1 = dt
    self.receiptNum1 = receiptNum
    self.list1 = list
    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.button_1.remove_from_parent()
    receName = self.receiptNum1 + ".pdf"
    media_object = anvil.server.call('create_pdf', self.billTo.text, self.contact.text, self.receiptNum1, self.date1, self.repeating_panel_1.items, receName)
    anvil.media.download(media_object)

  def outlined_button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Transactions', True)
    
