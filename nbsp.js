var grammar = `
unhtml {
  text = htmlchar*
  htmlchar =
      "&nbsp; " -- nbsp
    | "&amp;"  -- amp
    | any      -- any
}
`;

var str = `
#!/bin/bash
# create rect facts
<p class=&quot;p1&quot; style=&quot;margin: 0px ; font-stretch: normal ; font-size: 11px ; line-height: normal ; font-family: &#34;menlo&#34;&quot;><span class=&quot;s1&quot;>## create rect fact for every vertex that is not an edge/ellipse/text</span></p><p class=&quot;p1&quot; style=&quot;margin: 0px ; font-stretch: normal ; font-size: 11px ; line-height: normal ; font-family: &#34;menlo&#34;&quot;><span class=&quot;s1&quot;>## sequence.drawio file contains vertexes, and marks all edge and ellipse (and text)</span></p><p class=&quot;p1&quot; style=&quot;margin: 0px ; font-stretch: normal ; font-size: 11px ; line-height: normal ; font-family: &#34;menlo&#34;&quot;><span class=&quot;s1&quot;>## but does not mark rectangles (the default)</span></p><p class=&quot;p1&quot; style=&quot;margin: 0px ; font-stretch: normal ; font-size: 11px ; line-height: normal ; font-family: &#34;menlo&#34;&quot;><span class=&quot;s1&quot;>## this pass finds the defaults and creates explicit rect(...) facts</span></p><p class=&quot;p1&quot; style=&quot;margin: 0px ; font-stretch: normal ; font-size: 11px ; line-height: normal ; font-family: &#34;menlo&#34;&quot;><span class=&quot;s1&quot;>swipl -q &#92;</span></p><p class=&quot;p1&quot; style=&quot;margin: 0px ; font-stretch: normal ; font-size: 11px ; line-height: normal ; font-family: &#34;menlo&#34;&quot;><span class=&quot;s1&quot;><span class=&quot;Apple-converted-space&quot;>&nbsp; &nbsp; &nbsp; </span>-g 'consult(5).' &#92;</span></p><p class=&quot;p1&quot; style=&quot;margin: 0px ; font-stretch: normal ; font-size: 11px ; line-height: normal ; font-family: &#34;menlo&#34;&quot;><span class=&quot;s1&quot;><span class=&quot;Apple-converted-space&quot;>&nbsp; &nbsp; &nbsp; </span>-g 'consult(rects).' &#92;</span></p><p class=&quot;p1&quot; style=&quot;margin: 0px ; font-stretch: normal ; font-size: 11px ; line-height: normal ; font-family: &#34;menlo&#34;&quot;><span class=&quot;s1&quot;><span class=&quot;Apple-converted-space&quot;>&nbsp; &nbsp; &nbsp; </span>-g 'printRects.' &#92;</span></p><p class=&quot;p1&quot; style=&quot;margin: 0px ; font-stretch: normal ; font-size: 11px ; line-height: normal ; font-family: &#34;menlo&#34;&quot;><span class=&quot;s1&quot;><span class=&quot;Apple-converted-space&quot;>&nbsp; &nbsp; &nbsp; </span>-g 'halt.' &#92;</span></p><p class=&quot;p1&quot; style=&quot;margin: 0px ; font-stretch: normal ; font-size: 11px ; line-height: normal ; font-family: &#34;menlo&#34;&quot;><span class=&quot;s1&quot;><span class=&quot;Apple-converted-space&quot;>&nbsp; &nbsp; &nbsp; </span>> 6.pl</span></p><p class=&quot;p2&quot; style=&quot;margin: 0px ; font-stretch: normal ; font-size: 11px ; line-height: normal ; font-family: &#34;menlo&#34; ; min-height: 13px&quot;><span class=&quot;s1&quot;></span>echo done >/dev/fd/4</p>
`;


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
