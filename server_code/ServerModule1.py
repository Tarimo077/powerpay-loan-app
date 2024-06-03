import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.http
import anvil.media
import pandas as pd
import anvil.js
import emoji
import anvil.pdf
from anvil.pdf import PDFRenderer

# This is a server module. It runs on the Anvil server,
# rather than in the user's browser.
#
# To allow anvil.server.call() to call functions here, we mark
# them with @anvil.server.callable.
# Here is an example - you can replace it with your own:
#
# @anvil.server.callable
# def say_hello(name):
#   print("Hello, " + name + "!")
#   return 42
#
@anvil.server.callable
def create_pdf(billTo, contact, receiptNum, dt, list, receName):
  pdf = PDFRenderer(page_size='A3', filename=receName).render_form('Receipt',False, billTo, contact, receiptNum, dt, list)
  return pdf

@anvil.server.callable
def emojiPass(e):
  emo = emoji.emojize(e)
  return emo
  
@anvil.server.callable
def req(data):
  url = "https://appliapay.com/command"
  headers = {
    "Content-Type": "application/json"
  }
  response = anvil.http.request(url, method="GET", data=data, headers=headers, username='admin', password='123Give!@#')
  return response

@anvil.server.callable
def getAllDeviceData():
  url = "https://appliapay.com/allDeviceData"
  headers = {
    "Content-Type": "application/json"
  }
  response = anvil.http.request(url, method="GET", headers=headers, username='admin', password='123Give!@#')
  return response

@anvil.server.callable
def changeStatus(data):
  url = "https://appliapay.com/changeStatus"
  headers = {
    "Content-Type": "application/json"
  }
  response = anvil.http.request(url, method="POST", data=data, headers=headers, username='admin', password='123Give!@#')
  return response

@anvil.server.callable
def addDevice(data):
  url = "https://appliapay.com/addDevice"
  headers = {
    "Content-Type": "application/json"
  }
  response = anvil.http.request(url, method="POST", data=data, headers=headers, username='admin', password='123Give!@#')
  return response

@anvil.server.callable
def sendUser(user):
  usr = user
  data = {
    "user": usr
  }
  url = "https://appliapay.com/usr"
  headers = {
    "Content-Type": "application/json"
  }
  response = anvil.http.request(url, method="POST", data=data, headers=headers, username='admin', password='123Give!@#')

@anvil.server.callable
def getSupport(feedback):
  data = feedback
  url = "https://appliapay.com/support"
  response = anvil.http.request(url, method="POST", data=data, username='admin', password='123Give!@#')

@anvil.server.callable
def getInfluxdb_devs():
  data = {
    'data': 0
  }
  url = "https://appliapay.com/devids"
  headers = {
    "Content-Type": "application/json"
  }
  response = anvil.http.request(url, method="GET", data=data, headers=headers, username='admin', password='123Give!@#')
  return response

@anvil.server.callable
def deletedCustomers(data):
  name = data['name']
  contact = data['contact']
  id_num = data['id_num']
  dt = {
    'name': name,
    'contact': contact,
    'id_num': id_num
  }
  url = "https://appliapay.com/deletedCustomers"
  headers = {
    "Content-Type": "application/json"
  }
  response = anvil.http.request(url, method="POST", data=dt, headers=headers, username='admin', password='123Give!@#')
  return response

@anvil.server.callable
def getoldcustomers():
  dt = {}
  url = "https://appliapay.com/oldcustomers"
  response = anvil.http.request(url, method="GET", data=dt, username='admin', password='123Give!@#')
  return response

@anvil.server.callable
def checkoldcustomers(data):
  url = "https://appliapay.com/checkoldcustomers"
  response = anvil.http.request(url, method="GET", data=data, username='admin', password='123Give!@#')
  return response

@anvil.server.callable
def removeoldcustomers(data):
  name = data['name']
  contact = data['contact']
  id_num = data['id_num']
  dt = {
    'name': name,
    'contact': contact,
    'id_num': id_num
  }
  url = "https://appliapay.com/remove"
  response = anvil.http.request(url, method="POST", data=dt, username='admin', password='123Give!@#')
  return response

