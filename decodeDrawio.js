var atob = require ('atob'); // npm install atob
var pako = require ('pako'); // npm install pako
var fs = require ('fs');

function decoder () {
    //console.log ('a');
    //var encoded = fs.readFileSync ('transpile_drawio_to_swipl.drawio', 'utf-8');
    var encoded = fs.readFileSync ('_raw.raw', 'utf-8');
    //console.log ('b');
    //console.log (encoded);
    var data = atob (encoded);
    // console.log ('c');
    // console.log (data);
    // console.log ('c1');
    var d8 = 	Uint8Array.from (data, c=>c.charCodeAt (0));
    //console.log (d8);
    var inf = pako.inflateRaw (d8, {to: 'string'});
    //console.log ('d');
    //console.log (inf);
    var str = decodeURIComponent (inf);
    //console.log ('e');
    //console.log (inf);
    return str;
}


// let decoded = decoder ();
// console.log (decoded);


function justRead () {
    var encoded = fs.readFileSync ('transpile_drawio_to_swipl.drawio', 'utf-8');
    fs.writeFileSync ('_raw3.raw', encoded, null);
}
    
justRead ();
