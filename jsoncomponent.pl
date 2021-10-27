jc(D,ID,N,I,O,SyncCode,C,X):-
    component(D,ID,N,I,O,SyncCode,C,X).


all(Comp):-
    jc(D,ID,N,I,O,SyncCode,C,X),
    Comp = component{
	    diagram:D,
	    id:ID,
	    name:N,
	    inputs:I,
	    outputs:O,
	    synccode:SyncCode,
	    children:C,
	    connections:X
	}.

allc():-
    bagof(C,all(C),Bag),
    json_write(user_output,Bag).
