from dgnx.classes import *
import matplotlib.pyplot as plt
import networkx as nx
import multiprocessing as mp
import time
import numpy as np
import random
import math

"""
Runs every NetworkX algorithm

Every NetworkX algorithm can be run in multiple snapshots with the option of using multi threading

IMPORTANT: this should be run on Linux, Windows does not support forks so each spawned process will have to copy the entire data structure
"""

# This can be updated with algorithms that are known to run faster single or multi threaded
MULTI_THREADED_ALGOS = []
SINGLE_THREADED_ALGOS = []


# Sets variables as global to share it with workers, reduces pickling of information
def setGlobal(DG, algoritm):
    global algorithm
    global DynG
    global t_list
    global result_list
    DynG = DG
    t_list = []
    result_list = []
    algorithm = algoritm


def run_singlethreaded_algo(DG, algorithm, asUndirected=False, **kwargs):
    t_list = []
    result_list = []
    for t_snap in DG.snapshots:
        t_list.append(t_snap)
        if asUndirected:
            result_list.append(getattr(nx, algorithm)(DG.snapshots[t_snap].to_undirected(), **kwargs))
        else:
            result_list.append(getattr(nx, algorithm)(DG.snapshots[t_snap], **kwargs))
    return t_list, result_list


def callback_append(l):
    # This is called after all run_multithreaded_algo_on_snapshot return a result.
    # t_list and result_list is modified only by the main process, not the pool workers.
    # No need for locks or mutexes!
    for r in l:
        t_list.append(r[0])
        result_list.append(r[1])


def run_multithreaded_algo_on_snapshot(t, **kwargs):
    #if asUndirected:
    #    return [t, getattr(nx, algorithm)(DynG.snapshots[t].to_undirected(), **kwargs)]
    #else:
    return [t, getattr(nx, algorithm)(DynG.snapshots[t], **kwargs)]


# Wrapps for usage of kwargs with pool
def worker_wrapper(arg):
    args, kwargs = arg
    return run_multithreaded_algo_on_snapshot(args, **kwargs)


def run_multithreaded_algo(DG, nprocs, algo, asUndirected=False, **kwargs):
    # Uses all cores
    if nprocs == -1:
        nprocs = mp.cpu_count()

    # starts multiprocess
    with mp.Manager() as multi_manager:
        setGlobal(DG, algo)

        # makes list of args to be passes to workers
        jobs = [(t, kwargs) for t in list(DG.snapshots.keys())]

        # initializes pool 
        pool = mp.Pool(nprocs)
        pool.map_async(worker_wrapper, jobs, callback=callback_append)
        pool.close()
        pool.join()

        return t_list, result_list


def run_algorithm_over_snapshots(DG, algorithm, nprocs=1, chart=False, fileloc='', asUndirected=False, **kwargs):
    begin_time = time.time()
    if algorithm in MULTI_THREADED_ALGOS or nprocs != 1:
        snap_t_list, result_list = run_multithreaded_algo(DG, nprocs, algorithm, asUndirected=asUndirected, **kwargs)
    else:
        snap_t_list, result_list = run_singlethreaded_algo(DG, algorithm, asUndirected=asUndirected, **kwargs)

    if chart:
        # Assumes result is a number
        print(result_list)
        if not isinstance(result_list[0], dict):
            avg_result_list = result_list
        # Assumes result is a dict
        else:
            avg_result_list = [sum(k.values()) / len(k.values()) if len(k.values()) != 0 else 0 for k in result_list]
        avg_of_algo = sum(avg_result_list) / len(avg_result_list)
        order = np.argsort(snap_t_list)
        xs = np.array(snap_t_list)[order]
        ys = np.array(avg_result_list)[order]
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_title(algorithm + ' over snapshots')
        ax.set_xlabel('Snap step')
        ax.set_ylabel(algorithm)
        ax.plot(xs, ys, 'b-', label=algorithm)
        ax.legend()
        ax.text(0.80, 0.05, 'Avg. of ' + algorithm + ' = ' + str(round(avg_of_algo, 2)),
                verticalalignment='center', horizontalalignment='center',
                transform=ax.transAxes,
                color='black', fontsize=10, )
        end_time = time.time()
        ax.text(0.825, 0.1, 'Time to Compute: ' + str(round(end_time - begin_time, 2)) + "s",
                verticalalignment='center', horizontalalignment='center',
                transform=ax.transAxes,
                color='black', fontsize=10, )
        plt.savefig(fileloc + "_" + algorithm + '_over_snapshots.png')
        plt.close()
    return snap_t_list, result_list


def compute_snapshots_and_run_algorithm(DG, t_list_or_number_of_snapshots, algoritm, nprocs=1, chart=False, fileloc='',
                                        asUndirected=False,
                                        **kwargs):
    # computes snapshots
    if t_list_or_number_of_snapshots is list:
        DG.compute_snapshots(t_list_or_number_of_snapshots)
    else:
        DG.compute_evenly_distributed_snapshots(t_list_or_number_of_snapshots)
    # runs desired algorithm
    return run_algorithm_over_snapshots(DG, algoritm, nprocs=nprocs, chart=chart, fileloc=fileloc,
                                        asUndirected=asUndirected, **kwargs)
