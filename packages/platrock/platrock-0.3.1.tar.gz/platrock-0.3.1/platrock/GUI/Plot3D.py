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
import matplotlib as mpl
import platrock
from descartes import PolygonPatch
import plotly.offline as plyo
import plotly.graph_objs as plygo
import platrock.Common.ColorPalettes as cp
import shapely

import matplotlib as mpl
if platrock.web_ui:
	mpl.use('Agg')
	#import plotly as ply
import matplotlib.pyplot as plt
if not platrock.web_ui: plt.ion()

mpl.rcParams["figure.subplot.bottom"]=0.05
mpl.rcParams["figure.subplot.top"]=0.95
mpl.rcParams["figure.subplot.left"]=0.0
mpl.rcParams["figure.subplot.right"]=0.92

fig=plt.figure("PlatRock Raster View",facecolor="w",edgecolor="w")
ax=plt.axes()

def clear():
	global fig,ax
	plt.close("all")
	fig=plt.figure("PlatRock Raster View",facecolor="w",edgecolor="w")
	ax=plt.axes()

def shaded_raster_from_z_raster(z_raster):
	azimuth=315
	angle_altitude=45
	x, y = np.gradient(z_raster.data["Z"].transpose())
	X,Y=np.meshgrid(z_raster.X, z_raster.Y)
	slope = np.pi/2. - np.arctan(np.sqrt(x*x + y*y))
	aspect = np.arctan2(-x, y)
	azimuthrad = azimuth*np.pi / 180.
	altituderad = angle_altitude*np.pi / 180.
	shaded = np.sin(altituderad) * np.sin(slope)\
	+ np.cos(altituderad) * np.cos(slope)\
	* np.cos(azimuthrad - aspect)
	return shaded

def draw_terrain(s, with_polygons=False):
	terrain=s.terrain
	
	#1- background raster:
	raster=s.pp.raster
	X,Y=np.meshgrid(raster.X, raster.Y)
	shaded=shaded_raster_from_z_raster(raster)
	plt.pcolormesh(X,Y,255*(shaded + 1)/2,cmap='Greys',rasterized=True)
	
	if(with_polygons):
		#4- terrain polygons
		for soil_param_set in terrain.soil_params:
			if not s.terrain._geojson_polygon_soil_offset_applied:
				poly=shapely.affinity.translate(soil_param_set["shapely_polygon"],xoff=-raster.xllcorner,yoff=-raster.yllcorner)
			else:
				poly=soil_param_set["shapely_polygon"]
			ax.add_patch(PolygonPatch(poly,facecolor=np.append(soil_param_set["color"]/255,0.65),edgecolor=soil_param_set["color"][0:3]/255,linewidth=1.5))
		
		#3- rocks start positions:
		for start_param_set in s.rocks_start_params:
			if not s._geojson_polygon_offset_applied:
				poly=shapely.affinity.translate(start_param_set["shapely_polygon"],xoff=-raster.xllcorner,yoff=-raster.yllcorner)
			else:
				poly=start_param_set["shapely_polygon"]
			ax.add_patch(PolygonPatch(poly,facecolor=np.append(start_param_set["color"]/255,0.65),edgecolor="black",linewidth=1))
	
	fig.set_size_inches(3+1,3*raster.data["Z"].shape[1]/raster.data["Z"].shape[0])
	ax.set_aspect("equal")
	fig.canvas.draw()
	

def draw_forest(terrain):
	from matplotlib import patches
	#ax.plot(terrain.trees_as_array[:,0],terrain.trees_as_array[:,1],"o",color="green")
	for t in terrain.trees_as_array:
		ax.add_patch(patches.Circle(t[0:2],t[2]/100,fc="green"))
	fig.canvas.draw()

def plot_checkpoints(s):
	for chkP in s.checkpoints:
		path=chkP.path-[s.pp.raster.xllcorner,s.pp.raster.yllcorner]
		ax.plot(path[:,0],path[:,1],lw=3,alpha=0.75,color="red")
	fig.canvas.draw()

