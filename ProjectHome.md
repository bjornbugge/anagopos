# Anagopos #

We present Anagopos, a tool for visualizing reduction graphs of terms in lambda calculus and term rewriting. Anagopos allows step-by-step generation of reduction graphs under 6 different graph drawing algorithms.

> - Niels Bjørn Bugge Grathwohl, Jeroen Ketema, Jens Duelund Pallesen and Jakob Grue Simonsen

# Executables #
## Debian based systems, e.g. Ubuntu ##
  * Install dependencies with the following command:
```
sudo apt-get install python-pyparsing python-opengl python-wxgtk2.8 python-pygraphviz python-numpy python-scipy
```
  * Download .deb package from: http://anagopos.googlecode.com/files/anagopos_2.0-1_i386.deb
  * Double click and install the aanagopos\_2.0-1\_i386.deb deb-package
  * or run:
```
sudo dpkg -i anagopos_2.0-1_i386.deb
```
It will now be placed under Applications -> Graphics -> Anagopos

## Mac OS X ##
  * Install Graphviz through Macports, Fink, pkgsrc or http://www.ryandesign.com/graphviz/
  * Download the application from http://anagopos.googlecode.com/files/anagopos_2.0.1.app.zip
  * Unzip it and start it.

# Get source code #
To get the latest stable release of the source code run:
```
svn checkout http://anagopos.googlecode.com/svn/tags/2.0.1 anagopos-read-only
```
To get the latest development release of the source code run (not guaranteed to work):
```
svn checkout http://anagopos.googlecode.com/svn/trunk anagopos-read-only
```

# Running the source code #
To run the application run the following command in the src directory:
```
python anagopos.py
```
You will need the following dependencies:
```
pyparsing pyopengl wxpython pygraphviz numpy scipy
```

On Debian/Ubuntu you can install these dependenies with the following command:
```
sudo apt-get install python-pyparsing python-opengl python-wxgtk2.8 python-pygraphviz python-numpy python-scipy 
```

On Macports (Mac OS X) you can install these dependenies with the following command:
```
sudo port install python26 py26-parsing py26-opengl py26-wxpython py26-pygraphviz py26-numpy py26-scipy
```