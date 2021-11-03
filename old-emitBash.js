var componentTable;
let pipenum = 0;
let script;

function emit (components) {
    let toplevel = null;
    let pipenum = 0;
    components.forEach (c => {
	if (c.toplevelcomponent) {
	    // no op
	} else if (c.synccode !== '') {
	    // no op
	} else if (c.connections.length > 0) {
	    emitAsyncContainerComponent (c);
	} else {
	    emitAsyncLeafComponent (c);
	}
    });
}

function emitAsyncLeafComponent (c) {
    newScript (c.name);
    let synccode = lookup (c.children[0]).synccode;
    emitToScript (synccode);
    endScript (c.name);
}

function emitAsyncContainerComponent (c) {
    newScript (c.name);
    emitPipes (c.pipes);
    emitChildComponents (c.children);
    emitChildWaits (c.children);
    emitRMPipes (c.pipes);
    endScript (c.name);
}

function emitChildComponents (children) {
    children.forEach (name => {
	let c = lookup (name);
	emitToScript (`./${name} ${c.inpipe} ${c.outpipe} &\n${name}_pid=\$\!`);
    });
}

function emitChildWaits (children) {
    children.forEach (name => {
	emitToScript (`wait \$${name}_pid`);
    });
}

function emitPipes (pipeNames) {
    pipeNames.forEach (p => {
	emitToScript (`mkfifo ${p}`);
    });
}

function emitRMPipes (pipeNames) {
    pipeNames.forEach (p => {
	emitToScript (`rm ${p}`);
    });
}

function lookup (name) {
    let component = componentTable [name];
    if (component) {
	return componentTable[name];
    } else {
	console.log (`lookup ${name}`);
	throw "lookup";
    }
}

function newScript (name) {
    script = '';
    emitToScript ('#!/bin/bash');
    emitToScript (`# ${name}`);
}

function endScript (name) {
    console.error ('writing');
    console.error (name);
    fs.writeFileSync (name, script);
}

function gatherComponents (components) {
    // make a table of components (for easier access in subsequent passes)
    componentTable = [];
    components.forEach (c => {
	if (c.toplevelcomponent) {
	    // no op
	} else {
	    componentTable [c.name] = c;
	    c.inpipe = '';
	    c.outpipe = '';
	}
    });
}	

function createPipeNames (components) {
    components.forEach (c => {
	if (c.toplevelcomponent) {
	    // no op
	} else if (c.connections && c.connections.length > 0) {
	    // composite Component
	    c.pipes = [];
	    c.connections.forEach (conn => {
		makePipeName (c, lookup (conn.source.component), lookup (conn.target.component));
	    });
	}
    });
}
function makePipeName (container, sourceComponent, targetComponent) {
    let pipeName = `pipe${pipenum}`;
    pipenum += 1;
    container.pipes.push (pipeName);
    sourceComponent.inpipe = `4>${pipeName}`;
    targetComponent.outpipe = `3<${pipeName}`;
}

function emitToScript (s) {
    script += (s + '\n');
}


var fs = require ('fs');
var components_string = fs.readFileSync ('7.json');
var components = JSON.parse(components_string);
gatherComponents (components);
createPipeNames (components);
emit (components);
