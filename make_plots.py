import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

from itertools import cycle


def plot_by_n(data: pd.DataFrame):
    data = data.drop(columns='k')
    data = data.groupby(['n', 'algorithm']).agg({'dt': ['mean', 'std']})
    data = data.reset_index()

    fig, ax = plt.subplots()
    for label, df in data.groupby('algorithm'):
        mean, std = df['dt', 'mean'], df['dt', 'std']
        ax.plot(df['n'], mean, label=label)
        ax.fill_between(df['n'], mean - std, mean + std, alpha=0.2)
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('n')
    ax.set_ylabel('time (ns)')
    ax.legend()
    ax.set_title('Time to compute convex hull')
    fig.tight_layout()
    fig.savefig('data/plot_by_n.png')
    fig.savefig('data/plot_by_n.pdf')
    fig.savefig('data/plot_by_n.pgf', backend='pgf')


def plot_3d(data: pd.DataFrame):
    data = data.groupby(['n', 'k', 'algorithm']).agg({'dt': ['mean', 'std']})
    data = data.reset_index()

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    fakelines, labels = [], []
    colors = cycle(mpl.rcParams['axes.prop_cycle'].by_key()['color'])
    for label, df in data.groupby('algorithm'):
        c = next(colors)
        mean, std = df['dt', 'mean'], df['dt', 'std']
        ax.plot_trisurf(np.log10(df['n']), np.log10(df['k']), np.log10(mean), label=label, alpha=0.3)
        fakelines.append(mpl.lines.Line2D([0],[0], linestyle="none", marker = 'o', c=c))
        labels.append(label)

    # Set ticks to be at log-scale intervals
    ax.xaxis.set_major_locator(plt.MultipleLocator(1))
    ax.yaxis.set_major_locator(plt.MultipleLocator(1))
    ax.zaxis.set_major_locator(plt.MultipleLocator(1))

    major_formatter = plt.FuncFormatter(lambda x, pos: f'$10^{{{int(x)}}}$')
    ax.xaxis.set_major_formatter(major_formatter)
    ax.yaxis.set_major_formatter(major_formatter)
    ax.zaxis.set_major_formatter(major_formatter)

    ax.set_xlabel('$n$')
    ax.set_ylabel('$k$')
    ax.set_zlabel('time (ns)')
    ax.set_title('Time to compute convex hull')
    ax.legend(fakelines, labels)
    fig.tight_layout()
    fig.savefig('data/plot_3d.png')
    fig.savefig('data/plot_3d.pdf')
    fig.savefig('data/plot_3d.pgf', backend='pgf')

def plot_n_projected(data: pd.DataFrame):
    data = data.groupby(['n', 'k', 'algorithm']).mean().reset_index()
    data = data.drop(columns='k')
    data = data.groupby(['n', 'algorithm']).agg(['min', 'max']).reset_index()

    fig, ax = plt.subplots()
    colors = cycle(mpl.rcParams['axes.prop_cycle'].by_key()['color'])
    for (label, df), c in zip(data.groupby('algorithm'), colors):
        ax.plot(df['n'], df['dt', 'min'], c=c, label=label)
        ax.plot(df['n'], df['dt', 'max'], c=c)
        ax.fill_between(df['n'], df['dt', 'min'], df['dt', 'max'], alpha=0.3, color=c)
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('$n$')
    ax.set_ylabel('time (ns)')
    ax.set_title('Time to compute convex hull (projected)')
    ax.legend()
    fig.tight_layout()
    fig.savefig('data/plot_n_projected.png')
    fig.savefig('data/plot_n_projected.pdf')
    fig.savefig('data/plot_n_projected.pgf', backend='pgf')


def plot_k_is_n(data: pd.DataFrame):
    data = data.groupby(['n', 'k', 'algorithm']).mean().reset_index()
    data = data[data['n'] == data['k']]

    fig, ax = plt.subplots()
    for label, df in data.groupby('algorithm'):
        ax.plot(df['n'], df['dt'], label=label)
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('$k$')
    ax.set_ylabel('time (ns)')
    ax.set_title('Time to compute convex hull with $n=k$')
    ax.legend()
    fig.tight_layout()
    fig.savefig('data/plot_k_is_n.png')
    fig.savefig('data/plot_k_is_n.pdf')
    fig.savefig('data/plot_k_is_n.pgf', backend='pgf')


def plot_n_is_5000(data: pd.DataFrame):
    data = data.groupby(['n', 'k', 'algorithm']).mean().reset_index()
    data = data[data['n'] == 5000]

    fig, ax = plt.subplots()
    for label, df in data.groupby('algorithm'):
        ax.plot(df['k'], df['dt'], label=label)
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('$k$')
    ax.set_ylabel('time (ns)')
    ax.set_title('Time to compute convex hull with $n=5000$')
    ax.legend()
    fig.tight_layout()
    fig.savefig('data/plot_n_is_5000.png')
    fig.savefig('data/plot_n_is_5000.pdf')
    fig.savefig('data/plot_n_is_5000.pgf', backend='pgf')


def main():
    data = pd.read_csv('data/data_2024-01-21_15:42:18.csv')
    data = data.drop(columns=['seed', 'correct'])
    data = data.replace({'graham_scan': 'Graham Scan', 'gift_wrapping': 'Jarvis March', 'chan': 'Chan\'s Algorithm'})
    plot_3d(data)
    plot_n_projected(data)
    plot_k_is_n(data)
    plot_n_is_5000(data)

if __name__ == '__main__':
    main()
