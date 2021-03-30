"use strict";
function DynamicNetwork(serialized) {

    if (serialized) {
        alert('shit');
    }

    var nodes = {}
    var edges = {}

    function _addNode(node) {
        nodes[node.id] = Object.keys(node).reduce((object, key) => {
            if (key != 'id') {object[key] = node[key]}
            return object
        }, {})
    }

    function addNodes(nodes) {
        nodes.forEach(e => { _addNode(e) });
    }

    // function _addEdge(edge){
    //     edge
    // }

    // function addEdges(){}



    return {
        nodes: nodes,
        edges: edges,
        addNodes: addNodes
    };
}


