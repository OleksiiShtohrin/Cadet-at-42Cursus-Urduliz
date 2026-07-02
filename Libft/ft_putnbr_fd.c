/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putnbr_fd.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/23 12:40:48 by oshtohri          #+#    #+#             */
/*   Updated: 2026/01/25 13:59:19 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	ft_putnbr_fd(int n, int fd)
{
	long	num;
	char	c;

	num = n;
	if (num < 0)
	{
		write(fd, "-", 1);
		num = -num;
	}
	if (num >= 10)
		ft_putnbr_fd(num / 10, fd);
	c = (num % 10) + '0';
	write(fd, &c, 1);
}
/*
#include <stdio.h>

int	main(void)
{
    int    a = 26;
    int    b = -2026;
    int    c = -2147483648;
    int    d = 2147483647;

    ft_putnbr_fd(a, 1);
    printf("\n");

    ft_putnbr_fd(b, 1);
    printf("\n");

    ft_putnbr_fd(c, 1);
    printf("\n");

    ft_putnbr_fd(d, 1);
    printf("\n");

    return (0);
}*/