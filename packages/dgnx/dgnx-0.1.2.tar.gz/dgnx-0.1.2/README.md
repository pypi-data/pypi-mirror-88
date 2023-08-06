![](docs/Images/dgnx.gif)

## Introduction

dgnx is a library for analyzing Dynamic Graphs.

A dynamic graph is composed by an initial state and incremental changes to the network.
This allows for an explicit trade-off between computation and memory usage when computing algorithms or visualizing it.

*Warning* This lib should be used with Linux, running algorithms with several processes in Windows/MacOs will use all your memory because Windows/MacOS spawns processes instead of using fork.

## Tools & Pre-requisites

Pre-requisites can be found [here](requirements.txt).

## Installation 

````
pip install dgnx
````

## How to Run

There are code snippets that can be found on [Examples](docs/Examples)

This [example](docs/Examples/run_algorithm.py) creates a random dynamic graph and computes the betweenness centrality for each snapshot using 16 threads.

````
from dgnx.algorithms import *
import random

if __name__ == '__main__':

    dyn = DynamicDirectedGraph()
    for v in range(0, 1000, 10):
        dyn.add_delta(v, 1, v, weight=2)
        for u in range(random.randint(0,100)):
            dyn.add_delta(v, u, random.randint(0,2000), weight=2)

    t, r = compute_snapshots_and_run_algorithm(dyn, 100, 'betweenness_centrality', nprocs=16)
    for t in zip(t,r):
        print(t)
````



