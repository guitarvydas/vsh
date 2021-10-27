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

%% allid(ID):-
%%         jc(D,ID,N,I,O,SyncCode,C,X).

jall:-
    bagof(C,all(C),Bag),
    json_write(user_error,Bag).
