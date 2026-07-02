/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/16 14:24:02 by oshtohri          #+#    #+#             */
/*   Updated: 2026/06/26 09:38:24 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static int	start_simulation(t_simulation *sim, t_config *config)
{
	if (init_simulation(sim, config))
		return (EXIT_FAILURE);
	sim->start_time = get_timestamp();
	set_initial_compile_time(sim);
	if (start_scheduler(sim))
	{
		destroy_simulation(sim);
		return (EXIT_FAILURE);
	}
	if (start_monitor(sim))
	{
		destroy_simulation(sim);
		return (EXIT_FAILURE);
	}
	if (start_coders(sim))
	{
		destroy_simulation(sim);
		return (EXIT_FAILURE);
	}
	return (EXIT_SUCCESS);
}

int	main(int argc, char **argv)
{
	t_parse_error	error;
	t_config		config;
	t_simulation	sim;

	error = parse_args(argc, argv, &config);
	if (error != PARSE_OK)
	{
		print_parse_error(error);
		return (EXIT_FAILURE);
	}
	if (start_simulation(&sim, &config))
		return (EXIT_FAILURE);
	join_coders(&sim);
	join_scheduler(&sim);
	join_monitor(&sim);
	destroy_simulation(&sim);
	return (EXIT_SUCCESS);
}
