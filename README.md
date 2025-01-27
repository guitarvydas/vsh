# demo of Visual SHell
- this demo draws a trivial shell script using draw.io
- compiles and runs with output formatted as JSON
- uses das2json.js to transpile the draw.io file to JSON (vsh.drawio -> vsh.drawio.json)
- uses 0D (kernel0d.py) to run the program
- supports fan-out and composition of software parts
# diagram
![vsh.drawio](vsh-main.drawio.svg)
# usage
make
## expected output
The actual output depends on what processes are running on your system and are picked up by the "ps" command.

I see:
```
[
{"":"PID TTY           TIME CMD
  599 ttys000    0:00.02 -zsh
  602 ttys001    0:00.02 -zsh
  615 ttys002    0:00.02 -zsh
  639 ttys003    0:00.02 -zsh
  668 ttys004    0:00.02 -zsh
 7601 ttys005    0:00.40 -zsh
  714 ttys006    0:00.02 -zsh
62494 ttys007    0:00.07 /bin/zsh -i
89482 ttys008    0:00.83 -zsh
  904 ttys010    0:00.07 -zsh
 1829 ttys011    0:00.01 /Library/Developer/CommandLineTools/usr/bin/make
 1839 ttys011    0:00.03 /opt/homebrew/Cellar/python@3.13/3.13.1/Frameworks/Python.framework/Versions/3.13/Resources/Python.app/Contents/MacOS/Python main.py . . start main vsh.drawio.json
97472 ttys011    0:00.10 -zsh
  990 ttys012    0:01.80 -zsh
68815 ttys012    0:00.02 /Library/Developer/CommandLineTools/usr/bin/make
68842 ttys012    1:30.66 /Users/paultarvydas/.gem/ruby/3.3.5/bin/jekyll serve    
68885 ttys012    0:03.55 /Users/paultarvydas/.gem/ruby/3.3.5/gems/rb-fsevent-0.11.2/bin/fsevent_watch --format=otnetstring --latency 0.1 /Users/paultarvydas/Desktop/blogs/indir/guitarvydas
 1016 ttys013    0:00.09 -zsh
18368 ttys013    2:22.07 /opt/homebrew/Cellar/python@3.13/3.13.1/Frameworks/Python.framework/Versions/3.13/Resources/Python.app/Contents/MacOS/Python -m http.server"}
,
{"processes":"19"}
,
{"grep":"1839 ttys011    0:00.03 /opt/homebrew/Cellar/python@3.13/3.13.1/Frameworks/Python.framework/Versions/3.13/Resources/Python.app/Contents/MacOS/Python main.py . . start main vsh.drawio.json"}
]
```
# disclaimer
This demo is just a simple demo that shows that a number of programming languages can be used to produce a DPL (Diagrammatic Programming Language) version of the Bourne Shell. This demo focuses mainly on multi-branching and pipes and excludes many of the features of a full-blown shell (I would argue that, if you have pipes and composition of parts, you don't really need the rest of the features since you can get the same result by simply using parts built in various languages).

It is intended that the kernel be automatically generated from a higher level description. But, that's another project ("rt") and this kernel0d.py was slightly modified by hand (mostly to format the output as JSON).

This demo has only been lightly tested.
