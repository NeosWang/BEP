(function (factory) {
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
})(function () {
    "use strict";

    var VERSION = "ver 0.0.1"

    var AUTHOR = "Yichen Wang"

    function sortKeyValuePair(obj, reverse = false) {
        let output = {}
        let keys = Object.keys(obj).sort()
        if (reverse) { keys.reverse() }
        keys.forEach((key) => output[key] = obj[key])
        return output
    }

    function sortByKey(array, key) {
        return array.sort(function (a, b) {
            var x = a[key]; var y = b[key];
            return ((x < y) ? -1 : ((x > y) ? 1 : 0));
        });
    }


    function max(array) {
        return Math.max.apply(Math, array)
    }

    function quantile(array, v) {
        v = _convertToType(array[0], v)
        return array.indexOf(v) * 100 / (array.length - 1)
    }

    function _convertToType(t, e) {
        return (t.constructor)(e);
    }

    function formatter(array, floatIndex) {
        return array[Math.round(floatIndex)]
    }

    function cleanedElement(str) {
        return $(str).empty()
    }

    var MySetInterval = function (callback, delay) {
        var setIntervalId, start, remaining = delay;

        this.pause = function () {
            window.clearInterval(setIntervalId);
        };

        this.play = function () {
            start = new Date();
            window.clearInterval(setIntervalId);
            setIntervalId = window.setInterval(callback, remaining);
        };
    }

    function uniqueSubArray(master, sub) {
        return sub.every(e => master.filter(v => v == e).length == 1);
    }


    function replaceIcon(i, before, after) {
        i.removeClass(before);
        i.addClass(after);
    }

    function uniqueElements(array) {
        return (new Set(array)).size === array.length;
    }

    function limitFileSize(file, limitSize) {
        var arr = ["KB", "MB", "GB"]
        var limit = limitSize.toUpperCase();
        var limitNum = 0;
        for (var i = 0; i < arr.length; i++) {
            var leval = limit.indexOf(arr[i]);
            if (leval > -1) {
                limitNum = parseInt(limit.substr(0, leval)) * Math.pow(1024, (i + 1))
                break
            }
        }
        return file.size <= limitNum
        // if (file.size > limitNum) {
        //     return false
        // }
        // return true
    }

    function transpose(m) {
        return m[0].map(function (_, c) {
            return m.map(function (r) { return r[c]; });
        });
    }

    return {
        version: VERSION,
        author: AUTHOR,
        MySetInterval: MySetInterval,
        sortKeyValuePair: sortKeyValuePair,
        sortByKey: sortByKey,
        max: max,
        quantile: quantile,
        formatter: formatter,
        cleanedElement: cleanedElement,
        uniqueSubArray: uniqueSubArray,
        replaceIcon: replaceIcon,
        limitFileSize: limitFileSize,
        uniqueElements: uniqueElements,
        transpose: transpose
    };
});