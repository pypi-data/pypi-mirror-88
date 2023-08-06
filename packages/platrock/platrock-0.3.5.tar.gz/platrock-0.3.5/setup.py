import sys
if sys.version_info < (3,6):
	sys.exit('Sorry, Python < 3.6 is not supported')
elif sys.version_info[0]==3 and sys.version_info[1]==6:
	max_numpy_version=",<=1.19.4" #from 1.20, numpy doesn't support python 3.6
else:
	max_numpy_version=""

from setuptools import setup,Extension,find_packages,dist

#The following line will get numpy NOW, its a trick that we use as numpy is needed for the Cython extensions declaration below.
dist.Distribution().fetch_build_eggs(["numpy>=1.17.5"+max_numpy_version])
try:
	import numpy
	ext_modules = [
		Extension("platrock.ThreeD.ThreeDEnginesToolbox",["./platrock/Cython/ThreeDEnginesToolbox.pyx"],include_dirs=[numpy.get_include()]),
		Extension("platrock.Common.Math",["./platrock/Cython/Math.pyx"],include_dirs=[numpy.get_include()]),
	]
except:
	sys.exit("Numpy not found !")

#python-gdal is required, but it in turn needs a system library (libgdal) to be installed, AND BOTH NEED THE EXACT SAME VERSION NUMBER.
from subprocess import Popen,PIPE,STDOUT
import re
#Get the system gdal version:
p = Popen('gdalinfo --version', shell=True, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
returncode=p.wait()
if not returncode==0:
	sys.exit("Gdal seems not to be installed ('gdalinfo --version' doesn't work). Please install gdal before platrock with for instance: 'sudo apt install gdal-bin'.")
else:
	"""
	NOTE: gdal-bin will install system-wide python3-gdal in the same version. We will set the gdal=='gdal_version' to the requirements anyway to satisfy this dependency in the case the user doesn't use the system python3 version. If he doesn't, pip3 will install and compile gdal for the right python3 and the right system libgdal version.
	"""
	S=p.stdout.read().decode("utf8")
	gdal_version=re.search('([0-9]([0-9]|\.)*)',S).groups()[0]

with open("readme.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
	name = "platrock",
	version = "0.3.5",
	author = "François Kneib",
	author_email = "francois.kneib@gmail.com",
	description="Rockfall simulation software",
	long_description=long_description,
	long_description_content_type="text/markdown",
	url = "https://gitlab.com/platrock/platrock",

	setup_requires = ["cython"],
	install_requires = ["numpy>=1.17.5"+max_numpy_version,"gdal=="+gdal_version, "numpy-quaternion", "yappi","ipython", "jsonpickle==1.3", "matplotlib", "numba", "h5py", "shapely", "descartes", "plotly", "scipy","scikit-image","psutil"],
	# Force jsonpickle==1.3 as newer version fails at saving/loading a 2D simulation (bad py/id reference). To test it, try to re-launch a TwoD simulation via WebUI (doesn't work with jsonpickle 1.4.1).
	scripts=['bin/platrock'],
	ext_modules = ext_modules,
	packages = find_packages(),
	package_data={'': ['*.pxd', '*.pyx', 'Common/Toe_2018/*', "examples/*"]},
	# Disable zip_safe, because:
	#   - Cython won't find .pxd files inside installed .egg, hard to compile libs depending on this one
	#   - dynamic loader may need to have the library unzipped to a temporary directory anyway (at import time)
	zip_safe = False,
	classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
	python_requires='>=3.6'
)
