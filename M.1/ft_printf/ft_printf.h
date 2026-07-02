/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_printf.h                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/31 13:26:57 by oshtohri          #+#    #+#             */
/*   Updated: 2026/02/05 14:03:52 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef FT_PRINTF_H
# define FT_PRINTF_H

# include <stdlib.h>
# include <unistd.h>
# include <stdarg.h>

int	ft_printf(const char *format, ...);

int	ft_putchar(int c);
int	ft_putstr(char *s);
int	ft_putnbr(int num);
int	ft_putunsigned(unsigned int u);
int	ft_puthex(unsigned int hex, char specifier);
int	ft_print_ptr(void *ptr);
int	ft_putptr(unsigned long long ptr);

#endif
