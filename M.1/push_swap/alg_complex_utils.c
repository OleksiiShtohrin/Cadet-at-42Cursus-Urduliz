/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   alg_complex_utils.c                                :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dzhambal <dzhambal@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/22 21:47:12 by dzhambal          #+#    #+#             */
/*   Updated: 2026/02/22 21:47:17 by dzhambal         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int	ps_get_max_bits(int n)
{
	int	bits;
	int	max;

	if (n <= 1)
		return (1);
	max = n - 1;
	bits = 0;
	while ((max >> bits) != 0)
		bits++;
	return (bits);
}

void	ps_do_bit_pass(t_stack *a, t_stack *b, int bit)
{
	int	i;
	int	size;

	if (!a || !b)
		return ;
	i = 0;
	size = a->size;
	while (i < size)
	{
		if (((a->top->index >> bit) & 1) == 0)
			op_pb(a, b);
		else
			op_ra(a);
		i++;
	}
	while (b->size > 0)
		op_pa(a, b);
}
