/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   alg_small.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dzhambal <dzhambal@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/23 09:30:08 by dzhambal          #+#    #+#             */
/*   Updated: 2026/02/23 09:30:12 by dzhambal         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	run_2(t_stack *a, t_stack *b)
{
	(void)b;
	if (!a || a->size != 2)
		return ;
	if (a->top->value > a->top->next->value)
		op_sa(a);
}

void	run_3(t_stack *a, t_stack *b)
{
	(void)b;
	if (!a || a->size != 3)
		return ;
	ps_sort_three(a);
}

void	run_4(t_stack *a, t_stack *b)
{
	if (!a || !b || a->size != 4)
		return ;
	ps_rotate_min_to_top(a);
	op_pb(a, b);
	run_3(a, b);
	op_pa(a, b);
}

void	run_5(t_stack *a, t_stack *b)
{
	if (!a || !b || a->size != 5)
		return ;
	ps_rotate_min_to_top(a);
	op_pb(a, b);
	ps_rotate_min_to_top(a);
	op_pb(a, b);
	run_3(a, b);
	op_pa(a, b);
	op_pa(a, b);
}
