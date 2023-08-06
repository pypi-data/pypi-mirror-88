"""Base class for dynamic graphs.

    Dynamic graph is composed by an initial state and incremental changes to the network.
    This allows for an explicit trade-off between computation and memory usage when computing algorithms or visualizing.

    Got 128GB of Ram? Do lots of snapshots
    Got a threadripper? Don't do snapshots
    Got both? Do neither
    Dynamic graph calculations works both forward and backwards for reduced computations
"""

import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
from copy import deepcopy

__author__ = 'Tiago Barbosa'
__license__ = "BSD"
__email__ = "tiago.l.barbosa@tecnico.ulisboa.pt"


class DynamicDirectedGraph:

    def __init__(self, data=None, **attr):
        # initial state of graph
        self.initial_state = nx.DiGraph(data, **attr)

        # changes to the network - keys are timestamps values are lists of changes
        self.deltas = {}

        # snapshots - list of dict of pre-computed snapshots of the network - keys are timestamps values are nx graphs
        self.snapshots = {0: self.initial_state.copy()}

        # current state - current nx object
        self.current_state = self.copy_snapshot(0, self.snapshots[0])

    # representation of a change [ u, v, **kwargs, timestamp]
    @staticmethod
    def create_change(u, v, **kwargs):
        return [u, v, kwargs]

    # Iterator over changes of delta time step
    def get_changes(self, t):
        for change in self.deltas[t]:
            yield change

    def add_delta(self, t, u, v, **kwargs):
        change = self.create_change(u, v, **kwargs)
        if t in self.deltas:
            self.deltas[t].append(change)
        else:
            self.deltas[t] = [change]

    def apply_change(self, step):
        # isForward
        if self.current_state['t'] <= step:
            for change in self.get_changes(step):
                self.add_change(change)
            # updates current state
            self.current_state['t'] = step
        # isBackwards
        else:
            for change in self.get_changes(step):
                self.remove_change(change)
            # updates current state
            self.current_state['t'] = step - 1

    def add_change(self, change):
        nfrom = change[0]
        nto = change[1]
        # Checks if edge exists in the present, applies changes
        if self.current_state['state'].get_edge_data(nfrom, nto) is not None:
            new_edge_kwargs = self.current_state['state'].get_edge_data(nfrom, nto).copy()
            # has to sum changes
            for kwarg in change[2:][0]:
                if kwarg in new_edge_kwargs:
                    new_edge_kwargs[kwarg] += change[2:][0][kwarg]
            # Edge update
            if all(v <= 0 for v in new_edge_kwargs.values()):
                self.current_state['state'].remove_edge(nfrom, nto)
                # Checks if nodes become orphans
                if self.current_state['state'].degree(nfrom) == 0:
                    self.current_state['state'].remove_node(nfrom)
                if self.current_state['state'].degree(nto) == 0:
                    self.current_state['state'].remove_node(nto)
            else:
                self.current_state['state'].add_edge(nfrom, nto, **new_edge_kwargs)
        # Edge didn't exist
        else:
            self.current_state['state'].add_edge(change[0], change[1], **change[2])

    def remove_change(self, change):
        # Only has to negate kwargs and then add_change, same effect as going back in time
        negated_change = change.copy()
        for kwarg in negated_change[2:][0]:
            negated_change[2:][0][kwarg] = -negated_change[2:][0][kwarg]
        self.add_change(negated_change)

    def load_changes_from_csv(self, fileloc):
        self.deltas = pd.read_csv(fileloc + ".csv")

    def copy_snapshot(self, t, state):
        sto = {'t': t, 'state': deepcopy(state)}
        return sto

    # Iterator over snapshots
    def get_snapshots(self):
        for snapshot in self.snapshots:
            yield snapshot

    def compute_snapshot(self, t, png=False):

        # snapshot already exists
        if t in self.snapshots:
            self.current_state = self.copy_snapshot(t, self.snapshots[t])
            return

        # searches for the closest snapshot O(n) TODO improve to optimized search
        closest_snapshot = -1
        isForward = True
        for snap_t in self.get_snapshots():
            diff = snap_t - t
            if abs(diff) < abs(t - closest_snapshot) or closest_snapshot == -1:
                closest_snapshot = snap_t
                # checks if snapshot is at timestamp before or after the desired computed snapshot
                if diff > 0:
                    isForward = False
                else:
                    isForward = True

        self.current_state = self.copy_snapshot(closest_snapshot, self.snapshots[closest_snapshot])

        if isForward:
            stateRange = range(self.current_state['t'], t + 1)
        else:
            stateRange = list(range(t + 1, self.current_state['t'] + 1))
            stateRange.reverse()

        # computes snapshot
        for step in stateRange:
            if step in self.deltas:
                # applies deltas
                self.apply_change(step)

        # adds to snapshot dict
        self.snapshots[t] = self.current_state['state'].copy()
        if png:
            self.save_current_state_png()

    def compute_snapshots(self, t_list, png=False):
        # sort list of timestamps
        t_list.sort()
        # always compute first snapshot and pop null graph at 0
        self.compute_snapshot(1, png=png)
        self.snapshots.pop(0, False)

        # iterate and compute snapshot
        for t in t_list:
            self.compute_snapshot(t, png=png)

    def compute_evenly_distributed_snapshots(self, number_of_snapshots, png=False):
        if self.deltas:
            max_t = sorted(self.deltas.keys())[-1] + 1
            if number_of_snapshots > max_t:
                number_of_snapshots = max_t
            step = max_t // number_of_snapshots
            t_list = []
            for t in range(1, max_t + 1, step):
                t_list.append(t)
            # always computes snapshot
            t_list.append(max_t)
            self.compute_snapshots(t_list, png=png)
        else:
            print("No deltas in network.")

    def save_current_state_png(self):
        nx.draw_networkx(self.current_state['state'])
        plt.savefig("Graph_" + str(self.current_state['t']) + ".png", format="PNG")
        plt.close()

    def save_state_png(self, t):
        # computes snapshot
        self.compute_snapshot(t)
        self.save_current_state_png()

    def save_states_pngs(self, list_t):
        for t in list_t:
            self.save_state_png(t)

    def save_snapshots_pngs(self):
        for t in self.snapshots:
            self.save_state_png(t)
