(function(factory) {
    if (typeof define === "function" && define.amd) {
        // AMD. Register as an anonymous module.
        define([], factory);
    } else if (typeof exports === "object") {
        // Node/CommonJS
        module.exports = factory();
    } else {
        // Browser globals
        window.yc = factory();
    }
})(function(){
    "use strict";

    var VERSION = "ver 0.0.1"

    function sortKeyValuePair(obj,reverse=false){
        let output={}
        let keys = Object.keys(obj).sort()
        if(reverse){ keys.reverse()}
        keys.forEach((key)=>output[key]=obj[key])
        return output
    }

    function sortByKey(array, key) {
        return array.sort(function(a, b) {
            var x = a[key]; var y = b[key];
            return ((x < y) ? -1 : ((x > y) ? 1 : 0));
        });
    }

    // function countByKey(array, key) {
    //     let outputDict = array.reduce((outputDict, obj) => {
    //         const value = obj[key];
    //         outputDict[value] = (outputDict[value] || []).concat([obj.i, obj.j]);
    //         return outputDict;
    //     }, {});
    //     Object.entries(outputDict).forEach(([key, value]) => {
    //         outputDict[key] = [...new Set(value)].length
    //     });
    //     return outputDict;
    // }

    function countByKey(array, key) {
        let outputDict = array.reduce((outputDict, obj) => {
            const value = obj[key];
            outputDict[value] = (outputDict[value] || []).concat([obj.i, obj.j]);
            return outputDict;
        }, {});
        Object.entries(outputDict).forEach(([key, value]) => {
            outputDict[key] = {n:[...new Set(value)].length, l:(value.length)/2} 
        });
        return outputDict;
    }
    
    function getMax(array){
        return Math.max.apply(Math,array)
    }

    function getListByKey(obj, key){
        let output=[];
        Object.entries(obj).forEach(([k,v]) => output.push(v[key]));
        return output
    }

    return {
        version: VERSION,
        sortKeyValuePair: sortKeyValuePair,
        sortByKey:sortByKey,
        countByKey:countByKey,
        getListByKey:getListByKey,
        getMax:getMax
    };
});