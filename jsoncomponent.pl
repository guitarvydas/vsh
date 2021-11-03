jc(D,ID,N,I,O,II,OO,SyncCode,C,X):-
    component(D,ID,N,I,O,II,OO,SyncCode,C,X).


all(Comp):-
    jc(D,ID,N,I,O,II,OO,SyncCode,C,X),
    Comp = component{
	    diagram:D,
	    id:ID,
	    name:N,
	    inputs:I,
	    outputs:O,
	    pervasiveinputs:II,
	    pervasiveoutputs:OO,
	    synccode:SyncCode,
	    children:C,
	    connections:X
	}.

allc():-
    bagof(C,all(C),Bag),
    json_write(user_output,Bag).
