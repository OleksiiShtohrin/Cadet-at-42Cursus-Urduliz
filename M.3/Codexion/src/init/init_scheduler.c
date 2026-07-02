/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   init_scheduler.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/18 11:14:17 by oshtohri          #+#    #+#             */
/*   Updated: 2026/06/26 09:34:18 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

int	init_scheduler(t_simulation *sim)
{
	sim->scheduler.heap.capacity = sim->config.coder_count;
	sim->scheduler.heap.size = 0;
	sim->scheduler.heap.arrival_counter = 0;
	sim->scheduler.heap.nodes = malloc(
			sizeof(t_heap_node) * sim->config.coder_count);
	if (!sim->scheduler.heap.nodes)
		return (1);
	sim->scheduler.policy = sim->config.policy;
	if (pthread_mutex_init(&sim->scheduler.mutex, NULL) != 0)
	{
		free(sim->scheduler.heap.nodes);
		return (1);
	}
	if (pthread_cond_init(&sim->scheduler.cond, NULL) != 0)
	{
		pthread_mutex_destroy(&sim->scheduler.mutex);
		free(sim->scheduler.heap.nodes);
		return (1);
	}
	return (0);
}

int	start_scheduler(t_simulation *sim)
{
	if (pthread_create(
			&sim->scheduler.thread,
			NULL,
			scheduler_routine,
			sim) != 0)
		return (1);
	return (0);
}

void	join_scheduler(t_simulation *sim)
{
	pthread_join(sim->scheduler.thread, NULL);
}
