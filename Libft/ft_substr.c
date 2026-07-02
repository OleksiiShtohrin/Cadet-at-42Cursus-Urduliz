/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_substr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/21 17:32:33 by oshtohri          #+#    #+#             */
/*   Updated: 2026/01/25 18:54:57 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_substr(char const *s, unsigned int start, size_t len)
{
	char	*sub;
	size_t	i;

	if (s == NULL)
		return (NULL);
	if (start > ft_strlen(s))
		return (ft_strdup(""));
	if (len > ft_strlen(s) - start)
		len = ft_strlen(s) - start;
	sub = (char *) malloc(len + 1);
	if (sub == NULL)
		return (NULL);
	i = 0;
	while (i < len)
	{
		sub[i] = s[start + i];
		i++;
	}
	sub[i] = '\0';
	return (sub);
}
/*
#include <stdio.h>

int main(void)
{
    char    str[] = "HoLa estudiante de 42 cursus en 2026!";
	char	*res;
	char	*res2;
	char	*res3;
	char	*res4;

	res = ft_substr(str, 0, 11);
	if (res)
	{
		printf("%s\n", res);
		free(res);
	}

	res2 = ft_substr(str, 19, 9);
	if (res2)
	{
		printf("%s\n", res2);
		free(res2);
	}

	res3 = ft_substr(str, 6, 0);
	if (res3)
	{
		printf("%s\n", res3);
		free(res3);
	}

	res4 = ft_substr(str, 100, 100); //0, 0
	if (res4)
	{
		printf("%s\n", res4);
		free(res4);
	}

    return (0);
}*/