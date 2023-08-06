import tensorflow as tf
import tensorflow_probability as tfp

from scrinet.analysis.timeseries_batch import TimeSeries
from scrinet.analysis import matchedfilter_batch as matchedfilter
from scrinet.sample.sample_helpers import generate_surrogate
from scrinet.analysis.utils import tf_generate_surrogate_at_detector
import numpy as np

tfd = tfp.distributions
tfb = tfp.bijectors


# @tf.function(experimental_compile=True, autograph=False, experimental_relax_shapes=True)
def simple_gw_log_like(y_true,
                       x,
                       amp_model,
                       amp_basis,
                       phase_model,
                       phase_basis,
                       dt,
                       epoch):
    x = tf.stack([8 * x[:, 0],
                  x[:, 1],
                  x[:, 2],
                  x[:, 3],
                  x[:, 4],
                  x[:, 5],
                  x[:, 6]],
                 axis=1)

    x = tf.cast(x, tf.float64)

    # y_mu, _, _, _ = generate_surrogate(x[:, 0:3],
    #                                    amp_model=amp_model,
    #                                    amp_basis=amp_basis,
    #                                    phase_model=phase_model,
    #                                    phase_basis=phase_basis)

    y_mu = tf_generate_surrogate_at_detector(x,
                                             amp_model=amp_model,
                                             amp_basis=amp_basis,
                                             phase_model=phase_model,
                                             phase_basis=phase_basis)

    data = TimeSeries(y_true,
                      delta_t=dt,
                      epoch=epoch)

    template = TimeSeries(y_mu,
                          delta_t=dt,
                          epoch=[epoch] * y_mu.shape[0])

    shifted_y_true, y_mu = matchedfilter.coalign_waveforms(template, data)

    # shifted_y_true = shifted_y_true.data
    # y_mu = y_mu.data

    # std = tf.cast(x[:, 7], tf.float32)

    # like = tfd.Normal(loc=shifted_y_true,
    #                 scale=std[..., None])
    # return tf.reduce_sum(like.log_prob(y_mu), axis=1)

    shifted_y_true = shifted_y_true
    y_mu = y_mu

    like = gw_log_like(y_mu, shifted_y_true)

    return like


def gw_log_like(signal, template, delta_f=1., psd=None):
    """

    :param signal:
    :param template:
    :param delta_f:
    :param psd:
    :return:
    """

    duration = 1. / delta_f

    _, qtilde_fs_sig_temp, _ = matchedfilter.matched_filter_core(template, signal, psd=psd)

    d_inner_h = 4 / duration * tf.math.reduce_sum(qtilde_fs_sig_temp.data, axis=1)

    _, qtilde_sig_sig, _ = matchedfilter.matched_filter_core(signal, signal, psd=psd)

    optimal_snr_squared = 4 / duration * tf.math.reduce_sum(qtilde_sig_sig.data, axis=1)

    log_l = d_inner_h - optimal_snr_squared / 2

    return tf.math.real(log_l)


# @tf.function(experimental_compile=True, autograph=False, experimental_relax_shapes=True)
def simple_gw_prior(x):
    prior_q = tfd.Uniform(0, 1.).log_prob(x[:, 0])
    prior_spin = tf.reduce_sum(tfd.Uniform(0, 1.).log_prob(x[:, 1:3]),
                               axis=1)
    prior_ra = tfd.Uniform(0, 2 * np.pi).log_prob(x[:, 3])

    # need to add cosine prior for dec, not sure what is easiest way to do this ?
    # cos_dec = tf.math.cos(x[:, 4])
    # prior_dec = tfd.Uniform(0, 2*np.pi).log_prob(cos_dec)
    prior_dec = tfd.Uniform(-np.pi / 2, np.pi / 2).log_prob(x[:, 4])
    # hack am passing t =0.5
    prior_time = tfd.Uniform(0.1, 1.).log_prob(x[:, -2])
    prior_psi = tfd.Uniform(0, 2 * np.pi).log_prob(x[:, -1])
    # prior_noise = tfd.Uniform(0.01, 0.2).log_prob(x[:, -1])
    return prior_spin + prior_q + prior_ra + prior_dec + prior_time + prior_psi
