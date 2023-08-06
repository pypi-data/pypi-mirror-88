"""Contains helper functions for visualizing the results of experiments
and comparing recorded experiments to one another.
"""

import matplotlib.pyplot as plt

from researcher.fileutils import *

def final_compare(experiments, metrics, draw_plots=False, **kwargs):
    """Prints the final recorded value for each experiment and accross 
    each metric, averaged over folds. Optionally also presents this 
    information on lineplots.

    Args:
        experiments (list[Experiment]): The experiments that to
        compare.

        metrics (list[string]): The metrics to compare the given 
        experiments on. 

        draw_plots (bool): Indicates whether to plot graphs as well as
        displaying printouts. 
    """

    if draw_plots:
        fig, axes = plt.subplots(len(metrics), **kwargs)
    
    for i, metric in enumerate(metrics):  
        print("\n" + metric)
        for e in experiments:
            if e.has_observation(metric):
                scores = e.final_observations(metric)
                labels = [f"fold_{i}" for i in range(len(scores))]
                scores += [np.mean(scores)]
                labels += ["mean"]
                if draw_plots:
                    axes[i].plot(labels, scores[:])
                print( "mean", scores[-1], e.identifier())
        if draw_plots:
            axes[i].grid()
    
    if draw_plots:
        fig.legend([e.identifier() for e in experiments])

def plot_compare(experiments, metrics, **kwargs):
    """For each experiment and for each metric, prints the fold-averaged 
    final score, and also plots all those scores onto a line graph.

    Args:
        experiments (list[Experiment]): The experiments that to
        compare.

        metrics (list[string]): The metrics to compare the given 
        experiments on. 
    """
    fig, axes = plt.subplots(len(metrics), **kwargs)
    if not isinstance(axes, list):
        axes = [axes]
    
    for i, metric in enumerate(metrics):  
        print("\n" + metric)
        for e in experiments:
            if e.has_observation(metric):
                scores = e.final_observations(metric)
                labels = [f"fold_{i}" for i in range(len(scores))]
                scores += [np.mean(scores)]
                labels += ["mean"]
                axes[i].plot(labels, scores[:])
                print( "mean", scores[-1], e.identifier())
        axes[i].grid()
            
    fig.legend([e.identifier() for e in experiments])

def plot_lr(e, metric, lr_name, n_increases=3):
    """Plots the progression of the metric score over the course of the 
    given experiment, compared to the learning rate. This is primarily 
    used to help estimate an appropriate learning rate for a given model 
    architecture. Additional lines and printouts are added where the metric
    begins to decrease or increase.

    Args:
        e (Experiment): The experiment of interest.

        metric (string): The metric of interest. 
        
        n_increases (int, optional): The first n_increases times that the 
        metric goes from falling to rising will be highlighted with 
        printouts and plotted vertical lines. Defaults to 3.
    """
    _, ax = plt.subplots(figsize=(20, 5))
    
    values = np.mean(e.observations[metric], axis=0)
    lr_values = np.mean(e.observations[lr_name], axis=0)
    
    ax.plot(values)
    
    start_index = 0
    start = values[0]
    
    for i, v in enumerate(values):
        if v < start:
            start_index = i
            break
            
    first_increase_index = 1
    increasing=False
    for i, v in enumerate(values[start_index+1:]):
        if increasing:
            if v < values[i]:
                increasing=False
        elif v > values[i]:
            increasing=True
            first_increase_index = i + start_index + 1
            
            print("loss began to increase at: ", first_increase_index)
            print("corresponding lr: ", round(lr_values[first_increase_index], 6))
            plt.plot([first_increase_index, first_increase_index], [np.max(values), np.min(values)])

            n_increases-= 1
            if n_increases == 0:
                break
    
    min_index = np.argmin(values)
    
    plt.plot([min_index, min_index], [np.max(values), np.min(values)])
    
    print("loss began to decrease at: ", start_index)
    print("corresponding lr: ", round(lr_values[start_index], 6))
    
    print("lowest loss achieved at: ", min_index)
    print("corresponding lr: ", round(lr_values[min_index], 6))

def plot_training(es, metrics, **kwargs):
    """For each given metric, the progression of that metric over all the
    given experiments will be plotted on a separate line graph.

    Args:
        es (list[Experiment]): The experiments of intererst.

        metrics (list[string]): The metrics on which to compare the 
        experiments of interest. 
    """
    if not isinstance(es, list):
        es = [es]
    
    _, ax = plt.subplots(len(metrics), **kwargs)
    
    if len(metrics) == 1:
        ax = [ax]

    for i, m in enumerate(metrics):
        for e in es:
            folds = e.observations[m]
            line, = ax[i].plot(np.mean(folds, axis=0))
            line.set_label(f"{e.identifier()} {m}")
        ax[i].legend()
        ax[i].grid()

def plot_folds(es, metrics, **kwargs):
    """For each metric, the final values of each fold of each of the given
    experiments will be plotted on a scatter graph.

    Args:
        es (list[Experiment]): The experiments of interest.

        metrics (list[string]): The metrics on which to compare the 
        experiments of interest.
    """
    if not isinstance(es, list):
        es = [es]
    
    f, ax = plt.subplots(len(metrics), **kwargs)
    
    if len(metrics) == 1:
        ax = [ax]
    
    for i, m in enumerate(metrics):
        for e in es:
            folds = e.final_observations(m)
            ax[i].scatter([e.identifier()] * len(folds), folds)
        ax[i].grid()
    plt.xticks(rotation=45)