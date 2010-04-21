from OpenGL.GLUT import *
from OpenGL.GLU import *
from OpenGL.GL import *

def drawtext(xPos, yPos, text):
	glMatrixMode(GL_PROJECTION)
	glPushMatrix()
	glLoadIdentity()
	gluOrtho2D(0.0, GLUT_WINDOW_WIDTH, 0.0, GLUT_WINDOW_HEIGHT)
	
	glMatrixMode(GL_MODELVIEW)
	glPushMatrix()
	glLoadIdentity()
	
	glColor3f(0.0, 1.0, 0.0) # Green
	
	glRasterPos2f(xPos, yPos)
	
	font = GLUT_BITMAP_9_BY_15
	print font
	
	for c in text:
		glutBitmapCharacter(font, c)
	
	# Restore back the matrices.
	
	glMatrixMode(GL_MODELVIEW)
	glPopMatrix()
	
	glMatrixMode(GL_PROJECTION)
	glPopMatrix()