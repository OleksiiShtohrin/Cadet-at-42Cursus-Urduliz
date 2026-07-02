/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   dongle_utils.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/18 12:03:31 by oshtohri          #+#    #+#             */
/*   Updated: 2026/06/26 09:33:02 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

int	is_dongle_ready(t_dongle *dongle)
{
	if (dongle->status == DONGLE_AVAILABLE)
		return (1);
	if (dongle->status == DONGLE_COOLDOWN
		&& get_timestamp() >= dongle->cooldown_end)
	{
		dongle->status = DONGLE_AVAILABLE;
		return (1);
	}
	return (0);
}

t_dongle	*get_first_dongle(t_coder *coder)
{
	if (coder->left_dongle->id < coder->right_dongle->id)
		return (coder->left_dongle);
	return (coder->right_dongle);
}

t_dongle	*get_second_dongle(t_coder *coder)
{
	if (coder->left_dongle->id < coder->right_dongle->id)
		return (coder->right_dongle);
	return (coder->left_dongle);
}

int	take_single_dongle(t_coder *coder, t_dongle *first)
{
	pthread_mutex_lock(&first->mutex);
	if (get_stop(coder->simulation))
	{
		pthread_mutex_unlock(&first->mutex);
		return (1);
	}
	first->owner = coder;
	first->status = DONGLE_BUSY;
	log_dongle(coder);
	while (!get_stop(coder->simulation))
		usleep(1000);
	pthread_mutex_unlock(&first->mutex);
	return (1);
}
