/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ps_string.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dzhambal <dzhambal@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/23 09:35:55 by dzhambal          #+#    #+#             */
/*   Updated: 2026/02/23 09:35:59 by dzhambal         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int	ps_strcmp(char *s1, char *s2)
{
	int	i;

	i = 0;
	while (s1[i] != '\0' || s2[i] != '\0')
	{
		if (s1[i] != s2[i])
		{
			return (s1[i] - s2[i]);
		}
		i++;
	}
	return (0);
}

int	ps_isdigit(int c)
{
	return (c >= '0' && c <= '9');
}

int	ps_isspace(int c)
{
	return (c == ' ' || (c >= 9 && c <= 13));
}

int	ps_streq(const char *a, const char *b)
{
	size_t	i;

	if (!a || !b)
		return (0);
	i = 0;
	while (a[i] && b[i])
	{
		if (a[i] != b[i])
			return (0);
		i++;
	}
	return (a[i] == '\0' && b[i] == '\0');
}
