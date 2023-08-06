import matplotlib.pyplot as plt
from scipy import stats

from researcher.fileutils import *

def display_results(record_path, hash_segment, metric):
    e = past_experiment_from_hash(record_path, hash_segment)
    fig, ax = plt.subplots()

    print(np.mean(e.get_metric(metric)))

    for fold in e.get_metric(metric):
        ax.scatter(0, np.array(fold))
    
    return e

def scatter_compare(experiments, metrics, **kwargs):
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

def plot_lr(e, metric):
    _, ax = plt.subplots(figsize=(20, 20))
    
    values = e.get_metric(metric)[0]
    lr_values = e.get_metric('learning_rate')[0]
    
    ax.plot(values)
    ax.plot(lr_values)
    
    start_index = 0
    start = values[0]
    for i, v in enumerate(values):
        if v < start:
            start_index = i
            break
    
    print("loss began to decrease at: ", start_index)
    print("corresponding lr: ", lr_values[start_index])
    
    best_index = np.argmin(values)
    print("lowest loss achieved at: ", best_index)
    print("corresponding lr: ", lr_values[best_index])

def plot_training(es, metrics, **kwargs):
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