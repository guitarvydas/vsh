:- use_module(library(pcre)).

fixupName(Original,Fixed):-
    re_replace(" "/g,"-",Original,Fixed).

    
