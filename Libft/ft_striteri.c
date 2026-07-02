/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_striteri.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/23 12:39:30 by oshtohri          #+#    #+#             */
/*   Updated: 2026/01/25 17:45:22 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	ft_striteri(char *s, void (*f)(unsigned int, char*))
{
	unsigned int	i;

	if (s == 0 || f == 0)
		return ;
	i = 0;
	while (s[i] != '\0')
	{
		f(i, &s[i]);
		i++;
	}
}
/*
#include <stdio.h>

void	all_cap(unsigned int i, char *c)
{
    if (i % 2 == 0) //(void)i; si no quiero usar i.
	{
        if (*c >= 'a' && *c <= 'z')
            *c = *c - ('a' - 'A');
    }
}
int main(void)
{
    char    str[] = "Hola estudiante de 42 cursus en 2026!";

    ft_striteri(str, &all_cap);
    printf("%s\n", str);

    return (0);
}*/