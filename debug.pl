debug:-
    bagof([C,Syn,Sh,Clr],
	  (
	      leafcomponent(_,_,_,C),
	      rect(C,_),
	      synonym(C,Syn),
	      shape(C,Sh),
	      color(C,Clr)
	  ) ,Bag),
    json_write(user_output,Bag),
    nl.

color(C,Clr):-fillColor(C,Clr),!.
color(_,"").
