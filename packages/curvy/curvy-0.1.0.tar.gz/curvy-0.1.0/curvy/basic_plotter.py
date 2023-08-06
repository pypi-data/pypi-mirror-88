def plot_figure(model_history=None, metric=None, all=True, test_data=True):
    """
    Plot the performance metrics of the model


    :param model_history: history

    The model history obtained from model.fit()

    :param metric: str
    The performance metric you want to use.**loss**, **accuracy**

    :param all: bool
    default=True. If true, overrides metric and plots figures of accuracy and loss.
    If false, plots the metric defined.

    :param test_data: bool
    default = True.
    If you have used validation data or not

    :return:
    Performance of the model
    """
    import seaborn as sns
    import matplotlib.pyplot as plt

    if all:
        if test_data:
            acc = model_history.history['accuracy']
            val_acc = model_history.history['val_accuracy']

            loss = model_history.history['loss']
            val_loss = model_history.history['val_loss']
            epochs = range(len(acc))

            ax = sns.lineplot(epochs, val_acc, label='validation accuracy')
            ax = sns.lineplot(epochs, acc, label='train accuracy')
            ax.set(xlabel='epochs', ylabel='accuracy', title='Epochs vs Accuracy')
            ax.legend()
            plt.show()

            bx = sns.lineplot(epochs, val_loss, label='validation loss')
            bx = sns.lineplot(epochs, loss, label='train loss')
            bx.set(xlabel='epochs', ylabel='loss', title='Epochs vs Loss')
            bx.legend()
            plt.show()

        if not test_data:
            acc = model_history.history['accuracy']
            loss = model_history.history['loss']
            epochs = range(len(acc))

            cx = sns.lineplot(epochs, acc, label='train accuracy')
            cx.set(xlabel='epochs', ylabel='accuracy', title='Epochs vs accuracy')
            cx.legend()
            plt.show()

            cx = sns.lineplot(epochs, loss, label='train loss')
            cx.set(xlabel='epochs', ylabel='loss', title='Epochs vs loss')
            cx.legend()
            plt.show()

    if not all:
        if test_data:
            value_train = model_history.history[metric]
            value_test = model_history.history['val_{}'.format(metric)]
            epochs = range(len(value_train))

            dx = sns.lineplot(epochs, value_train, label='train')
            dx = sns.lineplot(epochs, value_test, label='test')
            dx.set(xlabel='epochs', ylabel='{}'.format(metric), title='Epochs vs {}'.format(metric))
            dx.legend()
            plt.show()

        if not test_data:
            value_train = model_history.history[metric]
            epochs = range(len(value_train))

            ex = sns.lineplot(epochs, value_train, label='train')
            ex.set(xlabel='epochs', ylabel='{}'.format(metric), title='Epochs vs {}'.format(metric))
            ex.legend()
            plt.show()
