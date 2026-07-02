/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_isalnum.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/16 12:37:57 by oshtohri          #+#    #+#             */
/*   Updated: 2026/01/20 12:25:11 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

int	ft_isalnum(int c)
{
	if ((c >= 'a' && c <= 'z')
		|| (c >= 'A' && c <= 'Z')
		|| (c >= '0' && c <= '9'))
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

	printf("Test 1 '%c': %d; isalnum: %d\n", test1,
		ft_isalnum(test1), isalnum(test1));
	printf("Test 2 '%c': %d; isalnum: %d\n", test2,
		ft_isalnum(test2), isalnum(test2));
	printf("Test 3 '%c': %d; isalnum: %d\n", test3,
		ft_isalnum(test3), isalnum(test3));
	return 0;
}*/
