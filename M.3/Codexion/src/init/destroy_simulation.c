/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   destroy_simulation.c                               :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/17 12:29:54 by oshtohri          #+#    #+#             */
/*   Updated: 2026/06/26 09:33:22 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

void	destroy_scheduler(t_simulation *sim)
{
	pthread_mutex_destroy(&sim->scheduler.mutex);
	pthread_cond_destroy(&sim->scheduler.cond);
	free(sim->scheduler.heap.nodes);
	sim->scheduler.heap.nodes = NULL;
}

void	destroy_coders(t_simulation *sim)
{
	int	i;

	i = 0;
	while (i < sim->config.coder_count)
	{
		pthread_cond_destroy(&sim->coders[i].cond);
		pthread_mutex_destroy(&sim->coders[i].mutex);
		i++;
	}
}

void	destroy_dongles(t_simulation *sim)
{
	int	i;

	i = 0;
	while (i < sim->config.coder_count)
	{
		pthread_mutex_destroy(&sim->dongles[i].mutex);
		i++;
	}
}

void	destroy_simulation(t_simulation *sim)
{
	if (!sim)
		return ;
	pthread_mutex_destroy(&sim->stop_mutex);
	pthread_mutex_destroy(&sim->log_mutex);
	destroy_scheduler(sim);
	destroy_coders(sim);
	destroy_dongles(sim);
	free(sim->coders);
	free(sim->dongles);
	sim->coders = NULL;
	sim->dongles = NULL;
}
