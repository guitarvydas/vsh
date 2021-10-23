%% jc(D,C):-
%%     component(D,ID,N,I,O,C,X),
%%     format("~w ~w ~w ~w ~w ~w~n",[ID,N,I,O,C,X]).

%% jc(Diagrams):-
%%     bagof(D,jc(D,_),Diagrams).

jc(D,ID,N,I,O,SyncCode,C,X):-
    component(D,ID,N,I,O,SyncCode,C,X).

jc:-
    forall(
	diagram(D,_),
	jcd(D)).

jsonify(Strm,D,ID):-
    jc(D,ID,N,I,O,SyncCode,C,X),
    json_write(Strm,component{
			      diagram:D,
			      id:ID,
			      name:N,
			      inputs:I,
			      outputs:O,
			      synccode:SyncCode,
			      children:C,
			      connections:X
		    }),
    nl(Strm),
    write(Strm,","),
    nl(Strm).


allc:-
    writeTopLevelComponents(user_output),
    nl(user_output),
    writeAllComponents(user_output),
    nl(user_output),!.
allc.

writeAllComponents(Strm):-
    forall(
	diagram(D,_),
	(
	 forall(
	    childComponent(D,ID),
	    jsonify(Strm,D,ID)
	 ),
	 write(Strm,"true]")
	)
    ).

writeTopLevelComponents(Strm):-
    forall(
	diagram(D,_),
	forall(
	    toplevelComponent(D,ID),
	    writeTopLevelComponent(Strm,D,ID)
	)
    ).    

writeTopLevelComponent(Strm,D,ID):-
    write(Strm,"["),
    json_write(Strm,tlc{diagram:D,toplevelcomponent:ID}),
    write(Strm,","),
    nl(Strm).

