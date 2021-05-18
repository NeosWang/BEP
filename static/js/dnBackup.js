function DynamicNetwork(serialized) {
    "use strict";
    var VERSION = "ver 0.0.1"

    var AUTHOR = "Yichen Wang"


    /*
    edges: obj
    {
        node:{node:weight}
    }
    */
    function Graph(isDirected=false) {
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
                    let adjNode = {};
                    Object.keys(graph.edges[k]).forEach(e=>{
                        if(v[e]){
                            adjNode[e] = v[e]+1
                        }
                    });
                    if (Object.keys(adjNode).length) newEdges[k] = adjNode;
                }
            });
            let intersection = new Graph(this.isDirected);
            intersection.edges = newEdges;
            intersection.discrete += this.discrete;
            return intersection;
        },
        union: function (graph) {
            let newEdges = JSON.parse(JSON.stringify( this.edges));
            Object.entries(graph.edges).forEach(([k, v]) => {
                if (newEdges[k]) {
                    Object.entries(v).forEach(([node,weight])=>{
                        if(newEdges[k][node]){
                            newEdges[k][node] +=weight;
                        }else{
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
            let diffNodes = this.nodes().filter(e=>{return !graph.nodes().includes(e);})
            let diffEdges = JSON.parse(JSON.stringify( this.edges));
            Object.entries(diffEdges).forEach(([k, v]) => {
                //对于当前graph，如果邻接的graph里有相同的边，则pop该边
                if (graph.edges[k]) {
                    Object.entries(v).forEach(([node,weight])=>{
                        if(graph.edges[k].hasOwnProperty(node)){
                            delete diffEdges[k][node];
                            if(!Object.keys(diffEdges[k]).length){
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
            Object.entries(this.edges).forEach(([k, v]) => {
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
        serializeEdges: function(){
            let output=[];
            Object.entries(this.edges).forEach(([k,v])=>{
                Object.keys(v).forEach(e=>{
                    if(this.isDirected){
                        output.push({
                            source:k,
                            target:e,
                            lineStyle:{
                                width:2.5, 
                                // color:'LightGray'
                            }
                        })
                    }else{
                        if(k<e){
                            output.push({
                                source:k,
                                target:e,
                                lineStyle:{
                                    width:2.5,
                                    // color:'LightGray'
                                }
                            })
                        }
                    }
                })
            });
            return output;
        }
    }













    if (serialized) {
        alert('shit');
    }

    var nodes = {}
    var relationships = {}
    var features = {}


    let _addNode = (node) => {
        nodes[node.id] = Object.keys(node).reduce((object, key) => {
            if (key != 'id') { 
                object[key] = node[key];
                features[key] = features[key] || [];
                features[key].push(node[key]);
            }
            return object
        }, {});
    }

    let addNodes = (nodes) => {
        nodes.forEach(e =>_addNode(e));
        Object.entries(features).forEach(([k,v])=>{
            features[k]=Array.from( new Set(v)).sort();

        });        

    }

    let _addRelationship = (edge, isDirected) => {
        if (!relationships[edge.t]) {
            relationships[edge.t] = new Graph(isDirected); 
        }
        relationships[edge.t].addEdge(edge.i, edge.j);
    }

    let addRelationships = (edges, isDirected = false) => {
        edges.forEach(e => _addRelationship(e, isDirected));
        console.log(Object.keys(relationships));
    }

    let getGraph = (time)=>{
        return relationships[time];
    }

    let getTimeline = () => { return Object.keys(relationships); }

    let getListNrOfVertices = () => {
        let output = [];
        Object.entries(relationships).forEach(([k, v]) => output.push(v.countVertices()));
        return output;
    }

    let getListPctOfVertices = () =>{
        let ttl = Object.keys(nodes).length;
        return getListNrOfVertices().map(function(e) { return (e/ttl).toFixed(4) })
    }

    let getListNrOfEdges = () => {
        let output = [];
        Object.entries(relationships).forEach(([k, v]) => output.push(v.countEdges()));
        return output;
    }

    let getListMaximumClique = () => {
        let output = [];
        Object.entries(relationships).forEach(([k, v]) => {
            let reporter = [];
            v.maximalCliques(reporter);
            let maximumClique = []
            reporter.forEach(a => {
                maximumClique = a.length > maximumClique.length ? a : maximumClique;
            });
            output.push(maximumClique.length)
        });
        return output;
    }

    let getListActiveDensity = () => {
        let output = [];
        Object.entries(relationships).forEach(([k, v]) => output.push(v.activeDensity()));
        return output;
    }

    let getListNrOfdisconnected = () => {
        let output = [];
        Object.entries(relationships).forEach(([k, v]) => output.push(v.disconnected()));
        return output
    }

    let intersectionGraph = function (start, end) {
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
    }

    let unionGraph = function (start, end) {
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
    }
    /*
    serialize Graph to json array for plot
    param {
        g: Graph,
        all: bool // whether to show all nodes
        cate: str // the feature to be categorized
    }
    return {int node_id : int unnormalized betweenness}
    */
    let serialize = function(g, all, cate){
        let output={};
        Object.entries(features).forEach(([k,v])=>{
            output[k]=[];
            v.forEach(e=> output[k].push({name:e}));
        });
        output.edges = g.serializeEdges();
        output.nodes = []
        Object.entries(nodes).forEach(([k,v])=>{
            if(!all && !g.nodes().includes(String(k))){       
            }else{
                let obj = {};
                obj.id = k;
                obj.category = features[cate].indexOf(v[cate]);
                obj.name = `id:${k}\nclass:${v.class}\ngender:${v.gender}`;

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
    }

    let serializeColoring = function(series, diffGraph, color){
        series.nodes.forEach(n => { 
            let s = n.id
            if(diffGraph.diffNodes.includes(s)){
                n.itemStyle={
                    borderColor : color,
                    borderWidth : 1.5,
                }
            }
        });
        series.edges.forEach(e => {
            let s =  e.source;
            let t =  e.target;
            if(diffGraph.edges[s]){
                if(diffGraph.edges[s][t]){
                    e.lineStyle.color=color;
                }
            }
        })
        return series;
    }

    

    return {
        version: VERSION,
        author: AUTHOR,
        nodes: nodes,
        relationships: relationships,
        features: features,
        timeSeries:timeSeries,
        addNodes: addNodes,
        addRelationships: addRelationships,
        getTimeline: getTimeline,
        getGraph:getGraph,
        getListNrOfVertices: getListNrOfVertices,
        getListPctOfVertices: getListPctOfVertices,
        getListNrOfEdges: getListNrOfEdges,
        getListMaximumClique: getListMaximumClique,
        getListActiveDensity: getListActiveDensity,
        getListNrOfdisconnected: getListNrOfdisconnected,
        intersectionGraph: intersectionGraph,
        unionGraph: unionGraph,
        serialize: serialize,
        serializeColoring:serializeColoring
    };
}







