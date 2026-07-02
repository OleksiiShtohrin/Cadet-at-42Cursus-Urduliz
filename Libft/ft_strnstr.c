/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strnstr.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/16 12:07:07 by oshtohri          #+#    #+#             */
/*   Updated: 2026/01/21 17:25:14 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_strnstr(const char *big, const char *little, size_t len)
{
	size_t	i;
	size_t	j;

	i = 0;
	if (*little == '\0')
		return ((char *)big);
	while (big[i] != '\0' && i < len)
	{
		j = 0;
		while (little[j] != '\0' && (i + j) < len && big[i + j] == little[j])
			j++;
		if (little[j] == '\0')
			return ((char *)&big[i]);
		i++;
	}
	return (0);
}
/*
#include <stdio.h>
#include <string.h>
#include <bsd/string.h>

int	main(void)
{
	char	str[] = "Piscineros!";
	char	*res;

	printf("%s\n", str);
	res = ft_strnstr(str, "nero", 4);
	if (res != 0)
		printf("%s\n", res);
	else
		printf("Nada!\n");

	res = ft_strnstr(str, "nero", 10);
	if (res != 0)
		printf("Found: %s\n", res);

	char	str2[] = "Piscineros!";
	char	*res2;	
	
	printf("%s\n", str2);
	res2 = strnstr(str2, "nero", 4);
	if (res2 != 0)
		printf("%s\n", res2);
	else
		printf("Nada!\n");
    
	res2 = strnstr(str2, "nero", 10);
	if (res2 != 0)
		printf("Found: %s\n", res2);
	return (0);
}*/
