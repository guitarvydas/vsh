var grammar = `
test {
  main = space* any space*
}
`;

var str = '#';

var ohm = require ('ohm-js');
var fs = require ('fs');

var parser = ohm.grammar (grammar);

var cst = parser.match (str);

if (cst.succeeded ()) {
    console.log ('OK');
} else {
    var pos = cst._rightmostFailurePosition;
    console.error (parser.trace (grammar).toString ());
    console.log ("FAIL: at position " + pos.toString ());
}

var fstr = fs.readFileSync ('test.txt');
cst = parser.match (fstr);
if (cst.succeeded ()) {
    console.log ('OK');
} else {
    var pos = cst._rightmostFailurePosition;
    console.error (parser.trace (grammar).toString ());
    console.log ("FAIL: at position " + pos.toString ());
}

var crfstr = fs.readFileSync ('create-rect-facts');
cst = parser.match (fstr);
if (cst.succeeded ()) {
    console.log ('OK');
} else {
    var pos = cst._rightmostFailurePosition;
    console.error (parser.trace (grammar).toString ());
    console.log ("FAIL: at position " + pos.toString ());
}
