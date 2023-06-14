from ._anvil_designer import CustomerAnalyticsTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables

class CustomerAnalytics(CustomerAnalyticsTemplate):
  def __init__(self, data, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    malecount = 0
    femalecount = 0
    otherscount = 0
    counties = []
    for x in data:
      counties.append(x['county'])
      date_obj = datetime.strptime(x['date'], "%d %B %Y %I:%M %p")
      if x['gender'] == 'male':
          malecount = malecount + 1
      elif x['gender'] == 'female':
          femalecount = femalecount + 1
      else:
        otherscount = otherscount + 1

    primary_color = '#8fce00'
    print(data)
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
    self.plot_1.layout.template = "rally_dark"

    # Any code you write here will run before the form opens.
