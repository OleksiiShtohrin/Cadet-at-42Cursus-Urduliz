/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strncmp.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/16 12:34:02 by oshtohri          #+#    #+#             */
/*   Updated: 2026/01/21 17:25:09 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

int	ft_strncmp(const char *s1, const char *s2, size_t n)
{
	size_t	i;

	i = 0;
	while (i < n)
	{
		if ((unsigned char)s1[i] != (unsigned char)s2[i] || s1[i] == '\0')
		{
			return ((unsigned char)s1[i] - (unsigned char)s2[i]);
		}
		i++;
	}
	return (0);
}
/*
#include <stdio.h>
#include <string.h>

int	main(void)
{
	printf("ft_strncmp: %d\n", ft_strncmp("abcdef", "abcd", 5));
	printf("strncmp: %d\n", strncmp("abcdef", "abcd", 5));
	printf("ft_strncmp: %d\n", ft_strncmp("ABCDEF", "ABCDE", 2));
	printf("strncmp: %d\n", strncmp("ABCDEF", "ABCDE", 2));
	printf("ft_strncmp: %d\n", ft_strncmp("123", "12345", 4));
	printf("strncmp: %d\n", strncmp("123", "12345", 4));

	const char* str[] = {"Ship", "Shopping", "Shematic",
		"Super", "Car", "Sherif"};
	for(size_t i = 0; i < sizeof(str) / sizeof(*str); ++i)
		if (ft_strncmp(str[i], "Sh", 2) == 0)
			puts(str[i]);
	return (0);
}*/
