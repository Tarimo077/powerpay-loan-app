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
from datetime import datetime, timezone, timedelta

class DeviceData(DeviceDataTemplate):
  def __init__(self, dev, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    devList = anvil.server.call('getDevList')
    devArr = []
    for x in devList:
      devArr.append(x['deviceID'])
      if x['deviceID'] == dev:
        devData = x
      else:
        pass
    if(devData['active']== True):
      devData['active'] = 'Yes'
    if(devData['active']== False):
      devData['active'] = 'No'
    if(devData['active']=='Yes'):
      self.statusChange.text = 'Deactivate'
      self.statusChange.background = '#DB4437'
      self.statusChange.tooltip = 'Deactivate ' + devData['deviceID']
      self.statusChange.foreground = '#FFFFFF'
      self.label_6.text = "Last Activation Time:"
    else:
      self.statusChange.text = 'Activate'
      self.statusChange.background = '#0080FF'
      self.statusChange.tooltip = 'Activate ' + devData['deviceID']
      self.statusChange.foreground = '#FFFFFF'
      self.label_6.text = "Last Deactivation Time:"
    self.devList.items = devArr
    self.devList.selected_value = dev
    self.activity.text = devData['active']
    if 'time' in devData:
      time_obj_utc = datetime.fromisoformat(devData['time'].replace("Z", "+00:00"))

# Convert the datetime object to the server's timezone
      time_obj_server_tz = time_obj_utc.astimezone(timezone.utc).astimezone()

# Convert the datetime object to Kenyan time
      tz_offset = timedelta(hours=3)
      time_obj_kenya = time_obj_server_tz # + tz_offset

# Format the datetime object as a string in the desired format
      formatted_time_str = time_obj_kenya.strftime("%d %B %Y %I:%M%p").replace("AM", " AM").replace("PM", " PM")
      formatted_time_str = formatted_time_str.replace("th ", "").replace("st ", "").replace("nd ", "").replace("rd ", "")
      self.statusTime.text = formatted_time_str
    else:
      self.statusTime.text = devData['last status change']
    self.devData = devData
    self.lastLabel.visible = False
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
    lat = res['lat']
    long = res['long']
    rawData = res['rawData']
    self.rawData = rawData
    self.map_1.clear()
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
    z = GoogleMap.Circle(center=GoogleMap.LatLng(lat, long), radius=550, fill_color="#0800FF")
    self.map_1.add_component(z)
    self.deviceLabel.text = " " + dev
    last_time = str(res['time'])
    formatted_timestamp = datetime.strptime(last_time, "%Y%m%d%H%M%S").strftime("%Y-%m-%d %H:%M:%S")
    self.lastTime.text = " " + str(formatted_timestamp)
    if dev == 'OfficeFridge1':
      self.label_2.text = "Last Operation Time"
      lb = f"TOTAL OPERATION TIME"
    else:
      lb = f"TOTAL COOKING TIME"
    value = res['totalkwh']  # Replace with your actual value
    self.totalRuntime = res['runtime']
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
    title=lb,
    number={'suffix': f" {uts}"},
    gauge={
        'axis': {'range': [None, 50]},
        'bar': {'color': 'orange'}
    }
)]
    self.energyCost.data = [go.Indicator(
    mode="gauge+number",
    value=(value)*23,
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
    self.dataParseAndPlot(rawData)
    # Any code you write here will run before the form opens.

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form("Request")

  def dataParseAndPlot(self, rawData):
    # Create a dictionary to store cumulative kWh values for each date
    daily_kwh_totals = {}
  # Iterate over the rawData and calculate cumulative kWh values for each date
    for entry in rawData:
  # Extract txtime and convert to date format
      txtime_str = str(entry['txtime'])
      txtime_date = datetime.strptime(txtime_str, '%Y%m%d%H%M%S').strftime('%d-%b-%y')
  # Extract kWh value
      kwh_value = entry['kwh']
  # Add kWh value to the cumulative total for the corresponding date
      daily_kwh_totals[txtime_date] = daily_kwh_totals.get(txtime_date, 0) + kwh_value
  # Extract dates and total kWh values from the dictionary
    dates = list(daily_kwh_totals.keys())
    kwh_totals = list(daily_kwh_totals.values())
    self.plotTS(dates, kwh_totals)


  def plotTS(self, dates, totals):
    # Plot the data
    primary_color = '#0080FF'
    self.plot_2.data = go.Bar(x=dates, y=totals, marker=dict(color=primary_color),
                        hovertemplate='<b>%{x}</b><br>' + 'kwh: %{y}')
    # Configure the plot layout
    self.plot_2.layout = {
      'title': 'ENERGY ACTIVITY ',
      'xaxis': {
        'title': 'TIME'
      },
      'yaxis': {
        'title': 'KWH'
      }
    }

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
    value=(self.adjsum)*23,
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
    self.plotTime.data = [go.Indicator(
    mode="gauge+number",
    value=self.runtime,
    title=f"TOTAL COOKING TIME",
    number={'suffix': f" {uts}"},
    gauge={
        'axis': {'range': [None, 50]},
        'bar': {'color': 'orange'}
    }
)]
    
  def drop_down_1_change(self, **event_args):
    """This method is called when an item is selected"""
    selectedRange = self.drop_down_1.selected_value
    index = self.drop_down_1.items.index(selectedRange)
    if(index == 0):
      self.lastLabel.visible = False
      self.adjsum = self.totalKwh
      self.runtime = self.totalRuntime
      self.remapGauges()
      self.dataParseAndPlot(self.rawData)
    else:
      self.lastLabel.visible = True
      self.adjVal = self.timeMap[index-1]
      dt = {
        "range": self.adjVal,
        "device": self.dev
      }
      dataTs = anvil.server.call('changeRange', dt)
      res = dataTs.get_bytes().decode('utf-8')
      res = json.loads(res)
      sum_value = res['sum']
      self.runtime = res['runtime']
      self.adjsum = sum_value
      time_range = self.timeMap[index - 1]
      start_time = datetime.now() - timedelta(minutes=time_range)
      filtered_data = [entry for entry in self.rawData if datetime.strptime(str(entry['txtime']), '%Y%m%d%H%M%S') >= start_time]
      self.dataParseAndPlot(filtered_data)
      self.remapGauges()

  def devList_change(self, **event_args):
    """This method is called when an item is selected"""
    self.__init__(self.devList.selected_value)

  def statusChange_click(self, **event_args):
    """This method is called when the button is clicked"""
    status = self.devData['active']
    if(status == 'Yes'):
      status = True
      strconc = 'deactivate'
    else:
      status = False
      strconc = 'activate'
    dt = {
      'selectedDev' : self.devData['deviceID'],
      'status' : status
    }
    em = ':eyes:'
    e = anvil.server.call('emojiPass', em)
    c = confirm('Are you sure you want to ' + strconc + ' ' + self.devData['deviceID'] +' '+ e , buttons=[("Yes", True),("No", False)])
    if(c==True):
      anvil.server.call('changeStatus', dt)
      dt = {
      "data": 'GET'
      }
      response = anvil.server.call('req', dt)
      text = response.get_bytes().decode('utf-8')
      my_array = json.loads(text)
      sorted_items = sorted(my_array, key=lambda x: x['deviceID'])
      anvil.server.call('strDevArr', sorted_items)
      if(strconc=='deactivate'):
        ef = ':red_circle:'
      else:
        ef = ':blue_circle:'
      et = anvil.server.call('emojiPass', ef)
      alert(et + ' '+self.devData['deviceID'] + ' ' + strconc + 'd', buttons=None)
      open_form('DeviceData', self.devData['deviceID'])
    else:
      pass
      
    
