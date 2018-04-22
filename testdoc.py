# -*- coding: utf-8 -*-
"""
Created on Wed Mar 21 14:53:18 2018

@author: Khushbu
"""
import dbConnection
import RideDetailsClass
import EuclideanDistClass
import ConversionShortPath2
import CombineRides
import itertools




#testing block
dbConnObj = dbConnection.DB_Connect()
rideDetails = RideDetailsClass.RideDetailClass()
con = dbConnObj.dbConnection()

loc, fare, passCount, drop, offs = rideDetails.getRideDetails(con,'0')
euclObj = EuclideanDistClass.EuclideanDistance(3)
#

eucDistS, eucDistDest, nextPoolID,toShortPathSources, toShortPathDest, individualTrips = euclObj.getEuclideanDistanceDict(loc,passCount)

#print (toShortPathSources['107,145'])
#print (toShortPathDest['107,145'])

#d1TestSource = dict(itertools.islice(iter(toShortPathSources.items()),100))
#d1TestDest = dict(itertools.islice(iter(toShortPathDest.items()),100))

d1TestSource = toShortPathSources
d1TestDest = toShortPathDest

convObj = ConversionShortPath2.Conversion()
sourceDetails,destDetails = convObj.getShortestPathDetailDict(d1TestSource,d1TestDest)

combineObj = CombineRides.CombineRides()
sortedMap = combineObj.mergeSourceDestDist(sourceDetails,destDetails)

print (len(toShortPathSources)*2)

#print (sourceDetails['1,7'])
#print (destDetails['1,7'])