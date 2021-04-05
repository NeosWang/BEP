"use strict";

function DynamicNetwork(serialized) {

    var VERSION = "ver 0.0.1"

    var AUTHOR = "Yichen Wang"

    function Graph(directed) {
        this.edges = {};
        this.directed = directed;
    }
    Graph.prototype = {

        _addVertex: function (node) {
            this.edges[node] = this._adjacent(node)
        },
        _adjacent: function (node) {
            return this.edges[node] || []
        },
        addEdge: function (u, v) {
            u = String(u)
            v = String(v)
            this._addVertex(u);
            this._addVertex(v);
            this._adjacent(u).push(v)
            if (!this.directed) { this._adjacent(v).push(u) }
        },
        nrOfVertices: function () {
            return Object.keys(this.edges).length
        },
        nrOfEdges: function () {
            let output = 0
            Object.entries(this.edges).forEach(([k, v]) => output += v.length / (2 - this.directed));
            return output
        },
        // cliques === start
        maximalCliques: function (reporter, clique = [], candidates = Object.keys(this.edges), excluded = []) {
            if (!candidates.length && !excluded.length) {
                reporter.push(clique);
                return
            }
            let pivot = this._pick_random(candidates) || this._pick_random(excluded);
            (candidates.filter(x => !this.edges[pivot].includes(x))).forEach(v => {  // the nodes which adjoins pivot will not be considered into iteration
                let newCandidates = candidates.filter(x => this.edges[v].includes(x));
                let newExcluded = excluded.filter(x => this.edges[v].includes(x));
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
        },// cliques === end
        // merge graphs === start
        intersection: function (graph) {
            let newEdges = {};
            Object.entries(this.edges).forEach(([k, v]) => {
                if (graph.edges[k]) {
                    let lst = v.filter(x => graph.edges[k].includes(x));
                    if (lst.length) newEdges[k] = lst;
                }
            });
            let intersection = new Graph(this.directed);
            intersection.edges = newEdges;
            return intersection;
        },
        union: function (graph) {
            let newEdges = Object.assign({}, this.edges);
            Object.entries(graph.edges).forEach(([k, v]) => {
                if (newEdges[k]) {
                    newEdges[k] = [...new Set([...newEdges[k], ...graph.edges[k]])];
                } else {
                    newEdges[k] = [...graph.edges[k]];
                }
            })
            let union = new Graph(this.directed);
            union.edges = newEdges;
            return union;
        },// merge graphs === end
        // betweennes centrality === start
        betweennes: function(){
            var Q=[]; //queue
            var S=[]; //stack
            var pred = {}; //list of predecessors on shortest paths from source
            var dist ={};  // distance from source
            var sigma = {} //number of shortest paths from source to key
            var delta ={} //dependency of source on key
            var currentNode = 0;
            var centrality = {};
            Object.keys(this.edges).forEach(key=>this._setCentralityToZero(centrality, key));
            Object.keys(this.edges).forEach(key=>this._calculateCentrality(currentNode,key));
            console.log(currentNode);
            if(!this.directed){
                Object.keys(centrality).forEach(key=>this._divideByTwo(centrality,key));
            }
            return currentNode;
        },
        _setCentralityToZero:function(centrality,key){centrality[key]=0;},
        _divideByTwo: function(centrality,key){centrality[key] /=2;},
        _calculateCentrality:function(currentNode, key){
            // to-do Dijkstra
            currentNode = key;
        }

    }







    if (serialized) {
        alert('shit');
    }

    var nodes = {}
    var relationships = {}

    let _addNode = (node) => {
        nodes[node.id] = Object.keys(node).reduce((object, key) => {
            if (key != 'id') { object[key] = node[key] }
            return object
        }, {});
    }

    let addNodes = (nodes) => nodes.forEach(e => _addNode(e));

    let _addRelationship = (edge, directed) => {
        if (!relationships[edge.t]) { relationships[edge.t] = new Graph(directed); }
        relationships[edge.t].addEdge(edge.i, edge.j);
    }

    let addRelationships = (edges, directed = false) => edges.forEach(e => _addRelationship(e, directed));

    let getTimeline = () => { return Object.keys(relationships); }

    let getListNrOfVertices = () => {
        let output = [];
        Object.entries(relationships).forEach(([k, v]) => output.push(v.nrOfVertices()));
        return output;
    }

    let getListNrOfEdges = () => {
        let output = [];
        Object.entries(relationships).forEach(([k, v]) => output.push(v.nrOfEdges()));
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


    return {
        version: VERSION,
        author: AUTHOR,
        nodes: nodes,
        relationships: relationships,
        addNodes: addNodes,
        addRelationships: addRelationships,
        getTimeline: getTimeline,
        getListNrOfVertices: getListNrOfVertices,
        getListNrOfEdges: getListNrOfEdges,
        getListMaximumClique: getListMaximumClique,
        intersectionGraph: intersectionGraph,
        unionGraph: unionGraph
    };
}


