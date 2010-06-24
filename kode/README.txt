To run the application you run:
python reductiongraphvisualizer.py

Dependencies for this are:
gtk, pygraphviz, cairo, numpy, scipy

These are available in most linux package management systems. If you are on a
GNOME system you already have "gtk" and "cairo" installed.
We have tested with python 2.6, but it should work with other versions. We can
not guarantee it though.
On Ubuntu (or other debian based system) you install the packages with the
following commands:
 - sudo apt-get install python-numpy
 - sudo apt-get install python-scipy
 - sudo apt-get install python-pygraphviz

Shortcuts in the application:
Forward:			Ctrl+f or Ctrl+n
Back:				Ctrl+b or Ctrl+p
Redraw graph:		Ctrl+o
Optimize graph:		Ctrl+r

Lambda term:
When entering a lambda term in the "Lambda Term" text field you can use both λ
and # as the lambda character. If you enter a lambda term, which is
syntactical incorrect the background color in the text field changes to red.

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
should furthermore be aware that, because of bezier curves, the "dot" will
look weird dragging nodes because it is not possible to re-calculate the
bezier curve positions in the behind pygraphviz graph.

examples of interesting lambda terms from the results section in the report:
cons(2,3):					λx.(λy.(λx.(λy.(λs.(sxy)))λx.(λy.y)(λx.(λy.(λs.(sxy)))xy)))λf.(λx.(f(fx)))λf.(λx.(f(f(fx))))
cons(5,0):					λx.(λy.(λx.(λy.(λs.(sxy)))λx.(λy.y)(λx.(λy.(λs.(sxy)))xy)))λf.(λx.(f(f(f(fx)))))λf.(λx.(x))
cons(4,4):					λx.(λy.(λx.(λy.(λs.(sxy)))λx.(λy.y)(λx.(λy.(λs.(sxy)))xy)))λf.(λx.(f(f(fx))))λf.(λx.(f(f(fx))))
Successor to 5:				#n.(#f.(#x.(f (n f x)))) #f.(#x.(f (f (f (f (f x))))))
Predecessor to 5:			#n.(#f.(#x.(n (#g.(#h.(h (g f)))) (#u.(x)) (#u.(u))))) #f.(#x.(f (f (f (f (f x))))))
2+2:						#m.(#n.(#f.(#x.(m f (n f x))))) #f.(#x.(f (f x))) #f.(#x.(f (f x)))
2*2							#m.(#n.(#f.(#x.(m (n f) x)))) #f.(#x.(f (f x))) #f.(#x.(f (f x)))
2^2							#m.(#n.(#f.(#x.(m n f x)))) #f.(#x.(f (f x))) #f.(#x.(f (f x)))

The following examples are not as concrete as the ones above, but gives interesting graphs non the less:
1.		#a.(b) (#x.((x x) x) #y.((y y) y))
2.		#f.(#x.(f (x x))) (#x.(f (x x))) #y.((y y) y)
3.		((#b1.(b1) #b2.((#b3.(b2) #b4.((#b5.(b2) b4))))) #b6.((#b7.(b6) #b8.(#b9.(#b10.(#b11.(b11)))))))
4.		(#B1.(#B2.(((#B3.(#B4.(#B5.(#B6.(B1)))) #B7.(#B8.(B7))) (#B9.(B1) #B10.(#B11.(B1)))))) (#B12.(#B13.(B13)) #B14.(#B15.(#B16.((#B17.(B17) B16))))))
5.		λB1.((λB2.(λB3.((λB4.((B4 (λB5.(B1) λB6.(λB7.(B7))))) λB8.(B8)))) B1))
6.		#f.(#x.(f (x x))) (#x.(f (x x))) #y.(y y)
7.		#f.(#x.(f (x x))) (#x.(f (x x))) #x.#y.(y y x)
8.		#f.(#x.(f (x x))) (#x.(f (x x))) #x.#y.(y y x)