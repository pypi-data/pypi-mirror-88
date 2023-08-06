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

#cython: language_level=3, boundscheck=False, wraparound=False
#add ", profile=True" to the above line to activate cython profiling.

from numpy cimport ndarray
cimport numpy as np
cimport cython

from libc.math cimport sqrt
import platrock.ThreeD.Objects as Objects

cdef double squared_norm3(double* A):
	return A[0]**2+A[1]**2+A[2]**2

cdef double norm3(double* A):
	return sqrt(squared_norm3(A))

cdef double dot3(double* A, double* B):
	cdef double result
	result = A[0]*B[0]+A[1]*B[1]+A[2]*B[2]
	return result

#NOTE: commented as unused
#cdef double dot2(double* A, double* B):
	#cdef double result
	#result = A[0]*B[0]+A[1]*B[1]
	#return result

cdef double* cross3(double* A, double* B, double* out):
	out[0]=A[1]*B[2]-A[2]*B[1]
	out[1]=A[2]*B[0]-A[0]*B[2]
	out[2]=A[0]*B[1]-A[1]*B[0]
	return out

cdef double cross2(double* A, double *B):
	return A[0]*B[1]-A[1]*B[0]

cdef double* sub2(double* A, double* B, double* out):
	for i in range(2):
		out[i]=A[i]-B[i]
	return out

cdef double* sub3(double* A, double* B, double* out):
	for i in range(3):
		out[i]=A[i]-B[i]
	return out

cdef double* add3(double* A, double* B, double* out):
	for i in range(3):
		out[i]=A[i]+B[i]
	return out

cdef double* mult_s3(double A, double* B, double* out):
	for i in range(3):
		out[i]=A*B[i]
	return out

cdef bint is_point_inside_3D(double* p0, double* p1, double* p2, double* n ,double* p):
	cdef double[3] point_on_face
	sub3(p, mult_s3(dot3(sub3(p,p0,point_on_face),n),n,point_on_face),point_on_face)	#compute point_on_face
	cdef double[3] buff_1, buff_2, buff_3
	cdef double cp1 = dot3( cross3(sub3(p1,p0,buff_1), sub3(point_on_face,p0,buff_2),buff_3), n)
	cdef double cp2 = dot3( cross3(sub3(p2,p1,buff_1), sub3(point_on_face,p1,buff_2),buff_3), n)
	cdef double cp3 = dot3( cross3(sub3(p0,p2,buff_1), sub3(point_on_face,p2,buff_2),buff_3), n)
	cdef bint result = ((cp1>0 and cp2>0 and cp3>0) or (cp1<0 and cp2<0 and cp3<0))
	return result

cdef bint is_point_inside_2D(double* p0, double* p1, double* p2, double* n ,double* p):
	cdef double[2] point_xy = [p[0],p[1]]
	cdef double[2] buff_1, buff_2
	cdef double cp1 = cross2(sub2(p1,p0,buff_1), sub2(point_xy,p0,buff_2))
	cdef double cp2 = cross2(sub2(p2,p1,buff_1), sub2(point_xy,p1,buff_2))
	cdef double cp3 = cross2(sub2(p0,p2,buff_1), sub2(point_xy,p2,buff_2))
	cdef bint result = ((cp1>0 and cp2>0 and cp3>0) or (cp1<0 and cp2<0 and cp3<0))
	return result

def verlet_run(Verlet_update_instance,s):
	r=s.current_rock
	
	cdef double r_radius = r.radius
	cdef double bb_half_length = r.bounding_box.half_length
	cdef double[3] r_pos = r.pos
	cdef double[3] bb_pos = r.bounding_box.pos
	cdef int i #counters
	
	#1-DO WE HAVE TO UPDATE THE VERLET LIST ?
	if( not(
			(r_pos[0]-r_radius*1.1<bb_pos[0]-bb_half_length) or
			(r_pos[1]-r_radius*1.1<bb_pos[1]-bb_half_length) or
			(r_pos[2]-r_radius*1.1<bb_pos[2]-bb_half_length) or
			(r_pos[0]+r_radius*1.1>bb_pos[0]+bb_half_length) or
			(r_pos[1]+r_radius*1.1>bb_pos[1]+bb_half_length) or
			(r_pos[2]+r_radius*1.1>bb_pos[2]+bb_half_length)
		)
	):return

	
	#2-UPDATE THE BOUNDING BOX PROPERTIES
	r.bounding_box.half_length=Verlet_update_instance.dist_factor*r.radius
	bb_half_length = r.bounding_box.half_length
	r.bounding_box.pos[:]=r.pos[:]
	bb_pos=r.bounding_box.pos
	
	#3-GET THE FACES OF TERRAIN THAT HAVE AT LEAST ONE POINT IN THE BOUNDING SPHERE
	cdef int size = s.terrain.faces_xyz_bb.shape[0]
	cdef double[:,:] faces_bb_min_max_mv = s.terrain.faces_xyz_bb
	r.verlet_faces_list=[]
	for i in range(size):
		outside=(	(bb_pos[0]+bb_half_length<faces_bb_min_max_mv[i,0]) or
					(bb_pos[1]+bb_half_length<faces_bb_min_max_mv[i,2]) or
					(bb_pos[2]+bb_half_length<faces_bb_min_max_mv[i,4]) or
					(bb_pos[0]-bb_half_length>faces_bb_min_max_mv[i,1]) or
					(bb_pos[1]-bb_half_length>faces_bb_min_max_mv[i,3]) or
					(bb_pos[2]-bb_half_length>faces_bb_min_max_mv[i,5])
				)
		if(not outside):r.verlet_faces_list.append(s.terrain.faces[i])
	
	#4-GET THE TREES OF TERRAIN THAT ARE IN THE BOUNDING SPHERE
	cdef double[:,:] trees_mv
	if(s.enable_forest):
		trees_mv = s.terrain.trees_as_array
		size = s.terrain.trees_as_array.shape[0]
		r.verlet_trees_list=[]
		for i in range(size):
			if( (trees_mv[i,0]-r_pos[0])**2 + (trees_mv[i,1]-r_pos[1])**2 <  (bb_half_length - trees_mv[i,2]/2)**2 ):
				r.verlet_trees_list.append(s.terrain.trees[i])


