# Offline Toolbox Generator

## Mirroring and parsing

1. Mirring is done using wget, the command used is in the shell script (mirror.sh). This creates a mirror folder www.fao.org.
2. Parsing is done using Python 3.6 and the libraries in the Pipfile. The Python scripts run through the local HTML and parse it to json files.
3. Downloading of PDFs and Videos is done with get-attachments.py and saves copies to local "files" and "videos" folders

## Indexing and Generating

3. Generation uses [Eleventy.js](https://v0-7-0.11ty.dev/) within the Node framework. The scripts expect the data to be in the _data folder and resources to be local "files" and "videos" folders.
5. Search uses [Luna.js](https://lunrjs.com/) both server and client side. The json files are used to build an index using index/buildIndex.js. This then saves to a js file. Json files shouldbe converted js and saved in the script folder to (see search.pug) be imported for search results.