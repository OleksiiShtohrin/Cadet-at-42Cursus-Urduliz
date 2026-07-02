/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_print_ptr.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/31 18:01:30 by oshtohri          #+#    #+#             */
/*   Updated: 2026/02/05 14:01:26 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

int	ft_putptr(unsigned long long ptr)
{
	int		p;
	char	*base;

	p = 0;
	base = "0123456789abcdef";
	if (ptr >= 16)
		p += ft_putptr(ptr / 16);
	p += ft_putchar(base[ptr % 16]);
	return (p);
}

int	ft_print_ptr(void *ptr)
{
	unsigned long long	numb;
	int					res;

	res = 0;
	if (ptr == 0)
		return (ft_putstr("(nil)"));
	numb = (unsigned long long)ptr;
	res += ft_putstr("0x");
	res += ft_putptr(numb);
	return (res);
}
