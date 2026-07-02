/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_printf.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/31 13:25:51 by oshtohri          #+#    #+#             */
/*   Updated: 2026/02/05 13:58:24 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"

static int	print_format(char specifier, va_list ap)
{
	int		res;

	res = 0;
	if (specifier == 'c')
		res += ft_putchar(va_arg(ap, int));
	else if (specifier == 's')
		res += ft_putstr(va_arg(ap, char *));
	else if (specifier == 'p')
		res += ft_print_ptr(va_arg(ap, void *));
	else if (specifier == 'd' || specifier == 'i')
		res += ft_putnbr(va_arg(ap, int));
	else if (specifier == 'u')
		res += ft_putunsigned(va_arg(ap, unsigned int));
	else if (specifier == 'x' || specifier == 'X')
		res += ft_puthex(va_arg(ap, unsigned int), specifier);
	else if (specifier == '%')
		res += ft_putchar('%');
	else
		res += write(1, &specifier, 1);
	return (res);
}

int	ft_printf(const char *format, ...)
{
	int		i;
	int		res;
	va_list	ap;

	va_start (ap, format);
	i = 0;
	res = 0;
	while (format[i] != '\0')
	{
		if (format[i] == '%' && format[i + 1])
			res += print_format(format[++i], ap);
		else
			res += write(1, &format[i], 1);
		i++;
	}
	va_end (ap);
	return (res);
}