def contacts_detector_run(self,s):	#for sphere only !
		
		# ROCK-TERRAIN :
		r=s.current_rock
		r.terrain_active_contact = None
		cdef double r_radius = r.radius
		cdef double face_candidate_dist = 1e10
		cdef double[3] r_pos = r.pos
		cdef double[3] r_vel = r.vel
		cdef double[3] face_normal, branch, edge, proj
		cdef double[3][3] face_pts
		cdef double[3] buff
		cdef double proj_coef
		cdef int nb_faces = len(r.verlet_faces_list)
		cdef int pi,i,fi #counters
		cdef int face_contact_indice = -1
		cdef double dist
		cdef bint found_edge_contact = False
		
		for fi in range(nb_faces):
			for i in range(3):
				face_pts[i] = r.verlet_faces_list[fi].points[i].pos
			face_normal = r.verlet_faces_list[fi].normal
			dist=dot3( face_normal,sub3( r_pos,face_pts[0],buff ) )-r_radius
			if(dist>0): # no penetration with the plan : no contact
				continue
			#if(dot3(r_vel,face_normal)>0):
				#continue
			if(is_point_inside_3D(face_pts[0], face_pts[1], face_pts[2], face_normal,r_pos)):
				if(dist<face_candidate_dist):
					face_contact_indice=fi
					face_candidate_dist=dist
				continue
			found_edge_contact=False
			for pi in range(-1,2):
				branch=sub3(r_pos,face_pts[pi],buff)
				edge=sub3(face_pts[pi+1],face_pts[pi],buff)
				proj_coef=dot3(branch,edge)/squared_norm3(branch)
				if(proj_coef>1 or proj_coef<0):continue
				proj=mult_s3(proj_coef,edge,buff)
				dist=norm3(sub3(branch,proj,buff))-r_radius
				if(dist<face_candidate_dist):
					face_contact_indice=fi
					face_candidate_dist=dist
					found_edge_contact=1
			if(found_edge_contact):continue
			for pi in range(3):
				dist=norm3(sub3(face_pts[pi],r_pos,buff))-r_radius
				if(dist<face_candidate_dist):
					#this is currently the best candidate
					face_contact_indice=fi
					face_candidate_dist=dist
		if(face_candidate_dist<0):
			r.terrain_active_contact = Objects.Rock_terrain_contact(r.points[0],r.verlet_faces_list[face_contact_indice])
			r.terrain_active_contact.dist=face_candidate_dist
		
		# ROCK - TREES :
		cdef double[2] tree_pos
		cdef double tree_dhp
		cdef bint tree_active
		if(s.enable_forest):
			r.tree_active_contact=None
			size = len(r.verlet_trees_list)
			for fi in range(size):
				tree_active = r.verlet_trees_list[fi].active
				if(tree_active):
					tree_pos = r.verlet_trees_list[fi].pos
					tree_dhp = r.verlet_trees_list[fi].dhp
					dist=(tree_pos[0]-r_pos[0])**2 + (tree_pos[1]-r_pos[1])**2	#NOTE: this is not the real dist
					if( dist < (r_radius+tree_dhp/2/100)**2 ):
						r.tree_active_contact=Objects.Rock_tree_contact(r.verlet_trees_list[fi])
						r.tree_active_contact.dist=sqrt(dist)-r_radius+tree_dhp/2

def nscd_integrator_run(self,s):
	r=s.current_rock
	cdef double[:] vel = s.current_rock.vel
	cdef double dt = s.dt
	cdef double gravity = s.gravity
	vel[2]-=gravity*dt
	cdef double[:] pos = s.current_rock.pos
	for i in range(3):
		pos[i]+=vel[i]*dt
	if(r.pos[2]<s.terrain.min_height):
		r.is_stopped=True
		r.out_of_bounds=True
	
from platrock.Common import  Math
def set_faces_normals_and_cogs(faces):
	cdef int nb_faces = len(faces)
	cdef int i,j,k
	cdef double[3] normal, cog, buff1, buff2, buff3
	cdef double[3][3] points
	for i in range(nb_faces):
		for j in range(3):
			for k in range(3):
				points[j][k]=faces[i].points[j].pos[k]
		normal=cross3(sub3(points[0],points[1],buff1),sub3(points[2],points[1],buff2),buff3)
		normal=mult_s3(1./norm3(normal),normal,buff1)
		if(normal[2]<0.):
			normal=mult_s3(-1,normal,buff1)
		faces[i].normal=Math.Vector3(normal)
		cog=mult_s3(1./3, add3(add3(points[0],points[1],buff1),points[2],buff2),buff3)
		faces[i].cog=Math.Vector3(cog)
	
	
