/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_atoi.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/16 12:21:05 by oshtohri          #+#    #+#             */
/*   Updated: 2026/01/21 13:00:58 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

int	ft_atoi(char *str)
{
	int	res;
	int	num;
	int	i;

	res = 0;
	num = 1;
	i = 0;
	if (str[i] == 0)
		return (0);
	while (str[i] == ' ' || str[i] == '\f' || str[i] == '\n'
		|| str[i] == '\r' || str[i] == '\t' || str[i] == '\v')
		i++;
	if (str[i] == '-' || str[i] == '+')
	{
		if (str[i] == '-')
			num = -1;
		i++;
	}
	while (str[i] >= '0' && str[i] <= '9')
	{
		res = res * 10 + (str[i] - '0');
		i++;
	}
	return (num * res);
}
/*
#include <stdio.h>
#include <stdlib.h>

int	main(void)
{
	char	*str1 = "  -123456o78";
	int	result1 = ft_atoi(str1);

	printf("1 ft_atoi: %d; atoi: %d\n", result1, atoi(str1));

	char	*str2 = "     +123u4u56";
	int	result2 = ft_atoi(str2);

	printf("2 ft_atoi: %d; atoi: %d\n", result2, atoi(str2));
    
	char	*str3 = " ---+--+1234ab567";
	int	result3 = ft_atoi(str3);

	printf("3 ft_atoi: %d; atoi: %d\n", result3, atoi(str3));
	return 0;
}*/
