# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 14:53:18 2018

@author: Khushbu
"""
import dbConnection
import RideDetailsClass
import EuclideanDistClass
import ConversionShortPath

import itertools



#testing block
dbConnObj = dbConnection.DB_Connect()
rideDetails = RideDetailsClass.RideDetailClass()
con = dbConnObj.dbConnection()

loc, fare, passCount, drop, offs = rideDetails.getRideDetails(con,'0')
euclObj = EuclideanDistClass.EuclideanDistance(2)
eucDistS, eucDistDest, nextPoolID,toShortPathSources, toShortPathDest, individualTrips = euclObj.getEuclideanDistanceDict(loc,passCount)

#print (toShortPathSources)

d1TestSource = dict(itertools.islice(iter(toShortPathSources.items()),100))
d1TestDest = dict(itertools.islice(iter(toShortPathDest.items()),100))

convObj = ConversionShortPath.Conversion()
sourceDetails,destDetails = convObj.getShortestPathDetailDict(d1TestSource,d1TestDest)

print (sourceDetails)
print (destDetails)
