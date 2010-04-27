import math
from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

def write(xPos, yPos, text, font = GLUT_BITMAP_9_BY_15):
	'''
	Writes text with a bitmap font on the (x,y) position indicated. The 
	optional parameter font specify the GLUT bitmap font to use.
	Available fonts are:
	GLUT_BITMAP_8_BY_13
	GLUT_BITMAP_9_BY_15
	GLUT_BITMAP_TIMES_ROMAN_10
	GLUT_BITMAP_TIMES_ROMAN_24
	GLUT_BITMAP_HELVETICA_10
	GLUT_BITMAP_HELVETICA_12
	GLUT_BITMAP_HELVETICA_18
	'''
	glRasterPos2f(xPos, yPos)
	for c in text:
		glutBitmapCharacter(font, ord(c))
	
def arrowhead(x1, y1, x2, y2, noderadius, arrowwidth, angle = 10):
	'''
	Draws an arrow head on the line segment between the coordinate pairs
	(x1,y1) and (x2,y2). The arrow head is placed in the (x2,y2)-end.
	'''
	Pi = math.pi
	x21 = x2-x1
	if x21==0:
		LineAngle = math.atan(0)
	else:
		LineAngle = math.atan((y2-y1)/(x2-x1))
	
	EndAngle1 = LineAngle + angle * Pi/180
	EndAngle2 = LineAngle - angle * Pi/180
	
	xOffset = noderadius * math.cos(LineAngle)
	yOffset = noderadius * math.sin(LineAngle)
		
	if x1 < x2:
		x2 -= xOffset
		y2 -= yOffset
		
		Y3 = y2 - arrowwidth * math.sin(EndAngle1)
		Y4 = y2 - arrowwidth * math.sin(EndAngle2)
		X3 = x2 - arrowwidth * math.cos(EndAngle1)
		X4 = x2 - arrowwidth * math.cos(EndAngle2)
	else:
		x2 += xOffset
		y2 += yOffset
		
		Y3 = y2 + arrowwidth * math.sin(EndAngle1)
		Y4 = y2 + arrowwidth * math.sin(EndAngle2)
		X3 = x2 + arrowwidth * math.cos(EndAngle1)
		X4 = x2 + arrowwidth * math.cos(EndAngle2)
	
	glBegin(GL_POLYGON);
	glVertex2f(x2,y2);
	glVertex2f(X3,Y3);
	glVertex2f(X4,Y4);
	glEnd();