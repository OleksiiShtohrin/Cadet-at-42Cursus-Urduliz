/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strlcat.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/15 12:28:44 by oshtohri          #+#    #+#             */
/*   Updated: 2026/01/21 17:24:53 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

size_t	ft_strlcat(char *dst, const char *src, size_t size)
{
	size_t	d_len;
	size_t	s_len;
	size_t	i;

	d_len = 0;
	s_len = 0;
	i = 0;
	while (d_len < size && dst[d_len] != '\0')
		d_len++;
	while (src[s_len] != '\0')
		s_len++;
	if (d_len >= size)
		return (size + s_len);
	while (src[i] != '\0' && d_len + i < size - 1)
	{
		dst[d_len + i] = src[i];
		i++;
	}
	dst[d_len + i] = '\0';
	return (d_len + s_len);
}
/*
#include <string.h>
#include <stdio.h>
#include <bsd/string.h>

int main(void)
{
    char    dest[20] = "Hello ";
    char    str[10] = "my world!";

    int len = ft_strlcat(dest, str, 8);
    printf("ft_strlcat Copied '%s' into '%s', length %d\n", str, dest, len);

    char    dest3[20] = "Hello ";
    char    str3[10] = "my world!";
    
    int len3 = strlcat(dest3, str3, 8);

    printf("   strlcat Copied '%s' into '%s', length %d\n", str3, dest3, len3);
    return 0;
}*/
