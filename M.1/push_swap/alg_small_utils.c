/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   alg_small_utils.c                                  :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dzhambal <dzhambal@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/23 09:30:36 by dzhambal          #+#    #+#             */
/*   Updated: 2026/02/23 09:30:42 by dzhambal         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static int	ps_min_pos(t_stack *a)
{
	t_node	*cur;
	int		min;
	int		pos;
	int		i;

	if (!a || a->size == 0)
		return (0);
	cur = a->top;
	min = cur->value;
	pos = 0;
	i = 0;
	while (i < a->size)
	{
		if (cur->value < min)
		{
			min = cur->value;
			pos = i;
		}
		cur = cur->next;
		i++;
	}
	return (pos);
}

static void	ps_rot_up(t_stack *a, int count)
{
	int	i;

	i = 0;
	while (i < count)
	{
		op_ra(a);
		i++;
	}
}

static void	ps_rot_down(t_stack *a, int count)
{
	int	i;

	i = 0;
	while (i < count)
	{
		op_rra(a);
		i++;
	}
}

void	ps_rotate_min_to_top(t_stack *a)
{
	int	pos;

	if (!a || a->size < 2)
		return ;
	pos = ps_min_pos(a);
	if (pos <= a->size / 2)
		ps_rot_up(a, pos);
	else
		ps_rot_down(a, a->size - pos);
}
