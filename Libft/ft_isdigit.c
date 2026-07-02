/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_isdigit.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/13 14:17:48 by oshtohri          #+#    #+#             */
/*   Updated: 2026/01/20 12:12:28 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

int	ft_isdigit(int c)
{
	if (c >= '0' && c <= '9')
	{
		return (1);
	}
	return (0);
}
/*
#include <ctype.h>
#include <stdio.h>

int	main(void)
{
	char	test1 = 'A';
	char	test2 = '2';
	char	test3 = '!';

	printf("Test 1 '%c': %d; isdigit: %d\n", test1,
		ft_isdigit(test1), isdigit(test1));
	printf("Test 2 '%c': %d; isdigit: %d\n", test2,
		ft_isdigit(test2), isdigit(test2));
	printf("Test 3 '%c': %d; isdigit: %d\n", test3,
		ft_isdigit(test3), isdigit(test3));
	return 0;
}*/
