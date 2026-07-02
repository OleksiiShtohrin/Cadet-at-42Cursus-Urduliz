/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ps_itoa.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/23 12:34:26 by oshtohri          #+#    #+#             */
/*   Updated: 2026/02/21 15:46:07 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static int	ps_count(int n);

char	*ps_itoa(int n)
{
	char	*res;
	int		len;
	long	num;

	len = ps_count(n);
	res = malloc(len + 1);
	if (res == 0)
		return (NULL);
	res[len] = '\0';
	num = n;
	if (num < 0)
		num = -num;
	while (len--)
	{
		res[len] = (num % 10) + '0';
		num /= 10;
	}
	if (n < 0)
		res[0] = '-';
	return (res);
}

static int	ps_count(int n)
{
	int		len;
	long	num;

	num = n;
	len = 0;
	if (num <= 0)
		len = 1;
	while (num)
	{
		num /= 10;
		len++;
	}
	return (len);
}
