/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   log_action.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/23 11:18:26 by oshtohri          #+#    #+#             */
/*   Updated: 2026/06/26 09:37:59 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

void	log_action(t_coder *coder, const char *msg)
{
	pthread_mutex_lock(&coder->simulation->log_mutex);
	if (!get_stop(coder->simulation))
	{
		printf("%ld %d %s\n",
			get_elapsed_time(coder->simulation),
			coder->id,
			msg);
	}
	pthread_mutex_unlock(&coder->simulation->log_mutex);
}

void	log_burnout(t_coder *coder)
{
	pthread_mutex_lock(&coder->simulation->log_mutex);
	printf("%ld %d burned out\n",
		get_elapsed_time(coder->simulation),
		coder->id);
	pthread_mutex_unlock(&coder->simulation->log_mutex);
}

void	log_dongle(t_coder *coder)
{
	pthread_mutex_lock(&coder->simulation->log_mutex);
	if (!get_stop(coder->simulation))
	{
		printf("%ld %d has taken a dongle\n",
			get_elapsed_time(coder->simulation),
			coder->id);
	}
	pthread_mutex_unlock(&coder->simulation->log_mutex);
}
