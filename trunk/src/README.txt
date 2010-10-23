# Reduction Visualizer. A tool for visualization of reduction graphs.
# Copyright (C) 2010 Niels Bjørn Bugge Grathwohl & Jens Duelund Pallesen
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

To run the application you run:
python reductiongraphvisualizer.py

We have used the following:
 - gtk 2.16.0
 - pygraphviz 0.99.1
 - cairo 1.8.8
 - numpy 1.4.1
 - scipy 0.7.2

These are available in most Linux package management systems. If you are on a
GNOME system you already have "gtk" and "cairo" installed.
We have tested with python 2.6, but it should work with other versions. 
On Ubuntu (or other Debian based systems) you install the packages with the
following commands:
 - sudo apt-get install python-numpy
 - sudo apt-get install python-scipy
 - sudo apt-get install python-pygraphviz


Shortcuts in the application:
Forward:            Ctrl+f or Ctrl+n
Back:               Ctrl+b or Ctrl+p
Redraw graph:       Ctrl+o
Optimize graph:     Ctrl+r

Lambda term:
When entering a lambda term in the "Lambda Term" text field you can use both λ
and # as the lambda character. If you enter a lambda term, which is
syntactically incorrect, the background color in the text field changes to red.

Start:
In the "Start" text field you can enter the generation from which the first
graph should be generated from. If you enter a number higher than the number
of generations available from the current lambda term, the background color in
the text field changes to red.

Clicking on nodes:
You can click on any given node to see it's lambda term. It will be displayed
in the "Clicked term" text field. When you click on a node all outgoing edges
will furthermore be highlighted.

Dragging nodes:
You can drag nodes around as you wish. If you have chosen either "Neato" or
"Neato Animated" the graph will update the layout slightly after you have
dragged the node. This is not possible with any of the other graphs. You
should furthermore be aware that, because of bezier curves, the "Dot" will
look weird dragging nodes because it is not possible to re-calculate the
bezier curve positions in the PyGraphviz graph underneath.

examples of interesting lambda terms from the results section in the report:
cons(2,3):                  #x.(#y.(#x.(#y.(#s.(sxy)))#x.(#y.y)(#x.(#y.(#s.(sxy)))xy)))
                            #f.(#x.(f(fx)))#f.(#x.(f(f(fx))))
cons(5,0):                  #x.(#y.(#x.(#y.(#s.(sxy)))#x.(#y.y)(#x.(#y.(#s.(sxy)))xy)))
                            #f.(#x.(f(f(f(fx)))))#f.(#x.(x))
cons(4,4):                  #x.(#y.(#x.(#y.(#s.(sxy)))#x.(#y.y)(#x.(#y.(#s.(sxy)))xy)))
                            #f.(#x.(f(f(fx))))#f.(#x.(f(f(fx))))
Successor to 5:             #n.(#f.(#x.(f (n f x)))) #f.(#x.(f (f (f (f (f x))))))
Predecessor to 5:           #n.(#f.(#x.(n (#g.(#h.(h (g f)))) (#u.(x)) (#u.(u))))) 
                            #f.(#x.(f (f (f (f (f x))))))
2+2:                        #m.(#n.(#f.(#x.(m f (n f x))))) #f.(#x.(f (f x))) #f.(#x.(f (f x)))
2*2                         #m.(#n.(#f.(#x.(m (n f) x)))) #f.(#x.(f (f x))) #f.(#x.(f (f x)))
2^2                         #m.(#n.(#f.(#x.(m n f x)))) #f.(#x.(f (f x))) #f.(#x.(f (f x)))
Cantor set:                 #x.(x x (x x)) #x.(x x f)
Self-referencing snake:     #x.(x x) #x.(x x) (#x.(x x c) #x.(x x d))
Regular and nice:           #x.(x a) (#x.(x x b) #x.(x x c))
Eight self-references:      #x.(x x x a) (#x.(x x x) #x.(x x))
Cycle:                      #x.(#y.(y y y y x x y)) #x.(#y.(y y y y x x y)) #x.(x)
Cycle with start:           #x.(#y.(x y y y x x y)) #x.(#y.(y y y y x x y)) #x.(x)
Prism:                      #x.(#y.(y y y y x x y)) #x.(#y.(y y y y x x y)) #x.(x)
                            (#x.(#y.(y y y y x x y)) #x.(#y.(y y y y x x y)) #x.(x))
O3 (O3 O3):                 #x.(x x x ) #x.(x x x) (#x.(x x x ) #x.(x x x))
Many self-references:       #x.(x x) (#x.(x x x) (#x.(x x x) #x.( x x)))
3D cube:                    (#x.(x) f) (#x.(x) f) (#x.(x) f)
K_4                         (#x.y) ((#x.y) ((#x.y) (#x.y)))
5-sided regular polygon:    #x.(#y.(y y y x x y)) #x.(#y.(y y y x x y)) #x.(x)
"Ketcher"                   #x.(#y.(y y y y y y y x x y)) #x.(#y.(y y y y y y x x y)) #x.(x)
Finite tube:                #x.(#y.(y y y x x y)) #x.(#y.( y y y x x y)) #x.(x)
                            (#x.(#y.(y y)) #x.(#y.(y y)) #x.(x))
Infinite tube:              #x.(#y.(y y y y y y x x y)) #x.(#y.(y y y y y y x x y)) 
                            #x.(x) (#x.(#y.(x x y)) #x.(#y.(x x y)) #x.(x))
Ball-like, n=6:             #x.(#y.(y y y y y y x x y))  #x.(#y.(y y y y y y x x y)) 
                            #x.(x) (#x.(#y.(y y y y y y x x y)) #x.(#y.(y y y y y y x x y)) 
                            #x.(x))
The graph from Exercise 3.5.5(i) in [Barendregt]:
                            (#x.#y.x (#z.y z y) x) #x.(x) (#x.#y.x (#z.y z y) x)

The following examples are not as concrete as the ones above, but give 
interesting graphs nonetheless:
1.      #a.(b) (#x.((x x) x) #y.((y y) y))
2.      #f.(#x.(f (x x))) (#x.(f (x x))) #y.((y y) y)
3.      ((#b1.(b1) #b2.((#b3.(b2) #b4.((#b5.(b2) b4))))) 
         #b6.((#b7.(b6) #b8.(#b9.(#b10.(#b11.(b11)))))))
4.      (#B1.(#B2.(((#B3.(#B4.(#B5.(#B6.(B1)))) #B7.(#B8.(B7))) (#B9.(B1) #B10.(#B11.(B1)))))) 
         (#B12.(#B13.(B13)) #B14.(#B15.(#B16.((#B17.(B17) B16))))))
5.      #B1.((#B2.(#B3.((#B4.((B4 (#B5.(B1) #B6.(#B7.(B7))))) #B8.(B8)))) B1))
6.      #f.(#x.(f (x x))) (#x.(f (x x))) #y.(y y)
7.      #f.(#x.(f (x x))) (#x.(f (x x))) #x.#y.(y y x)
8.      #f.(#x.(f (x x))) (#x.(f (x x))) #x.#y.(y y x)