@anvil.server.callable
def getchurn(data):
  url = "https://appliapay.com/churn"
  response = anvil.http.request(url, method="GET", data=data, username='admin', password='123Give!@#')
  return response

@anvil.server.callable
def getcashin():
  url = "https://appliapay.com/mpesarecords"
  response = anvil.http.request(url, method="GET", username='admin', password='123Give!@#')
  return response

@anvil.server.callable
def getcustomers():
  url = "https://appliapay.com/customerRequest"
  response = anvil.http.request(url, method="GET", username='admin', password='123Give!@#')
  return response

@anvil.server.callable
def getloans():
  url = "https://appliapay.com/loans"
  response = anvil.http.request(url, method="GET", username='admin', password='123Give!@#')
  return response

@anvil.server.callable
def strloans(dt):
  anvil.server.session['loans'] = dt

@anvil.server.callable
def getloansstored():
  loans = anvil.server.session.get('loans')
  return loans

@anvil.server.callable
def strDevArr(dt):
  anvil.server.session['devList'] = dt

@anvil.server.callable
def getDevList():
  devs = anvil.server.session.get('devList', 0)
  return devs

@anvil.server.callable
def strusr(dt):
  anvil.server.session['usr'] = dt

@anvil.server.callable
def getusername():
  usrn = anvil.server.session.get('usr', 0)
  return usrn

@anvil.server.callable
def strRawData(dt):
  anvil.server.session['rawData'] = dt

@anvil.server.callable
def getRawData():
  rwDt = anvil.server.session.get('rawData')
  return rwDt

@anvil.server.callable
def strInit(dt):
  anvil.server.session['init'] = dt

@anvil.server.callable
def getInit():
  init = anvil.server.session.get('init')
  return init

@anvil.server.callable
def strKwh(dt):
  anvil.server.session['totalKwh'] = dt

@anvil.server.callable
def getKwh():
  kwh = anvil.server.session.get('totalKwh')
  return kwh

@anvil.server.callable
def strRuntime(dt):
  anvil.server.session['runtime'] = dt

@anvil.server.callable
def getRuntime():
  runtime = anvil.server.session.get('runtime')
  return runtime

@anvil.server.callable
def download_customers(arr):
  array = arr
  df = pd.DataFrame(array)
  df.to_excel('/tmp/output.xlsx', index=False)
  X_media = anvil.media.from_file('/tmp/output.xlsx', 'xlsx', 'customers.xlsx')
  return X_media

@anvil.server.callable
def download_transactions(arr):
  array = arr
  df = pd.DataFrame(array)
  df.to_excel('/tmp/output.xlsx', index=False)
  X_media = anvil.media.from_file('/tmp/output.xlsx', 'xlsx', 'transactions.xlsx')
  return X_media

@anvil.server.callable
def sendsms(dt):
  url = "https://appliapay.com/smsintegrate"
  response = anvil.http.request(url, method="POST", username='admin', password='123Give!@#', data=dt)
  return response

@anvil.server.callable
def getdevicedata(dt):
  url = "https://appliapay.com/devicedata"
  response = anvil.http.request(url, method="GET", username='admin', password='123Give!@#', data=dt)
  return response

@anvil.server.callable
def getMeals(dt):
  url = "https://appliapay.com/dynamicTsFlutter"
  response = anvil.http.request(url, method="GET", username='admin', password='123Give!@#', data=dt)
  return response
  
@anvil.server.callable
def changeRange(dt):
  url = "https://appliapay.com/dynamicTs"
  response = anvil.http.request(url, method="GET", username='admin', password='123Give!@#', data=dt)
  return response

@anvil.server.callable
def changeRangeIndex(dt):
  url = "https://appliapay.com/dynamicTsIndex"
  response = anvil.http.request(url, method="GET", username='admin', password='123Give!@#', data=dt)
  return response

@anvil.server.callable
def animate_label(label, val):
  # Initialize count
  count = 0
  # Loop to animate the label
  for i in range(val+1):
  # Update label text
    anvil.js.call_js_function(label, 'setText', str(i))
        # Wait for 1 second (1000 milliseconds)
    anvil.js.call_js_function(js.window, 'setTimeout', lambda: None, i * 1000)
  
  
