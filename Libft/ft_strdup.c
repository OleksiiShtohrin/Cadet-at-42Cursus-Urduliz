/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strdup.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/18 16:05:07 by oshtohri          #+#    #+#             */
/*   Updated: 2026/01/21 17:29:21 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_strdup(const char *s)
{
	char	*dst;
	size_t	i;
	size_t	s_len;

	s_len = 0;
	while (s[s_len] != '\0')
		s_len++;
	dst = (char *) malloc(s_len + 1);
	if (dst == 0)
		return (NULL);
	i = 0;
	while (i < s_len)
	{
		dst[i] = s[i];
		i++;
	}
	dst[s_len] = '\0';
	return (dst);
}
/*
#include <string.h>
#include <stdio.h>

int	main(void)
{
	char	org[12] = "Hello world!";
	char	*dup;
	int	o_len, d_len;

	dup = ft_strdup(org);
	o_len = strlen(org);
	d_len = strlen(dup);

	printf("org string: '%s' (%d)\n", org, o_len);
	printf("dup string: '%s' (%d)\n", dup, d_len);
	free(dup);
	return 0;
}*/
