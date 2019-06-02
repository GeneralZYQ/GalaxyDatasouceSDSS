from __future__ import print_function, division
import SciServer
from SciServer import Authentication, LoginPortal, Config, CasJobs, SkyQuery, SciDrive, SkyServer, Files, Jobs
import os;
import pandas as pd;
import sys;
import json;
from io import StringIO
from io import BytesIO
#from PIL import Image
import numpy as np
from PyAstronomy import pyasl
import csv
from PIL import Image
import time
print ("Start transorm")

# Define login Name and password before running these examples
Authentication_loginName = 'generalzyq';
Authentication_loginPassword = 'waZYQ@1993'

token1 = Authentication.login(Authentication_loginName, Authentication_loginPassword);
token2 = Authentication.getToken()
token3 = Authentication.getKeystoneToken()
token4 = Authentication.token.value
print("token1=" + token1)#
print("token2=" + token2)#
print("token3=" + token3)#
print("token4=" + token4)#

galaxies = pd.read_csv("GalaxyZoo1_DR_table7.csv", skiprows=950)

ellipticIndex = 8
cwSpiralIndex = 9
acwSpiralIndex = 10
edgeIndex = 11
dkIndex = 12
mergeIndex = 13
combinedIndex = 14

totalCount = 0

print (galaxies.shape)
for x in xrange(8,galaxies.shape[0]):

	imgName = str(galaxies.iloc[x][0]) + ".jpeg"
	if x % 50 == 0:
		print ("The interate is %d" % x)

	maxValue = 0
	shapeIndex = ellipticIndex
	for y in xrange(ellipticIndex,combinedIndex + 1):
		if galaxies.iloc[x][y] > maxValue:
			maxValue = galaxies.iloc[x][y]
			shapeIndex = y

	if shapeIndex != dkIndex:
		continue


	totalCount = totalCount + 1
	if totalCount % 50 == 0:
		print ("Total number is %d in time %s" % (totalCount, time.time()))

	if totalCount == 500:
		break


	hd2 = galaxies.iloc[x][1] + " " + galaxies.iloc[x][2]


	# Obtain decimal representation
	ra1, dec1 = pyasl.coordsSexaToDeg(hd2)
	img = SkyServer.getJpegImgCutout(ra=ra1, dec=dec1, width=1024, height=1024, scale=0.1, 
                                 dataRelease="DR13",opt="I",
                                 query="SELECT TOP 1 g.objID, g.ra, g.dec, g.r FROM fGetObjFromRectEq(ra1-0.5,dec1-0.5,ra1+0.5,dec1+0.5) n, Galaxy g WHERE n.objID=g.objID")
	im = Image.fromarray(img)
	im.save(imgName)

	# with open('shapes.csv', 'a') as f:
	#     writer = csv.writer(f)
	#     writer.writerow([str(galaxies.iloc[x][0]), str(shapeIndex)])

# shiips = pd.read_csv("shapes.csv")
# print ("Sucessfully collect %d galaxies !" % shiips.shape[0])





