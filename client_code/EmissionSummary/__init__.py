from ._anvil_designer import EmissionSummaryTemplate
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
from datetime import datetime, timedelta

class EmissionSummary(EmissionSummaryTemplate):
  def __init__(self, **properties):
        # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.bar = False
    self.drop_down_1.items = ["All Time", "Last 5 min", "Last 30 min", "Last 1 hr", "Last 3 hrs", "Last 12 hrs", "Last 24 hrs", "Last 3 days", "Last 7 days", "Last 2 weeks",
                              "Last 1 month", "Last 3 months", "Last 6 months", "Last 1 year", "Last 3 years"]
    self.timeMap = [5, 30, 60, 180, 720, 1440, 4320, 10080, 20160, 40320, 120960, 241920, 483840, 1451520]
    res = anvil.server.call('getAllDeviceData')
    res = res.get_bytes().decode('utf-8')
    res = json.loads(res)
    rawData = res['rawData']
    totalKwh = res['totalkwh']
    self.rawData = rawData
    self.dataParseAndPlot(rawData)
    self.totalEmissions.text = str(round((totalKwh*0.4999*0.28),2)) + " KGS"
    self.emissionsPerDevice.text = str(round((totalKwh*0.4999*0.28),2)/len(self.dt)) + " KGS/DEVICE"
    self.totalEmissions.tooltip = self.totalEmissions.text + " represents the amount of carbon released by all devices"
    self.emissionsPerDevice.tooltip = self.emissionsPerDevice.text + " represents the average amount of carbon released by all devices"    
    

  def dataParseAndPlot(self, rawData):
    # Create a dictionary to store cumulative kWh values for each date
    daily_kwh_totals = {}
  # Iterate over the rawData and calculate cumulative kWh values for each date
    for entry in rawData:
  # Extract txtime and convert to date format
      txtime_str = str(entry['txtime'])
      txtime_date = datetime.strptime(txtime_str, '%Y%m%d%H%M%S').strftime('%d-%b-%y')
  # Extract kWh value
      kwh_value = (entry['kwh'])*(0.4999*0.28)
  # Add kWh value to the cumulative total for the corresponding date
      daily_kwh_totals[txtime_date] = daily_kwh_totals.get(txtime_date, 0) + kwh_value
  # Extract dates and total kWh values from the dictionary
    dates = list(daily_kwh_totals.keys())
    kwh_totals = list(daily_kwh_totals.values())
  # Plot the data
    self.plot_data_bar(dates, kwh_totals)
    self.dates = dates
    self.totals = kwh_totals
    dt = self.getKwhPwerDevice(rawData)
    self.plotKwhPerDevice(dt)
    self.dt = dt
    morning, afternoon, night = self.categorize_kwh(rawData)
    self.plotKwhPerMeal(morning, afternoon, night)
  

  def plot_data_bar(self, dates, totals, **event_args):
    self.bar = True
    primary_color = '#0080FF'
    self.plot_3.data = go.Bar(x=dates, y=totals, marker=dict(color=primary_color),
                        hovertemplate='<b>%{x}</b><br>' + 'kgs: %{y}')
    # Configure the plot layout
    self.plot_3.layout = {
      'title': 'EMISSIONS PER DAY',
      'xaxis': {
        'title': 'DAYS'
      },
      'yaxis': {
        'title': 'KGS'
      }
    }

  def plot_data_line(self, dates, totals, **event_args):
    self.bar = False
    primary_color = '#DB4437'
    self.plot_3.data = go.Scatter(x=dates, y=totals, marker=dict(color=primary_color), mode='lines',
                        line=dict(shape='spline',smoothing=0.7,width=3), hovertemplate='<b>%{x}</b><br>' + 'kgs: %{y}')
    # Configure the plot layout
    self.plot_3.layout = {
      'title': 'EMISSIONS PER DAY',
      'xaxis': {
        'title': 'DAYS'
      },
      'yaxis': {
        'title': 'KGS'
      }
    }

  def getKwhPwerDevice(self, records):
    device_kwh_totals = {}    
    for record in records:
        device_id = record['deviceID']
        kwh = (record['kwh'])*(0.4999*0.28)        
  # If device_id not in dictionary, add it with initial kwh value
        if device_id not in device_kwh_totals:
          device_kwh_totals[device_id] = kwh
  # If device_id already exists, add kwh to existing total
        else:
          device_kwh_totals[device_id] += kwh
    
    return device_kwh_totals

  def plotKwhPerDevice(self, datas):
    countr = len(datas)
    countr = str(countr) + " DEVICES"
    self.plot_2.data = go.Pie(hole=.5, values=list(datas.values()), hoverinfo="label+value+percent",
                              labels=list(datas.keys()), title=countr)
    self.plot_2.layout = {
      'title': 'EMISSIONS PER DEVICE' }

  def categorize_kwh(self, data):
    morning_kwh = 0
    afternoon_kwh = 0
    night_kwh = 0
    for record in data:
      txtime = str(record['txtime'])
      hour = str(txtime[8:10])  # Extracting the hour component
  # Categorizing based on the hour
      if 4 <= int(hour) < 11:  # Morning: 4am - 11:29am
        morning_kwh += (record['kwh'])*(0.4999*0.28)
      elif 11 <= int(hour) < 17:  # Afternoon: 11:30am - 4:59pm
        afternoon_kwh += (record['kwh'])*(0.4999*0.28)
      else:  # Night: 5:00pm - 3:59am
        night_kwh += (record['kwh'])*(0.4999*0.28)
    return morning_kwh, afternoon_kwh, night_kwh

  def plotKwhPerMeal(self, morning, afternoon, night):
    totz = round((morning + afternoon + night),2)
    totz = str(totz) + " KGS"
    self.plot_1.data = go.Pie(hole=.5, values=[morning, afternoon, night], hoverinfo="label+value+percent",
                              labels=["Breakfast", "Lunch", "Supper"], title=totz)
    self.plot_1.layout = {
      'title': 'EMISSIONS PER MEAL' }

  def switchGraph_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.bar:
      self.switchGraph.background = "#DB4437"
      self.switchGraph.text = "SWITCH TO BAR GRAPH"
      self.switchGraph.icon = "fa:bar-chart"
      self.plot_data_line(self.dates, self.totals)
    else:
      self.switchGraph.background = "#0800FF"
      self.switchGraph.text = "SWITCH TO LINE GRAPH"
      self.switchGraph.icon = "fa:line-chart"
      self.plot_data_bar(self.dates, self.totals)
    

    # Any code you write here will run before the form opens.

  def drop_down_1_change(self, **event_args):
    """This method is called when an item is selected"""
    selectedRange = self.drop_down_1.selected_value
    index = self.drop_down_1.items.index(selectedRange)
    if index == 0:  # All Time
  # No filtering needed, use the stored raw data directly
      self.dataParseAndPlot(self.rawData)
    else:
  # Filter the stored raw data based on the selected time range
      time_range = self.timeMap[index - 1]
      start_time = datetime.now() - timedelta(minutes=time_range)
      filtered_data = [entry for entry in self.rawData if datetime.strptime(str(entry['txtime']), '%Y%m%d%H%M%S') >= start_time]
      self.dataParseAndPlot(filtered_data)
