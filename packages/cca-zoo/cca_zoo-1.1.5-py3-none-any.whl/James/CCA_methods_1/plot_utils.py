import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from sklearn import metrics
import pylab
import scipy.cluster.hierarchy as spc

def plot_results(data, labels):
    # data is c*3*k where c is the different models and k is the number of latents and 3 is train,test,val

    # Compare sum of first k dimensions
    corr_sum = np.sum(data, axis=2)

    # set width of bar
    barWidth = 0.7
    r = 2*np.arange(len(labels))
    r1 = [x - barWidth / 2 for x in r]
    r2 = [x + barWidth / 2 for x in r]

    # Make the plot
    fig, ax = plt.subplots()
    ax.bar(r1, corr_sum[:, 0], width=barWidth, edgecolor='white', label='Train')
    ax.bar(r2, corr_sum[:, 1], width=barWidth, edgecolor='white', label='Test')

    # Add xticks on the middle of the group bars
    ax.set_xlabel('model', fontweight='bold')
    # plt.xticks([r + barWidth for r in range(len(labels))], labels)
    ax.set_xticks(r)
    ax.set_xticklabels(labels)
    ax.xaxis.set_tick_params(rotation=90)


    # Create legend & Show graphic
    ax.legend()
    fig.tight_layout()
    fig.savefig('compare_train_test')

    # Train dimensions
    plt.figure()
    plt.plot(data[:, 0, :].T)
    plt.title('train canonical correlations')
    plt.legend(labels)
    plt.xlabel('Dimension')
    plt.tight_layout()
    plt.savefig('train_dims')

    # Test dimensions
    plt.figure()
    plt.plot(data[:, 1, :].T)
    plt.title('test canonical correlations')
    plt.legend(labels)
    plt.xlabel('Dimension')
    plt.tight_layout()
    plt.savefig('test_dims')

def p_rule(y_pred, z_values, threshold=0.5):
    y_z_1 = y_pred[z_values == 1] > threshold if threshold else y_pred[z_values == 1]
    y_z_0 = y_pred[z_values == 0] > threshold if threshold else y_pred[z_values == 0]
    odds = y_z_1.mean() / y_z_0.mean()
    return np.min([odds, 1/odds]) * 100


def plot_distributions(y_true, Z_true, y_pred, Z_pred=None, epoch=None):

    fig, axes = plt.subplots(1, 2, figsize=(10, 4), sharey=True)

    subplot_df = (
        Z_true
        .assign(race=lambda x: x['race'].map({1: 'white', 0: 'black'}))
        .assign(sex=lambda x: x['sex'].map({1: 'male', 0: 'female'}))
        .assign(y_pred=y_pred)
    )
    _subplot(subplot_df, 'race', ax=axes[0])
    _subplot(subplot_df, 'sex', ax=axes[1])
    _performance_text(fig, y_true, Z_true, y_pred, Z_pred, epoch)
    fig.tight_layout()
    return fig


def _subplot(subplot_df, col, ax):
    for label, df in subplot_df.groupby(col):
        sns.kdeplot(df['y_pred'], ax=ax, label=label, shade=True)
    ax.set_title(f'Sensitive attribute: {col}')
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 7)
    ax.set_yticks([])
    ax.set_ylabel('Prediction distribution')
    ax.set_xlabel(r'$P({{income>50K}}|z_{{{}}})$'.format(col))


def _performance_text(fig, y_test, Z_test, y_pred, Z_pred=None, epoch=None):

    if epoch is not None:
        fig.text(1.0, 0.9, f"Training epoch #{epoch}", fontsize='16')

    clf_roc_auc = metrics.roc_auc_score(y_test, y_pred)
    clf_accuracy = metrics.accuracy_score(y_test, y_pred > 0.5) * 100
    p_rules = {'race': p_rule(y_pred, Z_test['race']),
               'sex': p_rule(y_pred, Z_test['sex']),}
    fig.text(1.0, 0.65, '\n'.join(["Classifier performance:",
                                   f"- ROC AUC: {clf_roc_auc:.2f}",
                                   f"- Accuracy: {clf_accuracy:.1f}"]),
             fontsize='16')
    fig.text(1.0, 0.4, '\n'.join(["Satisfied p%-rules:"] +
                                 [f"- {attr}: {p_rules[attr]:.0f}%-rule"
                                  for attr in p_rules.keys()]),
             fontsize='16')
    if Z_pred is not None:
        adv_roc_auc = metrics.roc_auc_score(Z_test, Z_pred)
        fig.text(1.0, 0.20, '\n'.join(["Adversary performance:",
                                       f"- ROC AUC: {adv_roc_auc:.2f}"]),
                 fontsize='16')

def plot_weights(w, c):
    # Train dimensions
    fig, ax = plt.subplots()
    ax.plot(w[:, 0], label='brain weights', color="blue")
    ax.set_xlabel('PCA component')
    ax.set_ylabel('CCA_archive weights across input PCA components (brain)')
    ax2 = ax.twinx()
    ax2.plot(c[:, 0], label='behaviour weights', color="red")
    ax2.set_ylabel('CCA_archive weights across input PCA components (behaviour)')
    plt.tight_layout()
    plt.savefig('weight')


def plot_connectome_correlations(ordered_connectivity, cca_connectivity, linkage):
    # Compute and plot first dendrogram.
    fig = pylab.figure(figsize=(8, 8))
    ax1 = fig.add_axes([0.01, 0.7, 0.3, 0.3])
    Z1 = spc.dendrogram(linkage)
    ax1.set_xticks([])
    ax1.set_yticks([])

    # Plot distance matrix.
    axmatrix = fig.add_axes([0.01, 0.4, 0.3, 0.3])
    im = axmatrix.matshow(ordered_connectivity, aspect='auto', cmap=pylab.cm.YlGnBu)
    axmatrix.set_xticks([])
    axmatrix.set_yticks([])

    # Plot distance matrix.
    axmatrix = fig.add_axes([0.01, 0.1, 0.3, 0.3])
    im2 = axmatrix.matshow(cca_connectivity, aspect='auto', cmap=pylab.cm.YlGnBu)
    axmatrix.set_xticks([])
    axmatrix.set_yticks([])
    fig.savefig('connectivity_correlation.png')