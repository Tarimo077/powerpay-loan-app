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
from datetime import datetime

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
    lat = res['lat']
    long = res['long']
    self.map_1.center = GoogleMap.LatLng(lat, long) 
    self.map_1.zoom = 15
    self.map_1.disable_double_click_zoom = True
    self.map_1.zoom_control = True
    self.map_1.draggable = False
    self.map_1.fullscreen_control = False
    self.map_1.disable_default_ui = True
    self.map_1.rotate_control = False
    self.map_1.street_view_control = False
    m = GoogleMap.Marker(position=GoogleMap.LatLng(lat, long), animation=GoogleMap.Animation.DROP)
    self.map_1.add_component(m)
    self.deviceLabel.text = " " + dev
    last_time = str(res['time'])
    formatted_timestamp = datetime.strptime(last_time, "%Y%m%d%H%M%S").strftime("%Y-%m-%d %H:%M:%S")
    self.lastTime.text = " " + str(formatted_timestamp)
    value = res['totalkwh']  # Replace with your actual value
    units = "kWh"  # Replace with your desired units
    uts = "HOURS"
    unitz = "KSH"
    utz = "KGS"
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
        'bar': {'color': 'orange'}
    }
)]
    self.energyCost.data = [go.Indicator(
    mode="gauge+number",
    value=(value)*31,
    title=f"ENERGY COST",
    number={'suffix': f" {unitz}"},
    gauge={
        'axis': {'range': [None, 500]},
        'bar': {'color': 'yellow'}
    }
)]
    self.carbonEmissions.data = [go.Indicator(
    mode="gauge+number",
    value=(value)*0.4999*0.28,
    title=f"CARBON EMISSIONS",
    number={'suffix': f" {utz}"},
    gauge={
        'axis': {'range': [None, 50]},
        'bar': {'color': 'blue'}
    }
)]
    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("Request")

