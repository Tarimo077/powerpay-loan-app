from ._anvil_designer import HomeTemplate
from anvil import *
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.server
import plotly.graph_objects as go
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.users
from datetime import datetime, timedelta
import json
import anvil.js
from anvil_extras.animation import animate, fade_in, Transition


class Home(HomeTemplate):
  def __init__(self, boo, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    #res = anvil.server.call('getoldcustomers')
    #text = res.get_bytes().decode('utf-8')
    #old_customers = json.loads(text)
    self.boo = boo
    usr = anvil.server.call('getusername')
    words = usr.split()

# Extract the first character of each word and convert it to uppercase
    initials = [word[0].upper() for word in words]

# Join the initials together
    initials_string = ''.join(initials)
    self.username_label.text = initials_string
    # Get today's date
    #today = datetime.now().date()
# Calculate the date 1 month ago from today
    #one_month_ago = today - timedelta(days=30)
    #customers_begin_of_period = app_tables.customers.search(active_date=q.less_than_or_equal_to(one_month_ago))
    #new_customers = app_tables.customers.search(active_date=q.greater_than(one_month_ago))
    #bgn = len(customers_begin_of_period)
    #nw = len(new_customers)    
    #dats = {}
    #rxt = anvil.server.call('getchurn', dats)
    #rxt = rxt.get_bytes().decode('utf-8')
    #rxt = json.loads(rxt)
    #customers_this_month = app_tables.customers.search()
    #customers_this_month = len(customers_this_month)
    
    #curr_customers = len(app_tables.customers.search())
    #churn = (rxt/(bgn+nw))*100
    #portfolio = ((customers_this_month-bgn)/bgn)*100
    #churn = round(churn, 1)
    #portfolio = round(portfolio, 1)
    #self.churn.text = "   "+str(churn)+"%"
    #self.portfolio.text = "   "+str(portfolio)+"%"
    #dt = {
     # "data": 'GET'
    #}
    #response = anvil.server.call('req', dt)
    #text = response.get_bytes().decode('utf-8')
    #my_array = json.loads(text)
    #dev_total = len(my_array)
    #self.range = 3
    #self.plot_dt()
    #customer_table = app_tables.customers

# Count the number of rows in the table
    #customer_count = len(customer_table.search())
    #rt = anvil.server.call('getcustomers')
    #rt = rt.get_bytes().decode('utf-8')
    #rt = json.loads(rt)
    #leng = len(rt)
    #self.product_no.text = dev_total
    #self.customers_no.text = str(leng)
    # Any code you write here will run before the form opens.


#  def plot_dt(self, **event_args):
#    today = datetime.utcnow().date()
#    date_counts = {}
  
#    for i in range(self.range):
#      date = today - timedelta(days=i)
#      start = datetime.combine(date, datetime.min.time())
#      end = datetime.combine(date, datetime.max.time())
#      query = app_tables.customers.search(active_date=q.between(start, end))
#      count = len(query)
#      date_counts[date] = count
  
#    x = list(date_counts.keys())
#    y = list(date_counts.values())

#    primary_color = '#8fce00'
#    self.plot_1.data = go.Bar(x=x, y=y, marker=dict(color=primary_color),
#                              hovertemplate='<b>%{x}</b><br>' + 'New Customers: %{y}')
    # Configure the plot layout
#    self.plot_1.layout = {
#      'title': 'NEW CUSTOMERS PER DAY',
#      'xaxis': {
#        'title': 'TIME'
#      },
#      'yaxis': {
#        'title': 'CUSTOMERS'
#      }
#    } 
#    self.plot_1.layout.yaxis.title = 'CUSTOMERS' 
    
  def home_link_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Home', 0)

  def customers_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Customers')

  def last_3_days_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.range = 3
    self.last_3_days.background = '#8fce00'
    self.last_7_days.background = '#ffa500'
    self.last_14_days.background = '#ffa500'
    self.last_30_days.background = '#ffa500'
    self.last_60_days.background = '#ffa500'
    self.last_90_days.background = '#ffa500'
    self.plot_dt()

  def last_7_days_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.range = 7
    self.last_7_days.background = '#8fce00'
    self.last_3_days.background = '#ffa500'
    self.last_30_days.background = '#ffa500'
    self.last_14_days.background = '#ffa500'
    self.last_60_days.background = '#ffa500'
    self.last_90_days.background = '#ffa500'
    self.plot_dt()

  def last_14_days_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.range = 14
    self.last_14_days.background = '#8fce00'
    self.last_3_days.background = '#ffa500'
    self.last_30_days.background = '#ffa500'
    self.last_7_days.background = '#ffa500'
    self.last_60_days.background = '#ffa500'
    self.last_90_days.background = '#ffa500'
    self.plot_dt()

  def last_30_days_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.range = 30
    self.last_30_days.background = '#8fce00'
    self.last_3_days.background = '#ffa500'
    self.last_14_days.background = '#ffa500'
    self.last_7_days.background = '#ffa500'
    self.last_60_days.background = '#ffa500'
    self.last_90_days.background = '#ffa500'
    self.plot_dt()

  def request_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Request')

  def last_60_days_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.range = 60
    self.last_60_days.background = '#8fce00'
    self.last_30_days.background = '#ffa500'
    self.last_3_days.background = '#ffa500'
    self.last_14_days.background = '#ffa500'
    self.last_7_days.background = '#ffa500'
    self.last_90_days.background = '#ffa500'
    self.plot_dt()

  def last_90_days_click(self, **event_args):
    """This method is called when the button is clicked"""
    self.range = 90
    self.last_90_days.background = "#8fce00"
    self.last_60_days.background = '#ffa500'
    self.last_30_days.background = '#ffa500'
    self.last_3_days.background = '#ffa500'
    self.last_14_days.background = '#ffa500'
    self.last_7_days.background = '#ffa500'
    self.plot_dt()

  def home_link_copy_2_click(self, **event_args):
    """This method is called when the link is clicked"""
    c = confirm('Are you sure you want to logout?')
    if(c==True):
      open_form('Login')
    else:
      pass

  def home_link_copy_3_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Support')

  def transactions_click(self, **event_args):
    """This method is called when the link is clicked"""
    open_form('Transactions', True)

  def outlined_button_1_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Customers')

  def outlined_button_2_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Request')

  def outlined_button_4_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Support')

  def outlined_button_3_click(self, **event_args):
    """This method is called when the button is clicked"""
    open_form('Transactions', True)

  def home_customer_img_mouse_enter(self, x, y, **event_args):
    """This method is called when the mouse cursor enters this component"""
    bounce = Transition(translateY=[0, 0, "-30px", "-30px", 0, "-15px", 0, "-15px", 0], offset=[0, 0.2, 0.4, 0.43, 0.53, 0.7, 0.8, 0.9, 1])
    shake = Transition(translateX=[0] + ["10px", "-10px"] * 4 + [0])
    animate(self.home_customer_img, shake, duration=2000)

  def image_2_mouse_enter(self, x, y, **event_args):
    """This method is called when the mouse cursor enters this component"""
    bounce = Transition(translateY=[0, 0, "-30px", "-30px", 0, "-15px", 0, "-15px", 0], offset=[0, 0.2, 0.4, 0.43, 0.53, 0.7, 0.8, 0.9, 1])
    shake = Transition(translateX=[0] + ["10px", "-10px"] * 4 + [0])
    animate(self.image_2, shake, duration=2000)

  def image_3_mouse_enter(self, x, y, **event_args):
    """This method is called when the mouse cursor enters this component"""
    bounce = Transition(translateY=[0, 0, "-30px", "-30px", 0, "-15px", 0, "-15px", 0], offset=[0, 0.2, 0.4, 0.43, 0.53, 0.7, 0.8, 0.9, 1])
    shake = Transition(translateX=[0] + ["10px", "-10px"] * 4 + [0])
    animate(self.image_3, shake, duration=2000)

  def image_4_mouse_enter(self, x, y, **event_args):
    """This method is called when the mouse cursor enters this component"""
    bounce = Transition(translateY=[0, 0, "-30px", "-30px", 0, "-15px", 0, "-15px", 0], offset=[0, 0.2, 0.4, 0.43, 0.53, 0.7, 0.8, 0.9, 1])
    shake = Transition(translateX=[0] + ["10px", "-10px"] * 4 + [0])
    animate(self.image_4, shake, duration=2000)



















    
