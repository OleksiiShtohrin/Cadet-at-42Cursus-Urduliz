/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strjoin.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/21 17:34:32 by oshtohri          #+#    #+#             */
/*   Updated: 2026/01/25 18:45:11 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_strjoin(char const *s1, char const *s2)
{
	char	*res;
	int		i;
	int		j;

	if (s1 == 0 || s2 == 0)
		return (NULL);
	res = (char *) malloc(ft_strlen(s1) + ft_strlen(s2) +1);
	if (res == 0)
		return (NULL);
	j = 0;
	while (s1[j])
	{
		res[j] = s1[j];
		j++;
	}
	i = 0;
	while (s2[i])
	{
		res[j + i] = s2[i];
		i++;
	}
	res[j + i] = '\0';
	return (res);
}
/*
#include <stdio.h>

int main(void)
{
    char    str1[] = "HoLa estudiante ";
	char    str2[] = "de 42 cursus en 2026!";
	char	*res;

	//str1[0] = '\0';
	//str2[0] = '\0';
	res = ft_strjoin(str1, str2);
	if (res)
	{
		printf("%s\n", res);
		free(res);
	}

    return (0);
}*/