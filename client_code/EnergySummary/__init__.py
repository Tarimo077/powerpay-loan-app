from ._anvil_designer import EnergySummaryTemplate
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


class EnergySummary(EnergySummaryTemplate):
  def __init__(self, **properties):
        # Set Form properties and Data Bindings.
    self.init_components(**properties)
    res = anvil.server.call('getAllDeviceData')
    res = res.get_bytes().decode('utf-8')
    res = json.loads(res)
    rawData = res['rawData']
        
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
        
        # Plot the data
    self.plot_data_bar(dates, kwh_totals)

  def plot_data_bar(self, dates, totals, **event_args):
    primary_color = '#0080FF'
    self.plot_1.data = go.Bar(x=dates, y=totals, marker=dict(color=primary_color),
                        hovertemplate='<b>%{x}</b><br>' + 'kwh: %{y}')
    # Configure the plot layout
    self.plot_1.layout = {
      'title': 'ENERGY ACTIVITY',
      'xaxis': {
        'title': 'TIME'
      },
      'yaxis': {
        'title': 'KWH'
      }
    }
