import json
import requests
import sys
from pytube import YouTube
import logging
import time
import os.path as path

logging.basicConfig( format = '%(asctime)s\t%(levelname)-10s\t%(message)s', level=logging.INFO, filename = time.strftime("my-%Y-%m-%d.log"))

resourceTypes = ['tools','cases']
langs = ['es']

s = requests.session()


for resourceType in resourceTypes:
    for lang in langs:
        datFile = open(f'json/{resourceType}-{lang}.json')
        resourceList = json.load(datFile)
        i = 0
        for resource in resourceList:
            
            resUrl = resource['url']
            try:
                hd = s.head(resUrl, allow_redirects=True, timeout=20)
            except:
                logging.error("{}\t{}\t{}\t{}\t{}\t{}".format("Time Out", resourceType, resource['id'], resource['title'], hd.status_code, resUrl))
                continue
            
            if hd.status_code == 404:
                print(i, 'not found')
                logging.error("{}\t{}\t{}\t{}\t{}\t{}".format("Not Found", resourceType, resource['id'], resource['title'], hd.status_code, resUrl))
            
            if hd.status_code == 200:
                print(hd.status_code , resource['url'])
                i+=1
                if (hd.status_code == 200 and hd.headers['content-type']=="application/pdf") :
                    fid = resource['id']
                    if not path.exists(f'files/{fid}.pdf'):
                        print(i, 'New pdf')
                        try:
                            r = requests.get(resource['url'], timeout=60)
                           
                            open(f'files/{fid}.pdf', 'wb').write(r.content)
                            logging.info("{}\t{}\t{}\t{}\t{}\t{}\t{}".format("Downloaded",resourceType, resource['id'], resource['title'], hd.status_code, resUrl, hd.headers['content-type']))
                            resource['hasPDF']=True
                            resourceList[i]=resource
                        except:
                            print(i, "Error getting that pdf")
                            logging.error("{}\t{}\t{}\t{}\t{}\t{}".format("Not Downloaded", resourceType, resource['id'], resource['title'], hd.status_code, resUrl))
                    else:
                        print (i, 'PDF already downloaded')
                        logging.info("{}\t{}\t{}\t{}\t{}\t{}\t{}".format("Downloaded",resourceType, resource['id'], resource['title'], hd.status_code, resUrl, hd.headers['content-type']))
                        

                elif (resUrl.lower().find('youtube') != -1):
                    if not path.exists(f'video/{fid}.mp4') and not path.exists(f'video/{fid}.webm'):
                        #get video here
                        print(i, 'New video')
                        try:
                            yt = YouTube(resource['url'])
                            stream = yt.streams.filter(progressive=True).first()
                            if stream == None:
                                 stream = yt.streams.desc().first()

                            fid = resource['id']
                            stream.download('video',fid)
                            logging.info("{}\t{}\t{}\t{}\t{}\t{}\t{}".format("Downloaded",resourceType, resource['id'], resource['title'], hd.status_code, resUrl, hd.headers['content-type']))
                            resource['hasVideo']=True
                            resourceList[i]=resource
                        except:
                            print(i, "Error getting that vid")
                            logging.error("{}\t{}\t{}\t{}\t{}\t{}".format("Not Downloaded", resourceType, resource['id'], resource['title'], hd.status_code, resUrl))   
                    else:
                        print(i, 'Video already downloaded')
                        logging.info("{}\t{}\t{}\t{}\t{}\t{}\t{}".format("Downloaded",resourceType, resource['id'], resource['title'], hd.status_code, resUrl, hd.headers['content-type']))
 
                else:
                    print(i, 'no downloadable resource') 
                    logging.info("{}\t{}\t{}\t{}\t{}\t{}\t{}".format("Not Downloadable", resourceType, resource['id'], resource['title'], hd.status_code, resUrl, hd.headers['content-type']))

            else:
                logging.error("{}\t{}\t{}\t{}\t{}".format("HTTP Error", resourceType, resource['id'], resource['title'], hd.status_code, resUrl))

    outFile = open(f'json/{resourceType}-{lang}-dl.json', 'w')
    json.dump(resourceList,outFile)