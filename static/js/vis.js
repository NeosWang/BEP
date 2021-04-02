(function(factory) {
    if (typeof define === "function" && define.amd) {
        // AMD. Register as an anonymous module.
        define([], factory);
    } else if (typeof exports === "object") {
        // Node/CommonJS
        module.exports = factory();
    } else {
        // Browser globals
        window.vis = factory();
    }
})(function(){
    "use strict";

    var VERSION = "ver 0.0.1"

    var AUTHOR = "Yichen Wang"

    function slider(id, data){
        var slider = document.getElementById(id);
        noUiSlider.create(slider, {
            start: [0,0,data.length - 1,data.length - 1],
            connect: true,
            behaviour: "drag",
            dragAllHandles: true,
            tooltips: [{
                to: function (value) {
                    return data[Math.round(value)]
                }
            },
            {
                to: function (value) {
                    return data[Math.round(value)]
                }
            },
            {
                to: function (value) {
                    return data[Math.round(value)]
                }
            },
            {
                to: function (value) {
                    return data[Math.round(value)]
                }
            }
        ],
            range: {
                'min': 0,
                'max': data.length - 1
            },
            step: 1,
        });
        return slider
    }
    
    
    function bindSliderInputs(slider, inputs){
        inputs.forEach((input,i)=>{
            input.addEventListener('change', function(){
                let value = new Array(inputs.length).fill(null);
                value[i] = this.value;
                slider.noUiSlider.set(value);
            });
        });
        slider.noUiSlider.on('update', function (values, handle) {
            inputs[handle].value = parseInt(values[handle]);
        });
    }

    function dataZoomScaleSlider(slider) {
        let option = myChart.getOption();
        let startValue = option.dataZoom[0].startValue;
        let endValue = option.dataZoom[0].endValue;

        let tooltips = slider.noUiSlider.get();
        let i;
        for (i = 0; i < tooltips.length; i++) {
            tooltips[i] = tooltips[i] < startValue ? startValue : tooltips[i];
            tooltips[i] = tooltips[i] > endValue ? endValue : tooltips[i];
        }

        slider.noUiSlider.updateOptions({
            start: tooltips,
            range: {
                'min': startValue,
                'max': endValue
            }
        });
    }

    function mergeTooltips(slider, threshold, separator) {
        slider.noUiSlider.on('update', function (values, handle, unencoded, tap, positions) {
            let handleGroup = [[0]];
            let valueGroup = [[yc.formatter(timeData,values[0])]];
            for (let i = 1; i < values.length; i++) {
                if (positions[i] - positions[i - 1] > threshold) {
                    handleGroup.push([i]);
                    valueGroup.push([yc.formatter(timeData,values[i])]);
                }
                else {
                    handleGroup[handleGroup.length - 1].push(i);
                    valueGroup[valueGroup.length - 1].push(yc.formatter(timeData,values[i]));
                }
            }
            for (let i = 0; i < handleGroup.length; i++) {
                let item = handleGroup[i]
                if (item.length > 1) {
                    let noTooltip = true
                    for (let j = 0; j < item.length; j++) {
                        tooltips[item[j]].style.marginLeft='';
                        tooltips[item[j]].style.display = 'none';
                        if (noTooltip && item[j] != handle) {
                            tooltips[item[j]].style.display = 'block';
                            tooltips[item[j]].innerHTML = valueGroup[i].join(separator)
                            if(item[j]<handle){
                                tooltips[item[j]].style.marginLeft='20px';
                            }else{tooltips[item[j]].style.marginLeft='-20px'}
                            noTooltip = false;
                        }
                    }
                } else {
                    tooltips[item[0]].style.marginLeft='';
                    tooltips[item[0]].style.display = 'block';
                    if (item[0]!=handle){tooltips[item[0]].innerHTML = valueGroup[i][0];}                    
                }
            }
        });
    }


    return {
        version: VERSION,
        author: AUTHOR,
        slider: slider,
        bindSliderInputs:bindSliderInputs,
        dataZoomScaleSlider:dataZoomScaleSlider,
        mergeTooltips:mergeTooltips
    };
});