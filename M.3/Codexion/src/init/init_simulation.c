/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   init_simulation.c                                  :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/17 12:30:30 by oshtohri          #+#    #+#             */
/*   Updated: 2026/06/26 09:34:28 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static int	allocate_arrays(t_simulation *sim)
{
	sim->coders = malloc(sizeof(t_coder) * sim->config.coder_count);
	if (!sim->coders)
		return (1);
	sim->dongles = malloc(sizeof(t_dongle) * sim->config.coder_count);
	if (!sim->dongles)
	{
		free(sim->coders);
		sim->coders = NULL;
		return (1);
	}
	return (0);
}

static int	init_all_mutexes(t_simulation *sim)
{
	if (pthread_mutex_init(&sim->log_mutex, NULL) != 0)
		return (1);
	if (pthread_mutex_init(&sim->stop_mutex, NULL) != 0)
	{
		pthread_mutex_destroy(&sim->log_mutex);
		return (1);
	}
	return (0);
}

int	init_simulation(t_simulation *sim, t_config *config)
{
	if (!sim || !config)
		return (1);
	sim->config = *config;
	sim->coders = NULL;
	sim->dongles = NULL;
	sim->stop = false;
	sim->start_time = 0;
	if (init_all_mutexes(sim))
		return (1);
	if (allocate_arrays(sim))
	{
		pthread_mutex_destroy(&sim->log_mutex);
		pthread_mutex_destroy(&sim->stop_mutex);
		return (1);
	}
	if (init_modules(sim))
	{
		destroy_simulation(sim);
		return (1);
	}
	return (0);
}
