from ._anvil_designer import RequestTemplate
from anvil import *
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.http
import json

class Request(RequestTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)

    # Any code you write here will run before the form opens.

  def send_click(self, **event_args):
    """This method is called when the button is clicked"""
    
    data = self.data.text
    dtn = {
      'command': data
    }
    headers = {'Content-Type': 'application/json'}
    url = "https://applipay.com/commands"
    res = anvil.http.request(url, method="POST", headers=headers, data=dtn, json=True)
    json_str = json.dumps(res)
    rs = json.loads(json_str)
    valu = str(rs["val"])
    self.display.text = valu

