/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strrchr.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/16 12:34:31 by oshtohri          #+#    #+#             */
/*   Updated: 2026/01/21 17:25:28 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_strrchr(const char *s, int c)
{
	const char	*p;
	int			s_len;

	s_len = 0;
	while (s[s_len] != '\0')
		s_len++;
	p = s + s_len;
	while (p >= s)
	{
		if (*p == (char) c)
			return ((char *) p);
		p--;
	}
	return (NULL);
}
/*
#include <string.h>
#include <stdio.h>

int main(void)
{
    char *str = "My Cursus In 2026! I'm glad)";
    char *first = ft_strrchr(str, 'I');
    printf("first: '%s\n'", first);

    char *random = ft_strrchr(str, 'A');
    if (random == NULL)
        printf("No 'A' found\n");

    char *str2 = "My Cursus In 2026! I'm glad)";
    char *first2 = strrchr(str2, 'I');
    printf("first2: '%s\n'", first2);

    char *random2 = strrchr(str2, 'A');
    if (random2 == NULL)
        printf("No 'A' found\n");
    return 0;
}*/
