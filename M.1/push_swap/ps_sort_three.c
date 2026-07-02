/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ps_sort_three.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dzhambal <dzhambal@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/23 09:35:08 by dzhambal          #+#    #+#             */
/*   Updated: 2026/02/23 09:35:11 by dzhambal         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	ps_sort_three(t_stack *s)
{
	int	a;
	int	b;
	int	c;

	if (!s || s->size != 3)
		return ;
	a = s->top->value;
	b = s->top->next->value;
	c = s->top->prev->value;
	if (a > b && b < c && a < c)
		op_sa(s);
	else if (a > b && b > c)
	{
		op_sa(s);
		op_rra(s);
	}
	else if (a > b && b < c && a > c)
		op_ra(s);
	else if (a < b && b > c && a < c)
	{
		op_sa(s);
		op_ra(s);
	}
	else if (a < b && b > c && a > c)
		op_rra(s);
}
