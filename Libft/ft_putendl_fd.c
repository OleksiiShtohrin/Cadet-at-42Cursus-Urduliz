/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putendl_fd.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/23 12:40:30 by oshtohri          #+#    #+#             */
/*   Updated: 2026/01/25 14:05:01 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	ft_putendl_fd(char *s, int fd)
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
	write(fd, "\n", 1);
}
/*
int	main(void)
{
    char    str[] = "Hola estudiante de 42 cursus en 2026!";
    char    str2[] = "  Hola\nestudiante\r42 cursus\t2026  ";
    char    str3[] = "Hola estudi\0ante";
    char    str4[] = "";

    ft_putendl_fd(str, 1);

    ft_putendl_fd(str2, 1);

    ft_putendl_fd(str3, 1);

    ft_putendl_fd(str4, 2);

    return (0);
}*/