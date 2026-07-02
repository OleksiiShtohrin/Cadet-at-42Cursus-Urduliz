/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memset.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/17 10:33:59 by oshtohri          #+#    #+#             */
/*   Updated: 2026/01/21 17:24:32 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	*ft_memset(void *s, int c, size_t n)
{
	unsigned char	*p;

	p = s;
	while (n > 0)
	{
		*p = (unsigned char)c;
		p++;
		n--;
	}
	return (s);
}
/*
#include <string.h>
#include <stdio.h>

int	main(void)
{
	char	str[11] = "abcdefghij";
	char	str2[11] = "ABCDEFGHIJ";

	printf("Before: %s\n", str);
	printf("Before2: %s\n", str2);
	ft_memset(str+3, '1', 4);
	memset(str2+3, '2', 4);
	printf("After: %s\n", str);
	printf("memset: %s\n", str2);
}*/
