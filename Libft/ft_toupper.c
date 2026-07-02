/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_toupper.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/16 12:34:43 by oshtohri          #+#    #+#             */
/*   Updated: 2026/01/20 17:31:45 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

int	ft_toupper(int c)
{
	if (c >= 'a' && c <= 'z')
	{
		return (c - 32);
	}
	return (c);
}
/*
#include <ctype.h>
#include <stdio.h>

int	main(void)
{
	char	test1 = 'A';
	char	test2 = '2';
	char	test3 = 'a';

	printf("Test '%c': %d; toupper: %d\n", test1,
		ft_toupper(test1), toupper(test1));
	printf("Test '%c': %d; toupper: %d\n", test2,
		ft_toupper(test2), toupper(test2));
	printf("Test '%c': %d; toupper: %d\n", test3,
		ft_toupper(test3), toupper(test3));
	return 0;
}*/
