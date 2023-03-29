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
  dtn = {
      'data': data
    }
  headers = {'Content-Type': 'application/json'}
  url = "https://applipay.com/commands"
  response = anvil.http.request(url, method="POST", headers=headers, data=dtn,
                                username='admin', password='123Give!@#', json=True)
  return response
