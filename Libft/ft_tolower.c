/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_tolower.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/16 12:34:53 by oshtohri          #+#    #+#             */
/*   Updated: 2026/01/20 17:34:04 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

int	ft_tolower(int c)
{
	if (c >= 'A' && c <= 'Z')
	{
		return (c + 32);
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

	printf("Test '%c': %d; tolower: %d\n", test1,
		ft_tolower(test1), tolower(test1));
	printf("Test '%c': %d; tolower: %d\n", test2,
		ft_tolower(test2), tolower(test2));
	printf("Test '%c': %d; tolower: %d\n", test3,
		ft_tolower(test3), tolower(test3));
	return 0;
}*/
