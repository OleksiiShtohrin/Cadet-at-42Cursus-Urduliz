/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strmapi.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/23 12:35:21 by oshtohri          #+#    #+#             */
/*   Updated: 2026/01/25 17:46:31 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

char	*ft_strmapi(char const *s, char (*f)(unsigned int, char))
{
	char			*str;
	unsigned int	i;
	size_t			len;

	if (s == 0 || f == 0)
		return (NULL);
	len = 0;
	while (s[len])
		len++;
	str = (char *) malloc(sizeof(char) * (len + 1));
	if (str == 0)
		return (NULL);
	i = 0;
	while (s[i])
	{
		str[i] = f(i, s[i]);
		i++;
	}
	str[i] = '\0';
	return (str);
}
/*
#include <stdio.h>

char	to_lower(unsigned int i, char c)
{
    if (i == 0)
		return (c);
	if (c >= 'A' && c <= 'Z')
		c = c + 32;
	return (c);
}
int main(void)
{
    char    str[] = "HoLa eStudiAnte de 42 cuRsus eN 2026!";
	char	*res;

	res = ft_strmapi(str, &to_lower);
	if (res)
	{    
		printf("%s\n", str);
		printf("%s\n", res);
		free(res);
	}
    return (0);
}*/