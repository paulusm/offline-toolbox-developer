const fs = require("fs");

global.hasLocalVersion = function(id){
    if(fs.existsSync(`video/${id}.mp4`)){
        return "hasVideoMp4";
    }
    if(fs.existsSync(`video/${id}.webm`)){
        return "hasVideoWebm";
    }
    if(fs.existsSync(`files/${id}.pdf`)){
        return "hasPDF";
    }
    return "noLocal";
}

global.curLang = "fr";

module.exports = function(eleventyConfig) {
    eleventyConfig.setPugOptions({ pretty: true, globals: ["hasLocalVersion", "curLang"]}); //, debug:true 
    eleventyConfig.addPassthroughCopy("css");
    eleventyConfig.addPassthroughCopy("images");
    eleventyConfig.addPassthroughCopy("scripts");
    eleventyConfig.addPassthroughCopy("files");
    eleventyConfig.addPassthroughCopy("video");
};