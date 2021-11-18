onSameDiagram(A,B):-
    diagramContains(D,A),
    diagramContains(D,B).
    
diagramContains(D,X):-
    diagram(D,_),
    transitivecontains(D,X).

transitivecontains(D,X):-contains(D,X).
transitivecontains(D,X):-contains(D,Y),contains(Y,X).
