import matplotlib.pyplot as plt

from researcher.fileutils import *

def display_results(record_path, hash_segment, metric):
    """Locates a record and prints the average score recorded for the 
    given metric and plots the score for that metric for each fold in 
    that record.

    Args:
        record_path (string): The relative path where the record we want 
        to display information about is located.

        hash_segment (string): At least 8 consecutive characters from the 
        unique hash of the record we want to display information about.
        
        metric (string): The name of the metric we want to display. 

    Returns:
        researcher.Experiment: The experiment from the given record 
        directory that contains the given hash segment.
    """
    e = past_experiment_from_hash(record_path, hash_segment)
    _, ax = plt.subplots()

    print(np.mean(e.get_metric(metric)))

    for fold in e.get_metric(metric):
        ax.scatter(0, np.array(fold))
    
    return e

def plot_compare(experiments, metrics, **kwargs):
    """For each experiment and for each metric, prints the fold-averaged 
    final score, and also plots all those scores onto a line graph.

    Args:
        experiments (list[researcher.Experiment]): The experiments that to
        compare.

        metrics ([list[string]): The metrics to compare the given 
        experiments on. 
    """
    fig, axes = plt.subplots(len(metrics), **kwargs)
    
    for i, metric in enumerate(metrics):  
        print("\n" + metric)
        for e in experiments:
            if e.has_metric(metric):
                scores = e.get_final_metric_values(metric)
                labels = [f"fold_{i}" for i in range(len(scores))]
                scores += [np.mean(scores)]
                labels += ["mean"]
                axes[i].plot(labels, scores[:])
                print( "mean", scores[-1], e.identifier())
        axes[i].grid()
            
    fig.legend([e.identifier() for e in experiments])

def plot_lr(e, metric, n_increases=3):
    """Plots the progression of the metric score over the course of the 
    given experiment. This is primarily used to help estimate an 
    appropriate learning rate for a given model architecture. Additional
    lines and printouts are added where the metric begins to decrease or
    increase.

    Args:
        e (researcher.Experiment): The experiment of interest.

        metric (string): The metric of interest. 
        
        n_increases (int, optional): The first n_increases times that the 
        metric goes from falling to rising will be highlighted with 
        printouts and plotted vertical lines. Defaults to 3.
    """
    _, ax = plt.subplots(figsize=(20, 5))
    
    values = e.get_metric(metric)[0]
    lr_values = e.get_metric('learning_rate')[0]
    
    
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
        es (list[researcher.Experiment]): The experiments of intererst.

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
            folds = e.get_metric(m)
            line, = ax[i].plot(np.mean(folds, axis=0))
            line.set_label(f"{e.identifier()} {m}")
        ax[i].legend()
        ax[i].grid()

def plot_folds(es, metrics, **kwargs):
    """For each metric, the final values of each fold of each of the given
    experiments will be plotted on a scatter graph.

    Args:
        es (list[researcher.Experiment]): The experiments of interest.

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
            folds = e.get_final_metric_values(m)
            ax[i].scatter([e.identifier()] * len(folds), folds)
        ax[i].grid()
    plt.xticks(rotation=45)