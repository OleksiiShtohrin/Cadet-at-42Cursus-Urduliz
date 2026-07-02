/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   op_rotate.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dzhambal <dzhambal@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/23 09:32:36 by dzhambal          #+#    #+#             */
/*   Updated: 2026/02/23 09:32:38 by dzhambal         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static void	rotate_up(t_stack *s)
{
	if (!s || s->size < 2)
		return ;
	s->top = s->top->next;
}

void	op_ra(t_stack *a)
{
	rotate_up(a);
	bench_inc(a->bench, "ra");
	write(1, "ra\n", 3);
}

void	op_rb(t_stack *b)
{
	rotate_up(b);
	bench_inc(b->bench, "rb");
	write(1, "rb\n", 3);
}

void	op_rr(t_stack *a, t_stack *b)
{
	rotate_up(a);
	rotate_up(b);
	bench_inc(a->bench, "rr");
	write(1, "rr\n", 3);
}
