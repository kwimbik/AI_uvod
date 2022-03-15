(define (domain transport)
(:predicates (place ?r) (box ?b) (at ?b ?r) (car ?b) (empty ?b) (full ?b) )

(:action load
:parameters (?box  ?car ?place)
:precondition ( and (empty ?car) (box ?box) (place ?place) (car ?car) ( at  ?car ?place) (at ?box ?place))
:effect ( and (full ?car) (at ?box ?car) (not(at ?box ?place))))

(:action unload
:parameters (?box  ?car ?place)
:precondition ( and (full ?car) ( at ?car ?place) (box ?box) (place ?place) (car ?car) (at ?box ?car))
:effect ( and (empty ?car) (at ?box ?place) (not(at ?box ?car)) (not(full ?car))))

(:action move
:parameters (?car ?from ?to )
:precondition (and (at  ?car ?from) (place ?from) (place ?to) (car ?car)) 
:effect (and (at ?car ?to) (not (at ?car ?from)))))



