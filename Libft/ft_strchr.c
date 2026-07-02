/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strchr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/16 12:31:26 by oshtohri          #+#    #+#             */
/*   Updated: 2026/01/21 17:24:38 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_strchr(const char *s, int c)
{
	unsigned int	i;

	i = 0;
	while (s[i] != '\0')
	{
		if (s[i] == (char) c)
			return ((char *) &s[i]);
		i++;
	}
	if ((char) c == '\0')
		return ((char *) &s[i]);
	return (NULL);
}
/*
#include <string.h>
#include <stdio.h>

int	main(void)
{
	char	*str = "My Cursus In 2026! I'm glad)";
	char	*first = ft_strchr(str, 'I');
	printf("first: '%s\n'", first);

	char	*random = ft_strchr(str, 'A');
	if (random == NULL)
		printf("No 'A' found\n");

	char	*str2 = "My Cursus In 2026! I'm glad)";
	char	*first2 = strchr(str2, 'I');
	printf("first2: '%s\n'", first2);

	char	*random2 = strchr(str2, 'A');
	if (random2 == NULL)
		printf("No 'A' found\n");
	return 0;
}*/
