from osgeo import gdal
import functools,operator



def get_geojson_all_properties(filename,unique=True):
	result=[]
	shp_file=gdal.OpenEx(filename)
	for feat in shp_file.GetLayer(0):
		feat_dict=feat.ExportToJson(as_object=True) #loop on rocks start polygons
		result.append(list(feat_dict['properties'].keys()))
	if unique:
		result=functools.reduce(operator.iconcat, result, []) #flatten
		unique_result = list(set(result))
		return unique_result
	return result

def get_geojson_all_shapes(filename,unique=True):
	result=[]
	shp_file=gdal.OpenEx(filename)
	for feat in shp_file.GetLayer(0):
		feat_dict=feat.ExportToJson(as_object=True) #loop on rocks start polygons
		result.append(feat_dict['geometry']["type"])
	if unique:
		#result=functools.reduce(operator.iconcat, result, []) #flatten
		unique_result = list(set(result))
		return unique_result
	return result
