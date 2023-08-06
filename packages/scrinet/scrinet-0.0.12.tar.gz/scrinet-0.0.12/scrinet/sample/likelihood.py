import tensorflow as tf
import tensorflow_probability as tfp

from scrinet.analysis.timeseries_batch import TimeSeries
from scrinet.analysis import matchedfilter_batch as matchedfilter
from scrinet.sample.sample_helpers import generate_surrogate

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
                  x[:, 3]],
                 axis=1)

    x = tf.cast(x, tf.float64)

    y_mu, _, _, _ = generate_surrogate(x[:, 0:3],
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

    shifted_y_true = shifted_y_true.data
    y_mu = y_mu.data

    std = tf.cast(x[:, 3], tf.float32)

    like = tfd.Normal(loc=shifted_y_true,
                      scale=std[..., None])

    return tf.reduce_sum(like.log_prob(y_mu), axis=1)


def gw_log_like(signal, template, delta_f=1., psd=None):
    """

    :param signal:
    :param template:
    :param delta_f:
    :param psd:
    :return:
    """

    duration = 1./delta_f

    _, qtilde_fs_sig_temp, _ = matchedfilter.matched_filter_core(signal, template, psd=psd)

    d_inner_h = 4/duration * tf.math.reduce_sum(qtilde_fs_sig_temp.data)

    _, qtilde_sig_sig, _ = matchedfilter.matched_filter_core(signal, signal, psd=psd)

    optimal_snr_squared = 4/duration * tf.math.reduce_sum(qtilde_sig_sig.data)

    log_l = d_inner_h - optimal_snr_squared / 2

    return tf.math.real(log_l)


# @tf.function(experimental_compile=True, autograph=False, experimental_relax_shapes=True)
def simple_gw_prior(x):
    prior_q = tfd.Uniform(0, 1.).log_prob(x[:, 0])
    prior_spin = tf.reduce_sum(tfd.Uniform(0, 1.).log_prob(x[:, 1:3]),
                               axis=1)

    prior_noise = tfd.Uniform(0.01, 0.2).log_prob(x[:, 3])
    return prior_spin + prior_q + prior_noise
