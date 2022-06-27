from neuron import h
import matplotlib.pyplot as plt
from neuron.units import ms, mV, µm
import defaults
h.load_file("stdrun.hoc")

class neuronal_cell:
	id = 0
	def __init__(self, dend_count):
		self.id = neuronal_cell.id
		neuronal_cell.id += 1
		self.soma = h.Section(name="soma", cell=self)
		self.dends = [h.Section(name="dend_"+str(i), cell=self) for i in range(dend_count)] 
		self.all = [self.soma] + self.dends

		self._set_morphology()
		self._set_biophysics()
			
	def _set_morphology(self):
		self.soma.L = defaults.SOMA_DIAMITER
		self.soma.diam = defaults.SOMA_DIAMITER

		for dend in self.dends:
			dend.connect(self.soma)
			dend.L = defaults.DENDRITE_LENGTH
			dend.diam = defaults.DINDRITE_DIAMITER

	def _set_biophysics(self):
		for d in self.all:
			d.Ra = defaults.AXIAL_RESISTANCE
			d.cm = defaults.MEMBRANE_CAPACITANCE

		self.soma.insert("hh")

		for seg in self.soma: #for multiple segments? https://neuronsimulator.github.io/nrn/tutorials/ball-and-stick-1.html
			seg.hh.gnabar = (defaults.SODIUM_CONDUCTANCE)
			seg.hh.gkbar  = (defaults.POTASSIUM_CONDUCTANCE)
			seg.hh.gl     =  defaults.LEAK_CONDUCTANCE
			seg.hh.el     = (defaults.REVERSEAL_POTENTIAL) 

		#Passice current in dendrites
		for dend in self.dends:
			dend.insert("pas")
			for seg in dend:
				seg.pas.g = defaults.PASSIVE_CONDUCTANCE
				seg.pas.e = defaults.LEAK_REVERSAL_POTENTIAL

	def update_biophysics_soma(self, property, value):
		for seg in self.soma:
			exec("seg.{} = {}".format(property,value))
			
	def get_id(self):
		return self.id

	def __repr__(self):
		return "neuronal_cell(id: "+str(self.id)+")"
		

'''
n = neuronal_cell(2)


print(h.topology())
for sec in h.allsec():
    print("%s: %s" % (sec, ", ".join(sec.psection()["density_mechs"].keys())))

stim = h.IClamp(n.dends[0](1))
stim.delay = 5
stim.dur = 1
stim.amp = 0.1

soma_v = h.Vector().record(n.soma(0.5)._ref_v)
t = h.Vector().record(h._ref_t)
h.finitialize(-65 * mV)
h.continuerun(25 * ms)



plt.figure()
plt.plot(t, soma_v)
plt.xlabel("t (ms)")
plt.ylabel("v (mV)")
plt.savefig("t")
'''

