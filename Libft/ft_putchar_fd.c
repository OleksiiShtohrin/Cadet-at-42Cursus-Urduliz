/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putchar_fd.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/23 12:39:55 by oshtohri          #+#    #+#             */
/*   Updated: 2026/01/25 13:05:52 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	ft_putchar_fd(char c, int fd)
{
	write(fd, &c, 1);
}
/*
#include <stdio.h>

int	main(void)
{
    int		i;

    i = '0';
    while (i <= '9')
    {
        ft_putchar_fd(i, 1);
		i++;
    }
    printf("\n");

    i = 'A';
    while (i <= 'Z')
    {
        ft_putchar_fd(i, 1);
        i++;
    }
    printf("\n");

	return (0);
}*/