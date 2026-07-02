/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   coder_utils.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/18 11:15:16 by oshtohri          #+#    #+#             */
/*   Updated: 2026/06/26 09:32:28 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

void	wait_for_approval(t_coder *coder)
{
	pthread_mutex_lock(&coder->mutex);
	while (coder->status != CODER_APPROVED && !get_stop(coder->simulation))
	{
		pthread_cond_wait(&coder->cond, &coder->mutex);
	}
	pthread_mutex_unlock(&coder->mutex);
}

void	request_compilation(t_coder *coder)
{
	t_scheduler	*scheduler;
	long		priority;

	scheduler = &coder->simulation->scheduler;
	pthread_mutex_lock(&coder->mutex);
	coder->status = CODER_WAITING;
	pthread_mutex_unlock(&coder->mutex);
	pthread_mutex_lock(&scheduler->mutex);
	if (scheduler->policy == POLICY_FIFO)
		priority = 0;
	else
		priority = coder->last_compile_start
			+ coder->simulation->config.burnout_time;
	heap_push(&scheduler->heap, coder, priority, scheduler->policy);
	pthread_cond_broadcast(&scheduler->cond);
	pthread_mutex_unlock(&scheduler->mutex);
}
