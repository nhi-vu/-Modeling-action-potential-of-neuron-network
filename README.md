# -Modeling-action-potential-of-neuron-network
===================

If you have python3 installed all you need to do is run pip3 neuron.
That being said we only got this to work on a linux machine, we couldn't
make it work on Windows, and did not try on Mac.

Tour of our files
=================

defaults.py
	This hold global constant values that are the defaults for the
		creation of neurons.

nueron.py
	This is home to the neuronal_cell class which manages the
		morphology and biomechanics of individual cells.

network.py
	Creates and manages a collection of neuronal_cells forming them
		into a network specified by an input edge list.

control.py, decreased_potassium_conductance.py, increased_sodium_conductance.py,
	leak_conductance.py

	All of these files run different experiments and are nearly identical 
		but with slight modifications that reflect the names of the
		files.

Running the experiments
=======================

Assuming you have successfully downloaded NEURON it should be easy to run the
experiments. Make sure all of these files are in the same directory and
run "python3 [expirement_name.py]" (e.g. python3 control.py) this will
save 6 figures to the current directory (2 per network morphology).The exact
values of what is being plotted is returned from the stimulate method in the form 
tuple(list[recorded_nueron_1, recorded_nueron_2, ... , recorded_nueron_n], time_vector)

Team: Nhi Vu, Christopher Moore, Arabdha Biswas, Nicholas Trujillo
