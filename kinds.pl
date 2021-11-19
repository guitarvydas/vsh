isellipse(X):-
    kind(X,"ellipse").

isedge(X):-
    edge(X,_).

istext(_):-false.

isrect(X):-
    rect(X,_).

shape(X,"ellipse"):-kind(X,"ellipse").
shape(X,"edge"):-isedge(X).
shape(X,"text"):-istext(X).
shape(X,"rect"):-isrect(X),\+codebox(X),\+shape(X,"ellipse").
shape(X,"code"):-codebox(X).
