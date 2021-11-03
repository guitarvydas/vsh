:- dynamic ellipse/2.

portdirection([P,'input']):-
    ellipse(P,_),
    fillColor(P,"green").
portdirection([P,'pervasiveinput']):-
    ellipse(P,_),
    fillColor(P,"red").
portdirection([P,'output']):-
    ellipse(P,_),
    fillColor(P,"yellow").
portdirection([P,'pervasiveoutput']):-
    ellipse(P,_),
    fillColor(P,"purple").
allDirections(Bag):-
    bagof(Pair,portdirection(Pair),Bag).

printDirection([]).
printDirection([H|T]):-
    format("portdirection(~w,~w).~n", H),
    printDirection(T).

printAllDirections:-
    allDirections(Bag),
    printDirection(Bag).
printAllDirections.
