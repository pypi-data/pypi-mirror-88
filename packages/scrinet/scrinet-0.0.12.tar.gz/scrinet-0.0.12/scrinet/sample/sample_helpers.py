import tensorflow as tf
import tensorflow_probability as tfp

import numpy as np
import arviz as az

tfd = tfp.distributions
tfb = tfp.bijectors


@tf.function(experimental_compile=True, autograph=True, experimental_relax_shapes=True)
def predict_hack(model, _input):
    """
    Function to re-create model.predict(input) but allows the graph to be built correctly
    (see https://github.com/tensorflow/tensorflow/issues/33997)

    :param model: A trained scrinet Neural Network
    :param _input: The point at which you want to make a prediction
    :return:
    """
    x = _input
    x = x_scale_hack(model, x)
    pred = tf.convert_to_tensor(x)
    # the three should be an argument for ndim of problem
    pred = tf.reshape(pred, shape=(-1, 3))
    net_layers = model.model.layers
    output_shape = net_layers[-1].output_shape[-1]
    for layer in net_layers:
        pred = layer(pred)
    pred = tf.reshape(
        pred, shape=(-1, output_shape,))
    pred = y_inv_scale_hack(model, pred)
    return pred


@tf.function(experimental_compile=True, experimental_relax_shapes=True)
def x_scale_hack(model, _input):
    """
    Function to re-create sklearn standard scaler for the input (as a tensorflow function)

    :param model: A trained scrinet Neural Network
    :param _input: The point at which you want to scale
    :return:
    """
    x = _input
    means = tf.constant([model.X_scalers[i].mean_[0]
                         for i in range(x.shape[0])])
    stds = tf.constant([model.X_scalers[i].scale_[0]
                        for i in range(x.shape[0])])
    means = tf.cast(means, tf.float32)
    stds = tf.cast(stds, tf.float32)

    x_scaled = (tf.reshape(x, shape=(-1, x.shape[0],)) - means) / stds
    x_scaled = tf.cast(x_scaled, tf.float32)
    return x_scaled


@tf.function(experimental_compile=True, experimental_relax_shapes=True)
def get_model_y_std_scalers(model, _input):
    """
    Re-casts the sklearn output std scalers for each output basis

    :param model: A trained scrinet Neural Network
    :param _input: The point at which you want to scale
    :return:
    """
    std = [model.Y_scalers[i].scale_[0] for i in range(_input.shape[1])]
    std = tf.stack(std, axis=0)
    std = tf.cast(std, tf.float32)
    return std


@tf.function(experimental_compile=True, experimental_relax_shapes=True)
def get_model_y_mean_scalers(model, _input):
    """
    Re-casts the sklearn output mean scalers for each output basis

    :param model: A trained scrinet Neural Network
    :param _input: The point at which you want to scale
    :return:
    """
    mean = [model.Y_scalers[i].mean_[0] for i in range(_input.shape[1])]
    mean = tf.stack(mean, axis=0)
    mean = tf.cast(mean, tf.float32)
    return mean


@tf.function(experimental_compile=True, experimental_relax_shapes=True)
def y_inv_scale_hack(model, _input):
    """
    Re-creates the sklearn inverse standard scaler as a tensorflow function,

    :param model: A trained scrinet Neural Network
    :param _input: The point at which you want to scale
    :return:
    """
    y_scaled = _input
    y_scaled = tf.reshape(y_scaled, shape=(-1, y_scaled.shape[1]))

    mean = get_model_y_mean_scalers(model, _input)

    std = get_model_y_std_scalers(model, _input)
    y = y_scaled * std + mean
    return y


# @tf.function(experimental_compile=True, experimental_relax_shapes=True)
def generate_surrogate(x,
                       amp_model,
                       amp_basis,
                       phase_model,
                       phase_basis):
    """
    Predict a full surrogate waveform for a given position and basis

    :param x: The location in parameter space - currently (q, chi1, chi2)
    :param amp_model: The pre-loaded amplitude nn generator
    :param amp_basis: The pre-loaded amplitude basis
    :param phase_model: The pre-loaded phase nn generator
    :param phase_basis: The pre-loaded phase basis
    :return:
    """

    x = tf.transpose(
        tf.stack([tf.math.log(x[:, 0]), x[:, 1], x[:, 2]], axis=0))
    x = tf.cast(x, tf.float32)
    x = tf.reshape(x, shape=(-1, x.shape[0]))
    x = tf.convert_to_tensor(x, dtype=tf.float32)

    amp_alpha = predict_hack(amp_model, x)

    amp = tf.tensordot(amp_alpha,
                       amp_basis,
                       axes=1)

    phase_alpha = predict_hack(phase_model,
                               x)

    phase = tf.tensordot(phase_alpha,
                         phase_basis,
                         axes=1)

    phase = tf.cast(phase, tf.complex64)
    amp = tf.cast(amp, tf.complex64)

    h = amp * tf.math.exp(-1.j * phase)
    phase = tf.cast(phase, tf.float32)
    #phase = phase[0]
    #phase = phase - phase[0]

    return tf.math.real(h), tf.math.imag(h), amp, phase


def convert_tfp_chains_to_arviz_object(chains):
    """
    Changes the output from sampling into an arviz object, this makes it easier to perform diagnostics
    and plots using arviz

    :param chains: The raw output from the tfp sampler

    :return:
    """
    samples_ar = np.array(chains)
    samples_right_shape = np.swapaxes(samples_ar, 0, 1)
    arv_samples = az.convert_to_inference_data(samples_right_shape)
    return arv_samples
