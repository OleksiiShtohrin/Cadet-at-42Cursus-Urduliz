/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   coder_routine.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/18 11:14:22 by oshtohri          #+#    #+#             */
/*   Updated: 2026/06/26 09:32:09 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

void	*coder_routine(void *arg)
{
	t_coder	*coder;

	coder = (t_coder *)arg;
	while (!get_stop(coder->simulation)
		&& coder->compile_count
		< coder->simulation->config.number_of_compiles)
	{
		request_compilation(coder);
		wait_for_approval(coder);
		if (take_dongles(coder))
			break ;
		start_compiling(coder);
		release_dongles(coder);
		if (get_stop(coder->simulation))
			break ;
		start_debugging(coder);
		if (get_stop(coder->simulation))
			break ;
		start_refactoring(coder);
	}
	pthread_mutex_lock(&coder->mutex);
	if (coder->status != CODER_BURNED_OUT)
		coder->status = CODER_FINISHED;
	pthread_mutex_unlock(&coder->mutex);
	return (NULL);
}

int	start_coders(t_simulation *sim)
{
	int	i;

	i = 0;
	while (i < sim->config.coder_count)
	{
		if (pthread_create(
				&sim->coders[i].thread,
				NULL, coder_routine, &sim->coders[i]) != 0)
			return (1);
		i++;
	}
	return (0);
}

void	join_coders(t_simulation *sim)
{
	int	i;

	i = 0;
	while (i < sim->config.coder_count)
	{
		pthread_join(sim->coders[i].thread, NULL);
		i++;
	}
}
