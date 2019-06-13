import os
import shutil
import argparse
import tensorflow as tf

from .dataset import BatchGenerator
from .model import create_graph


def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--seq_len', dest='seq_len', default=256, type=int)
    parser.add_argument('--batch_size', dest='batch_size', default=64, type=int)
    parser.add_argument('--epochs', dest='epochs', default=30, type=int)
    parser.add_argument('--window_mixtures', dest='window_mixtures', default=10, type=int)
    parser.add_argument('--output_mixtures', dest='output_mixtures', default=20, type=int)
    parser.add_argument('--lstm_layers', dest='lstm_layers', default=3, type=int)
    parser.add_argument('--units_per_layer', dest='units', default=400, type=int)
    parser.add_argument('--restore', dest='restore', default=None, type=str)
    return parser.parse_args()


def next_experiment_path():
    idx = 0
    path = os.path.join('summary', 'experiment-{}')
    while os.path.exists(path.format(idx)):
        idx += 1
    path = path.format(idx)
    os.makedirs(os.path.join(path, 'models'))
    os.makedirs(os.path.join(path, 'backup'))
    for file in filter(lambda x: x.endswith('.py'), os.listdir('.')):
        shutil.copy2(file, os.path.join(path, 'backup'))
    return path


def train():
    args = get_args()
    restore_model = args.restore
    seq_len = args.seq_len
    batch_size = args.batch_size
    num_epoch = args.epochs
    batches_per_epoch = 1000

    batch_generator = BatchGenerator(batch_size, seq_len)
    g, vs = create_graph(batch_generator.num_letters, batch_size,
                         num_units=args.units, lstm_layers=args.lstm_layers,
                         window_mixtures=args.window_mixtures,
                         output_mixtures=args.output_mixtures)

    with tf.Session(graph=g) as sess:
        model_saver = tf.train.Saver(max_to_keep=2)
        if restore_model:
            model_file = tf.train.latest_checkpoint(os.path.join(restore_model, 'models'))
            experiment_path = restore_model
            epoch = int(model_file.split('-')[-1]) + 1
            model_saver.restore(sess, model_file)
        else:
            sess.run(tf.global_variables_initializer())
            experiment_path = next_experiment_path()
            epoch = 0

        summary_writer = tf.summary.FileWriter(experiment_path, graph=g, flush_secs=10)
        summary_writer.add_session_log(tf.SessionLog(status=tf.SessionLog.START),
                                       global_step=epoch * batches_per_epoch)

        for e in range(epoch, num_epoch):
            print('\nEpoch {}'.format(e))
            for b in range(1, batches_per_epoch + 1):
                coords, seq, reset, needed = batch_generator.next_batch()
                if needed:
                    sess.run(vs.reset_states, feed_dict={vs.reset: reset})
                l, s, _ = sess.run([vs.loss, vs.summary, vs.train_step],
                                   feed_dict={vs.coordinates: coords,
                                              vs.sequence: seq})
                summary_writer.add_summary(s, global_step=e * batches_per_epoch + b)
                print('\r[{:5d}/{:5d}] loss = {}'.format(b, batches_per_epoch, l), end='')

            model_saver.save(sess, os.path.join(experiment_path, 'models', 'model'),
                             global_step=e)


if __name__ == '__main__':
    train()
