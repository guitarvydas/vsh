:- dynamic edge/2.
:- dynamic ellipse/2.

component(C):-
    rect(C,_),
    \+ codebox(C).

port(P):-
    ellipse(P,_).

codebox(C):-
    rect(C,_),
    fillColor(C,"red").

component(Diagram,C,Name,Ins,Outs,IIns,IOuts,SyncCode,Children,Connections) :-
    leafcomponent(Diagram,_,_,C),
    rect(C,_),
    componentname(C,Name),
    hasport(C),
    inputsof(C,Ins),
    outputsof(C,Outs),
    pervasiveinputsof(C,IIns),
    pervasiveoutputsof(C,IOuts),
    componentcode(C,SyncCode),
    childrenOf(C,Children),
    connectionsOf(C,Connections).

leafcomponent(D,MXG,ROOT,LeafComponent):-
    diagram(D,_),contains(D,MXG),contains(MXG,ROOT),contains(ROOT,LeafComponent).

leafcomponent(LeafComponent):-
    diagram(D,_),contains(D,MXG),contains(MXG,ROOT),contains(ROOT,LeafComponent).

inputsof(C,InBag):-
    inputof(C,_),
    bagof(I,inputof(C,I),InBag).
inputsof(C,[]) :- \+ inputof(C,_).

outputsof(C,InBag):-
    outputof(C,_),
    bagof(I,outputof(C,I),InBag).
outputsof(C,[]) :- \+ outputof(C,_).

hasport(C):-
    inputof(C,_).
hasport(C):-
    pervasiveinputof(C,_).
hasport(C):-
    outputof(C,_).
hasport(C):-
    pervasiveoutputof(C,_).

pervasiveinputsof(C,InBag):-
    pervasiveinputof(C,_),
    bagof(I,pervasiveinputof(C,I),InBag).
pervasiveinputsof(C,[]):- \+ pervasiveinputof(C,_).

pervasiveoutputsof(C,InBag):-
    pervasiveoutputof(C,_),
    bagof(I,pervasiveoutputof(C,I),InBag).
pervasiveoutputsof(C,[]):- \+ pervasiveoutputof(C,_).

    

childrenOf(C,Children):-
    childof(C,_),
    bagof(Child,childof(C,Child),Children),!.
childrenOf(_,[]).

connectionsOf(C,Connections):-
    connectionOf(C,_),
    bagof(Conn,connectionOf(C,Conn),Connections),!.
connectionsOf(_,[]).
    

toplevelComponent(Diagram,C):-
    diagramContains(Diagram,C),
    rect(C,_),
    value(C,_),
    \+ contains(_,C).

childComponent(Diagram,C):-
    diagramContains(Diagram,C),
    rect(C,_),
    value(C,_).

alltoplevelComponentsOnDiagram(Diagram,Bag):-
    setof(C,toplevelComponent(Diagram,C),Bag).

allchildrenComponents(C,Bag):-
    setof(Child,contains(C,Child),Bag).

inputof(C,Name):-
    ellipse(I,_),
    contains(C,I),
    fillColor(I,"green"),
    componentname(I,Name).

outputof(C,Name):-
    ellipse(O,_),
    contains(C,O),
    fillColor(O,"yellow"),
    componentname(O,Name).

pervasiveinputof(C,Name):-
    ellipse(I,_),
    contains(C,I),
    fillColor(I,"red"),
    componentname(I,Name).

pervasiveoutputof(C,Name):-
    ellipse(O,_),
    contains(C,O),
    fillColor(O,"purple"),
    componentname(O,Name).

childof(C,Name):-
    contains(C,Child),
    rect(Child,_),
    componentname(Child,Name).

connectionOf(C,connection{name:ConnectionName,source:pair{component:SourceName,port:SourcePort},target:pair{component:TargetName,port:TargetPort}}):-
    contains(C,E),
    edge(E,_),
    source(E,SC),
    componentname(SC,SourcePort),
    contains(SourceParent,SC),
    getname(SourceParent,SourceName),
    target(E,TC),
    componentname(TC,TargetPort),
    contains(TargetParent,TC),
    getname(TargetParent,TargetName),
    gensym(x,ConnectionName).
    
