/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_isalpha.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/13 14:10:35 by oshtohri          #+#    #+#             */
/*   Updated: 2026/01/20 12:14:00 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

int	ft_isalpha(int c)
{
	if ((c >= 'a' && c <= 'z')
		|| (c >= 'A' && c <= 'Z'))
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

	printf("Test 1 '%c': %d; isalpha: %d\n", test1, 
		ft_isalpha(test1), isalpha(test1));
	printf("Test 2 '%c': %d; isalpha: %d\n", test2,
		ft_isalpha(test2), isalpha(test2));
	printf("Test 3 '%c': %d; isalpha: %d\n", test3,
		ft_isalpha(test3), isalpha(test3));
	return 0;
}*/
