all:
	node das2json.js vsh.drawio
	python3 main.py . . "start" main vsh.drawio.json

# dev workflow
dev: das2json.js
	node das2json.js vsh.drawio
	python3 main.py . . "start" main vsh.drawio.json

das2json.js : ~/projects/jdas2json/das2json.js
	cp ~/projects/jdas2json/das2json.js .
# end dev workflow

install:
	npm install
