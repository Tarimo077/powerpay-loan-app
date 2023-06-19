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
    malecount = 0
    femalecount = 0
    otherscount = 0
    counties = {}
    counts = {}
    for x in data:
      date_obj = datetime.strptime(x['date'], "%d %B %Y %I:%M %p")
      date = date_obj.date()
      kaunty = x['county']
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
    county_names = list(counties.keys())
    county_no = list(counties.values())
    primary_color = '#8fce00'
    self.plot_1.data = go.Bar(y=[malecount, femalecount, otherscount], x=['Male', 'Female', 'Others'], marker=dict(color=primary_color),width=0.1)
    #Configure the plot layout
    self.plot_1.layout = {
      'title': 'CUSTOMERS BY GENDER',
      'xaxis': {
        'title': ''
      },
      'yaxis': {
        'title': 'NUMBER OF CUSTOMERS'
      }
    }
    self.plot_1.layout.template = "rally_light"
    self.plot_2.data = go.Bar(x=dates, y=countz, marker=dict(color=primary_color))
    self.plot_2.layout = {
      'title': 'NEW CUSTOMERS BY DAY',
      'xaxis': {
        'title': 'TIME'
      },
      'yaxis': {
        'title': 'NUMBER OF CUSTOMERS'
      }
    }
    self.plot_3.data = go.Bar(x=county_names, y=county_no, marker=dict(color=primary_color), width=0.5)
    self.plot_3.layout = {
      'title': 'CUSTOMERS BY COUNTY',
      'xaxis': {
        'title': 'COUNTY'
      },
      'yaxis': {
        'title': 'NUMBER OF CUSTOMERS'
      }
    }
    self.mapping_func(county_names)
    print(county_names)

    # Any code you write here will run before the form opens.

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
        results = GoogleMap.geocode(address=x)
        print(results)
        #m = Marker(position=results[0].geometry.location)
        self.map_1.map_data.add(GoogleMap.Data.Feature(geometry=))
        
    
    
    #Naks = GoogleMap.Point(-0.29726907778613565, 36.11320027767494)
    #Kiambu = GoogleMap.Point(-1.1731848164507699, 36.83101474225459)
    #self.map_1.map_data.add(GoogleMap.Data.Feature(geometry=GoogleMap.Data.Point(GoogleMap.LatLng(-0.29726907778613565, 36.11320027767494))))
    #self.map_1.map_data.add(GoogleMap.Data.Feature(geometry=GoogleMap.Data.Point(GoogleMap.LatLng(-1.1731848164507699, 36.83101474225459))))
    self.map_1.map_data.style = GoogleMap.Data.StyleOptions(icon=GoogleMap.Symbol(path=GoogleMap.SymbolPath.CIRCLE,
          scale=20,
          fill_color='#ffa500',
          fill_opacity=0.6,
          stroke_opacity=1,
          stroke_weight=1
  )
)

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Customers')



    
