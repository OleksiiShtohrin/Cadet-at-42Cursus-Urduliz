/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   init_modules.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/17 12:30:17 by oshtohri          #+#    #+#             */
/*   Updated: 2026/06/26 09:33:55 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static int	init_dongles(t_simulation *sim)
{
	int	i;

	i = 0;
	while (i < sim->config.coder_count)
	{
		sim->dongles[i].id = i + 1;
		sim->dongles[i].owner = NULL;
		sim->dongles[i].status = DONGLE_AVAILABLE;
		sim->dongles[i].cooldown_end = 0;
		if (pthread_mutex_init(&sim->dongles[i].mutex, NULL) != 0)
		{
			while (--i >= 0)
				pthread_mutex_destroy(&sim->dongles[i].mutex);
			return (1);
		}
		i++;
	}
	return (0);
}

static int	init_coder(t_simulation *sim, int i)
{
	sim->coders[i].id = i + 1;
	sim->coders[i].simulation = sim;
	sim->coders[i].left_dongle = &sim->dongles[i];
	sim->coders[i].right_dongle = &sim->dongles[
		(i + 1) % sim->config.coder_count];
	sim->coders[i].status = CODER_WAITING;
	sim->coders[i].compile_count = 0;
	sim->coders[i].last_compile_start = 0;
	if (pthread_mutex_init(&sim->coders[i].mutex, NULL) != 0)
		return (1);
	if (pthread_cond_init(&sim->coders[i].cond, NULL) != 0)
	{
		pthread_mutex_destroy(&sim->coders[i].mutex);
		return (1);
	}
	return (0);
}

static int	init_coders(t_simulation *sim)
{
	int	i;

	i = 0;
	while (i < sim->config.coder_count)
	{
		if (init_coder(sim, i))
		{
			while (--i >= 0)
			{
				pthread_cond_destroy(&sim->coders[i].cond);
				pthread_mutex_destroy(&sim->coders[i].mutex);
			}
			return (1);
		}
		i++;
	}
	return (0);
}

int	init_modules(t_simulation *sim)
{
	if (init_dongles(sim))
		return (1);
	if (init_coders(sim))
	{
		destroy_dongles(sim);
		return (1);
	}
	if (init_scheduler(sim))
	{
		destroy_coders(sim);
		destroy_dongles(sim);
		return (1);
	}
	return (0);
}
