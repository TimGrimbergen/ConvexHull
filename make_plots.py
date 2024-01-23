import pandas as pd
import matplotlib.pyplot as plt


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
    plt.show()

def plot_by_k(data: pd.DataFrame):
    data = data.where(data['n'] == 5000).drop(columns='n')
    data = data.groupby(['k', 'algorithm']).agg({'dt': ['mean', 'std']})
    data = data.reset_index()
    print(data)
    fig, ax = plt.subplots()
    for label, df in data.groupby('algorithm'):
        mean, std = df['dt', 'mean'], df['dt', 'std']
        ax.plot(df['k'], mean, label=label)
        ax.fill_between(df['k'], mean - std, mean + std, alpha=0.2)
    ax.set_xscale('log')
    ax.set_yscale('log')
    ax.set_xlabel('k')
    ax.set_ylabel('time (ns)')
    ax.legend()
    plt.show()


def plot_diff(data: pd.DataFrame):
    data = data.where(data['n'] == 5000).drop(columns='n')
    data = data[data['algorithm'] != 'gift_wrapping']
    data = data.groupby(['k', 'algorithm']).mean()
    data = data.reset_index()
    data = data.pivot(index='k', columns='algorithm', values='dt')
    data['diff'] = data['chan'] - data['graham_scan']
    data = data.reset_index()

    fix, ax = plt.subplots()
    ax.plot(data['k'], data['diff'])

    ax.set_xscale('log')
    ax.set_xlabel('k')
    ax.set_ylabel('time (ns)')
    plt.show()


def plot_at_k_3(data: pd.DataFrame):
    data = data.where(data['k'] == 3).drop(columns='k')
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
    plt.show()


def main():
    data = pd.read_csv('data/data_2024-01-21_15:42:18.csv')
    data = data.drop(columns=['seed', 'correct'])
    plot_at_k_3(data)


if __name__ == '__main__':
    main()
