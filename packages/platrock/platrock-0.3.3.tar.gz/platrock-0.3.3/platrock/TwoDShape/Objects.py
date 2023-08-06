"""
Copyright (c) 2019 François Kneib
Copyright (c) 2019 Franck Bourrier
Copyright (c) 2019 David Toe
Copyright (c) 2019 Frédéric Berger
Copyright (c) 2019 Stéphane Lambert

This file is part of PlatRock.

PlatRock is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, version 3 of the License.

PlatRock is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with Foobar. If not, see <http://www.gnu.org/licenses/>.
"""

import numpy as np
import platrock.TwoD.Objects
from  platrock.Common.PyUtils import FriendImporter
import platrock.Common.Math as Math
from siconos.mechanics.collision import SiconosConvexHull2d

class Rock(FriendImporter):
	friendClass=platrock.TwoD.Objects.Rock
	friendImportNames=[	
		"pos",
		"vel",
		"angVel",
		"mass",
		"I",
		"density",
		"is_stopped",
		"current_segment",
		"flying_direction",
		"color",
		"out_of_bounds",
		"update_current_segment",
		"setup_kinematics",
	]
	valid_shape_params=np.array([
		["aspect_ratio",	"Aspect ratio",			float,	1,		10,	2]
	])
	def __init__(self,**kwargs):
		for param_name in self.valid_shape_params[:,0]:
			self.__dict__[param_name]=kwargs.pop(param_name)
		FriendImporter.__init__(self)
		self.__base_vertices__=None
		self.__base_inertia__=None #inertia corresponding to a volume of 1 and a density of 1
		self.__base_ly__=None #the third dimension, equal to the dimension in the Z axis for a volume of 1
		self.vertices=None
		self.ly=None
		
	"""
	This method is called right after shape vertex definition. Its goal is to modify the shape so that it fits PlatRock convention :
	- the __base_vertices__ must be sorted in polar coord system (use Math.sort_2d_polygon_vertices)
	- the corresponding polygon COG must be at (0,0) (use Math.center_2d_polygon_vertices)
	- the polygon volume must be ==1
	- the __base_inertia__ is computed for volume=1 and density=1
	"""
	def __normalize_shape__(self):
		#Cleanup vertices:
		Math.sort_2d_polygon_vertices(self.__base_vertices__)
		Math.center_2d_polygon_vertices(self.__base_vertices__)
		#The following line normalizes the __base volume (V==1) and the density (=1), then computes everything for the __base solid
		self.set_volume(1.,modify_base_shape=True)
	
	"""
	Homothetic transform of the rock, with modification of all geometrical and physical quantities
	It uses the __base*__ normalized solid to fastly apply the changes, so only set modify_base_shape to True at rock instanciation for normalization purpose.
	"""
	def set_volume(self,dest_vol,modify_base_shape=False):
		if modify_base_shape: #only at rock instanciation
			start_area,self.__base_inertia__ = Math.get_2D_polygon_area_inertia(self.__base_vertices__,1.,cog_centered=True) #assume 2D density=1 for now, so inertia will be computed later as its proportionnal to density
			self.__base_inertia__*=self.__base_ly__ #now we switch to 3D density=1
			start_volume=start_area*self.__base_ly__
		else:
			start_volume=1# we assume that the __base volume is 1
		vol_factor=dest_vol/start_volume
		coord_factor=vol_factor**(1/3)
		if modify_base_shape: #this will be run at instanciation
			self.__base_vertices__*=coord_factor
			self.__base_ly__*=coord_factor
			self.__base_inertia__*=coord_factor**5
		else: # this will be run before rock launch
			self.volume=dest_vol
			self.vertices=self.__base_vertices__*coord_factor
			self.ly=self.__base_ly__*coord_factor
			self.I=self.__base_inertia__*coord_factor**5*self.density
			self.mass=self.volume*self.density
			self.dims = [	self.vertices[:,0].max() - self.vertices[:,0].min(),
							self.vertices[:,1].max() - self.vertices[:,1].min()]
		
	def get_siconos_shape(self):
		siconos_shape=SiconosConvexHull2d(self.vertices)
		siconos_shape.setInsideMargin(min(self.dims)*0.02)
		siconos_shape.setOutsideMargin(0)
		return siconos_shape

"""
NOTE: in all the shapes below, the output (=self.__base_vertices__) is supposed to be a list of vertices with the following characteristics:
- for aspect_ratio > 1, the larger dimension must be along X
"""
class Rectangle(Rock):
	def __init__(self,**kwargs):
		super(Rectangle,self).__init__(**kwargs)
		#Start with a rectangle of size along x == 1, centered at (0,0)
		Lx=1
		Lz=Lx/self.aspect_ratio
		self.__base_vertices__=np.array([[-Lx/2, -Lz/2], [Lx/2, -Lz/2], [Lx/2, Lz/2], [-Lx/2, Lz/2]])
		#Set the last (virtual) dimension to the smallest one (so the one along Z)
		self.__base_ly__=Lz
		self.__normalize_shape__()

class Ellipse(Rock):
	valid_shape_params=np.append(Rock.valid_shape_params,np.array([["nbPts",	"Number of points",	int,3,100,10]]),axis=0)
	def __init__(self,**kwargs):
		super(Ellipse,self).__init__(**kwargs)
		Lx=1
		Lz=Lx/self.aspect_ratio
		t=np.linspace(0,np.pi*2,self.nbPts+1)[:-1]
		self.__base_vertices__=np.array([Lx/2.*np.cos(t) , Lz/2.*np.sin(t)]).transpose()
		self.__base_ly__=self.__base_vertices__[:,1].max()-self.__base_vertices__[:,1].min()
		self.__normalize_shape__()

class Random(Rock):
	valid_shape_params=np.append(Rock.valid_shape_params,np.array([["nbPts",	"Number of points",	int,3,100,10]]),axis=0)
	def __init__(self,**kwargs):
		super().__init__(**kwargs)
		Lx=1
		Lz=Lx/self.aspect_ratio
		self.__base_vertices__=Math.get_random_convex_polygon(self.nbPts,Lx,Lz)
		self.__base_ly__=Lz
		self.__normalize_shape__()

Contact=platrock.TwoD.Objects.Contact
ParamsDict=platrock.TwoD.Objects.ParamsDict
ParamsZone=platrock.TwoD.Objects.ParamsZone

class Segment(FriendImporter):
	friendClass=platrock.TwoD.Objects.Segment
	friendImportNames=[	
		"points",
		"set_geometrical_quantities",
		"get_y",
	]
	
	def __init__(self,start_point,end_point,e=0.5,mu=0.3,mu_r=0.5):
		FriendImporter.__init__(self,start_point,end_point)
		self.e=e
		self.mu=mu
		self.mu_r=mu_r
		self.set_geometrical_quantities()

class Terrain(platrock.TwoD.Objects.Terrain):
	valid_input_attrs=np.array([	["e",		"e",				float,	0,		1.	],
									["mu",		"μ",				float,	0,		100.	],
									["mu_r",	"μ<sub>r</sub>",	float,	0,		100.	]])
	def __init__(self,file=None):
		super(Terrain,self).__init__(file,segments_type=Segment)
		del self.rebound_models_available
	
	def check_segments_parameters_consistency(self):
		pass

























