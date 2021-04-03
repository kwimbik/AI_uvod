;; Test move box1 from place1 to place2 and box2 from place2 to place1
(define (problem transport)
    (:domain transport)
    (:objects car1 place1 place2 box1 box2 box3)
    (:init
        (car car1)
        (place place1)
        (place place2)
        (box box1)
        (box box2)
        (box box3)
        (empty car1)
        (at box1 place1)
        (at box2 place1)
        (at box3 place2)
        (at car1 place2)
    )
    (:goal (and
        (at box1 place2)
        (at box2 place2)
        (at box3 place1)
    ))
)