def draw_rocks_count(raster):
	data=raster.data['crossings']
	#use masked array to set a "bad" value to the cmap. It allows to set the cmap to fully transparent when crossings==0
	masked_array = np.ma.array (data, mask=(data==raster.header_data["NODATA_value"]))
	cmap = mpl.cm.jet
	cmap.set_bad('gray',0.)	#gray color but opacity=0
	x,y=np.meshgrid(raster.X, raster.Y,indexing="ij")
	cm=ax.pcolormesh(x,y,masked_array,cmap=cmap,zorder=1)
	ax.set_title("Nombre de passages")
	cbar=plt.colorbar(cm,aspect=30)
	cbar.set_label("# passages")
	ax.set_aspect("equal")
	fig.canvas.draw()

def draw_mean_vel(raster):
	data=raster.data['vels_mean']
	#use masked array to set a "bad" value to the cmap. It allows to set the cmap to fully transparent when vel==0
	masked_array = np.ma.array(data, mask=(data==raster.header_data["NODATA_value"]))
	cmap = mpl.cm.jet
	cmap.set_bad('gray',0.)	#gray color but opacity=0
	x,y=np.meshgrid(raster.X, raster.Y,indexing="ij")
	cm=ax.pcolormesh(x,y,masked_array,cmap=cmap,zorder=1)
	ax.set_title("Vitesses moyennes")
	cbar=plt.colorbar(cm,aspect=30)
	cbar.set_label("$[m.s^{-1}]$")
	ax.set_aspect("equal")
	fig.canvas.draw()

def draw_mean_Ec(raster):
	data=raster.data['Ec_mean']/1000.
	#use masked array to set a "bad" value to the cmap. It allows to set the cmap to fully transparent when vel==0
	masked_array = np.ma.array (data, mask=(data==raster.header_data["NODATA_value"]))
	cmap = mpl.cm.jet
	cmap.set_bad('gray',0.)	#gray color but opacity=0
	x,y=np.meshgrid(raster.X, raster.Y,indexing="ij")
	cm=ax.pcolormesh(x,y,masked_array,cmap=cmap,zorder=1)
	ax.set_title("Énergie cinétique moyenne")
	cbar=plt.colorbar(cm,aspect=30)
	cbar.set_label("$[kJ]$")
	ax.set_aspect("equal")
	fig.canvas.draw()

def draw_number_of_source_cells(raster):
	data=raster.data['number_of_source-cells']
	#use masked array to set a "bad" value to the cmap. It allows to set the cmap to fully transparent when vel==0
	masked_array = np.ma.array (data, mask=(data==raster.header_data["NODATA_value"]))
	cmap = mpl.cm.jet
	cmap.set_bad('gray',0.)	#gray color but opacity=0
	x,y=np.meshgrid(raster.X, raster.Y,indexing="ij")
	cm=ax.pcolormesh(x,y,masked_array,cmap=cmap,zorder=1)
	ax.set_title("Nombre de cellules source")
	cbar=plt.colorbar(cm,aspect=30)
	cbar.set_label("$Number$")
	ax.set_aspect("equal")
	fig.canvas.draw()

def draw_rocks_trajectories(s,rocks_ids):
	for rock_nb in rocks_ids:
		draw_rock_trajectory(s,rock_nb,draw=False)
	fig.canvas.draw()
			
def draw_rock_trajectory(s,nb,draw=True,use_plotly=False):
	pos=s.output.get_contacts_pos(nb)
	if use_plotly:
		return pos[:,0],pos[:,1]
	else:
		ax.plot(pos[:,0],pos[:,1],'-',ms=0.5,lw=1.5,zorder=99)
		if draw:
			fig.canvas.draw()

def draw_sample_trajectories(s,nb=50,use_plotly=False):
	rocks_to_plot=[]
	if(nb>=s.nb_rocks):
		rocks_to_plot=range(s.nb_rocks)
	else:
		rocks_to_plot=np.linspace(0,s.nb_rocks-1,nb,dtype=int)
	if not use_plotly:
		draw_rocks_trajectories(s,rocks_to_plot)
	else:
		#this will create [ [X_r1,Y_r1,Z_r1], [X_r2,Y_r2,Z_r2] ...]
		return [ draw_rock_trajectory(s,i,use_plotly=True) for i in rocks_to_plot ]

