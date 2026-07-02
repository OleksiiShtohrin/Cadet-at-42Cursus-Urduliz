/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   alg_medium_rotate.c                                :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dzhambal <dzhambal@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/23 09:28:49 by dzhambal          #+#    #+#             */
/*   Updated: 2026/02/23 09:28:54 by dzhambal         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static void	do_rotate(t_stack *s, int times, int is_a)
{
	int	i;

	i = 0;
	while (i < times)
	{
		if (is_a)
			op_ra(s);
		else
			op_rb(s);
		i++;
	}
}

static void	do_rev_rotate(t_stack *s, int times, int is_a)
{
	int	i;

	i = 0;
	while (i < times)
	{
		if (is_a)
			op_rra(s);
		else
			op_rrb(s);
		i++;
	}
}

void	ps_rotate_to_top(t_stack *s, int pos, int is_a)
{
	int	half;

	if (!s || s->size < 2 || pos <= 0)
		return ;
	half = s->size / 2;
	if (pos <= half)
		do_rotate(s, pos, is_a);
	else
		do_rev_rotate(s, s->size - pos, is_a);
}
