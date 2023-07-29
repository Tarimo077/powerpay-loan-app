from ._anvil_designer import CustomerAnalyticsTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import plotly.graph_objects as go
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from datetime import datetime, timedelta

class CustomerAnalytics(CustomerAnalyticsTemplate):
  def __init__(self, data, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.graph = False 
    malecount = 0
    femalecount = 0
    otherscount = 0
    counties = {}
    counts = {}
    sals = []
    for x in data:
      date_obj = datetime.strptime(x['date'], "%d %B %Y %I:%M %p")
      date = date_obj.date()
      kaunty = x['county']
      salary = x['salary']
      if salary is not 'N/A':  
        sals.append(int(salary))        
      if x['gender'] == 'male':
          malecount = malecount + 1
      elif x['gender'] == 'female':
          femalecount = femalecount + 1
      else:
        otherscount = otherscount + 1
      if date in counts:
        counts[date] += 1
      else:
        counts[date] = 1
      if kaunty in counties:
        counties[kaunty] += 1
      else:
        counties[kaunty] = 1

    dates = list(counts.keys())
    countz = list(counts.values())
    self.dates = dates
    self.countz = countz
    mx = max(countz)
    self.mx = mx
    county_names = list(counties.keys())
    county_no = list(counties.values())
    totals = 0
    counties_by_percentage = []
    for t in county_no:
      totals = totals + t
    for d in county_no:
      d = (d/totals) * 100
      d = round(d, 1)
      counties_by_percentage.append(d)
    primary_color = '#8fce00'
    self.plot_1.data = go.Bar(x=[malecount, femalecount, otherscount], y=['Male', 'Female', 'Others'],
                              marker=dict(color=primary_color),width=0.4, orientation='h')
    #Configure the plot layout
    self.plot_1.layout = {
      'title': 'CUSTOMERS BY GENDER',
      'yaxis': {
        'title': ''
      },
      'xaxis': {
        'title': 'NUMBER OF CUSTOMERS'
      }
    }
    ##Plot here
    primary_color = '#8fce00'
    self.plot_2.data = go.Bar(x=self.dates, y=self.countz, marker=dict(color=primary_color),
                        hovertemplate='<b>%{x}</b><br>' + 'Customers: %{y}')
    # Configure the plot layout
    self.plot_2.layout = {
      'title': 'NEW CUSTOMERS BY DAY',
      'xaxis': {
        'title': 'TIME'
      },
      'yaxis': {
        'title': 'NUMBER OF CUSTOMERS',
        'range': [0, self.mx]
      }
    }    
    self.plot_3.data = go.Bar(y=county_names, x=counties_by_percentage, marker=dict(color=primary_color),
                              width=0.4, orientation='h')
    self.plot_3.layout = {
      'title': 'CUSTOMERS BY COUNTY',
      'yaxis': {
        'title': 'COUNTY'
      },
      'xaxis': {
        'title': 'PERCENTAGE OF CUSTOMERS'
      }
    }
    salaries = {
      'Under 20k': 0,
      '20-40k': 0,
      '40-60k': 0,
      '60-80k': 0,
      '80-100k': 0,
      'Over 100k' : 0
    }
    for r in sals:
      if r < 20000:
        salaries['Under 20k'] += 1
      elif r >= 20000 and r < 40000:
        salaries['20-40k'] += 1
      elif r >= 40000 and r < 60000:
        salaries['40-60k'] += 1
      elif r >= 60000 and r < 80000:
        salaries['60-80k'] += 1
      elif r >= 80000 and r < 100000:
        salaries['80-100k'] += 1
      elif r >= 100000:
        salaries['Over 100k'] += 1
      else:
        pass
    salkeys = list(salaries.keys())
    salvals = list(salaries.values())
    self.plot_4.data = go.Bar(x=salkeys, y=salvals, marker=dict(color=primary_color))
    self.plot_4.layout = {
      'title': 'CUSTOMERS BY INCOME',
      'yaxis': {
        'title': 'NO. OF CUSTOMERS'
      },
      'xaxis': {
        'title': 'SALARY RANGES'
      }
    }
    self.mapping_func(county_names)
    # Any code you write here will run before the form opens.

  def plot_data_line(self, **event_args):
    primary_color = '#8fce00'
    self.plot_2.data = go.Scatter(x=self.dates, y=self.countz, marker=dict(color=primary_color), mode='lines',
                        line=dict(shape='spline',smoothing=0.7,width=3), hovertemplate='<b>%{x}</b><br>' + 'Customers: %{y}')
    self.plot_2.layout = {
      'title': 'NEW CUSTOMERS BY DAY',
      'xaxis': {
        'title': 'TIME'
      },
      'yaxis': {
        'title': 'NUMBER OF CUSTOMERS'
      }
    }

  def plot_data_bar(self, **event_args):
    primary_color = '#8fce00'
    self.plot_2.data = go.Bar(x=self.dates, y=self.countz, marker=dict(color=primary_color),
                        hovertemplate='<b>%{x}</b><br>' + 'Customers: %{y}')
    # Configure the plot layout
    self.plot_2.layout = {
      'title': 'NEW CUSTOMERS BY DAY',
      'xaxis': {
        'title': 'TIME'
      },
      'yaxis': {
        'title': 'NUMBER OF CUSTOMERS',
        'range': [0, self.mx]
      }
    }

  def mapping_func(self, geos, **event_args):
    self.map_1.center = GoogleMap.LatLng(0.007488702331643685, 37.074308299465)
    self.map_1.zoom = 8
    self.map_1.disable_double_click_zoom = True
    self.map_1.zoom_control = False
    self.map_1.draggable = False
    self.map_1.fullscreen_control = False
    self.map_1.disable_default_ui = True
    self.map_1.rotate_control = False
    self.map_1.street_view_control = False
    for x in geos:
      if x == 'N/A':
        pass
      else:
        results = GoogleMap.geocode(address=x+', Kenya')
        #m = GoogleMap.Marker(position=results[0].geometry.location)
        s = GoogleMap.Circle(center=GoogleMap.LatLng(results[0].geometry.location), radius=10000,
                             fill_color='#FF0000', fill_opacity=0.7, stroke_color='#FF0000',
                            stroke_opacity=0.5, stroke_weight=0.5)
        self.map_1.add_component(s)
    #self.map_1.map_data.add(GoogleMap.Data.Feature(geometry=GoogleMap.Data.Point(GoogleMap.LatLng(-0.29726907778613565, 36.11320027767494))))
    #self.map_1.map_data.add(GoogleMap.Data.Feature(geometry=GoogleMap.Data.Point(GoogleMap.LatLng(-1.1731848164507699, 36.83101474225459))))
    self.map_1.map_data.style = GoogleMap.Data.StyleOptions(icon=GoogleMap.Symbol(path=GoogleMap.SymbolPath.CIRCLE,
          scale=40,
          fill_color='#ffa500',
          fill_opacity=0.6,
          stroke_opacity=1,
          stroke_weight=1
  )
)

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Customers')

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.graph == True:
      self.plot_data_bar()
      self.button_2.background = '#ffa500'
      self.button_2.text = 'SWITCH TO LINE GRAPH'
      self.graph = False
    else:
      self.plot_data_line()
      self.button_2.background = '#8fce00'
      self.button_2.text = 'SWITCH TO BAR GRAPH'
      self.graph = True

    


  


    
