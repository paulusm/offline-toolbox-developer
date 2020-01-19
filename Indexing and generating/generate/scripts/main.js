var toggleTabs = function(e){

    var tabSet = document.getElementsByClassName("tab-content");
    for(var i=0; i<tabSet.length; i++){
        tabSet[i].classList.remove("on");
        tabSet[i].classList.add("off");
    }
    document.getElementById(e.target.dataset.tabSection).classList.remove("off");
    document.getElementById(e.target.dataset.tabSection).classList.add("on");

    var tabSet = document.getElementsByClassName("module-section-title");
    for(var i=0; i<tabSet.length; i++){
        tabSet[i].classList.remove("on");
        tabSet[i].classList.add("off");
    }

    e.target.classList.remove("off");
    e.target.classList.add("on");
}

var initTabs = function(){
    var tabSet = document.getElementsByClassName("module-section-title");
    for(var i=0; i<tabSet.length; i++){
        tabSet[i].addEventListener("click", toggleTabs, false);
    }
}

initTabs();