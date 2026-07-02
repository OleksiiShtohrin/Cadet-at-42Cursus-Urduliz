/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_isprint.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/13 15:01:35 by oshtohri          #+#    #+#             */
/*   Updated: 2026/01/20 12:57:25 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

int	ft_isprint(int c)
{
	if (c >= ' ' && c <= '~')
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
	char	test4 = 0;

	printf("Test 1 '%c': %d; isprint: %d\n", test1,
		ft_isprint(test1), isprint(test1));
	printf("Test 2 '%c': %d; isprint: %d\n", test2,
		ft_isprint(test2), isprint(test2));
	printf("Test 3 '%c': %d; isprint: %d\n", test3,
		ft_isprint(test3), isprint(test3));
	printf("Test 4 '%c': %d; isprint: %d\n", test4,
		ft_isprint(test4), isprint(test4));
	return 0;
}*/
