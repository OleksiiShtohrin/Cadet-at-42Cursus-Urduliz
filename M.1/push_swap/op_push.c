/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   op_push.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dzhambal <dzhambal@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/23 09:31:57 by dzhambal          #+#    #+#             */
/*   Updated: 2026/02/23 09:32:01 by dzhambal         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static t_node	*pop_top(t_stack *s)
{
	t_node	*n;
	t_node	*tail;
	t_node	*new_top;

	if (!s || s->size == 0)
		return (NULL);
	n = s->top;
	if (s->size == 1)
	{
		s->top = NULL;
		s->size = 0;
		n->next = NULL;
		n->prev = NULL;
		return (n);
	}
	tail = n->prev;
	new_top = n->next;
	tail->next = new_top;
	new_top->prev = tail;
	s->top = new_top;
	s->size--;
	n->next = NULL;
	n->prev = NULL;
	return (n);
}

static void	push_top_node(t_stack *dst, t_node *n)
{
	if (!dst || !n)
		return ;
	(void)stack_push_top(dst, n);
}

static void	push_top(t_stack *dst, t_stack *src)
{
	t_node	*n;

	n = pop_top(src);
	if (!n)
		return ;
	push_top_node(dst, n);
}

void	op_pa(t_stack *a, t_stack *b)
{
	push_top(a, b);
	bench_inc(a->bench, "pa");
	write(1, "pa\n", 3);
}

void	op_pb(t_stack *a, t_stack *b)
{
	push_top(b, a);
	bench_inc(b->bench, "pb");
	write(1, "pb\n", 3);
}
