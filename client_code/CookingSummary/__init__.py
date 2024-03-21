from ._anvil_designer import CookingSummaryTemplate
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

class CookingSummary(CookingSummaryTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.bar = False
    res = anvil.server.call('getAllDeviceData')
    res = res.get_bytes().decode('utf-8')
    res = json.loads(res)
    rawData = res['rawData']
    runtime = (res['runtime'])
    meals = self.count_meals(rawData)
    keyDevs = []
    countMeals = []
    for device_id, info in meals.items():
      keyDevs.append(device_id)
      countMeals.append(info['count'])
    self.plotMealsPerDevice(keyDevs, countMeals)
    keyDevs2 = []
    countHrs = []
    for dev, hrs in runtime.items():
      keyDevs2.append(dev)
      countHrs.append(hrs)
    self.plotCookingTimePerDevice(keyDevs2, countHrs)
    self.cookingTimeValue.text = str(round(self.timeHrs,1)) + " HOURS"
    self.totalMealsValue.text = str(self.mealNum) + " MEALS"
    mls = self.classify_meals(rawData)
    meal_counts_per_day = {}
    datesMeals = []
    mlsCounts = []
    for date, info in mls.items():
      meal_counts_per_day[date] = info['meal_count']
    for date, count in meal_counts_per_day.items():
      datesMeals.append(date)
      mlsCounts.append(count)
    self.cntz = mlsCounts
    self.mlzDate = datesMeals
    self.plot_data_bar(self.mlzDate, self.cntz)
      
     # Any code you write here will run before the form opens.
    
  
  def count_meals(self, data):
    meals_cooked = {}
    for record in data:
      device_id = record['deviceID']
      txtime = datetime.strptime(str(record['txtime']), '%Y%m%d%H%M%S') 
      if device_id not in meals_cooked:
        meals_cooked[device_id] = {'count': 0, 'last_txtime': None}  
      last_txtime = meals_cooked[device_id]['last_txtime'] 
      if last_txtime is not None:
        time_diff = txtime - last_txtime
        if time_diff > timedelta(minutes=20):
          meals_cooked[device_id]['count'] += 1
        
      meals_cooked[device_id]['last_txtime'] = txtime
    
    return meals_cooked

  def plotMealsPerDevice(self, devs, counts):
    countr = 0
    for x in counts:
      countr = countr + x
    self.mealNum = countr
    countr = str(countr) + " MEALS"
    self.plot_1.data = go.Pie(hole=.5, values=counts, hoverinfo="label+value+percent",
                              labels=devs, title=countr)
    self.plot_1.layout = {
      'title': 'MEALS PER DEVICE' }

  def plotCookingTimePerDevice(self, devs, times):
    countr = 0
    for x in times:
      countr = countr + x
    self.timeHrs = countr
    countr = str(round(countr,1)) + " HOURS"
    self.plot_2.data = go.Pie(hole=.5, values=times, hoverinfo="label+value+percent",
                              labels=devs, title=countr)
    self.plot_2.layout = {
      'title': 'COOKING TIME PER DEVICE' }

  def classify_meals(self, records):
    meals_cooked_per_day = {}
  # Group records by date
    for record in records:
      txtime = datetime.strptime(record['time'], '%Y-%m-%dT%H:%M:%S.%fZ')
      date = txtime.date()
      if date not in meals_cooked_per_day:
        meals_cooked_per_day[date] = {'meal_count': 0, 'last_txtime': None}
      if meals_cooked_per_day[date]['last_txtime'] is not None:
        time_diff = txtime - meals_cooked_per_day[date]['last_txtime']
        if time_diff > timedelta(minutes=20):
          meals_cooked_per_day[date]['meal_count'] += 1        
      meals_cooked_per_day[date]['last_txtime'] = txtime   
    return meals_cooked_per_day

  
  def plot_data_bar(self, dates, totals, **event_args):
    self.bar = True
    primary_color = '#0080FF'
    self.plot_3.data = go.Bar(x=dates, y=totals, marker=dict(color=primary_color),
                        hovertemplate='<b>%{x}</b><br>' + 'meals: %{y}')
    # Configure the plot layout
    self.plot_3.layout = {
      'title': 'MEALS PREPARED PER DAY',
      'xaxis': {
        'title': 'TIME'
      },
      'yaxis': {
        'title': 'MEALS'
      }
    }

  def plot_data_line(self, dates, totals, **event_args):
    self.bar = False
    primary_color = '#DB4437'
    self.plot_3.data = go.Scatter(x=dates, y=totals, marker=dict(color=primary_color), mode='lines',
                        line=dict(shape='spline',smoothing=0.7,width=3), hovertemplate='<b>%{x}</b><br>' + 'meals: %{y}')
    # Configure the plot layout
    self.plot_3.layout = {
      'title': 'MEALS PREPARED PER DAY',
      'xaxis': {
        'title': 'TIME'
      },
      'yaxis': {
        'title': 'MEALS'
      }
    }

  def switchGraph_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.bar:
      self.switchGraph.background = "#DB4437"
      self.switchGraph.text = "SWITCH TO BAR GRAPH"
      self.switchGraph.icon = "fa:bar-chart"
      self.plot_data_line(self.mlzDate, self.cntz)
    else:
      self.switchGraph.background = "#0800FF"
      self.switchGraph.text = "SWITCH TO LINE GRAPH"
      self.switchGraph.icon = "fa:line-chart"
      self.plot_data_bar(self.mlzDate, self.cntz)
   
