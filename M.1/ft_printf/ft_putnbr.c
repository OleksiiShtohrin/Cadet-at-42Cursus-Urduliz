/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putnbr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/31 13:49:12 by oshtohri          #+#    #+#             */
/*   Updated: 2026/02/03 12:58:30 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int	ft_putnbr(int num)
{
	int		c;

	c = 0;
	if (num == -2147483648)
	{
		write(1, "-2147483648", 11);
		return (11);
	}
	if (num < 0)
	{
		c += write(1, "-", 1);
		num *= -1;
	}
	if (num >= 10)
		c += ft_putnbr(num / 10);
	c += ft_putchar((num % 10) + '0');
	return (c);
}
