/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   simulation_utils.c                                 :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/18 13:20:16 by oshtohri          #+#    #+#             */
/*   Updated: 2026/06/26 09:37:28 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

void	set_initial_compile_time(t_simulation *sim)
{
	int	i;

	i = 0;
	while (i < sim->config.coder_count)
	{
		sim->coders[i].last_compile_start = sim->start_time;
		i++;
	}
}

void	set_stop(t_simulation *sim, bool value)
{
	pthread_mutex_lock(&sim->stop_mutex);
	sim->stop = value;
	pthread_mutex_unlock(&sim->stop_mutex);
}

bool	get_stop(t_simulation *sim)
{
	bool	stop;

	pthread_mutex_lock(&sim->stop_mutex);
	stop = sim->stop;
	pthread_mutex_unlock(&sim->stop_mutex);
	return (stop);
}
