/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   alg_simple.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dzhambal <dzhambal@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/23 09:29:36 by dzhambal          #+#    #+#             */
/*   Updated: 2026/02/23 09:29:40 by dzhambal         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static int	find_min_pos(t_stack *a)
{
	t_node	*cur;
	int		min;
	int		min_pos;
	int		i;

	if (!a || a->size == 0)
		return (0);
	cur = a->top;
	i = 0;
	min = cur->value;
	min_pos = 0;
	while (i < a->size)
	{
		if (cur->value < min)
		{
			min = cur->value;
			min_pos = i;
		}
		cur = cur->next;
		i++;
	}
	return (min_pos);
}

static void	rotate_to_top(t_stack *a, int pos)
{
	int	half;
	int	i;

	if (!a || a->size < 2 || pos <= 0)
		return ;
	half = a->size / 2;
	i = 0;
	if (pos <= half)
	{
		while (i < pos)
		{
			op_ra(a);
			i++;
		}
	}
	else
	{
		while (i < (a->size - pos))
		{
			op_rra(a);
			i++;
		}
	}
}

/* run_simple: push minima to b until 3 left, sort them, push back */
void	run_simple(t_stack *a, t_stack *b)
{
	int	pos;

	if (!a || !b)
		return ;
	while (a->size > 3)
	{
		pos = find_min_pos(a);
		rotate_to_top(a, pos);
		op_pb(a, b);
	}
	if (a->size == 3)
		ps_sort_three(a);
	else if (a->size == 2 && a->top->value > a->top->next->value)
		op_sa(a);
	while (b->size > 0)
		op_pa(a, b);
}
