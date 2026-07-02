/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   dongle_ops.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/18 12:01:10 by oshtohri          #+#    #+#             */
/*   Updated: 2026/06/26 09:32:50 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

int	wait_for_first(t_coder *coder, t_dongle *first)
{
	pthread_mutex_lock(&first->mutex);
	while (!is_dongle_ready(first) && !get_stop(coder->simulation))
	{
		pthread_mutex_unlock(&first->mutex);
		usleep(1000);
		pthread_mutex_lock(&first->mutex);
	}
	if (get_stop(coder->simulation))
	{
		pthread_mutex_unlock(&first->mutex);
		return (1);
	}
	return (0);
}

int	wait_for_second(t_coder *coder, t_dongle *first, t_dongle *second)
{
	pthread_mutex_lock(&second->mutex);
	while (!is_dongle_ready(second) && !get_stop(coder->simulation))
	{
		pthread_mutex_unlock(&second->mutex);
		pthread_mutex_unlock(&first->mutex);
		usleep(1000);
		pthread_mutex_lock(&first->mutex);
		pthread_mutex_lock(&second->mutex);
	}
	if (get_stop(coder->simulation))
	{
		pthread_mutex_unlock(&second->mutex);
		pthread_mutex_unlock(&first->mutex);
		return (1);
	}
	return (0);
}

int	take_dongles(t_coder *coder)
{
	t_dongle	*first;
	t_dongle	*second;

	if (get_stop(coder->simulation))
		return (1);
	first = get_first_dongle(coder);
	second = get_second_dongle(coder);
	if (first == second)
		return (take_single_dongle(coder, first));
	if (wait_for_first(coder, first))
		return (1);
	if (wait_for_second(coder, first, second))
		return (1);
	first->owner = coder;
	second->owner = coder;
	first->status = DONGLE_BUSY;
	second->status = DONGLE_BUSY;
	log_dongle(coder);
	log_dongle(coder);
	return (0);
}

void	release_dongles(t_coder *coder)
{
	t_dongle	*first;
	t_dongle	*second;

	first = get_first_dongle(coder);
	second = get_second_dongle(coder);
	if (coder->left_dongle == coder->right_dongle)
	{
		coder->left_dongle->owner = NULL;
		coder->left_dongle->status = DONGLE_COOLDOWN;
		coder->left_dongle->cooldown_end = get_timestamp()
			+ coder->simulation->config.cooldown_time;
		pthread_mutex_unlock(&coder->left_dongle->mutex);
		return ;
	}
	first->owner = NULL;
	second->owner = NULL;
	first->status = DONGLE_COOLDOWN;
	second->status = DONGLE_COOLDOWN;
	first->cooldown_end = get_timestamp()
		+ coder->simulation->config.cooldown_time;
	second->cooldown_end = get_timestamp()
		+ coder->simulation->config.cooldown_time;
	pthread_mutex_unlock(&second->mutex);
	pthread_mutex_unlock(&first->mutex);
}
