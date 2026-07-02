/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   parse_utils.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/17 10:29:04 by oshtohri          #+#    #+#             */
/*   Updated: 2026/06/26 09:35:37 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

static bool	is_digit(char c)
{
	return (c >= '0' && c <= '9');
}

bool	parse_positive_long(const char *str, long *result)
{
	long	value;
	int		digit;

	value = 0;
	if (!str || !result || *str == '\0')
		return (false);
	while (*str)
	{
		if (!is_digit(*str))
			return (false);
		digit = *str - '0';
		if (value > (LONG_MAX - digit) / 10)
			return (false);
		value = value * 10 + digit;
		str++;
	}
	*result = value;
	return (true);
}

t_parse_error	parse_long_arg(const char *str, long *dst, t_parse_error error)
{
	if (!parse_positive_long(str, dst))
		return (error);
	return (PARSE_OK);
}

t_parse_error	parse_int_arg(const char *str, int *dst, t_parse_error error)
{
	long	value;

	if (!parse_positive_long(str, &value))
		return (error);
	if (value > INT_MAX)
		return (error);
	*dst = (int)value;
	return (PARSE_OK);
}

t_parse_error	parse_policy(const char *str, t_schedule_policy *policy)
{
	if (!str || !policy)
		return (PARSE_INVALID_POLICY);
	if (strcmp(str, "fifo") == 0)
	{
		*policy = POLICY_FIFO;
		return (PARSE_OK);
	}
	if (strcmp(str, "edf") == 0)
	{
		*policy = POLICY_EDF;
		return (PARSE_OK);
	}
	return (PARSE_INVALID_POLICY);
}
