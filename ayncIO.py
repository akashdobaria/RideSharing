# -*- coding: utf-8 -*-
"""
Created on Tue Apr  3 18:09:21 2018

@author: akash
"""

import asyncio
import aiohttp
import json

class Conversion2():
    #concurrent = 100
    
    shortPathDataDictSource = dict()
    shortPathDataDictDest = dict()   
    
    def handle_req_source(self, data, key):
        dataDictSource = json.loads(data.text)
        self.shortPathDataDictSource[key] = dataDictSource['routes'][0]['distance']
        
    def handle_req_dest(self, data, key):
        dataDictSource = json.loads(data.text)
        self.shortPathDataDictSource[key] = dataDictSource['routes'][0]['distance']
    
    def chunked_http_client(self,num_chunks):
        # Use semaphore to limit number of requests
        semaphore = asyncio.Semaphore(num_chunks)
        @asyncio.coroutine
        # Return co-routine that will download files asynchronously and respect
        # locking fo semaphore
        def http_get(url, key):
            nonlocal semaphore
            with (yield from semaphore):
                with aiohttp.ClientSession() as session:
                    response = yield from session.get(url)
                    body = yield from response.content.read()
                    yield from response.wait_for_close()
                
            return body, key
        return http_get
    
    def run_experiment_source(self, urls):
        http_client = self.chunked_http_client(100)
        # http_client returns futures, save all the futures to a list
        tasks = [http_client(url, key) for key, url in urls.items()]
        # wait for futures to be ready then iterate over them
        for future in asyncio.as_completed(tasks):
            data, key = yield from future
            try:
                self.handle_req_source(data, key)
            except Exception as err:
                print("Error for {0} - {1}")
    
    def run_experiment_dest(self,urls):
        http_client = self.chunked_http_client(100)
        # http_client returns futures, save all the futures to a list
        tasks = [http_client(url, key) for key, url in urls.items()]
        # wait for futures to be ready then iterate over them
        for future in asyncio.as_completed(tasks):
            data, key = yield from future
            try:
                self.handle_req_dest(data, key)
            except Exception as err:
                print("Error for {0} - {1}")
    
    def getShortestPathDetailDict(self,toShortPathSources,toShortPathDest):
            
        sourceList = dict()
        for key,value in toShortPathSources.items():
            
            lonS1=value[0][0]
            latS1=value[0][1]
            lonS2=value[0][2]
            latS2=value[0][3]
            #http://localhost:5000
            osrmURL = "http://localhost:5000/route/v1/driving/"+str(lonS1) +","+str(latS1)+";"+str(lonS2)+","+str(latS2)+"?overview=false";
            sourceList[key] = osrmURL
        
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.run_experiment_source(sourceList))
        
        destList = dict()
        for key,value in toShortPathDest.items():
            lonD1=value[0][0]
            latD1=value[0][1]
            lonD2=value[0][2]
            latD2=value[0][3]
            osrmURL = "http://localhost:5000/route/v1/driving/"+str(lonD1) +","+str(latD1)+";"+str(lonD2)+","+str(latD2)+"?overview=false";
            destList[key]=osrmURL
        
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.run_experiment_dest(destList))
        
        return self.shortPathDataDictSource,self.shortPathDataDictDest
