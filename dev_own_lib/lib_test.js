(function(factory) {
    if (typeof define === "function" && define.amd) {
        // AMD. Register as an anonymous module.
        define([], factory);
    } else if (typeof exports === "object") {
        // Node/CommonJS
        module.exports = factory();
    } else {
        // Browser globals
        window.yichen = factory();
    }
})(function(){
    "use strict";

    var VERSION = "ver 0.0.1"

    function initialize(target){
        console.log(target)
        // 如果为空或者对象没有nodeName属性
        if (!target || !target.nodeName){
            throw new Error("BEP (" + VERSION + "): create requires a single element, got: " + target);
        }

        if (target.yichen) {
            throw new Error("BEP (" + VERSION + "): tool was already initialized.");
        }

        // var options = testOptions(originalOptions, target);

        return "???"
    }

    return {
        version: VERSION,
        create: initialize
    };
});