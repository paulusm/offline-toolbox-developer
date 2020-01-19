
function initIndex() {
   
    toolbox_idx = lunr.Index.load(indexJSON);
    console.log("Index loaded - " + toolbox_idx.fields);

}


if(!toolbox_idx){
    var toolbox_idx;
    initIndex();
}

if(location.href.lastIndexOf("?q=") > 0){
    var query = location.href.substr(location.href.lastIndexOf("?q=")+3).replace("+"," ");
    query = decodeURIComponent(query);
    var qFeedback = document.createElement("h3");
    qFeedback.innerText = "Búsqueda '" + query + "'";
    var serp = document.getElementById("serp");
    serp.appendChild(qFeedback);

    //do the query
    var resultSet = toolbox_idx.search(query);

    if(resultSet.length ==0 ){
        var qFeedback = document.createElement("p");
        qFeedback.innerText = "Lo sentimos, no se encontraron resultados";
        var serp = document.getElementById("serp");
        serp.appendChild(qFeedback);
    }
    
    for(var i=0; i< resultSet.length && i<20; i++){
        //match the result set to the resource types by fall through
        resultItem = tooldata.filter(function(item){
            return item.id === resultSet[i].ref;
        });
        if(resultItem[0]){
            resultItem[0].resourceType = 'tool';
        }
        else{
            if(resultItem.length == 0){
                resultItem = casedata.filter(function(item){
                    return item.id === resultSet[i].ref;
                });
            }
            if(resultItem[0]){
                resultItem[0].resourceType = 'case';
            }
            else{
                if(resultItem.length == 0){
                    resultItem = moduledata.filter(function(item){
                        return item.slug === resultSet[i].ref;
                    });
                }
                resultItem[0].resourceType = 'module';
            }
        }

        console.log(resultItem);

        if(resultItem.length >0){
            //console.log(resultItem[0].title)
            //append to result set
            var searchLi = document.createElement("li");
            searchLi.className = "serp-" + resultItem[0].resourceType;
            var searchA = document.createElement("a");
            var searchP = document.createElement("p");
            // TODO: Create relevant link
            searchA.setAttribute("href",resultItem[0].resourceType + "s/es/" + (resultItem[0].resourceType === "module"?resultItem[0].slug:resultItem[0].id) + "/index.html");
            searchA.innerText = resultItem[0].resourceType.charAt(0).toUpperCase() + resultItem[0].resourceType.substr(1).toLowerCase() + ": " + resultItem[0].title;
            if(resultItem[0].thumb){
                searchThumb =  document.createElement("img");
                searchThumb.setAttribute("src","images/" + resultItem[0].thumb);
                searchThumb.setAttribute("width", "50");
                searchA.appendChild(searchThumb);
            }
            searchP.innerText = (resultItem[0].resourceType === "module"?resultItem[0].description:resultItem[0].abstract).substr(0,300).replace("<p class=\"bodytext\">","") + "...";
            searchLi.appendChild(searchA);
            searchLi.appendChild(searchP);
            serp.appendChild(searchLi);
        }
    }

}