def get_plotly_raw_html(s, sample_trajectories=False):
	#0- Initialize the lists
	data = []
	shapes = []
	updatemenus=[]
	
	#1- plot the terrain:
	shaded=shaded_raster_from_z_raster(s.terrain.Z_raster)
	shaded[s.terrain.Z_raster.data["Z"].transpose()==s.terrain.Z_raster.header_data["NODATA_value"]]=None
	terrain=plygo.Heatmap(
		name="terrain",
		z=shaded,
		x=s.terrain.Z_raster.X+s.terrain.Z_raster.cell_length/2, #plotly centers the square cells on (x,y) but we want bottom-left to be centered on (x,y).
		y=s.terrain.Z_raster.Y+s.terrain.Z_raster.cell_length/2, #plotly centers the square cells on (x,y) but we want bottom-left to be centered on (x,y).
		autocolorscale=False,
		colorscale="gray",
		hoverongaps=False,
		hoverinfo='skip', #dont show datapoints on mouse over
		showscale=False,
	)
	data.append(terrain)
	
	#2- Parameters polygons
		# terrain params
	polygons_id_start=len(data)
	for param_set_number,soil_param_set in enumerate(s.terrain.soil_params):
		polygons=soil_param_set["shapely_polygon"]
		multiPoly=True
		if isinstance(polygons,shapely.geometry.Polygon): #to handle polygons and multipolygons
			polygons=[polygons]
			multiPoly=True
		for polygon_number,p in enumerate(polygons):
			if not s.terrain._geojson_polygon_soil_offset_applied:
				p=shapely.affinity.translate(p,xoff=-s.terrain.Z_raster.xllcorner,yoff=-s.terrain.Z_raster.yllcorner)
			data.append(
				plygo.Scatter(
					name="Soil zone "+str(param_set_number),
					x=list(p.exterior.xy[0]),
					y=list(p.exterior.xy[1]),
					mode='lines',
					text=soil_param_set["params"].__repr__().replace("'","").replace("{","").replace("}","").replace(", ","<br>"),
					fill="toself",
					line=dict(
						color=cp.color_to_html(soil_param_set["color"]),
						width=2
					),
					fillcolor=cp.color_to_html(soil_param_set["color"],0.65),
					legendgroup="Soil zone "+str(param_set_number),
					showlegend=True if polygon_number==0 else False
				)
			)
		# forest params
	for param_set_number,forest_param_set in enumerate(s.terrain.forest_params):
		polygons=forest_param_set["shapely_polygon"]
		multiPoly=True
		if isinstance(polygons,shapely.geometry.Polygon): #to handle polygons and multipolygons
			polygons=[polygons]
			multiPoly=True
		for polygon_number,p in enumerate(polygons):
			if not s.terrain._forest_offset_applied:
				p=shapely.affinity.translate(p,xoff=-s.terrain.Z_raster.xllcorner,yoff=-s.terrain.Z_raster.yllcorner)
			data.append(
				plygo.Scatter(
					name="Forest zone "+str(param_set_number),
					x=list(p.exterior.xy[0]),
					y=list(p.exterior.xy[1]),
					mode='lines',
					text=forest_param_set["params"].__repr__().replace("'","").replace("{","").replace("}","").replace(", ","<br>"),
					line=dict(
						color=cp.color_to_html(forest_param_set["color"]),
						width=2,
						dash='dot',
					),
					legendgroup="Forest zone "+str(param_set_number),
					showlegend=True if polygon_number==0 else False
				)
			)
	
		# rocks start params:
	for param_set_number,start_param_set in enumerate(s.rocks_start_params):
		polygons=start_param_set["shapely_polygon"]
		multiPoly=True
		if isinstance(polygons,shapely.geometry.Polygon): #to handle polygons and multipolygons
			polygons=[polygons]
			multiPoly=True
		for polygon_number,p in enumerate(polygons):
			if not s.terrain._geojson_polygon_soil_offset_applied:
				p=shapely.affinity.translate(p,xoff=-s.terrain.Z_raster.xllcorner,yoff=-s.terrain.Z_raster.yllcorner)
			data.append(
				plygo.Scatter(
					name="Start zone "+str(param_set_number),
					x=list(p.exterior.xy[0]),
					y=list(p.exterior.xy[1]),
					mode='lines',
					fill="toself",
					line=dict(
						color="black",
						width=1
					),
					fillcolor=cp.color_to_html(start_param_set["color"],0.65),
					legendgroup="Start Zone "+str(param_set_number),
					showlegend=True if polygon_number==0 else False
				)
			)

	polygons_id_end=len(data)-1
	updatemenus.append(dict(
		type="buttons",
		showactive=True,
		x=1.01,
		xanchor="left",
		y=1,
		yanchor="top",
		buttons=[
			dict(
				method="restyle",
				label="hide/show zones",
				args2=[{"visible":"legendonly"},list(range(polygons_id_start,polygons_id_end+1))],
				args=[{"visible":True},list(range(polygons_id_start,polygons_id_end+1))],
			)
		]
	))
	#3- plot the checkpoints:
	i=1
	for chkP in s.checkpoints:
		path=chkP.path-[s.terrain.Z_raster.xllcorner,s.terrain.Z_raster.yllcorner]
		hovertext=""
		if(sample_trajectories and len(chkP.vels)>0):
			hovertext="Crossings ratio: "+str(round(chkP.crossings_ratio*100,1))+"%<br>Mean height: "+str(round((np.asarray(chkP.pos)[:,2].mean()),2))+"m<br>Mean vel: "+str(round((np.linalg.norm(np.asarray(chkP.vels),axis=1).mean()),2))+"m/s"
		ax.plot(path[:,0],path[:,1],lw=3,alpha=0.75,color="red")
		data.append(
			plygo.Scatter(
				x=path[:,0],
				y=path[:,1],
				mode='lines+markers',
				line=dict(
					color="rgba(255,0,0,0.5)",
					width=4
				),
				hoverinfo='text+name', #dont show datapoints on mouse over
				hovertext=hovertext,
				name='Checkpoint '+str(i),
				showlegend=False,
			)
		)
		i+=1
	
	#4- plot sample trajectories:
	if(sample_trajectories):
		rocks_data = draw_sample_trajectories(s,nb=sample_trajectories, use_plotly=True)
		i=0
		for rock_data in rocks_data:
			i+=1
			color=s.random_generator.randint(255,size=3)
			color="rgb("+",".join(color.astype(str))+")"
			data.append(
				plygo.Scatter(
					name="rock n°"+str(i),
					x=rock_data[0],
					y=rock_data[1],
					mode = 'lines',
					line=dict(
						color=color,
						width=1
					),
					hoverinfo='skip', #dont show datapoints on mouse over
					showlegend=False,
				)
			)
	
	#5- optionnaly show trees:
	if len(s.terrain.trees):
		kwargs = {'type': 'circle', 'xref': 'x', 'yref': 'y', 'fillcolor': 'green', "line_width":0}
		shapes += [plygo.layout.Shape(x0=t[0]-t[2]/2/100., y0=t[1]-t[2]/2/100., x1=t[0]+t[2]/2/100., y1=t[1]+t[2]/2/100., **kwargs) for t in s.terrain.trees_as_array]
		
	#6- optionnaly show raster fields results:
	if s.pp and s.pp.has_run:
		fields=s.pp.raster.get_scalar_fields()
		if "Z" in fields: fields.remove("Z")
		cross=s.pp.raster.data["crossings"].astype(float) #data must be float, not int
		cross[cross==float(s.pp.raster.header_data["NODATA_value"])]=None #set nan where we have no data instead of the raster nodata.
		field_plot=plygo.Heatmap(
			name="Crossings",
			z=cross.transpose(),
			x=s.pp.raster.X+s.pp.raster.cell_length/2, #plotly centers the square cells on (x,y) but we want bottom-left to be centered on (x,y).
			y=s.pp.raster.Y+s.pp.raster.cell_length/2, #plotly centers the square cells on (x,y) but we want bottom-left to be centered on (x,y).
			showscale=True,
			colorscale="Burg",
			colorbar=dict(
				x= -0.02,
				xanchor="right",
				xpad=30,
				len= 0.5,
			),
			zmin=0,
			zmax=cross.max(initial=0,where=np.isfinite(cross)),
			zauto=False,
			visible=True,
			hoverongaps=False,
		)
		data.append(field_plot)
		field_plot_id=len(data)-1
		buttons=[]
		for field in fields:
			field_z=s.pp.raster.data[field].astype(float) #data must be float, not int
			field_z[field_z==float(s.pp.raster.header_data["NODATA_value"])]=None #set nan where we have no data instead of the raster nodata.
			zmin=0
			zmax=field_z.max(initial=0,where=np.isfinite(field_z))
			buttons.append(dict(
				method="restyle",
				label=field.capitalize(),
				args=[{"name":field.capitalize(),"visible":True,"z":[field_z.transpose()],"zmin":[zmin],"zmax":[zmax]},[field_plot_id]]
			))
		buttons.append(dict(method='restyle',label='None',args=[{"visible":False},[field_plot_id]]))
		updatemenus.append(dict(buttons=buttons))
	layout = plygo.Layout(
		updatemenus=updatemenus,
		autosize=False,
		width=1000,
		height=800,
		margin=plygo.layout.Margin(
			l=40,
			r=10,
			b=20,
			t=30,
			pad=4
		),
		xaxis = dict(
			#nticks = 10,
			linecolor= 'black',
			mirror=True,
			showgrid=True,
			range = [s.terrain.Z_raster.X[0],s.terrain.Z_raster.X[-1]+s.terrain.Z_raster.cell_length],
			zeroline=False,
		),
		yaxis = dict(
			linecolor= 'black',
			mirror=True,
			showgrid=True,
			zeroline=False,
			scaleanchor = "x", #to make 1:1 scale
			range = [s.terrain.Z_raster.Y[0],s.terrain.Z_raster.Y[-1]+s.terrain.Z_raster.cell_length],
		),
		legend = dict(
			y = 0.95,
		),
		#showlegend= False,
		hovermode = 'closest',
		shapes=shapes,
		#annotations=annotations,
	)
		
	#5- configure plotly menubar:
	config = dict(
		modeBarButtonsToRemove = ["hoverCompareCartesian","hoverClosestCartesian","select2d","lasso2d"],
		displaylogo = False,
		displayModeBar = True,
	)
	
	ply_fig = plygo.Figure(data=data, layout=layout)
	return plyo.plot(ply_fig, config=config, show_link=False, output_type="div", include_plotlyjs=False)

