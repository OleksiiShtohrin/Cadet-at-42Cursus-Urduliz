/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/31 18:09:23 by oshtohri          #+#    #+#             */
/*   Updated: 2026/02/01 11:31:29 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "ft_printf.h"
#include <stdio.h>
#include <limits.h>

int	main(void)
{
	void	*ptr;

	ptr = &main;
	printf("\n");
	ft_printf("Hello %a World\n", "my awesome 42");
	printf("\n");
	printf("c Char: %c\n", 'A');
	ft_printf("  Char: %c\n", 'A');
	printf("s String: %s\n", "42 School");
	ft_printf("  String: %s\n", "42 School");
	printf("p Pointer: %p\n", ptr);
	ft_printf("  Pointer: %p\n", ptr);
	printf("d Decimal: %d\n", (int)-2147483648);
	ft_printf("  Decimal: %d\n", -2147483648);
	printf("u Unsigned: %u\n", 4294967295U);
	ft_printf("  Unsigned: %u\n", 4294967295U);
	printf("x Hex lower: %x\n", 255);
	ft_printf("  Hex lower: %x\n", 255);
	printf("X Hex upper: %X\n", 255);
	ft_printf("  Hex upper: %X\n", 255);
	printf("Percent: %%\n");
	ft_printf("Percent: %%\n");
	printf("O %% Hello %s world %d!\n", "my", 2026);
	ft_printf("%tt%% Hello %s world %d! 2 %", "my", 2026);

	int r1, r2;

    // String
    r1 = printf("\nprintf:   [%s]\n", "42 School");
    r2 = ft_printf("ft_printf:[%s]\n", "42 School");
    printf("Return: printf = %d, ft_printf = %d\n\n", r1, r2);

    // Pointer
    r1 = printf("printf:   [%p]\n", ptr);
    r2 = ft_printf("ft_printf:[%p]\n", ptr);
    printf("Return: printf = %d, ft_printf = %d\n\n", r1, r2);

    // INT_MIN
    r1 = printf("printf:   [%d]\n", INT_MIN);
    r2 = ft_printf("ft_printf:[%d]\n", -2147483648);
    printf("Return: printf = %d, ft_printf = %d\n\n", r1, r2);

	return (0);
}
