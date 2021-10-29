'use strict';

var componentTable;
let pipenum = 0;
let script;
let componentNames = '';

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
	let pinputs ='';
	let poutputs ='';
	c.pervasiveinputs.forEach (pi => {
	    pinputs = pinputs + " " + pi;
	});
	c.pervasiveoutputs.forEach (po => {
	    poutputs = poutputs + " " + po;
	});
	emitToScript (`./${name} ${pinputs} ${poutputs} ${makeBashInput (bv (c.inpipe))} ${makeBashOutput (bv (c.outpipe))} &\n${name}_pid=\$\!`);
    });
}

function emitChildWaits (children) {
    children.forEach (name => {
	emitToScript (`wait \$${name}_pid`);
    });
}


function emitPipes (pipeNames) {
    pipeNames.forEach (p => {
	emitToScript (`${p}=pipe\${RANDOM}\nmkfifo ${bv(p)}`);
    });
}

function emitRMPipes (pipeNames) {
    pipeNames.forEach (p => {
	emitToScript (`rm ${bv(p)}`);
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

function endScript (sname) {
    let name = sname.replace (/ /g,'-');
    process.stderr.write (`emitting ${name}\n`);
    fs.writeFileSync (name, script);
    componentNames += ' ' + name;
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
    sourceComponent.outpipe = `${pipeName}`;
    targetComponent.inpipe = `${pipeName}`;
}

function emitToScript (code) {
    // see https://www.w3.org/wiki/Common_HTML_entities_used_for_typography
    let s = code;
    script += (s + '\n');
}

function bashVariable (s) {
    if (s) {
	return "$" + s;
    } else {
	return s;
    }
}

function bv (s) {
    return bashVariable (s);
}

function makeBashInput (s) {
    if (s) {
	return "3<" + s;
    } else {
	return '';
    }
}

function makeBashOutput (s) {
    if (s) {
	return "4>" + s;
    } else {
	return '';
    }
}

var fs = require ('fs');
var components_string = fs.readFileSync (process.argv [2]);
var components = JSON.parse(components_string);
gatherComponents (components);
createPipeNames (components);
emit (components);
console.log (componentNames);
