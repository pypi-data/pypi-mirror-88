"""
Copyright (c) 2017, 2018, 2019 Irstea
Copyright (c) 2017, 2018, 2019 François Kneib
Copyright (c) 2017, 2018, 2019 Franck Bourrier
Copyright (c) 2017, 2018, 2019 David Toe
Copyright (c) 2017, 2018, 2019 Frédéric Berger
Copyright (c) 2017, 2018, 2019 Stéphane Lambert

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
import copy


def from_terrain(terrain,cell_length,xllcorner=0,yllcorner=0):
	"""
	Create a new raster from the terrain only. /!\ if the terrain was generated from an asc, please use "from_asc" then "from_raster" to avoid shifting of the origin.
	"""
	r=Raster()
	xmin=terrain.points_as_array[:,0].min()
	xmax=terrain.points_as_array[:,0].max()
	ymin=terrain.points_as_array[:,1].min()
	ymax=terrain.points_as_array[:,1].max()
	r.cell_length=float(cell_length)
	r.X=np.arange(xmin,xmax+cell_length,cell_length)
	r.Y=np.arange(ymin,ymax+cell_length,cell_length)
	r.nx=len(r.X)
	r.ny=len(r.Y)
	r.xllcorner=xllcorner
	r.yllcorner=yllcorner
	return r

def from_raster(raster,cell_length=None):
	"""
	Copy a raster without the data, optionnaly change the cell_length (=remap the raster)
	"""
	r=copy.deepcopy(raster)
	r.data={}
	if(cell_length is not None and cell_length!=raster.cell_length):
		r.cell_length=cell_length
		r.X=np.arange(raster.X[0],raster.X[-1]+cell_length,cell_length)
		r.Y=np.arange(raster.Y[0],raster.Y[-1]+cell_length,cell_length)
		r.nx=len(r.X)
		r.ny=len(r.Y)
		if "Z" in raster.data.keys():
			from skimage.transform import resize
			r.data["Z"]=resize(raster.data["Z"],[r.nx,r.ny])
	elif "Z" in raster.data.keys():
		r.data["Z"]=copy.deepcopy(raster.data["Z"])
	return r

def from_asc(filename,data_name,header_lines_count=6):
	r=Raster()
	#LOAD FILE AND CREATE RASTER ARRAYS :
	#load header:
	r.header_data={"cellsize":None,"NODATA_value":None,"xllcorner":None,"yllcorner":None,"ncols":None,"nrows":None}
	with open(filename,'r') as f:
		for i in range(header_lines_count):
			data=f.readline().split()
			if data[0] in r.header_data:
				try:
					value=int(data[1])
				except:
					value=float(data[1])
				r.header_data[data[0]]=value
	r.cell_length=r.header_data["cellsize"]
	r.xllcorner=r.header_data["xllcorner"]
	r.yllcorner=r.header_data["yllcorner"]
	#load terrain:
	data = np.loadtxt(filename, skiprows=header_lines_count).T
	data = np.flip(data,axis=1) #numpy reads the file from top to bottom, but the origin of the ascii raster is at the bottom (right)
	r.nx=np.shape(data)[0]
	r.ny=np.shape(data)[1]
	r.X=np.arange(0,r.nx)*r.cell_length
	r.Y=np.arange(0,r.ny)*r.cell_length
	#store in raster data:
	r.data[data_name]=data
	return r
	
class Raster(object):
	def __init__(self):
		self.X=None
		self.Y=None
		self.nx=None
		self.ny=None
		self.cell_length=None
		self.xllcorner=None
		self.yllcorner=None
		self.data={}
	
	def get_indices_from_coords(self,coords):
		#coords must be np.array([x,y])
		indices_coords=(coords/self.cell_length).astype(int)					#indices of the cell ([xi,yi])
		return indices_coords
	
	def is_scalar_type(self,name):
		try:
			len(self.data[name][0,0])
			return False
		except Exception:
			return True
	
	def get_scalar_fields(self):
		return [f for f in self.data.keys() if self.is_scalar_type(f)]
	
	def get_vector_fields(self):
		return [f for f in self.data.keys() if not self.is_scalar_type(f)]
	
	def add_data_grid(self,name,type,default_value=0):
		self.data[name]=np.empty([self.nx,self.ny],dtype=type)
		if(type==list):
			for i in range(np.shape(self.data[name])[0]):
				for j in range(np.shape(self.data[name])[1]):
					self.data[name][i,j]=[]
		else:
			self.data[name].fill(default_value)
		return self.data[name]
	
	def get_asc_header_string(self):
		values={"ncols":int(self.nx),
				"nrows":int(self.ny),
				"xllcorner":int(self.xllcorner),
				"yllcorner":int(self.yllcorner),
				"cellsize":self.cell_length,
				"NODATA_value":self.header_data["NODATA_value"]
				}
		S=""
		for k in values:
			S+=str(k).ljust(14)+str(values[k])+"\n"
		return S
	
	def output_to_asc(self,output_to_string=False,fields=None):
		if not fields:
			fields=self.get_scalar_fields()
		class output_buff():
			def __init__(self):
				self.buff=""
			def write(self,what):
				self.buff+=what
			def __repr__(self):
				return self.buff

		outputs={}
		for fi in fields:
			if(output_to_string):
				outputs[fi]=output_buff()
			else:
				outputs[fi]=open(str(fi)+".asc",'w')
			outputs[fi].write(self.get_asc_header_string())
			np.savetxt(outputs[fi], np.flip(self.data[fi],axis=1).T, fmt="%.2f")	#flip and transpose to translate from numpy representation to ascii grid representation
			if(output_to_string):
				outputs[fi]=outputs[fi].buff
			else:
				outputs[fi].close()
		if(output_to_string):
			return outputs















