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
        destory:function(){
            this.slider.noUiSlider.destroy();
        },
        initSlider: function () {
            let start = new Array(Math.abs(this.handles)).fill(0);
            let tooltips = new Array(Math.abs(this.handles)).fill({
                to: function (value) {
                    return gDn.timeSeries[Math.round(value)];
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
                let valueGroup = [[yc.formatter(gDn.timeSeries, values[0])]];
                for (let i = 1; i < values.length; i++) {
                    if (positions[i] - positions[i - 1] > threshold) {
                        handleGroup.push([i]);
                        valueGroup.push([yc.formatter(gDn.timeSeries, values[i])]);
                    }
                    else {
                        handleGroup[handleGroup.length - 1].push(i);
                        valueGroup[valueGroup.length - 1].push(yc.formatter(gDn.timeSeries, values[i]));
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
        bindNetwork: function (network, barchart) {
            this.slider.noUiSlider.on('update', function (values, handle) {       
                if (values.length == 1) {
                    let time = gDn.timeSeries[parseInt(values[handle])];
                    gGraph = gDn.getGraph(time);
                    gGraphAdj=undefined;
                } else {
                    let startIdx, endIdx, aStartIdx, aEndIdx
                    switch(gSlider.handles){
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
                        gGraph = gDn.unionGraph(gDn.timeSeries[startIdx], gDn.timeSeries[endIdx]);
                        gGraphAdj = gDn.unionGraph(gDn.timeSeries[aStartIdx], gDn.timeSeries[aEndIdx]);
                    } else {
                        gGraph = gDn.intersectionGraph(gDn.timeSeries[startIdx], gDn.timeSeries[endIdx]);
                        gGraphAdj = gDn.intersectionGraph(gDn.timeSeries[aStartIdx], gDn.timeSeries[aEndIdx]);
                    }
                    if(aStartIdx>aEndIdx){
                        gGraphAdj=undefined;
                    }                    
                }
                let series = gDn.serialize(gGraph, false, gCate);
                
                let color = {
                    '-3':'limegreen',
                    '3':'red'
                }

                if(gGraphAdj){
                    series = gDn.serializeColoring(series, gGraph.difference(gGraphAdj), color[gSlider.handles])
                }
                network.update(series, gCate);

                let seriesStat = gDn.serializeStatistics(gGraph,false,gCateS);
                barchart.update(seriesStat);
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
                // right: 2
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
                data: gDn.timeSeries
            },
            yAxis: {
                name: '',
                type: 'value',
            },
        };
        option && this.myChart.setOption(option);
    }
    LineSummary.prototype = {
        destory:function(){
            this.myChart.dispose();
        },
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
     
            if(start==end){
                start--;
                if(start < 0){
                    start++;    end++;
                } 
                echart.setOption({
                    dataZoom: {
                        startValue: start,
                        endValue: end
                    }
                });        
            }

            let boundary = {
                start: start,//index of timeSeries
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







    function BarChart(id){
        this.myChart = echarts.init(document.getElementById(id));
        let option = {     
        };
        option && this.myChart.setOption(option);
    }
    BarChart.prototype = {
        destory:function(){
            this.myChart.dispose();
        },
        update: function (data, merge = true) {
            let newOption = {
                grid: {
                    top: '90px',
                    left: '5px',
                    right: '15px',
                    bottom: '50px',
                    containLabel: true
                },
                tooltip: {
                    trigger: 'axis',
                    axisPointer: {            // Use axis to trigger tooltip
                        type: 'shadow'        // 'shadow' as default; can also be 'line' or 'shadow'
                    },               
                },
                legend:{
                    data:data.y
                },
                series:[]
            };

            let c = {type: 'category', data: data.x};
            let v = {type: 'value'};

            if(data.horizontal){
                newOption['xAxis'] = v;
                newOption['yAxis'] = c;
            }else{

                newOption['xAxis'] = c;
                newOption['yAxis'] = v;
            }

            data.data.forEach((x,i) =>{
                newOption.series.push({
                    name: data.y[i],
                    type: 'bar',
                    stack: 'total',
                    label: {
                        show: true,
                        formatter: function(d) {
                            return d.data > 0 ? d.data : '';
                        }
                    },
                    emphasis: {
                        focus: 'series'
                    },
                    data: x  
                });

            });
            this.myChart.setOption(newOption,merge);
        },
        resize: function () {
            this.myChart.resize();
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
                emphasis: {
                    focus: 'adjacency',
                    lineStyle: {
                        width: 10
                    }
                }
            }]
        };
        option && this.myChart.setOption(option);
    }
    Network.prototype = {
        destory:function(){
            this.myChart.dispose();
        },
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

    return {
        version: VERSION,
        author: AUTHOR,
        LineSummary: LineSummary,
        Slider: Slider,
        Network: Network,
        BarChart:BarChart
    };
});