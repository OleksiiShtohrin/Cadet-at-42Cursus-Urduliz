/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   monitor_checks.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/22 12:34:12 by oshtohri          #+#    #+#             */
/*   Updated: 2026/06/26 09:34:53 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

int	check_burnout(t_simulation *sim)
{
	int		i;
	long	elapsed;

	i = 0;
	while (i < sim->config.coder_count)
	{
		pthread_mutex_lock(&sim->coders[i].mutex);
		if (sim->coders[i].status != CODER_COMPILING
			&& sim->coders[i].status != CODER_FINISHED
			&& sim->coders[i].status != CODER_BURNED_OUT)
		{
			elapsed = get_timestamp() - sim->coders[i].last_compile_start;
			if (elapsed >= sim->config.burnout_time)
			{
				sim->coders[i].status = CODER_BURNED_OUT;
				log_burnout(&sim->coders[i]);
				pthread_mutex_unlock(&sim->coders[i].mutex);
				return (1);
			}
		}
		pthread_mutex_unlock(&sim->coders[i].mutex);
		i++;
	}
	return (0);
}

int	all_coders_finished(t_simulation *sim)
{
	int	i;

	i = 0;
	while (i < sim->config.coder_count)
	{
		pthread_mutex_lock(&sim->coders[i].mutex);
		if (sim->coders[i].compile_count < sim->config.number_of_compiles)
		{
			pthread_mutex_unlock(&sim->coders[i].mutex);
			return (0);
		}
		pthread_mutex_unlock(&sim->coders[i].mutex);
		i++;
	}
	return (1);
}
