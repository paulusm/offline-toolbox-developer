import os
import os.path
import json
import re
from bs4 import BeautifulSoup

modulePath = "www.fao.org/sustainable-forest-management/toolbox/modules"

moduleSections = {'basic-knowledge':{'en':'Basic Knowledge','fr':'Notions de base','es':'Información básica'},
'in-more-depth':{'en':'In More Depth','fr':'Approfondissement','es':'Información más detallada'},
'further-learning':{'en':'Further Learning','fr':'Autres références','es':'Referencias adicionales'},
'credits':{'en':'Credits','fr':'Credits','es':'Credits'}}

modules = dict()

# Get the module home page to get thumbs
iFile = open(f'{modulePath}/en/index.html')
iSoup = BeautifulSoup(iFile, 'html.parser')

# Create structure
for lang in ['en','fr','es']:
    modules[lang] = []

for dir in os.listdir(modulePath):
    module = dict()
    for lang in ['en','fr','es']:
        module[lang] = dict()
        module[lang]['sections'] = []

        for sectionKey in moduleSections:
            # Get the page foreach module section
            try:
                bkFile = open(f'{modulePath}/{dir}/{sectionKey}/{lang}/index.html')
            except Exception as ex:
                print(f'{dir} had error opening HTML')
                continue

            moduleSection = dict()

            moduleSection['section']= moduleSections[sectionKey][lang]

            soup = BeautifulSoup(bkFile, 'html.parser')

            if sectionKey == 'basic-knowledge':
                # Get module title
                try:
                    modTitle = soup.find('h2', {'class':'csc-firstHeader'})
                    if modTitle is None:
                        modTitle = soup.find('h1', {'class':'csc-firstHeader'})
                    module[lang]['title'] = modTitle.string
                except:
                    print(f'{dir} had error finding title')
                    continue
                
                # Module image
                modImage = soup.select('div.csc-textpic-imagewrap > img')
                module[lang]['image'] = re.sub(".*/","",modImage[0]['src'])

                # Module thumb from index file
                try:
                    modThumb = iSoup.select(f'a[href="/sustainable-forest-management/toolbox/modules/{dir}/basic-knowledge/en/"] > img')
                    #modThumb = iSoup.select(f'a[href="../{dir}/basic-knowledge/en/index.html"] > img')
                    
                    #print(f'a[href="../{dir}/basic-knowledge/{lang}/index.html"] > img')
                    module[lang]['thumb'] = re.sub(".*/","",modThumb[0]['src'])
                except:
                    print(f'{dir} had error finding thumb')
                    continue

                # Get the body paras and append to description
                modDesc = soup.select('div.csc-textpic-text > p.bodytext')
                module[lang]['description'] = ''

                for contentLine in modDesc:
                    
                    if contentLine is not None:
                        module[lang]['description'] += str(contentLine)

                module[lang]['slug'] = dir


             
            modContent = soup.select('div.csc-default > p.bodytext')
            
            moduleSection['body'] = ''
            for contentLine in modContent:
                if contentLine is not None and contentLine.find(title="Instagram") is None and contentLine.find(title="Google Play") is None:
                    moduleSection['body'] += str(contentLine)

            # Add to dict
            module[lang]['sections'].append(moduleSection)

        for modLinks in ['tools', 'cases']:
            module[lang][modLinks]=[]
            for i in range(1,5):
                fLinks = f'{modulePath}/{dir}/{modLinks}/{lang}/index.html?page={i}&ipp=10&no_cache=1'
                if not os.path.exists(fLinks):
                    fLinks = fLinks + "&tx_dynalist_pi1[par]=YToxOntzOjE6IkwiO3M6MToiMCI7fQ=="
                if not os.path.exists(fLinks):
                    if i == 1:
                        fLinks = f'{modulePath}/{dir}/{modLinks}/{lang}/index.html'
                    else:
                        continue  
                try:
                    bkFile = open(fLinks)
                except Exception as ex:
                    print(f'{dir} had error opening tools/cases HTML')
                    continue

                soup = BeautifulSoup(bkFile, 'html.parser')
                

                resourceRecs = soup.select('div.list-title > a')

                for resourceRec in resourceRecs:
                    m =  re.search(r'[0-9]{6,7}', resourceRec['href'])
                    #print(f'{modTitle} - Got {modLinks}, {i}, {m[0]}')
                    resourcesItem = dict()
                    resourcesItem['id'] = m[0]
                    resourcesItem['title'] = resourceRec.string
                    module[lang][modLinks].append(resourcesItem)

        if  'title' in module[lang]:
            modules[lang].append(module[lang])

for lang in ['en','fr','es']:
    outFile = open(f'json/modules-{lang}.json', 'w')
    json.dump(sorted(modules[lang], key=lambda k: k['title']) ,outFile)