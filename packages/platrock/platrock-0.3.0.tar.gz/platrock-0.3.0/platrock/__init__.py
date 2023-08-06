name = "platrock"

try:
	from . import TwoDShape
	SICONOS_FOUND = True
except:
	SICONOS_FOUND = False

import pkg_resources
version = pkg_resources.require("platrock")[0].version

#Defaults to False, will be eventually overriden in platrock-webui:
web_ui = False
