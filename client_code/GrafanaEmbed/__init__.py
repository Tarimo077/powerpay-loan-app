from ._anvil_designer import GrafanaEmbedTemplate
from anvil import *
import anvil.server
import anvil.google.auth, anvil.google.drive
from anvil.google.drive import app_files
import anvil.users
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
from IFrames.IFrame import IFrame

class GrafanaEmbed(GrafanaEmbedTemplate):
  def __init__(self, **properties):
    # Set Form properties and Data Bindings.
    self.init_components(**properties)
    self.i_frame_1._url = 'http://appliatrix.com/d-solo/c37c9493-5301-4cdf-86aa-9d4ee3d22a10/device-9?orgId=1&panelId=2 width="450" height="200" frameborder="0"'
    self.i_frame_1.url = 'http://appliatrix.com/d-solo/c37c9493-5301-4cdf-86aa-9d4ee3d22a10/device-9?orgId=1&panelId=2 width="450" height="200" frameborder="0"'

    # Any code you write here will run before the form opens.
