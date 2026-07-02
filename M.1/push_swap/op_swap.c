/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   op_swap.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dzhambal <dzhambal@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/23 09:32:59 by dzhambal          #+#    #+#             */
/*   Updated: 2026/02/23 09:33:03 by dzhambal         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static void	swap_top_two(t_stack *s)
{
	t_node	*a;
	t_node	*b;
	t_node	*tail;
	t_node	*c;

	if (!s || s->size < 2)
		return ;
	if (s->size == 2)
	{
		s->top = s->top->next;
		return ;
	}
	a = s->top;
	b = a->next;
	tail = a->prev;
	c = b->next;
	tail->next = b;
	b->prev = tail;
	b->next = a;
	a->prev = b;
	a->next = c;
	c->prev = a;
	s->top = b;
}

void	op_sa(t_stack *a)
{
	swap_top_two(a);
	bench_inc(a->bench, "sa");
	write(1, "sa\n", 3);
}

void	op_sb(t_stack *b)
{
	swap_top_two(b);
	bench_inc(b->bench, "sb");
	write(1, "sb\n", 3);
}

void	op_ss(t_stack *a, t_stack *b)
{
	swap_top_two(a);
	swap_top_two(b);
	bench_inc(a->bench, "ss");
	write(1, "ss\n", 3);
}
