`transpile_drawio_to_swipl.drawio` contains 15 rounded rects, therefore 30 rects in total, but,
after
`pfr helloworld.drawio drawio.ohm drawio.glue $cdir/support.js >_.html`
I see only 10 mxCells in `_.html`.

1. Convert the .drawio file using raw JS and see what the result is.

