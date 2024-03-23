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
    self.noData.visible = False
    self.plot_2.visible = True
    self.plot_3.visible = True
    self.plot_1.visible = True
    self.switchGraph.visible = True
    self.drop_down_1.items = ["All Time", "Last 5 min", "Last 30 min", "Last 1 hr", "Last 3 hrs", "Last 12 hrs", "Last 24 hrs", "Last 3 days", "Last 7 days", "Last 2 weeks",
                              "Last 1 month", "3 months", "Last 6 months", "Last 1 year", "Last 3 years"]
    self.timeMap = [5, 30, 60, 180, 720, 1440, 4320, 10080, 20160, 40320, 120960, 241920, 483840, 1451520]
    res = anvil.server.call('getAllDeviceData')
    res = res.get_bytes().decode('utf-8')
    res = json.loads(res)
    rawData = res['rawData']
    runtime = res['runtime']
    self.rawData = rawData
    meals, mls = self.classify_and_count_meals(rawData)
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
    self.cookingTimeValue.tooltip = self.cookingTimeValue.text + " represents amount of cooking time for all devices"
    self.totalMealsValue.tooltip = self.totalMealsValue.text + " represents the number of meals prepared by all devices"
    meal_counts_per_day = {}
    datesMeals = []
    mlsCounts = []
    for date, count in meal_counts_per_day.items():
      datesMeals.append(date)
      mlsCounts.append(count)
    self.cntz = list(mls.values())
    self.mlzDate = list(mls.keys())
    self.plot_data_bar(self.mlzDate, self.cntz)
      
     # Any code you write here will run before the form opens.

  def classify_and_count_meals(self, data):
    # Sort the data by device ID and timestamp
    sorted_data = sorted(data, key=lambda x: (x['deviceID'], x['txtime']))

    # Initialize variables to store meal counts for each device and each day
    device_meal_counts = {}
    day_meal_counts = {}

    for entry in sorted_data:
        device_id = entry['deviceID']
        txtime = datetime.strptime(str(entry['txtime']), "%Y%m%d%H%M%S")

        # Update device meal counts
        if device_id not in device_meal_counts:
            device_meal_counts[device_id] = {'count': 0, 'last_txtime': None}
        if device_meal_counts[device_id]['last_txtime'] is not None:
            time_diff = txtime - device_meal_counts[device_id]['last_txtime']
            if time_diff > timedelta(minutes=20):
                device_meal_counts[device_id]['count'] += 1
        else:
            device_meal_counts[device_id]['count'] += 1

        # Update day meal counts
        date = txtime.strftime('%Y-%m-%d')
        if date not in day_meal_counts:
            day_meal_counts[date] = {}
        if device_id not in day_meal_counts[date]:
            day_meal_counts[date][device_id] = 0
        if 'last_txtime' in day_meal_counts[date]:
            time_diff = txtime - day_meal_counts[date]['last_txtime']
            if time_diff > timedelta(minutes=20):
                day_meal_counts[date][device_id] += 1
        else:
            day_meal_counts[date][device_id] += 1
        
        device_meal_counts[device_id]['last_txtime'] = txtime
        day_meal_counts[date]['last_txtime'] = txtime
    
    total_meals_per_day = {}
  # Iterate through each day's meal counts
    for date, counts in day_meal_counts.items():
  # Sum up the meal counts for the day
      total_meals = sum(count for device, count in counts.items() if device != 'last_txtime')
  # Store the total meals for the day
      total_meals_per_day[date] = total_meals
    return device_meal_counts, total_meals_per_day
    

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

  
  def plot_data_bar(self, dates, totals, **event_args):
    self.bar = True
    primary_color = '#0080FF'
    self.plot_3.data = go.Bar(x=dates, y=totals, marker=dict(color=primary_color),
                        hovertemplate='<b>%{x}</b><br>' + 'meals: %{y}')
    # Configure the plot layout
    self.plot_3.layout = {
      'title': 'MEALS PREPARED PER DAY',
      'xaxis': {
        'title': 'DAYS'
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
        'title': 'DAYS'
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

  def dataParseAndPlot(self, rawData):
    self.noData.visible = False
    self.plot_2.visible = True
    self.plot_3.visible = True
    self.plot_1.visible = True
    self.switchGraph.visible = True
    meals, mls = self.classify_and_count_meals(rawData)
    keyDevs = []
    countMeals = []
    for device_id, info in meals.items():
      keyDevs.append(device_id)
      countMeals.append(info['count'])
    self.plotMealsPerDevice(keyDevs, countMeals)
    keyDevs2 = []
    countHrs = []
    selectedRange = self.drop_down_1.selected_value
    index = self.drop_down_1.items.index(selectedRange)
    range = self.timeMap[index-1]
    dt = {
      "range": range
    }
    runtime = anvil.server.call('changeRangeIndex', dt)
    runtime = runtime.get_bytes().decode('utf-8')
    runtime = json.loads(runtime)
    if runtime == 0:
      self.switchGraph.visible = False
      self.plot_2.visible = False
      self.plot_3.visible = False
      self.plot_1.visible = False
      self.noData.text = 'NO DATA AVAILABLE FOR THE ' + str(self.drop_down_1.selected_value)
      self.noData.visible = True
    else:
      for device_info in runtime:  # Iterate over each dictionary in the list
        for dev, hrs in device_info.items():  # Extract key-value pairs from each dictionary
          keyDevs2.append(dev)
          hrs = hrs/3600
          countHrs.append(hrs)
      self.plotCookingTimePerDevice(keyDevs2, countHrs)
      self.cntz = list(mls.values())
      self.mlzDate = list(mls.keys())
      self.plot_data_bar(self.mlzDate, self.cntz)

  def drop_down_1_change(self, **event_args):
    """This method is called when an item is selected"""
    selectedRange = self.drop_down_1.selected_value
    index = self.drop_down_1.items.index(selectedRange)
    if index == 0:  # All Time
  # No filtering needed, use the stored raw data directly
      self.__init__()
    else:
  # Filter the stored raw data based on the selected time range
      time_range = self.timeMap[index - 1]
      start_time = datetime.now() - timedelta(minutes=time_range)
      filtered_data = [entry for entry in self.rawData if datetime.strptime(str(entry['txtime']), '%Y%m%d%H%M%S') >= start_time]
      self.dataParseAndPlot(filtered_data)
    
