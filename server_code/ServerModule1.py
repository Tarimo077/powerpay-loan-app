import anvil.google.auth, anvil.google.drive, anvil.google.mail
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.http

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
def req(data):
  url = "https://appliapay.com/command"
  headers = {
    "Content-Type": "application/json"
  }
  response = anvil.http.request(url, method="GET", data=data, headers=headers, username='admin', password='123Give!@#')
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
  url = "https://appliapay.com/customers"
  response = anvil.http.request(url, method="GET", username='admin', password='123Give!@#')
  return response

@anvil.server.callable
def strusr(dt):
  anvil.server.session['usr'] = dt

@anvil.server.callable
def getusername():
  usrn = anvil.server.session.get('usr', 0)
  return usrn

  
