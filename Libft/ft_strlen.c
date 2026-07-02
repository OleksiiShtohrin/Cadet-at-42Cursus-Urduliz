/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strlen.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/15 12:32:43 by oshtohri          #+#    #+#             */
/*   Updated: 2026/01/21 17:25:03 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

size_t	ft_strlen(const char *s)
{
	size_t	x;

	x = 0;
	while (s[x] != '\0')
		x++;
	return (x);
}
/*
#include <string.h>
#include <stdio.h>

int	main(void)
{
	char	str[] = "Hello World!";
	char	str2[] = "Hello World!";
	
	size_t	len = ft_strlen(str);
	size_t	len2 = strlen(str2);
	printf("%s - ft_strlen: %zu\n", str, len);
	printf("%s -    strlen: %zu\n", str2, len2);
	return 0;
}*/
