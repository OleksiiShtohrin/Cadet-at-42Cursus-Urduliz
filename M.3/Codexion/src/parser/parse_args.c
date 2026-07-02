/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   parse_args.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/17 10:27:37 by oshtohri          #+#    #+#             */
/*   Updated: 2026/06/26 09:35:21 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static t_parse_error	parse_time_args(t_config *config, char **argv)
{
	t_parse_error	error;

	error = parse_long_arg(
			argv[2], &config->burnout_time,
			PARSE_INVALID_BURNOUT_TIME);
	if (error != PARSE_OK || config->burnout_time == 0)
		return (PARSE_INVALID_BURNOUT_TIME);
	error = parse_long_arg(
			argv[3], &config->compile_time,
			PARSE_INVALID_COMPILE_TIME);
	if (error != PARSE_OK || config->compile_time == 0)
		return (PARSE_INVALID_COMPILE_TIME);
	error = parse_long_arg(
			argv[4], &config->debug_time,
			PARSE_INVALID_DEBUG_TIME);
	if (error != PARSE_OK || config->debug_time == 0)
		return (PARSE_INVALID_DEBUG_TIME);
	error = parse_long_arg(
			argv[5], &config->refactor_time,
			PARSE_INVALID_REFACTOR_TIME);
	if (error != PARSE_OK || config->refactor_time == 0)
		return (PARSE_INVALID_REFACTOR_TIME);
	return (PARSE_OK);
}

static t_parse_error	parse_compile_args(t_config *config, char **argv)
{
	t_parse_error	error;

	error = parse_int_arg(
			argv[6], &config->number_of_compiles,
			PARSE_INVALID_NUMBER_OF_COMPILES);
	if (error != PARSE_OK || config->number_of_compiles == 0)
		return (PARSE_INVALID_NUMBER_OF_COMPILES);
	error = parse_long_arg(
			argv[7], &config->cooldown_time,
			PARSE_INVALID_COOLDOWN_TIME);
	if (error != PARSE_OK || config->cooldown_time == 0)
		return (PARSE_INVALID_COOLDOWN_TIME);
	return (PARSE_OK);
}

static t_parse_error	parse_numeric_args(t_config *config, char **argv)
{
	t_parse_error	error;

	error = parse_int_arg(
			argv[1], &config->coder_count,
			PARSE_INVALID_CODER_COUNT);
	if (error != PARSE_OK || config->coder_count == 0)
		return (PARSE_INVALID_CODER_COUNT);
	error = parse_time_args(config, argv);
	if (error != PARSE_OK)
		return (error);
	error = parse_compile_args(config, argv);
	if (error != PARSE_OK)
		return (error);
	return (PARSE_OK);
}

t_parse_error	parse_args(int argc, char **argv, t_config *config)
{
	t_parse_error	error;

	if (!config)
		return (PARSE_NULL_CONFIG);
	if (argc != 9)
		return (PARSE_INVALID_ARG_COUNT);
	error = parse_numeric_args(config, argv);
	if (error != PARSE_OK)
		return (error);
	error = parse_policy(argv[8], &config->policy);
	if (error != PARSE_OK)
		return (error);
	return (PARSE_OK);
}
