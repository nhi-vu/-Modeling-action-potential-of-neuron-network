from nueron import neuronal_cell
from neuron import h
import matplotlib.pyplot as plt
from neuron.units import ms, mV, µm
from collections import defaultdict
import defaults
import random
import math
h.load_file("stdrun.hoc")

class network:
	def __init__(self, el):
		self.adjacency_list = defaultdict(lambda: set()) 
		self.adjacency_list_reverse = defaultdict(lambda: set()) #this is reverse connections are all of the things that connect to the key
		self.nodes = set()
		self.neurons = {}
		self.syns = []
		self.netcons = []

		for a, b in el:
			self.adjacency_list[a].add(b)
			self.adjacency_list_reverse[b].add(a)
			self.nodes.add(a)
			self.nodes.add(b)

		for n in self.nodes:
			self.neurons[n] = neuronal_cell(len(self.adjacency_list_reverse[n]))
		
		for t in self.nodes:
			i = 0
			for s in sorted(list(self.adjacency_list_reverse[t])):
				print(i,s,t, self.neurons[t].dends)

				syn = h.ExpSyn(self.neurons[t].dends[i](0.5))
				nc = h.NetCon(self.neurons[s].soma(0.5)._ref_v, syn, sec=self.neurons[s].soma)
				nc.weight[0] = 0.1
				nc.delay = 5
				i += 1
				
				self.netcons.append(nc)
				self.syns.append(syn)

	def stimulate(self, cell, dendrite, record, time, output, title):
		stim = h.NetStim()

		syn_ = h.ExpSyn(self.neurons[cell].dends[dendrite](0.5))

		stim.number = 1
		stim.start = 9
		ncstim = h.NetCon(stim, syn_)
		ncstim.delay = 1 * ms
		ncstim.weight[0] = 0.04  # NetCon weight is a vector.
		syn_.tau = 2 * ms

		soma_vs = []
		for r in record:
			soma_vs.append(h.Vector().record(self.neurons[r].soma(0.5)._ref_v))
		#dend_v = h.Vector().record(self.neurons[cell].dends[dendrite](0.5)._ref_v)
			t = h.Vector().record(h._ref_t)

		h.finitialize(-65 * mV)
		h.continuerun(time * ms)

		for i, soma_v in enumerate(soma_vs):
			plt.plot(t, soma_v, label="Nueron {}".format(record[i]))
		plt.title(title)
		plt.xlabel("Time (ms)")
		plt.ylabel("Activation (mV)")
		#plt.plot(t, dend_v, label="dend(0.5)")
		plt.legend()
		plt.savefig(output)

		return (t, soma_vs)

	def spike_times(self, cell, dendrite, time, out_file, title ,plot=True):
		stim = h.NetStim()

		syn_ = h.ExpSyn(self.neurons[cell].dends[dendrite](0.5))

		stim.number = 1
		stim.start = 9
		ncstim = h.NetCon(stim, syn_)
		ncstim.delay = 1 * ms
		ncstim.weight[0] = 0.04  # NetCon weight is a vector.
		syn_.tau = 2 * ms

		soma_v = h.Vector().record(self.neurons[cell].soma(0.5)._ref_v)
		dend_v = h.Vector().record(self.neurons[cell].dends[dendrite](0.5)._ref_v)
		t = h.Vector().record(h._ref_t)

		h.finitialize(-65 * mV)
		h.continuerun(time * ms)

		spike_times = [h.Vector() for nc in self.netcons]
		for nc, spike_times_vec in zip(self.netcons, spike_times):
			nc.record(spike_times_vec)


		h.finitialize(-65 * mV)
		h.continuerun(time * ms)

		for i, spike_times_vec in enumerate(spike_times):
			print("cell {}-{}: {}".format(self.netcons[i].precell().get_id(), self.netcons[i].postcell().get_id(),  list(spike_times_vec)))
			

		if plot:
			plt.figure()

			for i, spike_times_vec in enumerate(spike_times):
				if len(spike_times_vec) == 0:
					continue

				plt.vlines(spike_times_vec, self.netcons[i].precell().get_id() - 0.5, self.netcons[i].precell().get_id() + 0.5)

			plt.title(title)
			plt.xlabel("Time (ms)")
			plt.ylabel("Nueron ID")
			plt.savefig(out_file)

		return spike_times

def generate_ring(ring_size):
	return [(i % ring_size, (i+1) % ring_size) for i in range(ring_size)]






