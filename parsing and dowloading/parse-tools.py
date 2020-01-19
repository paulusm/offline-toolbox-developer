import os
import json
import re
from bs4 import BeautifulSoup

def getMeta(soup, field):
    try:
        fieldList = list(soup.select(f'div > {field}')[0].stripped_strings)
        ret = (fieldList[1] if len(fieldList) else "")
        return(ret)
    except:
        return("")



#"cases":"www.fao.org/sustainable-forest-management/toolbox/cases/case-detail/"
#"tools": "www.fao.org/sustainable-forest-management/toolbox/tools/tool-detail/", 

toolPaths = {
"tools": "www.fao.org/sustainable-forest-management/toolbox/tools/tool-detail/",
"cases":"www.fao.org/sustainable-forest-management/toolbox/cases/case-detail/"
}

langs = ["es"]  

for infoType in toolPaths.keys():
    print("getting - ", infoType)
    for lang in langs:
        tools = []
        if lang is not "en" and infoType is "tools":
            specificToolPath = f'www.fao.org/sustainable-forest-management/toolbox/tools/tools-details/{lang}/c'
        else:
            specificToolPath = f'{toolPaths[infoType]}{lang}/c'

        for dir in os.listdir(specificToolPath):
            print(lang, dir)
            indexFile = open(f'{specificToolPath}/{dir}/index.html')
            soup = BeautifulSoup(indexFile, 'html.parser')
            thisTool = dict()
            thisTool['id'] = dir
            thisTool['title'] = soup.find("h2").string
            thisTool['language'] = lang

            toolThumb = soup.select('div#sfm-image > img')
            if len(toolThumb)>0:
                thisTool['thumb'] = re.sub(".*/","",soup.select('div#sfm-image > img')[0]['src'])

            thisTool['url'] = (soup.select("div > #sfm-link > a")[0].string if len(soup.select("div > #sfm-link > a")) >0 else '')
            thisTool['abstract'] = (soup.select("div > #sfm-abstract")[0].string if len(soup.select("div > #sfm-abstract")) > 0 else '')
            
            fieldDict = {'author':'#sfm-spersonalAuthor', 'year':'#sfm-year',
                'type':'#sfm-typeOfMaterial','scale':'#sfm-scale',
                'region':'#sfm-region', 'biome':'#sfm-biome',
                'forestType':'#sfm-forestType','function':'#sfm-function',
                'responsibility':'#sfm-responsibility'
                }

            for key in fieldDict.keys():
                thisTool[key] = getMeta(soup, fieldDict[key])
            tools.append(thisTool)

        outFile = open(f'json/{infoType}-{lang}.json', 'w')
        json.dump(tools,outFile)