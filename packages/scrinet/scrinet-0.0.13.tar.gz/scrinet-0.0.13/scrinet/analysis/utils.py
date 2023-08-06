import tensorflow as tf
import numpy as np
import bilby
import scrinet.sample.sample_helpers as nn_help

H1 = bilby.gw.detector.get_empty_interferometer('H1')
L1 = bilby.gw.detector.get_empty_interferometer('L1')

h1_detector_tensor = tf.convert_to_tensor(H1.detector_tensor, dtype=tf.float64)
l1_detector_tensor = tf.convert_to_tensor(L1.detector_tensor, dtype=tf.float64)

detector_tensors = {'H1': tf.reshape(h1_detector_tensor, shape=(1, 3, 3)),
                    'L1': tf.reshape(l1_detector_tensor, shape=(1, 3, 3))}

def tf_gps_time_to_gmst(gps_time):
    """

    From bilby
    https://git.ligo.org/lscsoft/bilby/-/blob/master/bilby/core/utils.py#L322
    and turned into TF code

    NOTE THIS WILL NEED TO BE UPDATED TO TAKE INTO ACCOUNT THINGS LIKE
    CORRECTIONS TO THE SIDEREAL TIME SO THIS IS JUST A TOY MODEL...


    Convert gps time to Greenwich mean sidereal time in radians

    This method assumes a constant rotation rate of earth since 00:00:00, 1 Jan. 2000
    A correction has been applied to give the exact correct value for 00:00:00, 1 Jan. 2018
    Error accumulates at a rate of ~0.0001 radians/decade.

    Parameters
    -------
    gps_time: float
        gps time

    Returns
    -------
    float: Greenwich mean sidereal time in radians

    """
    #     LEAVING THIS IN AS A REMINDER THAT IF WE WANT TO DO ANY SERIOUS SCIENCE
    #     THEN WE SHOULD MAKE A PROPER TF CODE.
    #     warnings.warn(
    #         "Function gps_time_to_gmst deprecated, use "
    #         "lal.GreenwichMeanSiderealTime(time) instead",
    #         DeprecationWarning)
    omega_earth = 2 * np.pi * (1 / 365.2425 + 1) / 86400.
    gps_2000 = 630720013.
    gmst_2000 = (6 + 39. / 60 + 51.251406103947375 / 3600) * np.pi / 12
    correction_2018 = -0.00017782487379358614
    sidereal_time = omega_earth * (gps_time - gps_2000) + gmst_2000 + correction_2018
    gmst = tf.math.mod(tf.convert_to_tensor(sidereal_time, dtype=tf.float64), 2 * np.pi)
    return gmst


def tf_ra_dec_to_theta_phi(ra, dec, gmst):
    """ Convert from RA and DEC to polar coordinates on celestial sphere

    COPIED FROM BILBY - https://git.ligo.org/lscsoft/bilby/-/blob/master/bilby/core/utils.py
    Parameters
    -------
    ra: float
        right ascension in radians
    dec: float
        declination in radians
    gmst: float
        Greenwich mean sidereal time of arrival of the signal in radians

    Returns
    -------
    float: zenith angle in radians
    float: azimuthal angle in radians

    """
    phi = ra - gmst
    theta = np.pi / 2 - dec
    phi = tf.convert_to_tensor(phi, dtype=tf.float64)
    theta = tf.convert_to_tensor(theta, dtype=tf.float64)
    return theta, phi


def tf_theta_phi_to_ra_dec(theta, phi, gmst):
    ra = phi + gmst
    dec = np.pi / 2 - theta
    return ra, dec


