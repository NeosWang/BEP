(function (factory) {
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
})(function () {
    "use strict";

    var VERSION = "ver 0.0.1"

    var AUTHOR = "Yichen Wang"

    function Slider(id, boundary, handles = 1) {
        this.id = id;
        this.boundary = boundary;
        this.handles = handles;
        this.slider = this.initSlider();
        this.mergeTooltips();
    }
    Slider.prototype = {
        initSlider: function () {
            let start = new Array(Math.abs(this.handles)).fill(0);
            let tooltips = new Array(Math.abs(this.handles)).fill({
                to: function (value) {
                    return timeData[Math.round(value)];
                }
            })
            let slider = document.getElementById(this.id);
            noUiSlider.create(slider, {
                start: start,
                connect: true,
                behaviour: "drag",
                dragAllHandles: true,
                tooltips: tooltips,
                range: {
                    'min': this.boundary.start,
                    'max': this.boundary.end
                },
                step: 1,
            });
            return slider;
        },
        updateHandles: function (handles, boundary) {
            this.boundary = boundary;
            this.slider.noUiSlider.destroy();
            this.handles = handles;
            this.slider = this.initSlider();
            this.mergeTooltips();
            this._paintRange();
        },
        toolTips: function () {
            return this.slider.noUiSlider.getTooltips();
        },
        translation:function(n){
            let values = this.slider.noUiSlider.get();
            if(Array.isArray(values)){
                values = values.map(e=>{return parseInt(e) + n})
                if(values[0] < this.boundary.start || values[values.length-1] > this.boundary.end) return;
            }else{
                values = parseInt(values)+n
                if(values < this.boundary.start || values > this.boundary.end) return;
            }
            this.slider.noUiSlider.set(values);

        },
        setRange: function (boundary) {
            this.boundary = boundary;
            this.slider.noUiSlider.updateOptions({
                range: {
                    'min': this.boundary.start,
                    'max': this.boundary.end
                },
            });
            this.mergeTooltips()
        },
        mergeTooltips: function (threshold = 5, separator = ' - ') {
            let tooltips = this.toolTips();
            if (!Array.isArray(tooltips)) return;
            this.slider.noUiSlider.on('update', function (values, handle, unencoded, tap, positions) {
                let handleGroup = [[0]];
                let valueGroup = [[yc.formatter(timeData, values[0])]];
                for (let i = 1; i < values.length; i++) {
                    if (positions[i] - positions[i - 1] > threshold) {
                        handleGroup.push([i]);
                        valueGroup.push([yc.formatter(timeData, values[i])]);
                    }
                    else {
                        handleGroup[handleGroup.length - 1].push(i);
                        valueGroup[valueGroup.length - 1].push(yc.formatter(timeData, values[i]));
                    }
                }
                for (let i = 0; i < handleGroup.length; i++) {
                    let item = handleGroup[i]
                    if (item.length > 1) {
                        let noTooltip = true
                        for (let j = 0; j < item.length; j++) {
                            tooltips[item[j]].style.marginLeft = '';
                            tooltips[item[j]].style.display = 'none';
                            if (noTooltip && item[j] != handle) {
                                tooltips[item[j]].style.display = 'block';
                                tooltips[item[j]].innerHTML = valueGroup[i].join(separator)
                                if (item[j] < handle) {
                                    tooltips[item[j]].style.marginLeft = '20px';
                                } else { tooltips[item[j]].style.marginLeft = '-20px' }
                                noTooltip = false;
                            }
                        }
                    } else {
                        tooltips[item[0]].style.marginLeft = '';
                        tooltips[item[0]].style.display = 'block';
                        if (item[0] != handle) { tooltips[item[0]].innerHTML = valueGroup[i][0]; }
                    }
                }
            });
        },
        bindNetwork: function (network) {
            this.slider.noUiSlider.on('update', function (values, handle) {           
                if (values.length == 1) {
                    let time = timeData[parseInt(values[handle])];
                    gGraph = dn.getGraph(time);
                    gGraphAdj=undefined;
                } else {
                    let startIdx, endIdx, aStartIdx, aEndIdx
                    switch(slider.handles){
                        case 2:
                            startIdx =parseInt(values[0]);
                            endIdx = parseInt(values[1]);
                            break;
                        case -3:
                            aStartIdx = parseInt(values[0]);
                            aEndIdx = parseInt(values[1])-1;
                            startIdx = parseInt(values[1]);
                            endIdx = parseInt(values[2]);
                            break;
                        case 3:
                            startIdx = parseInt(values[0]);
                            endIdx = parseInt(values[1]);
                            aStartIdx = parseInt(values[1])+1;
                            aEndIdx = parseInt(values[2]);
                            break;
                    }
                    if (gIsUnion) {
                        gGraph = dn.unionGraph(timeData[startIdx], timeData[endIdx]);
                        gGraphAdj = dn.unionGraph(timeData[aStartIdx], timeData[aEndIdx]);
                    } else {
                        gGraph = dn.intersectionGraph(timeData[startIdx], timeData[endIdx]);
                        gGraphAdj = dn.intersectionGraph(timeData[aStartIdx], timeData[aEndIdx]);
                    }
                    if(aStartIdx>aEndIdx){
                        gGraphAdj=undefined;
                    }                    
                }
                let series = dn.serialize(gGraph, false, gCate);
                
                let color = {
                    '-3':'limegreen',
                    '3':'red'

                }

                if(gGraphAdj){
                    series = dn.serializeUpdate(series, gGraph.difference(gGraphAdj), color[slider.handles])
                }
                network.update(series, gCate);
            });
        },

        _paintRange: function () {
            let connect = this.slider.querySelectorAll('.noUi-connect');
            let classes = {
                before: 'c-before-color',
                center: 'c-center-color',
                after: 'c-after-color'
            };
            switch (this.handles) {
                case 2:
                    connect[0].classList.add(classes.center);
                    break;
                case -3:
                    connect[0].classList.add(classes.before)
                    connect[1].classList.add(classes.center)
                    break;
                case 3:
                    connect[0].classList.add(classes.center)
                    connect[1].classList.add(classes.after)
                    break;
            }

        }
    }

    function LineSummary(id) {
        this.myChart = echarts.init(document.getElementById(id));
        let option = {
            title: {
                left: 'center'
            },
            tooltip: {
                trigger: 'axis',
                axisPointer: {
                    animation: false
                }
            },
            toolbox: {
                feature: {
                    dataZoom: {
                        yAxisIndex: 'none'
                    },
                    restore: {},
                    saveAsImage: {}
                },
                right: 20
            },
            axisPointer: {
                link: { xAxisIndex: 'all' }
            },
            dataZoom: [
                {
                    type: 'inside',
                    show: true,
                    realtime: true,
                    rangeMode: ['value', 'value']
                },
                {
                    type: 'slider',
                    handleSize: '80%',
                    textStyle: {
                        fontSize: 10
                    },
                    bottom: 15,
                    height: 20
                }],
            grid: {
                left: 80,
                right: 80,
                top: 28,
                bottom: 55
            },
            xAxis: {
                type: 'category',
                boundaryGap: false,
                axisLine: { onZero: true },
                data: timeData
            },
            yAxis: {
                name: '',
                type: 'value',
            },
        };
        option && this.myChart.setOption(option);
    }
    LineSummary.prototype = {
        triggerRangeSlider: function (slider, zoomFrom, zoomTo) {
            let fn = [
                this._dataZoomScaleSlider
            ]
            this.myChart.on('dataZoom', function () {
                fn[0](this, slider, zoomFrom, zoomTo)

            });
            this.myChart.on('restore', function () {
                fn[0](this, slider, zoomFrom, zoomTo)
            });

        },
        dataZoomBoundary: function () {
            let option = this.myChart.getOption();
            return {
                start: option.dataZoom[0].startValue,
                end: option.dataZoom[0].endValue
            }
        },
        _dataZoomScaleSlider: function (echart, slider, zoomFrom, zoomTo) {
            let option = echart.getOption();
            let start = option.dataZoom[0].startValue;
            let end = option.dataZoom[0].endValue
            let boundary = {
                start: start,//index of timeData
                end: end
            }
            slider.setRange(boundary);
            zoomFrom.selectedIndex = start;
            zoomTo.selectedIndex = end;
        },
        update: function (data, merge = false) {
            this.myChart.setOption(data, merge);
        },
        resize: function () {
            this.myChart.resize();
        },
        updateTimeline: function () {
            let series = [];
            let legend = {
                data: [],
                left: 80
            }
            Object.entries(gMeasurements).forEach(([k, v]) => {
                if (v.show) {
                    legend.data.push(v.name)
                    let d = {
                        name: v.name,
                        type: 'line',
                        lineStyle: {
                            width: .8
                        },
                        hoverAnimation: false,
                        data: v.data,
                        markLine: {
                            symbol: 'none',
                            data: [
                                { type: 'max', name: 'max' }
                            ],
                        },
                    };
                    series.push(d)
                }
            });
            let opt = this.myChart.getOption()
            opt.legend = legend;
            opt.series = series;
            this.update(opt, true);
        }
    }



    function Network(id) {
        this.myChart = echarts.init(document.getElementById(id));
        let option = {
            series: [{
                type: 'graph',
                animation: true,
                // layout:'circular',
                // circular: {
                //     rotateLabel: true
                // },
                // lineStyle: {
                //     curveness: 0.3
                // },
                layout: 'force',
                force: {
                    initLayout: 'circular',
                    repulsion: 100,
                    edgeLength: 5
                },
                roam: true,
                label: {
                    position: 'right',
                    formatter: '{b}'
                },
                draggable: true,
                force: {
                    // gravity: 0.1,
                    repulsion: 40,
                },
            }]
        };
        option && this.myChart.setOption(option);
    }
    Network.prototype = {
        update: function (data, cate) {
            this.myChart.setOption({
                legend: [{
                    data: data[cate].map(function (a) {
                        return a.name;
                    })
                }],
                series: [{
                    data: data.nodes,
                    links: data.edges,
                    categories: data[cate]
                }]
            });
        },
        resize: function () {
            this.myChart.resize();
        }
    }





    function bindSliderInputs(slider, inputs) {
        inputs.forEach((input, i) => {
            input.addEventListener('change', function () {
                let value = new Array(inputs.length).fill(null);
                value[i] = this.value;
                slider.noUiSlider.set(value);
            });
        });
        slider.slider.noUiSlider.on('update', function (values, handle) {
            inputs[handle].value = parseInt(values[handle]);
        });
    }
    return {
        version: VERSION,
        author: AUTHOR,
        bindSliderInputs: bindSliderInputs,
        LineSummary: LineSummary,
        Slider: Slider,
        Network: Network
    };
});