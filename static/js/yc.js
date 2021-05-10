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

    var AUTHOR = "Yichen Wang"

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

    
    function max(array){
        return Math.max.apply(Math,array)
    }

    function quantile(array,v){
        v = _convertToType(array[0],v)        
        return array.indexOf(v) * 100 / (array.length-1)
    }

    function _convertToType (t, e) {
        return (t.constructor) (e);
    }

    function formatter(array, floatIndex){
        return array[Math.round(floatIndex)]
    }

    var MySetInterval = function (callback, delay) {
        var setIntervalId, start, remaining = delay;

        this.pause = function () {
            window.clearInterval(setIntervalId);
        };

        this.play= function () {
            start = new Date();
            window.clearInterval(setIntervalId);
            setIntervalId= window.setInterval(callback, remaining);
        };
    }


    return {
        version: VERSION,
        author: AUTHOR,
        MySetInterval:MySetInterval,
        sortKeyValuePair: sortKeyValuePair,
        sortByKey:sortByKey,
        max:max,
        quantile: quantile,
        formatter:formatter
    };
});