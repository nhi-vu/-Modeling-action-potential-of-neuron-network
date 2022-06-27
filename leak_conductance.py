from network import network, generate_ring
import matplotlib.pyplot as plt

ring = generate_ring(5)
chorded_ring = generate_ring(5) + [(2, 4)]
fig_8 = [(0,1), (1,2),(2,3), (3,4), (4,5), (5,6), (6,7), (7,8), (8,3), (3,9), (9,0)]

edge_lists = [ring, chorded_ring, fig_8]
names = ["ring", "chorded_ring", "fig_8"]
modified_nuerons = [1,4,6]
record_nuerons = [[0,1],[2,3,4],[5,6]]

for i, edge_list in enumerate(edge_lists):
	n = network(edge_list)
	n.neurons[modified_nuerons[i]].update_biophysics_soma("hh.gl", 0.003)


	n.stimulate(0,0, record_nuerons[i], 100, names[i]+"_leaky_activation", "Nueron Activation")
	plt.clf()
	n.spike_times(0,0, 100, names[i]+"_leaky_spike_times", "Nueron Spike Times", plot=True)
	plt.clf()
