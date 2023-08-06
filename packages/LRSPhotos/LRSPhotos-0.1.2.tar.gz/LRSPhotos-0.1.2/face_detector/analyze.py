import matplotlib.pyplot as plt
import numpy as np
import os


def plot(lis_path, y_label, x_label='Iterations'):
    data = np.load(lis_path, allow_pickle=True)
    x = np.arange(0, len(data))
    plt.figure()
    plt.scatter(x, data)
    plt.title('%s vs %s' % (x_label, y_label))
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.show()


def plot_all():
    root = './WIDER/data'
    data = [('train_loss_list.npy', 'Training Loss', 'Iterations'),
            ('val_f1.npy', 'F1 Score', 'Epochs'),
            ('val_mAP.npy', 'mAP Score', 'Epochs'),
            ('val_precision_list.npy', 'Precision', 'Epochs'),
            ('val_recall_list.npy', 'Recall', 'Epochs')]
    for file_name, y_label, x_label in data:
        path = os.path.join(root, file_name)
        plot(path, y_label, x_label)


def combine_data(data_1_pth, data_2_pth, out_path):
    data1 = np.load(data_1_pth, allow_pickle=True)
    data2 = np.load(data_2_pth, allow_pickle=True)
    data = np.concatenate((data1, data2))
    np.save(out_path, data, allow_pickle=True)


def combine_all():
    root = '/home/shuhao/Downloads/logs'
    data = ['train_loss_list', 'val_f1', 'val_mAP', 'val_precision_list', 'val_recall_list']
    for file_name in data:
        path1 = os.path.join(root, file_name + '_1.npy')
        path2 = os.path.join(root, file_name + '_2.npy')
        out_path = os.path.join(root, file_name + '.npy')
        combine_data(path1, path2, out_path)


if __name__=='__main__':
    # combine_all()
    plot_all()
