// 'var xxx;' belongs to the 'global' scope in browsers, but to the module local scope in node.js
// see https://nodejs.org/api/globals.html#globals_global

var atob = require ('atob'); // npm install atob
var pako = require ('pako'); // npm install pako


exports.decodeMxDiagram = (encoded) => {
    //reqDecodeMxDiagram ();
    return inline_decodeMxDiagram (encoded);
}    

function inline_decodeMxDiagram (encoded) {
    //process.stderr.write ('### support.js/decodeMxDiagram ###\n');
    var data = atob (encoded);
    var inf = pako.inflateRaw (
	Uint8Array.from (data, c=>c.charCodeAt (0)), {to: 'string'})
    var str = decodeURIComponent (inf);
    return str;
}

exports.expandStyle = (s) => {
    var sx = s
	.replace(/"/g,'')
	.replace(/ellipse;/g,'kind=ellipse;')
	.replace(/text;/g,'kind=text;')
	.replace (/([^=]+)=([^;]+);/g, '$1="$2" ');
    return sx;
}

exports.resetNames = () => {
    nameIndexTable = [];
    counter = 1;
}

exports.strMangle = (s) => {
        // remove HTML junk added by drawio
    var ret = s
	.replace (/&[^ ]+;/g, '\n')
	.replace (/\\\\/g, '');

    return ret
        // convert names to be acceptable to SWIPL
//	.replace (/-/g, '__')
	.replace (/\\/g, '\\\\')

//	.replace (/ __g /g, ' -g ')
//	.replace (/__q/g, '-q')
    ;
}



var nameIndexTable = [];
var counter = 1;



function newID(name, quoteds, scope) {
    var s = stripQuotes (quoteds. trim ());
    scope.scopeModify (name, s);
    nameIndexTable[s] = counter;
    counter += 1;
    return '';
}

function pushID (name, s, scope) {
    scope.scopeModify (name, namify (s));
    return '';
}

function getID (name, scope) {
    var s = scope.scopeGet (name);
    return refID (s);
}


/// cells
exports.newCellID = (s, scope) => {
    return newID ('cellid', s, scope);
}

exports.pushCellID = (s, scope) => {
    return pushID ('cellid', s, scope);
}

exports.getCellID = (scope) => {
    return getID ('cellid', scope);
}

exports.refCellID = (s) => {
    return refID (s);
}

/// diagrams

exports.newDiagramID = (s, scope) => {
    return newID ('diagramid', s, scope);
}

exports.pushDiagramID = (s, scope) => {
    return pushID ('diagramid', s, scope);
}

exports.getDiagramID = (scope) => {
    return getID ('diagramid', scope);
}


exports.setDiagram = (scope) => {
    var diagramID = getID (scope);
    scope.scopeAdd ('diagram', diagramID);
}

function namify (s) {
    var r = stripQuotes (s).trim ();
    var regex = new RegExp (/^[0-9A-Z]/);
    if (regex.test (r)) {
	r = "x_" + r;
    };
    return r
	.replace (/"/g,'')
	.replace (/-/g,'__')
	.replace (/ /g,'___');
}


function refID (s1, scope) {
    // produce smaller ID's (useful for debugging workbench)
    var s = stripQuotes (s1);
    var n = nameIndexTable[s];
    if (n) {
	return "id" + n.toString();
    } else {
	return namify (s);
    }
}    

function stripQuotes (s) {
    var s1 = s.replace (/^(\")/,'');
    var s2 = s1.replace (/([\"])$/,'');
    var s3 = s2.replace (/^(\")/,'');
    return s3;
}

exports.stripQuotes = (s) => {
    return stripQuotes (s.trim ());
}

exports.mangleNewlines = (s) => {
    return s.replace (/(\r\n|\r|\n)/g,'@~@');
}

/////

const http = require ('http');

const options = { method: 'POST'
};

var data = '';

function sendReq (fn_OK) {
    let request = http.request ('http://localhost:8000/decodeMxDiagram',
				options,
				(res) => {
				    if (res.statusCode !== 201) {
					console.error (`Did not get an OK from the server. Code ${res.statusCode}`);
					res.resume ();
					return;
				    }
				
				    res.on('data', (chunk) => { 
					data += chunk;
				    });
				    res.on('close', () => {
					return fn_OK (data);
				    });
				    
				    request.on('error', (err) => {
					console.error (err);
				    });
				});
    const reqData = { message: "hello" };
    request.write (JSON.stringify (reqData));
    request.end ();
}


async function reqDecodeMxDiagram () { 
    var p = (() => new Promise (fn_resolve => sendReq (fn_resolve))) ();
    var returneddata = await p; 
    return returneddata;
}

// var r = areq ();
// (async () => { console.log (await r); })();
