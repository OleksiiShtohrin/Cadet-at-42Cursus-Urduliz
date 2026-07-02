/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_bzero.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/16 12:21:14 by oshtohri          #+#    #+#             */
/*   Updated: 2026/01/21 17:23:25 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	ft_bzero(void *s, size_t n)
{
	char	*c;
	size_t	i;

	c = s;
	i = 0;
	while (i < n)
	{
		c[i] = '\0';
		i++;
	}
}
/*
#include <strings.h>
#include <stdio.h>
#include <bsd/string.h>

int	main(void)
{
	char	str[10] = "Hello!!+";

	printf("Before: '%s'\n", str);
	ft_bzero(str, 5);
	printf("ft_bzero: '%s'\n", str);
	printf("'0' - Byte 0: %d\n", str[0]);
	printf("'%c' - Byte 5: %d\n", str[5], str[5]);
	printf("'%c' - Byte 7: %d\n", str[7], str[7]);

	char	str2[10] = "Hello!!+";
    
	bzero(str2, 5);
	printf("bzero: '%s'\n", str2);
	printf("'0' - Byte 0: %d\n", str2[0]);
	printf("'%c' - Byte 5: %d\n", str2[5], str[5]);
	printf("'%c' - Byte 7: %d\n", str2[7], str[7]);

	return 0;
}*/
