/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   monitor_routine.c                                  :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/22 12:37:21 by oshtohri          #+#    #+#             */
/*   Updated: 2026/06/26 09:35:05 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static void	wakeup_all_threads(t_simulation *sim)
{
	int	i;

	pthread_mutex_lock(&sim->scheduler.mutex);
	pthread_cond_broadcast(&sim->scheduler.cond);
	pthread_mutex_unlock(&sim->scheduler.mutex);
	i = 0;
	while (i < sim->config.coder_count)
	{
		pthread_mutex_lock(&sim->coders[i].mutex);
		pthread_cond_broadcast(&sim->coders[i].cond);
		pthread_mutex_unlock(&sim->coders[i].mutex);
		i++;
	}
}

void	*monitor_routine(void *arg)
{
	t_simulation	*sim;

	sim = (t_simulation *)arg;
	while (!get_stop(sim))
	{
		if (check_burnout(sim))
		{
			set_stop(sim, true);
			break ;
		}
		if (all_coders_finished(sim))
		{
			set_stop(sim, true);
			break ;
		}
		usleep(1000);
	}
	wakeup_all_threads(sim);
	return (NULL);
}

int	start_monitor(t_simulation *sim)
{
	if (pthread_create(
			&sim->monitor_thread,
			NULL,
			monitor_routine,
			sim) != 0)
		return (1);
	return (0);
}

int	join_monitor(t_simulation *sim)
{
	if (pthread_join(sim->monitor_thread, NULL) != 0)
		return (1);
	return (0);
}
