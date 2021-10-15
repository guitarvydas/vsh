
makename(C):-
    codebox(C),
    gensym(code,Name),
    format("factname(~w,\"~w\").~n",[C,Name]),
    !.
makename(C):-
    port(C),
    value(C,Name),
    format("factname(~w,\"~w\").~n",[C,Name]),
    !.
makename(C):-
    component(C),
    value(C,Name),
    format("factname(~w,\"~w\").~n",[C,Name]),
    !.
makename(C):-
    gensym(u,Name),
    format("unknowncomponentname(~w,\"~w\").~n",[C,Name]).

getname(Child,Name):-
    factname(Child,Name),
    !.
getname(_,self).

componentname(C,Name):-
    factname(C,Name).




printNames:-
    forall( component(C),
	    makename(C)
	  ),
    forall( codebox(C),
	    makename(C)
	  ),
    forall( port(C),
	    makename(C)
	  ).
    
    
