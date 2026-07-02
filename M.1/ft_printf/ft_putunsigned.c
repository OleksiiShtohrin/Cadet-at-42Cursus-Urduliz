/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_putunsigned.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/31 17:59:56 by oshtohri          #+#    #+#             */
/*   Updated: 2026/02/03 12:55:00 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int	ft_putunsigned(unsigned int u)
{
	int	d;

	d = 0;
	if (u >= 10)
		d += ft_putunsigned(u / 10);
	d += ft_putchar((u % 10) + '0');
	return (d);
}
