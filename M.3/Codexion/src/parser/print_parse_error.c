/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   print_parse_error.c                                :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/17 10:29:17 by oshtohri          #+#    #+#             */
/*   Updated: 2026/06/26 09:35:53 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

void	print_parse_error(t_parse_error error)
{
	if (error == PARSE_INVALID_ARG_COUNT)
		fprintf(stderr, "Error: invalid argument count\n");
	else if (error == PARSE_INVALID_CODER_COUNT)
		fprintf(stderr, "Error: invalid coder count\n");
	else if (error == PARSE_INVALID_BURNOUT_TIME)
		fprintf(stderr, "Error: invalid burnout time\n");
	else if (error == PARSE_INVALID_COMPILE_TIME)
		fprintf(stderr, "Error: invalid compile time\n");
	else if (error == PARSE_INVALID_DEBUG_TIME)
		fprintf(stderr, "Error: invalid debug time\n");
	else if (error == PARSE_INVALID_REFACTOR_TIME)
		fprintf(stderr, "Error: invalid refactor time\n");
	else if (error == PARSE_INVALID_NUMBER_OF_COMPILES)
		fprintf(stderr, "Error: invalid number of compiles\n");
	else if (error == PARSE_INVALID_COOLDOWN_TIME)
		fprintf(stderr, "Error: invalid cooldown time\n");
	else if (error == PARSE_INVALID_POLICY)
		fprintf(stderr, "Error: invalid scheduling policy\n");
}
