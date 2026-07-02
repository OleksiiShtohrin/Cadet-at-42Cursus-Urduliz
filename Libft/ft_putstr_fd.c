/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putstr_fd.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/23 12:40:09 by oshtohri          #+#    #+#             */
/*   Updated: 2026/01/25 13:33:18 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	ft_putstr_fd(char *s, int fd)
{
	int	i;

	i = 0;
	if (s == 0)
		return ;
	while (s[i])
	{
		write(fd, &s[i], 1);
		i++;
	}
}
/*
#include <stdio.h>

int	main(void)
{
    char    str[] = "Hola estudiante de 42 cursus en 2026!";
    char    str2[] = "  Hola\nestudiante\r42 cursus\t2026  ";
    char    str3[] = "Hola estudi\0ante";
    char    str4[] = "";

    ft_putstr_fd(str, 1);
    printf("\n");

    ft_putstr_fd(str2, 1);
    printf("\n");

    ft_putstr_fd(str3, 1);
    printf("\n");

    ft_putstr_fd(str4, 2);

    return (0);
}*/