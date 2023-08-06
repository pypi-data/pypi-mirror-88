# -*-coding: utf-8-*-
from __future__ import division

__version__ = '0.1.0'
__revision__ = None
__version_info__ = tuple([int(num) for num in __version__.split('.')])

'''
sdata examples 
'''

import sdata
data = sdata.Data(name="data", uuid="38b26864e7794f5182d38459bab85841")
data.metadata.add("my_key", 123, unit="m^3", description="a volume", label="V")
data.metadata.add("force", 1.234, unit="kN", description="x force", label="F_x")
data