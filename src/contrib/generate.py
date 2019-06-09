import os
import pickle
import argparse
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
from collections import namedtuple
from io import StringIO


class HWGenerator(object):
    def __init__(self, config):
        self.config = config
        self._init_model()

        with open(os.path.join(config["data_path"], 'translation.pkl'), 'rb') as file:
            self.translation = pickle.load(file)
        with open(os.path.join(config["data_path"], 'styles.pkl'), 'rb') as file:
            self.styles = pickle.load(file)

    def __call__(self, text, bias=1., style=None):
        style_data = self._get_style(style)
        phi_data, window_data, kappa_data, stroke_data, coords = self.sample_text(text, bias=bias, style=style_data)
        return coords

    def plot_text(self, text, bias=1., style=None, show=False):
        coords = self(text, bias=bias, style=style)

        fig, ax = plt.subplots(1, 1)
        for stroke in self._split_strokes(self._cumsum(np.array(coords))):
            plt.plot(stroke[:, 0], -stroke[:, 1])
        ax.set_aspect('equal')
        if show:
            plt.show()

        imgdata = StringIO()
        fig.savefig(imgdata, format='svg')
        imgdata.seek(0)
        return imgdata.read()

    def sample_text(self, input_text, bias=1., style=None, force=False):
        text = np.array([self.translation.get(c, 0) for c in input_text])
        coord = np.array([0., 0., 1.])
        coords = [coord]

        # Prime the model with the author style if requested
        prime_len, style_len = 0, 0
        if style is not None:
            # Priming consist of joining to a real pen-position and character sequences the synthetic sequence
            # to generate and set the synthetic pen-position to a null vector (the positions are sampled from the MDN)
            style_coords, style_text = style
            prime_len = len(style_coords)
            style_len = len(style_text)
            prime_coords = list(style_coords)
            coord = prime_coords[0]  # Set the first pen stroke as the first element to process
            text = np.r_[style_text, text]  # concatenate on 1 axis the prime text + synthesis character sequence
            sequence_prime = np.eye(len(self.translation), dtype=np.float32)[style_text]
            sequence_prime = np.expand_dims(np.concatenate([sequence_prime, np.zeros((1, len(self.translation)))]),
                                            axis=0)

        sequence = np.eye(len(self.translation), dtype=np.float32)[text]
        sequence = np.expand_dims(np.concatenate([sequence, np.zeros((1, len(self.translation)))]), axis=0)

        phi_data, window_data, kappa_data, stroke_data = [], [], [], []
        sequence_len = len(input_text) + style_len
        self.sess.run(self.vs.zero_states)
        for s in range(1, 60 * sequence_len + 1):
            is_priming = s < prime_len
            e, pi, mu1, mu2, std1, std2, rho, finish, phi, window, kappa = self.sess.run(
                [self.vs.e, self.vs.pi, self.vs.mu1, self.vs.mu2, self.vs.std1, self.vs.std2,
                 self.vs.rho, self.vs.finish, self.vs.phi, self.vs.window, self.vs.kappa],
                feed_dict={
                    self.vs.coordinates: coord[None, None, ...],
                    self.vs.sequence: sequence_prime if is_priming else sequence,
                    self.vs.bias: bias
                })

            if is_priming:
                # Use the real coordinate if priming
                coord = prime_coords[s]
            else:
                # Synthesis mode
                phi_data += [phi[0, :]]
                window_data += [window[0, :]]
                kappa_data += [kappa[0, :]]
                # ---
                g = np.random.choice(np.arange(pi.shape[1]), p=pi[0])
                coord = self._sample(e[0, 0], mu1[0, g], mu2[0, g],
                                     std1[0, g], std2[0, g], rho[0, g])
                coords += [coord]
                stroke_data += [[mu1[0, g], mu2[0, g], std1[0, g], std2[0, g], rho[0, g], coord[2]]]

                if not force and finish[0, 0] > 0.8:
                    break

        coords = np.array(coords)
        coords[-1, 2] = 1.

        return phi_data, window_data, kappa_data, stroke_data, coords

    def _get_style(self, style):
        if style is not None:
            if style > len(self.styles[0]):
                raise ValueError(f"Requested style [{style}] is not in style list")
            return [self.styles[0][style], self.styles[1][style]]
        return None

    def _init_model(self):
        # sess_config = tf.ConfigProto(device_count={'GPU': 0})
        # self.sess = tf.Session(config=sess_config)
        self.sess = tf.Session()
        saver = tf.train.import_meta_graph(self.config["model_path"] + '.meta')
        saver.restore(self.sess, self.config["model_path"])

        fields = ['coordinates', 'sequence', 'bias',
                  'e', 'pi', 'mu1', 'mu2', 'std1', 'std2',
                  'rho', 'window', 'kappa', 'phi', 'finish', 'zero_states']
        self.vs = namedtuple('Params', fields)(
            *[tf.get_collection(name)[0] for name in fields]
        )

    @staticmethod
    def _sample(e, mu1, mu2, std1, std2, rho):
        cov = np.array([[std1 * std1, std1 * std2 * rho],
                        [std1 * std2 * rho, std2 * std2]])
        mean = np.array([mu1, mu2])

        x, y = np.random.multivariate_normal(mean, cov)
        end = np.random.binomial(1, e)
        return np.array([x, y, end])

    @staticmethod
    def _split_strokes(points):
        points = np.array(points)
        strokes = []
        b = 0
        for e in range(len(points)):
            if points[e, 2] == 1.:
                strokes += [points[b: e + 1, :2].copy()]
                b = e + 1
        return strokes

    @staticmethod
    def _cumsum(points):
        sums = np.cumsum(points[:, :2], axis=0)
        return np.concatenate([sums, points[:, 2:]], axis=1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--text', dest='text', type=str, default=None)
    args = parser.parse_args()

    config = {
        "model_path": "pretrained/model-29",
        "data_path": "."
    }

    generator = HWGenerator(config)
    generator.plot_text(args.text, show=True)

    # import matplotlib.cm as cm
    # import matplotlib.mlab as mlab
    # from matplotlib import animation
    # import seaborn
    #
    #
    # if args.animation:
    #     epsilon = 1e-8
    #     minx, maxx = np.min(strokes[:, 0]), np.max(strokes[:, 0])
    #     miny, maxy = np.min(strokes[:, 1]), np.max(strokes[:, 1])
    #
    #     strokes = np.array(stroke_data)
    #     strokes[:, :2] = np.cumsum(strokes[:, :2], axis=0)
    #
    #     fig, ax = plt.subplots(1, 1, frameon=False, figsize=(2 * (maxx - minx + 2) / (maxy - miny + 1), 2))
    #     ax.set_xlim(minx - 1., maxx + 1.)
    #     ax.set_ylim(-maxy - 0.5, -miny + 0.5)
    #     ax.set_aspect('equal')
    #     ax.axis('off')
    #     # ax.hold(True)
    #
    #     plt.draw()
    #     plt.show(False)
    #
    #     background = fig.canvas.copy_from_bbox(ax.bbox)
    #
    #     sumed = cumsum(coords)
    #
    #     def _update(i):
    #         c1, c2 = sumed[i: i + 2]
    #         fig.canvas.restore_region(background)
    #         if c1[2] == 1. and c2[2] == 1.:
    #             line, = ax.plot([c2[0], c2[0]], [-c2[1], -c2[1]])
    #         elif c1[2] != 1.:
    #             line, = ax.plot([c1[0], c2[0]], [-c1[1], -c2[1]])
    #         else:
    #             line, = ax.plot([c1[0], c1[0]], [-c1[1], -c1[1]])
    #         fig.canvas.blit(ax.bbox)
    #         return line,
    #
    #     anim = animation.FuncAnimation(fig, _update, frames=len(sumed) - 2,
    #                                    interval=16, blit=True, repeat=False)
    #     if args.save is not None:
    #         anim.save(args.save, fps=60, extra_args=['-vcodec', 'libx264'])
    #     plt.show()
