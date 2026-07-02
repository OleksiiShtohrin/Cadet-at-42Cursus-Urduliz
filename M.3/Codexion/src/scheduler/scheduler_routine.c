/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   scheduler_routine.c                                :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/22 10:31:11 by oshtohri          #+#    #+#             */
/*   Updated: 2026/06/26 09:37:11 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

void	approve_coder(t_coder *coder)
{
	pthread_mutex_lock(&coder->mutex);
	coder->status = CODER_APPROVED;
	pthread_cond_broadcast(&coder->cond);
	pthread_mutex_unlock(&coder->mutex);
}

t_coder	*wait_for_next_coder(t_scheduler *scheduler, t_simulation *sim)
{
	t_coder	*coder;

	pthread_mutex_lock(&scheduler->mutex);
	while (scheduler->heap.size == 0 && !get_stop(sim))
	{
		pthread_cond_wait(&scheduler->cond, &scheduler->mutex);
	}
	if (get_stop(sim))
	{
		pthread_mutex_unlock(&scheduler->mutex);
		return (NULL);
	}
	coder = heap_pop(&scheduler->heap, scheduler->policy);
	pthread_mutex_unlock(&scheduler->mutex);
	return (coder);
}

void	process_next_coder(t_scheduler *scheduler, t_simulation *sim)
{
	t_coder	*coder;

	coder = wait_for_next_coder(scheduler, sim);
	if (!coder)
		return ;
	approve_coder(coder);
}

void	*scheduler_routine(void *arg)
{
	t_simulation	*sim;

	sim = (t_simulation *)arg;
	while (!get_stop(sim))
	{
		process_next_coder(&sim->scheduler, sim);
	}
	return (NULL);
}
