/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   coder_actions.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/18 11:12:08 by oshtohri          #+#    #+#             */
/*   Updated: 2026/06/26 09:31:51 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

void	start_compiling(t_coder *coder)
{
	pthread_mutex_lock(&coder->mutex);
	coder->last_compile_start = get_timestamp();
	coder->status = CODER_COMPILING;
	coder->compile_count++;
	pthread_mutex_unlock(&coder->mutex);
	log_action(coder, "is compiling");
	usleep(coder->simulation->config.compile_time * 1000);
}

void	start_debugging(t_coder *coder)
{
	pthread_mutex_lock(&coder->mutex);
	coder->status = CODER_DEBUGGING;
	pthread_mutex_unlock(&coder->mutex);
	log_action(coder, "is debugging");
	usleep(coder->simulation->config.debug_time * 1000);
}

void	start_refactoring(t_coder *coder)
{
	pthread_mutex_lock(&coder->mutex);
	coder->status = CODER_REFACTORING;
	pthread_mutex_unlock(&coder->mutex);
	log_action(coder, "is refactoring");
	usleep(coder->simulation->config.refactor_time * 1000);
}
