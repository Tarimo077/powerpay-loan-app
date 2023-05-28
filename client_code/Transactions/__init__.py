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
import anvil.js
from ..Password import Password

class Transactions(TransactionsTemplate):
  def __init__(self, csh, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    label_element = anvil.js.get_dom_node(self.moneyin)
    label_element.style.filter = "blur(25px)"
    self.seecash = csh
    self.button_1.tooltip = 'view cash in'
    res = anvil.server.call('getcashin')
    text = res.get_bytes().decode('utf-8')
    my_array = json.loads(text)
    amounts = []
    dates = []
    totals = []
    total_amounts = {}
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
      name = x['name']
      amount = int(x['amount'])
      if name in total_amounts:
        total_amounts[name] += amount
      else:
        total_amounts[name] = amount
      x['amount'] = format(x['amount'], ',')
    amnt = 0
    sorted_transactors = sorted(total_amounts.items(), key=lambda x: x[1], reverse=True)
    output = [{'name': nme, 'amount': am} for nme, am in sorted_transactors]
    for s in output:
      s['amount'] = format(s['amount'], ',')
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
    self.repeating_panel_3.items = output

  def home_link_copy_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Transactions', True)

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

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    if(self.seecash==False):
      nw_frm = Password()
      alert(
          content = new_frm,
          large=False,
          title='ENTER PIN'
        )
      self.button_1.background = '#8fce00'
      self.button_1.icon = 'fa:eye'
      self.button_1.tooltip = 'view cash in'
      label_element = anvil.js.get_dom_node(self.moneyin)
      label_element.style.filter = "blur(25px)"
      self.seecash = True
    else:
      self.button_1.background = '#ffa500'
      self.button_1.icon = 'fa:eye-slash'
      self.button_1.tooltip = 'hide cash in'
      label_element = anvil.js.get_dom_node(self.moneyin)
      label_element.style.filter = "blur(0px)"
      self.seecash = False
      







