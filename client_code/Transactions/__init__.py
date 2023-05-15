from ._anvil_designer import TransactionsTemplate
from anvil import *
import plotly.graph_objects as go
import anvil.server
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import json
from datetime import datetime
from collections import Counter

class Transactions(TransactionsTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    res = anvil.server.call('getcashin')
    text = res.get_bytes().decode('utf-8')
    my_array = json.loads(text)
    amounts = []
    dates = []
    totals = []
    for x in my_array:
      transtime = str(x['transtime'])
      transtim = datetime.strptime(str(x['transtime']), '%Y%m%d%H%M%S')
      day = transtim.date().strftime('%Y-%m-%d')
    # Check if the day is already in the dates list
      if day in dates:
        index = dates.index(day)
        totals[index] += x['amount']
      else:
        dates.append(day)
        totals.append(x['amount'])
      amounts.append(x['amount'])
      parsed_date = datetime.strptime(transtime, '%Y%m%d%H%M%S')
      formatted_date = parsed_date.strftime('%d %B %Y %H:%M:%S')
      time_obj = datetime.strptime(formatted_date, '%d %B %Y %H:%M:%S')
# Convert the datetime object to the desired format
      formatted_time = time_obj.strftime('%d %B %Y %I:%M:%S %p')
      x['transtime'] = formatted_time
      x['amount'] = format(x['amount'], ',')
    amnt = 0
    for y in amounts:
      amnt = amnt + y 
    formatted_number = format(amnt, ',')
    self.moneyin.text = "KSH "+str(formatted_number)
    reversed = my_array[::-1]
    self.repeating_panel_1.items = reversed
    primary_color = '#8fce00'
    self.plot_1.data = go.Bar(x=dates, y=totals, marker=dict(color=primary_color),
                              hovertemplate='<b>%{x}</b><br>' + 'Amount: %{y}')
    # Configure the plot layout
    self.plot_1.layout = {
      'title': 'AMOUNT RECEIVED PER DAY',
      'xaxis': {
        'title': 'TIME'
      },
      'yaxis': {
        'title': 'AMOUNT'
      }
    }
    
    names = [obj['name'] for obj in my_array]
    name_counter = Counter(names)

# Get the top 5 most frequent transactors
    top_transactors = [{'name': name, 'frequency': count} for name, count in name_counter.most_common(5)]
    self.repeating_panel_2.items = top_transactors

  def home_link_copy_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Transactions')

  def home_link_copy_2_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Support')

  def home_link_copy_3_click(self, **event_args):
    """This method is called when the link is clicked"""
    c = confirm('Are you sure you want to logout?')
    if(c==True):
      open_form('Login')
    else:
      pass

  def home_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Home', 0)

  def customers_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Customers')

  def request_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Request')






