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
    self.drop_down_1.items = ["All Time", "5 min", "30 min", "1 hr", "3 hrs", "12 hrs", "24 hrs", "3 days", "7 days", "2 weeks", "1 month", "3 months",
                              "6 months", "1 year", "3 years"]
    self.timeMap = [5, 30, 60, 180, 720, 1440, 4320, 10080, 20160, 40320, 120960, 241920, 483840, 1451520]
    self.drop_down_1.selected_value = self.drop_down_1.items[0]
    self.dev = dev
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
    self.totalKwh = value
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

  def remapGauges(self, **event_args):
    units = "kWh"  # Replace with your desired units
    uts = "HOURS"
    unitz = "KSH"
    utz = "KGS"
    formatted_value = f"{self.adjVal} {units}"
    self.plot_1.data = [go.Indicator(
    mode="gauge+number",
    value=self.adjsum,
    title=f"ENERGY CONSUMPTION",
    number={'suffix': f" {units}"},
    gauge={
        'axis': {'range': [None, 100]},
        'bar': {'color': 'green'}
      }
        )]
    self.energyCost.data = [go.Indicator(
    mode="gauge+number",
    value=(self.adjsum)*31,
    title=f"ENERGY COST",
    number={'suffix': f" {unitz}"},
    gauge={
        'axis': {'range': [None, 500]},
        'bar': {'color': 'yellow'}
      }
        )]
    self.carbonEmissions.data = [go.Indicator(
    mode="gauge+number",
    value=(self.adjsum)*0.4999*0.28,
    title=f"CARBON EMISSIONS",
    number={'suffix': f" {utz}"},
    gauge={
        'axis': {'range': [None, 50]},
        'bar': {'color': 'blue'}
      }
        )]
    
  def drop_down_1_change(self, **event_args):
    """This method is called when an item is selected"""
    selectedRange = self.drop_down_1.selected_value
    index = self.drop_down_1.items.index(selectedRange)
    if(index == 0):
      self.lastLabel
      self.adjVal = self.totalKwh
    else:
      self.adjVal = self.timeMap[index-1]
      dt = {
        "range": self.adjVal,
        "device": self.dev
      }
      dataTs = anvil.server.call('changeRange', dt)
      res = dataTs.get_bytes().decode('utf-8')
      res = json.loads(res)
      sum_value = res[0]['sum']
      self.adjsum = sum_value
      self.remapGauges()
      
    
