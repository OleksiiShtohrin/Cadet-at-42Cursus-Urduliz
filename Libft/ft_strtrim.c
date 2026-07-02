/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strtrim.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/22 17:11:22 by oshtohri          #+#    #+#             */
/*   Updated: 2026/01/26 17:26:04 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_strtrim(char const *s1, char const *set)
{
	size_t	start;
	size_t	end;
	size_t	i;
	char	*res;

	if (s1 == 0 || set == 0)
		return (NULL);
	end = ft_strlen(s1);
	start = 0;
	while (s1[start] && ft_strchr(set, s1[start]))
		start++;
	while (end > start && ft_strchr(set, s1[end - 1]))
		end--;
	res = (char *) malloc(sizeof(char) * (end - start + 1));
	if (res == 0)
		return (NULL);
	i = 0;
	while (start < end)
		res[i++] = s1[start++];
	res[i] = '\0';
	return (res);
}
/*
#include <stdio.h>

int main(void)
{
    char	*res;
	char	*res2;
	char	*res3;
	char	*res4;

	res = ft_strtrim("    Hola estudiante de 42 cursus en 2026!   ", " ");
	printf("%s\n", res);
	free(res);
	
	res2 = ft_strtrim("!!!hello!!!", "!");
	printf("%s\n", res2);
	free(res2);

	res3 = ft_strtrim("Hola estudiante de 42 cursus en 2026!", "!6H2o");
	printf("%s\n", res3);
	free(res3);

	res4 = ft_strtrim("   ", " ");
	printf("%s\n", res4);
	free(res4);

    return (0);
}*/