#BETA 3D display:
def get_plotly_raw_html_3D(s, sample_trajectories=False):
	#Initialize the lists
	data = []
	annotations = []
	
	x=[]
	y=[]
	z=[]
	I=[]
	J=[]
	K=[]
	s.before_run_tasks()
	for p in s.terrain.points:
		x.append(p.pos[0])
		y.append(p.pos[1])
		z.append(p.pos[2])
	for f in s.terrain.faces:
		I.append(f.points[0].id-1)
		J.append(f.points[1].id-1)
		K.append(f.points[1].id-1)
		
	triangles=plygo.Mesh3d(
		x=x,
		y=y,
		z=z,
		hoverinfo='skip'
		#facecolor="rgb(255, 0,0)",
		#i=I,
		#j=J,
		#k=K,
		#name=''
	)
	data.append(triangles)
	axis = dict(
		showbackground=True,
		backgroundcolor="rgb(230, 230,230)",
		gridcolor="rgb(255, 255, 255)",
		zerolinecolor="rgb(255, 255, 255)",
    )
	#4- Configure layout (axes, etc...):
	layout = plygo.Layout(
		autosize=False,
		width=1000,
		height=800,
		margin=plygo.layout.Margin(
			l=40,
			r=10,
			b=20,
			t=30,
			pad=4
		),
		scene=dict(
			xaxis=dict(axis),
			yaxis=dict(axis),
			zaxis=dict(axis),
			#aspectratio=dict(
				#x=1,
				#y=1,
				#z=0.5
			#)
		),
		showlegend= False,
		#hovermode = 'closest',
		#annotations=annotations,
	)
	
	#5- configure plotly menubar:
	config = dict(
		modeBarButtonsToRemove = ["autoScale2d","toggleSpikelines","hoverCompareCartesian","hoverClosestCartesian","select2d","lasso2d"],
		displaylogo = False,
		displayModeBar = True,
	)
	
	#6- Generate plotly html/js:
	ply_fig = plygo.Figure(data=data, layout=layout)
	return plyo.plot(ply_fig, config=config, show_link=False, output_type="div", include_plotlyjs=False)




