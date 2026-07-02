/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strlcpy.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/15 12:40:51 by oshtohri          #+#    #+#             */
/*   Updated: 2026/01/21 17:24:59 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

size_t	ft_strlcpy(char *dst, const char *src, size_t size)
{
	size_t	s_len;
	size_t	i;

	s_len = 0;
	while (src[s_len] != '\0')
		s_len++;
	if (size == 0)
		return (s_len);
	i = 0;
	while (src[i] && i < size - 1)
	{
		dst[i] = src[i];
		i++;
	}
	dst[i] = '\0';
	return (s_len);
}
/*
#include <string.h>
#include <stdio.h>
#include <bsd/string.h>

int	main(void)
{
	char	source[100] = "Que tall piscineros 2025!";
	char	destination[17];
    int len = ft_strlcpy(destination, source, 17);
	printf("ft_strlcpy Copied '%s' into '%s', length %d\n",
        source, destination, len);

    char	source3[100] = "Que tall piscineros 2025!";
	char	destination3[17];
    int len3 = strlcpy(destination3, source3, 17);
	printf("   strlcpy Copied '%s' into '%s', length %d\n",
        source3, destination3, len3);
	return (0);
}*/
