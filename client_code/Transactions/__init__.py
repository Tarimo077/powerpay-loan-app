from ._anvil_designer import TransactionsTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
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
from ..DownloadPassword import DownloadPassword
from ..UserPopover import UserPopover
from anvil_extras import popover

class Transactions(TransactionsTemplate):
  def __init__(self, csh, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.graph = False
    self.drop_down_1.items = ['name', 'reference', 'date', 'transaction ID']
    self.drop_down_1.selected_value = self.drop_down_1.items[0]
    self.search.placeholder = 'search transactions by name'
    usr = anvil.server.call('getusername')
    words = usr.split()
# Extract the first character of each word and convert it to uppercase
    initials = [word[0].upper() for word in words]
# Join the initials together
    initials_string = ''.join(initials)
    self.username_label.text = initials_string
    self.seecash = csh
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
    if(self.seecash==True):
      self.hide_cash()
    else:
      self.view_cash()
    reversed = my_array[::-1]
    self.arr = reversed
    self.repeating_panel_1.items = reversed    
    names = [obj['name'] for obj in my_array]
    name_counter = Counter(names)
    self.plot_data_line(dates, totals)
    self.dates = dates
    self.totals = totals
# Get the top 5 most frequent transactors
    top_transactors = [{'name': name, 'frequency': count} for name, count in name_counter.most_common()]
    self.repeating_panel_2.items = top_transactors
    self.repeating_panel_3.items = output
    self.username_label.popover(UserPopover(), 
                          placement = 'bottom', 
                          trigger='stickyhover', 
                          delay={ "show": 100, "hide": 100 },
                          max_width='700px'
                         )

  def plot_data_line(self, dates, totals, **event_args):
    primary_color = '#0080FF'
    self.plot_1.data = go.Scatter(x=dates, y=totals, marker=dict(color=primary_color), mode='lines',
                        line=dict(shape='spline',smoothing=0.7,width=3), hovertemplate='<b>%{x}</b><br>' + 'Amount: %{y}')
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

  def plot_data_bar(self, dates, totals, **event_args):
    primary_color = '#0080FF'
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
    

  def home_link_copy_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Transactions', True)

  def home_link_copy_3_click(self, **event_args):
    """This method is called when the link is clicked"""
    c = confirm('Are you sure you want to logout?', buttons=[("Yes", True),("No", False)])
    if(c==True):
      open_form('Login')
    else:
      pass

  def home_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Index')

  def customers_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Customers')

  def request_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Request')

  def view_cash(self, **event_args):
    self.button_1.background = '#DB4437'
    self.button_1.icon = 'fa:eye-slash'
    self.button_1.tooltip = 'hide cash in'
    label_element = anvil.js.get_dom_node(self.moneyin)
    label_element.style.filter = "blur(0px)"
    self.seecash = False

  def hide_cash(self, **event_args):
    self.button_1.background = '#0080FF'
    self.button_1.icon = 'fa:eye'
    self.button_1.tooltip = 'view cash in'
    label_element = anvil.js.get_dom_node(self.moneyin)
    label_element.style.filter = "blur(25px)"
    self.seecash = True   
    

  def button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    if(self.seecash==True):
      nw_frm = Password()
      alert_instance = alert(
        content=nw_frm,
        large=False,
        title=None,
        dismissible=False,
        buttons=[('Cancel', 0)],
        role='outlined'
      )
      if(alert_instance==0):
        self.hide_cash()
        self.seecash = True
      else:
        self.seecash = False
    else:
      self.hide_cash()

  def bar_graph_click(self, **event_args):
    """This method is called when the button is clicked"""
    if self.graph == True:
      self.plot_data_line(self.dates, self.totals)
      self.bar_graph.background = '#DB4437'
      self.bar_graph.text = 'SWITCH TO BAR GRAPH'
      self.graph = False
    else:
      self.plot_data_bar(self.dates, self.totals)
      self.bar_graph.background = '#0080FF'
      self.bar_graph.text = 'SWITCH TO LINE GRAPH'
      self.graph = True

  def button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    nw_frm = DownloadPassword(self.arr)
    alert_instance = alert(
        content=nw_frm,
        large=False,
        title=None,
        dismissible=False,
        buttons=[('Cancel', 0)],
        role='outlined')

  def query_click(self, **event_args):
    """This method is called when the button is clicked"""
    frm = str(self.calender_from.date)
    to = str(self.calender_to.date)
    frm = datetime.strptime(frm, "%Y-%m-%d")
    to = datetime.strptime(to, "%Y-%m-%d")
    nw_arr = []
    for z in self.arr:
      dt = datetime.strptime(z['transtime'], "%d %B %Y %I:%M:%S %p")
      if dt <= to and dt >= frm:
        nw_arr.append(z)
      else:
        pass
    index = 1
    for y in nw_arr:
      y['index'] = index
      index = index + 1
    for e in nw_arr:
      e['index'] = str(e['index'])
    self.repeating_panel_1.items = nw_arr

  def calender_to_change(self, **event_args):
    """This method is called when the selected date changes"""
    if self.calender_to.date and self.calender_from.date is not None:
      self.query.visible = True
    else:
      self.query.visible = False

  def search_change(self, **event_args):
    """This method is called when the text in this text box is edited"""
    x = self.drop_down_1.selected_value
    if(x == 'name'):
      search_text = self.search.text
      leng = len(search_text)
      filtered_objects = [obj for obj in self.arr if obj['name'][:leng].lower() == search_text.lower()]
      index = 1
      for w in filtered_objects:
        w['index'] = index
        index = index + 1
      for e in filtered_objects:
        e['index'] = str(e['index'])
      self.repeating_panel_1.items = filtered_objects
    elif(x == 'reference'):
      search_text = self.search.text
      leng = len(search_text)
      filtered_objects = [obj for obj in self.arr if obj['ref'][:leng].lower() == search_text.lower()]
      index = 1
      for w in filtered_objects:
        w['index'] = index
        index = index + 1
      for e in filtered_objects:
        e['index'] = str(e['index'])
      self.repeating_panel_1.items = filtered_objects    
    elif(x == 'transaction ID'):
      search_text = self.search.text
      leng = len(search_text)
      filtered_objects = [obj for obj in self.arr if obj['id'][:leng].lower() == search_text.lower()]
      index = 1
      for w in filtered_objects:
        w['index'] = index
        index = index + 1
      for e in filtered_objects:
        e['index'] = str(e['index'])
      self.repeating_panel_1.items = filtered_objects  
    

  def drop_down_1_change(self, **event_args):
    """This method is called when an item is selected"""
    x = self.drop_down_1.selected_value
    self.repeating_panel_1.items = self.arr
    self.search.text = ''
    if(x == 'name'):
      self.search.placeholder = 'search transactions by name'
      self.from_date.visible = False
      self.to_date.visible = False
      self.calender_from.visible = False
      self.calender_to.visible = False
      self.search.visible = True
      self.query.visible = False
    elif(x == 'reference'):
      self.search.placeholder = 'search transactions by reference'
      self.from_date.visible = False
      self.to_date.visible = False
      self.calender_from.visible = False
      self.calender_to.visible = False
      self.search.visible = True
      self.query.visible = False
    elif(x == 'transaction ID'):
      self.search.placeholder = 'search transactions by transaction ID'
      self.from_date.visible = False
      self.to_date.visible = False
      self.calender_from.visible = False
      self.calender_to.visible = False
      self.search.visible = True
      self.query.visible = False
    else:
      self.from_date.visible = True
      self.to_date.visible = True
      self.calender_from.visible = True
      self.calender_to.visible = True
      self.search.visible = False
      self.query.visible = False
      






      
      







