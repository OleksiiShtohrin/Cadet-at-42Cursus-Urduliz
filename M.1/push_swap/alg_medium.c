/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   alg_medium.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dzhambal <dzhambal@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/22 21:51:24 by dzhambal          #+#    #+#             */
/*   Updated: 2026/02/23 12:07:19 by dzhambal         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static void	push_chunks(t_stack *a, t_stack *b, int chunk)
{
	int	cur_max;
	int	pos;
	int	current_idx;

	cur_max = chunk - 1;
	while (a->size > 0)
	{
		pos = ps_find_best_pos(a, cur_max);
		if (pos == -1)
		{
			cur_max += chunk;
			continue ;
		}
		ps_rotate_to_top(a, pos, 1);
		current_idx = a->top->index;
		op_pb(a, b);
		if (b->size > 1 && current_idx < (cur_max - chunk / 2))
			op_rb(b);
	}
}

static void	pull_back(t_stack *a, t_stack *b)
{
	int	pos;

	while (b->size > 0)
	{
		pos = ps_find_max_pos(b);
		ps_rotate_to_top(b, pos, 0);
		op_pa(a, b);
	}
}

void	run_medium(t_stack *a, t_stack *b)
{
	int	n;
	int	chunk;

	if (!a || !b || a->size < 2)
		return ;
	if (!ps_assign_indices(a))
		return ;
	n = a->size;
	chunk = ps_calc_chunk(n);
	push_chunks(a, b, chunk);
	pull_back(a, b);
}
