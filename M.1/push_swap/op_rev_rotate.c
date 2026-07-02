/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   op_rev_rotate.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dzhambal <dzhambal@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/23 09:32:18 by dzhambal          #+#    #+#             */
/*   Updated: 2026/02/23 09:32:21 by dzhambal         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static void	rotate_down(t_stack *s)
{
	if (!s || s->size < 2)
		return ;
	s->top = s->top->prev;
}

void	op_rra(t_stack *a)
{
	rotate_down(a);
	bench_inc(a->bench, "rra");
	write(1, "rra\n", 4);
}

void	op_rrb(t_stack *b)
{
	rotate_down(b);
	bench_inc(b->bench, "rrb");
	write(1, "rrb\n", 4);
}

void	op_rrr(t_stack *a, t_stack *b)
{
	rotate_down(a);
	rotate_down(b);
	bench_inc(a->bench, "rrr");
	write(1, "rrr\n", 4);
}
