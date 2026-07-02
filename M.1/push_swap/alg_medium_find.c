/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   alg_medium_find.c                                  :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dzhambal <dzhambal@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/23 09:27:44 by dzhambal          #+#    #+#             */
/*   Updated: 2026/02/23 12:29:53 by dzhambal         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int	ps_calc_chunk(int n)
{
	if (n <= 10)
		return (5);
	if (n <= 100)
		return (20);
	return (40);
}

int	ps_find_pos_eq(t_stack *s, int target)
{
	t_node	*cur;
	int		pos;

	if (!s || s->size <= 0)
		return (-1);
	cur = s->top;
	pos = 0;
	while (pos < s->size)
	{
		if (cur->index == target)
			return (pos);
		cur = cur->next;
		pos++;
	}
	return (-1);
}

int	ps_find_best_pos(t_stack *s, int target)
{
	int		i;
	int		first_match;
	int		last_match;
	t_node	*cur;

	cur = s->top;
	i = 0;
	first_match = -1;
	last_match = -1;
	while (i < s->size)
	{
		if (cur->index <= target)
		{
			if (first_match == -1)
				first_match = i;
			last_match = i;
		}
		cur = cur->next;
		i++;
	}
	if (first_match == -1)
		return (-1);
	if (first_match <= (s->size - last_match))
		return (first_match);
	return (last_match);
}

int	ps_find_max_pos(t_stack *s)
{
	t_node	*cur;
	int		max_idx;
	int		pos;
	int		best_pos;

	cur = s->top;
	max_idx = -1;
	pos = 0;
	best_pos = 0;
	while (pos < s->size)
	{
		if (cur->index > max_idx)
		{
			max_idx = cur->index;
			best_pos = pos;
		}
		cur = cur->next;
		pos++;
	}
	return (best_pos);
}
