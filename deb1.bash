while true
do
    clear
    swipl -g 'use_module(library(http/json))' \
	  -g 'consult(fb).' \
	  -g 'consult(onSameDiagram).' \
	  -g 'consult(kinds).' \
	  -g 'consult(component).' \
	  -g 'consult(names).' \
	  -g 'consult(fixup).' \
	  -g 'consult(code).' \
	  -g 'consult(jsoncomponent).' \
	  -g 'consult(debug).' \
	  -g 'debug.' -g 'halt.'
    read -p 'again?...'
done


