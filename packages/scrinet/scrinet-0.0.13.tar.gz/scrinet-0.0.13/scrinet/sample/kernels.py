import tensorflow_probability as tfp

tfd = tfp.distributions
tfb = tfp.bijectors

def make_hmc_kernel(target_log_prob_fn,
                    num_burnin_steps,
                    step_size,
                    step_size_adapter,
                    num_leapfrog_steps,
                    target_accept_prob,
                    ):
    inner_kernel = tfp.mcmc.HamiltonianMonteCarlo(
        target_log_prob_fn=target_log_prob_fn,
        step_size=step_size,
        num_leapfrog_steps=num_leapfrog_steps)

    if step_size_adapter == 'simple':
        kernel = tfp.mcmc.SimpleStepSizeAdaptation(
            inner_kernel=inner_kernel,
            num_adaptation_steps=int(num_burnin_steps * 0.8),
            target_accept_prob=target_accept_prob)

    elif step_size_adapter == 'dual':
        kernel = tfp.mcmc.DualAveragingStepSizeAdaptation(
            inner_kernel=inner_kernel,
            num_adaptation_steps=int(num_burnin_steps * 0.8),
            target_accept_prob=target_accept_prob)
    else:
        raise ValueError

    return kernel


def make_nuts_kernel(target_log_prob_fn,
                     num_burnin_steps,
                     step_size,
                     step_size_adapter='simple',
                     max_tree_depth=8,
                     parallel_iterations=20,
                     target_accept_prob=0.7
                     ):
    inner_kernel = tfp.mcmc.NoUTurnSampler(
        target_log_prob_fn=target_log_prob_fn,
        step_size=step_size,
        max_tree_depth=max_tree_depth,
        parallel_iterations=parallel_iterations,
    )

    if step_size_adapter == 'simple':

        kernel = tfp.mcmc.SimpleStepSizeAdaptation(
            inner_kernel,
            num_adaptation_steps=int(num_burnin_steps * 0.8),
            step_size_setter_fn=lambda pkr, new_step_size: pkr._replace(
                step_size=new_step_size
            ),
            step_size_getter_fn=lambda pkr: pkr.step_size,
            log_accept_prob_getter_fn=lambda pkr: pkr.log_accept_ratio,
            target_accept_prob=target_accept_prob,
        )

    elif step_size_adapter == 'dual':
        kernel = tfp.mcmc.DualAveragingStepSizeAdaptation(
            inner_kernel,
            num_adaptation_steps=int(num_burnin_steps * 0.8),
            step_size_setter_fn=lambda pkr, new_step_size: pkr._replace(
                step_size=new_step_size
            ),
            step_size_getter_fn=lambda pkr: pkr.step_size,
            log_accept_prob_getter_fn=lambda pkr: pkr.log_accept_ratio,
            target_accept_prob=target_accept_prob,
        )
    else:
        ValueError

    return kernel


def make_rwmcmc_kernel(target_log_prob_fn):
    inner_kernel = tfp.mcmc.RandomWalkMetropolis(target_log_prob_fn,
                                                 new_state_fn=tfp.mcmc.random_walk_normal_fn(scale=0.01)
                                                 )
    kernel = tfp.mcmc.TransformedTransitionKernel(inner_kernel=inner_kernel,
                                                  bijector=[tfb.Identity(),
                                                            tfb.Identity(),
                                                            tfb.Identity(),
                                                            tfb.Identity()])
    return kernel

