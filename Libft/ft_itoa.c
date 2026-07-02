/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_itoa.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/23 12:34:26 by oshtohri          #+#    #+#             */
/*   Updated: 2026/01/23 18:19:10 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

static int	ft_count(int n);

char	*ft_itoa(int n)
{
	char	*res;
	int		len;
	long	num;

	len = ft_count(n);
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

static int	ft_count(int n)
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

/*
#include <stdio.h>

int	main(void)
{
	char *res = ft_itoa(-9874);
	printf("%s\n", res);
	free(res);

	char *res1 = ft_itoa(-2147483648);
	printf("%s\n", res1);
	free(res1);

	char *res2 = ft_itoa(0);
	printf("%s\n", res2);
	free(res2);
}*/
