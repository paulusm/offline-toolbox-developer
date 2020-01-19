var lunr = require('lunr')
const fs = require('fs')

var langs = ['es']; // 'fr', 'en']
var resources = ['modules','tools', 'cases'] //,'cases','tools']

var idxBuilder = new lunr.Builder()

idxBuilder.pipeline.add(
  lunr.trimmer,
  lunr.stopWordFilter,
  lunr.stemmer
)

idxBuilder.searchPipeline.add(
  lunr.stemmer
)

idxBuilder.ref('id')
idxBuilder.field('title')
idxBuilder.field('body')
idxBuilder.field('type')

langs.forEach((lang)=>{
  resources.forEach((resource)=>{
      
    let rawdata = fs.readFileSync(`_data/${resource}_${lang}.json`)
    let dataFile = JSON.parse(rawdata)
    dataFile.forEach((record)=>{
      //console.log(record.title, record.slug)
      //,'body': record.description
      idxBuilder.add({
        'id': (resource==="modules"?record.slug:record.id),
        'title': record.title,
        'body': (resource==="modules"?record.description: record.abstract),
        'type' : resource
      })
    })

  })

  var idx = idxBuilder.build()

  //console.log(idx.toJSON())

  //console.log(idx.search("policy type:modules"))

  fs.writeFileSync(`scripts/index_${lang}.js`, "var indexJSON = " + JSON.stringify(idx.toJSON()))

  console.log(`index ${lang} written!`)

})