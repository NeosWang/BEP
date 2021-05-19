(function (factory) {
    if (typeof define === "function" && define.amd) {
        // AMD. Register as an anonymous module.
        define([], factory);
    } else if (typeof exports === "object") {
        // Node/CommonJS
        module.exports = factory();
    } else {
        // Browser globals
        window.dn = factory();
    }
})(function () {
    "use strict";

    var VERSION = "ver 0.0.1"

    var AUTHOR = "Yichen Wang"

    function Graph(isDirected = false) {
        this.discrete = 1;
        this.edges = {};
        this.isDirected = isDirected;
    }
    Graph.prototype = {
        _cloneArray: function (items) {
            return items.map(item => Array.isArray(item) ? this._cloneArray(item) : item);
        },
        _addVertex: function (node) {
            this.edges[node] = this._adjacent(node)
        },
        _adjacent: function (node) {
            return this.edges[node] || {}
        },
        addEdge: function (u, v) {
            u = String(u)
            v = String(v)
            this._addVertex(u);
            this._addVertex(v);
            this._adjacent(u)[v] = 1;
            if (!this.isDirected) {
                this._adjacent(v)[u] = 1;
            }
        },
        nodes: function () {
            return Object.keys(this.edges);
        },
        countVertices: function () {
            return this.nodes().length;
        },
        countEdges: function () {
            let output = 0
            Object.entries(this.edges).forEach(([k, v]) => output += Object.keys(v).length / (2 - this.isDirected));
            return output
        },
        // cliques ====== start
        maximalCliques: function (reporter, clique = [], candidates = this.nodes(), excluded = []) {
            if (!candidates.length && !excluded.length) {
                reporter.push(clique);
                return
            }
            let pivot = this._pick_random(candidates) || this._pick_random(excluded);
            (candidates.filter(x => !this.edges[pivot].hasOwnProperty(x))).forEach(v => {  // the nodes which adjoins pivot will not be considered into iteration
                let newCandidates = candidates.filter(x => this.edges[v].hasOwnProperty(x));
                let newExcluded = excluded.filter(x => this.edges[v].hasOwnProperty(x));
                let newClique = [...clique, v];
                this.maximalCliques(reporter, newClique, newCandidates, newExcluded);
                candidates = candidates.filter(x => x !== v);
                excluded.push(v);
            });
        },
        _pick_random: function (array) {
            if (array.length) {
                let e = array.pop();
                array.push(e);
                return e
            }
        },// cliques ====== end
        // merge graphs ====== start
        intersection: function (graph) {
            let newEdges = {};
            Object.entries(this.edges).forEach(([k, v]) => {
                if (graph.edges[k]) {
                    newEdges[k] = {};
                    Object.keys(graph.edges[k]).forEach(e => {
                        if (v[e]) {
                            newEdges[k][e] = v[e] + 1
                        }
                    })
                }
            });
            let intersection = new Graph(this.isDirected);
            intersection.edges = newEdges;
            intersection.discrete += this.discrete;
            return intersection;
        },
        union: function (graph) {
            let newEdges = JSON.parse(JSON.stringify(this.edges));
            Object.entries(graph.edges).forEach(([k, v]) => {
                if (newEdges[k]) {
                    Object.entries(v).forEach(([node, weight]) => {
                        if (newEdges[k][node]) {
                            newEdges[k][node] += weight;
                        } else {
                            newEdges[k][node] = weight;
                        }
                    });
                } else {
                    newEdges[k] = JSON.parse(JSON.stringify(v));
                }
            });
            let union = new Graph(this.isDirected);
            union.edges = newEdges;
            union.discrete += this.discrete;
            return union;
        },
        difference: function (graph) {
            let diffNodes = this.nodes().filter(e => { return !graph.nodes().includes(e); })
            let diffEdges = JSON.parse(JSON.stringify(this.edges));
            Object.entries(diffEdges).forEach(([k, v]) => {
                //对于当前graph，如果邻接的graph里有相同的边，则pop该边
                if (graph.edges[k]) {
                    Object.entries(v).forEach(([node, weight]) => {
                        if (graph.edges[k].hasOwnProperty(node)) {
                            delete diffEdges[k][node];
                            if (!Object.keys(diffEdges[k]).length) {
                                delete diffEdges[k];
                            }

                        }
                    });
                }
            });
            let difference = new Graph(this.isDirected);
            difference.edges = diffEdges;
            difference.diffNodes = diffNodes;
            return difference;
        },// merge graphs ====== end
        // node betweenness centrality ====== start
        /*
        calculate node betweenness of all nodes in graph
        return {int node_id : int unnormalized betweenness}
        */
        nodeBetweenness: function () {
            var nodeBetweenness = {};
            this.nodes().forEach(v => nodeBetweenness[v] = 0);
            this.nodes().forEach(source => this._calculateNodeBetweenness(source, nodeBetweenness));
            if (!this.isDirected) {
                Object.keys(nodeBetweenness).forEach(key => nodeBetweenness[key] /= 2);
            }
            return nodeBetweenness;
        },
        _calculateNodeBetweenness: function (source, betweenness) {
            let shortestPaths = this._dijkstra(source);
            Object.entries(shortestPaths).forEach(([dist, paths]) => {
                let freq = {};
                paths.flat().forEach(e => {
                    if (e != source) {
                        if (freq[e]) {
                            freq[e]++;
                        } else {
                            freq[e] = 1;
                        }
                    }
                });
                Object.entries(freq).forEach(([k, v]) => {
                    betweenness[k] += v / paths.length;
                })
            });
        },
        /*
        shortest paths from source to all nodes
        return {int distination : [[int]]}   if [[]] then no path from source to distination
        */
        _dijkstra: function (source) {
            let dist = {};
            let path = {};
            let Q = {};
            this.nodes().forEach(key => {
                dist[key] = key == source ? 0 : Infinity;
                path[key] = [[]];
                Q[key] = dist[key];
            });
            while (Object.keys(Q).length) {
                let u = Object.keys(Q).reduce((key, v) => Q[v] < Q[key] ? v : key);
                if (!isFinite(dist[u])) break;
                delete Q[u];
                Object.keys(this.edges[u]).forEach(v => {
                    let alt = dist[u] + 1;
                    if (alt < dist[v]) {
                        dist[v] = alt;
                        path[v] = this._cloneArray(path[u]);
                        path[v].forEach(array => array.push(u))
                        Q[v] = alt;
                    } else if (alt == dist[v]) {
                        let newPath = this._cloneArray(path[u]);
                        newPath.forEach(array => array.push(u));
                        path[v] = path[v].concat(newPath);
                    }
                });
            };
            delete path[source];
            return path
        },// node betweenness centrality ====== end
        // edge betweenness centrality ====== start
        /*
        calculate edge betweenness of all nodes in graph
        return {int vertex_id : {int vertex_id : float unnormalized betweenness}}
        */
        edgeBetweenness: function () {
            var edgeBetweenness = {};
            Object.entries(this.edges).forEach(([u, value]) => {
                edgeBetweenness[u] = {};
                value.forEach(v => {
                    edgeBetweenness[u][v] = 0;
                });
            });
            this.nodes().forEach(source => this._calculateEdgeBetweenness(source, edgeBetweenness));
            if (!this.isDirected) {
                Object.keys(edgeBetweenness).forEach(key => Object.keys(edgeBetweenness[key]).forEach(k => edgeBetweenness[key][k] /= 2));
            }
            return edgeBetweenness;
        },
        _calculateEdgeBetweenness: function (source, betweenness) {
            let shortestPaths = this._dijkstra(source);
            let verticesDepth = {} //{int level : [vertices]}
            Object.entries(shortestPaths).forEach(([dist, paths]) => { //indicate the level vertices in a shortest paths graph which rooted by u
                let depth = paths[0].length;
                if (depth) {
                    if (depth in verticesDepth) {
                        verticesDepth[depth].push(dist);
                    } else {
                        verticesDepth[depth] = [dist]
                    }
                }
            });
            let flow = {};
            Object.keys(verticesDepth).sort().reverse().forEach(lvl => {
                verticesDepth[lvl].forEach(v => { //for every vertices in current level
                    if (flow[v]) { //if vertex has in-flow from deep level
                        flow[v]++;
                    } else {
                        flow[v] = 1;
                    }
                    let prevs = {};
                    shortestPaths[v].forEach(array => {
                        let p = array[lvl - 1];
                        let pct = (p == source ? 1 : shortestPaths[p].length) / shortestPaths[v].length;
                        prevs[p] = pct.toFixed(2);
                    });
                    Object.entries(prevs).forEach(([p, pct]) => {
                        let f = pct * flow[v];
                        betweenness[v][p] += f;
                        betweenness[p][v] += f;
                        if (flow[p]) {
                            flow[p] += f;
                        } else {
                            flow[p] = f;
                        }

                    });
                });
            });
        },// edge betweenness centrality ====== end
        activeDensity: function () {
            let R = this.countEdges();
            let N = this.countVertices();
            return (2 * R / (N * (N - 1))).toFixed(5);
        },
        _disconnectedSubgraphs: function () {
            let output = []
            Object.entries(this.edges).forEach((k, v) => {
                let lst = Object.keys(v)
                lst.push(String(k))
                output.push(new Set(lst));
            });
            for (let i = output.length - 1; i > 0; i--) {
                for (let j = i - 1; j >= 0; j--) {
                    let union = new Set([...output[i], ...output[j]])
                    if (union.size < output[i].size + output[j].size) {
                        output.splice(i, 1);
                        output[j] = union;
                        break;
                    }
                }
            }
            return output;
        },
        disconnected: function () {
            return this._disconnectedSubgraphs().length;
        },

        // serialize ====== start
        serializeEdges: function (isWeighted) {
            let output = [];
            Object.entries(this.edges).forEach(([k, v]) => {
                Object.entries(v).forEach(([e, w]) => {
                    if (this.isDirected || k < e) {
                        let w0 = 3;
                        let w1 = 5 ;
                        let pct = Math.round((w / this.discrete) * 100) / 100;
                        let width = isWeighted ? w1 * pct : w0;
                        output.push({
                            source: k,
                            target: e,
                            lineStyle: {
                                width: width,
                                color: 'dimgrey'
                            },
                            label: {
                                formatter: `${k}${this.isDirected ? '>' : '—'}${e}${isWeighted? ' : '+ pct : ''}`,
                                padding: [3, 0]
                            },
                            emphasis: {
                                label: {
                                    show: true
                                }
                            }
                        });
                    }
                });
            });
            return output;
        }
    }














    function DynamicNetwork(isDirected = false) {
        this.nodes = {}
        this.relationships = {}
        this.features = {}
        this.timeSeries;
    }
    DynamicNetwork.prototype = {
        _addNode: function (node) {
            this.nodes[node.id] = Object.keys(node).reduce((object, key) => {
                if (key != 'id') {
                    object[key] = node[key];
                    this.features[key] = this.features[key] || [];
                    this.features[key].push(node[key]);
                }
                return object
            }, {});
        },

        addNodes: function (nodes) {
            nodes.forEach(e => this._addNode(e));
            Object.entries(this.features).forEach(([k, v]) => {
                this.features[k] = Array.from(new Set(v)).sort();

            });
        },

        _addRelationship: function (edge, isDirected) {
            if (!this.relationships[edge.t]) {
                this.relationships[edge.t] = new Graph(isDirected);
            }
            this.relationships[edge.t].addEdge(edge.i, edge.j);
        },

        addRelationships: function (edges, isDirected = false) {
            edges.forEach(e => this._addRelationship(e, isDirected));
            this.timeSeries = Object.keys(this.relationships);
        },

        getGraph: function (time) {
            return this.relationships[time];
        },

        getListNrOfVertices: function () {
            let output = [];
            console.log(this.nodes);
            Object.entries(this.relationships).forEach(([k, v]) => {
                output.push(v.countVertices())
            });
            return output;
        },

        getListPctOfVertices: function () {
            let ttl = Object.keys(this.nodes).length;
            return this.getListNrOfVertices().map(function (e) { return (e / ttl).toFixed(4) })
        },

        getListNrOfEdges: function () {
            let output = [];
            Object.entries(this.relationships).forEach(([k, v]) => output.push(v.countEdges()));
            return output;
        },

        getListMaximumClique: function () {
            let output = [];
            Object.entries(this.relationships).forEach(([k, v]) => {
                let reporter = [];
                v.maximalCliques(reporter);
                let maximumClique = []
                reporter.forEach(a => {
                    maximumClique = a.length > maximumClique.length ? a : maximumClique;
                });
                output.push(maximumClique.length)
            });
            return output;
        },

        getListActiveDensity: function () {
            let output = [];
            Object.entries(this.relationships).forEach(([k, v]) => output.push(v.activeDensity()));
            return output;
        },

        getListNrOfdisconnected: function () {
            let output = [];
            Object.entries(this.relationships).forEach(([k, v]) => output.push(v.disconnected()));
            return output
        },

        intersectionGraph: function (start, end) {
            let output = this.relationships[start];
            if (end) {
                let keys = Object.keys(this.relationships);
                let currentIdx = keys.indexOf(start);
                let endIdx = keys.indexOf(end);
                for (var i = currentIdx + 1; i <= endIdx; i++) {
                    output = output.intersection(this.relationships[keys[i]]);
                }
            }
            return output;
        },

        unionGraph: function (start, end) {
            let output = this.relationships[start];
            if (end) {
                let keys = Object.keys(this.relationships);
                let currentIdx = keys.indexOf(start);
                let endIdx = keys.indexOf(end);
                for (var i = currentIdx + 1; i <= endIdx; i++) {
                    output = output.union(this.relationships[keys[i]]);
                }
            }
            return output;
        },

        serialize: function (g, all, cate, isWeighted=true) {
            let output = {};
            Object.entries(this.features).forEach(([k, v]) => {
                output[k] = [];
                v.forEach(e => output[k].push({ name: e }));
            });
            output.edges = g.serializeEdges(isWeighted);
            output.nodes = []
            Object.entries(this.nodes).forEach(([k, v]) => {
                if (!all && !g.nodes().includes(String(k))) {
                } else {
                    let obj = {};
                    obj.id = k;
                    obj.category = this.features[cate].indexOf(v[cate]);
                    obj.name = `id: ${k}`;
                    Object.entries(v).forEach(([key, value]) => {
                        if (key != 'id') {
                            obj.name += `\n${key}: ${value}`
                        }
                    })

                    // obj.symbol = 'pin';
                    obj.itemStyle = {
                        // color:'orange',
                        // borderColor : '#00F',
                        // borderWidth : 2,
                    }

                    output.nodes.push(obj);
                }
            });
            return output;
        },

        serializeStatistics: function (g, all, cateS) {
            let cateX = cateS[0];
            let cateY = cateS[1];
            let lstCateX = [...this.features[cateX]];
            let lstCateY = cateX == cateY ? [null] : [...this.features[cateY]];
            let data = Array(lstCateY.length).fill().map(() => Array(lstCateX.length).fill(0));
            g.nodes().forEach(e => {
                let n = this.nodes[e];
                let x = lstCateX.indexOf(n[cateX]);
                let y = lstCateY.indexOf(n[cateY]);
                y = y == -1 ? 0 : y;
                data[y][x]++;
            })
            return {
                x: lstCateX,
                y: lstCateY,
                data: data,
                horizontal: cateS[2]
            }
        },

        serializeColoring: function (series, diffGraph, color) {
            series.nodes.forEach(n => {
                let s = n.id
                if (diffGraph.diffNodes.includes(s)) {
                    n.itemStyle = {
                        borderColor: color,
                        borderWidth: 1.5,
                    }
                }
            });
            series.edges.forEach(e => {
                let s = e.source;
                let t = e.target;
                if (diffGraph.edges[s]) {
                    if (diffGraph.edges[s][t]) {
                        e.lineStyle.color = color;
                    }
                }
            })
            return series;
        }
    }


    return {
        version: VERSION,
        author: AUTHOR,
        DynamicNetwork: DynamicNetwork,
    }
});