/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_isascii.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/13 14:19:24 by oshtohri          #+#    #+#             */
/*   Updated: 2026/01/20 12:48:24 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

int	ft_isascii(int c)
{
	if (c >= 0 && c <= 127)
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
	char    test1 = 'A';
	char    test2 = '2';
	char    test3 = '!';
	char    test4 = 164;

	printf("Test 1 '%c': %d; isascii: %d\n", test1,
		ft_isascii(test1), isascii(test1));
	printf("Test 2 '%c': %d; isascii: %d\n", test2,
		ft_isascii(test2), isascii(test2));
	printf("Test 3 '%c': %d; isascii: %d\n", test3,
		ft_isascii(test3), isascii(test3));
	printf("Test 4 '%c': %d; isascii: %d\n", test4,
		ft_isascii(test4), isascii(test4));
	return 0;
}*/
