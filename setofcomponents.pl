componentDescription(D,Description):-
    jc(D,ID,N,I,O,SyncCode,C,X),
    Description = component{
		      diagram:D,
		      id:ID,
		      name:N,
		      inputs:I,
		      outputs:O,
		      synccode:SyncCode,
		      children:C,
		      connections:X
		  }.
    
setOfComponents(Diagram,Array):-
    setof(C,diagramContains(Diagram,C),Array).
