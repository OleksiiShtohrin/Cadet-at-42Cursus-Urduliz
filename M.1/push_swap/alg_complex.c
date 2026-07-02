/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   alg_complex.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dzhambal <dzhambal@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/22 21:38:02 by dzhambal          #+#    #+#             */
/*   Updated: 2026/02/22 21:38:22 by dzhambal         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	run_complex(t_stack *a, t_stack *b)
{
	int	n;
	int	bits;
	int	i;

	if (!a || !b || a->size < 2)
		return ;
	if (!ps_assign_indices(a))
		return ;
	n = a->size;
	bits = ps_get_max_bits(n);
	i = 0;
	while (i < bits)
	{
		ps_do_bit_pass(a, b, i);
		i++;
	}
}
