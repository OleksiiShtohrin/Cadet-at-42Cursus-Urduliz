/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ps_atoi_safe.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dzhambal <dzhambal@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/23 09:34:06 by dzhambal          #+#    #+#             */
/*   Updated: 2026/02/23 09:34:09 by dzhambal         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static size_t	skip_spaces(const char *s, size_t i)
{
	while (s[i] && ps_isspace(s[i]))
		i++;
	return (i);
}

static int	is_sign(int c)
{
	return (c == '+' || c == '-');
}

static int	parse_sign(const char *s, size_t *i)
{
	int	sign;

	sign = 1;
	if (s[*i] && is_sign(s[*i]))
	{
		if (s[*i] == '-')
			sign = -1;
		(*i)++;
	}
	return (sign);
}

static int	accumulate_digits(const char *s, size_t *i, long *value, int sign)
{
	if (!s[*i] || !ps_isdigit(s[*i]))
		return (0);
	*value = 0;
	while (s[*i] && ps_isdigit(s[*i]))
	{
		*value = *value * 10 + (s[*i] - '0');
		if (sign == 1 && *value > INT_MAX)
			return (0);
		if (sign == -1 && (-*value) < INT_MIN)
			return (0);
		(*i)++;
	}
	return (1);
}

int	ps_atoi_safe(const char *s, int *out)
{
	long	value;
	int		sign;
	size_t	i;

	if (!s || !out)
		return (0);
	i = 0;
	i = skip_spaces(s, i);
	sign = parse_sign(s, &i);
	if (!accumulate_digits(s, &i, &value, sign))
		return (0);
	i = skip_spaces(s, i);
	if (s[i] != '\0')
		return (0);
	*out = (int)(value * sign);
	return (1);
}
