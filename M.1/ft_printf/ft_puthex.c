/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_puthex.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/31 17:58:42 by oshtohri          #+#    #+#             */
/*   Updated: 2026/02/03 12:45:33 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int	ft_puthex(unsigned int hex, char specifier)
{
	int		h;
	char	*base;

	h = 0;
	if (specifier == 'x')
		base = "0123456789abcdef";
	else
		base = "0123456789ABCDEF";
	if (hex >= 16)
		h += ft_puthex(hex / 16, specifier);
	h += ft_putchar(base[hex % 16]);
	return (h);
}
