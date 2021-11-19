color(X,"red"):-fillColor (X, "#f8cecc"),!.
color(X,"green"):-fillColor (X, "#d5e8d4"),!.
color(X,"yellow"):-fillColor (X, "#fff2cc"),!.
color(X,"purple"):-fillColor (X, "#9673A6"),!.
color(X,Clr):-fillColor(X,Clr),!.
color(_,"").

makeColor(X):-
    color(X,Clr),
    format("color(~w,~w).~n",[C,Clr]).

makeColors:-
    bagof(X,makeColor(X),_).