def tf_get_polarization_tensor(ra, dec, time, psi, mode):
    """
    Calculate the polarization tensor for a given sky location and time

    See Nishizawa et al. (2009) arXiv:0903.0528 for definitions of the polarisation tensors.
    [u, v, w] represent the Earth-frame
    [m, n, omega] represent the wave-frame
    Note: there is a typo in the definition of the wave-frame in Nishizawa et al.
    Parameters
    -------
    ra: float
        right ascension in radians
    dec: float
        declination in radians
    time: float
        geocentric GPS time
    psi: float
        binary polarisation angle counter-clockwise about the direction of propagation
    mode: str
        polarisation mode

    Returns
    -------
    array_like: A 3x3 representation of the polarization_tensor for the specified mode.

    """
    time = tf.convert_to_tensor(time, tf.float64)
    gmst = tf_gps_time_to_gmst(time)
    theta, phi = tf_ra_dec_to_theta_phi(ra, dec, gmst)

    u = tf.concat([tf.math.cos(phi) * tf.math.cos(theta),
                   tf.math.cos(theta) * tf.math.sin(phi),
                   -tf.math.sin(theta)],
                  axis=1)

    v = tf.concat([-tf.math.sin(phi),
                   tf.math.cos(phi),
                   tf.zeros_like(phi)],
                  axis=1)

    psi = tf.convert_to_tensor(psi, dtype=tf.float64)

    m = -u * tf.math.sin(psi) - v * tf.math.cos(psi)
    n = -u * tf.math.cos(psi) + v * tf.math.sin(psi)

    if mode.lower() == 'plus':
        return tf.einsum('...i,...j->...ij', m, m) - tf.einsum('...i,...j->...ij', n, n)
    elif mode.lower() == 'cross':
        return tf.einsum('...i,...j->...ij', m, n) + tf.einsum('...i,...j->...ij', n, m)


def tf_get_antenna_response(detector, ra, dec, time, psi, mode):
    """
    https://git.ligo.org/lscsoft/bilby/-/blob/master/bilby/gw/detector/interferometer.py
    Todo find function
    :param detector:
    :param ra:
    :param dec:
    :param time:
    :param psi:
    :param mode:
    :return:
    """
    polarisation_tensor = tf_get_polarization_tensor(ra, dec, time, psi, mode)
    return tf.einsum('...ij,...ij->...', detector_tensors[detector], polarisation_tensor)


def make_detector_waveform_from_polarisations(detector,
                                              h_plus,
                                              h_cross,
                                              ra,
                                              dec,
                                              time,
                                              psi):
    """
    https://git.ligo.org/lscsoft/bilby/-/blob/master/bilby/gw/detector/interferometer.py
    get_detector_response

    :param detector:
    :param h_plus:
    :param h_cross:
    :param ra:
    :param dec:
    :param time:
    :param psi:
    :return:
    """
    det_plus_response = tf.cast(tf_get_antenna_response(detector, ra, dec, time, psi, 'plus'), tf.float32)
    det_cross_response = tf.cast(tf_get_antenna_response(detector, ra, dec, time, psi, 'cross'), tf.float32)

    det_plus_response = tf.reshape(det_plus_response, (h_cross.shape[0], -1))

    det_cross_response = tf.reshape(det_cross_response, (h_cross.shape[0], -1))

    detector_h = h_plus * det_plus_response + h_cross * det_cross_response
    return detector_h


def tf_generate_surrogate_at_detector(params,
                                      amp_model,
                                      amp_basis,
                                      phase_model,
                                      phase_basis,
                                      detector='H1'):
    """
    # Todo add docs
    :param params:
    :param amp_model:
    :param amp_basis:
    :param phase_model:
    :param phase_basis:
    :param detector:
    :return:
    """
    # maybe use NamedTuple for this
    intrinsic_params = params[:, 0:3]
    extrinsic_params = params[:, 3:]

    sur_hp, sur_hc, _, _ = nn_help.generate_surrogate(
        intrinsic_params,
        amp_model=amp_model,
        amp_basis=amp_basis,
        phase_model=phase_model,
        phase_basis=phase_basis, )

    n_batch = sur_hp.shape[0]
    # messy
    ra = tf.reshape(extrinsic_params[:, 0], shape=(n_batch, -1))
    dec = tf.reshape(extrinsic_params[:, 1], shape=(n_batch, -1))
    time = tf.reshape(extrinsic_params[:, 2], shape=(n_batch, -1))
    psi = tf.reshape(extrinsic_params[:, 3], shape=(n_batch, -1))

    det_wvf = make_detector_waveform_from_polarisations(detector=detector,
                                                        h_plus=sur_hp,
                                                        h_cross=sur_hc,
                                                        ra=ra,
                                                        dec=dec,
                                                        time=time,
                                                        psi=psi)

    return det_wvf
