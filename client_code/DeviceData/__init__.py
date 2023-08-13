from ._anvil_designer import DeviceDataTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import json

class DeviceData(DeviceDataTemplate):
  def __init__(self, dev, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    dt = {
      "device": dev
    }
    res = anvil.server.call('getdevicedata', dt)
    res = res.get_bytes().decode('utf-8')
    res = json.loads(res)
    print(res)
    value = res['totalkwh']  # Replace with your actual value
    units = "kWh"  # Replace with your desired units
    uts = "HOURS"
    formatted_value = f"{value} {units}"
    self.plot_1.data = [go.Indicator(
    mode="gauge+number",
    value=value,
    title=f"ENERGY CONSUMPTION",
    number={'suffix': f" {units}"},
    gauge={
        'axis': {'range': [None, 100]},
        'bar': {'color': 'green'}
    }
)]
    self.plotTime.data = [go.Indicator(
    mode="gauge+number",
    value=res['runtime'],
    title=f"TOTAL RUNTIME",
    number={'suffix': f" {uts}"},
    gauge={
        'axis': {'range': [None, 50]},
        'bar': {'color': 'blue'}
    }
)]







    # Any code you write here will run before the form opens.
