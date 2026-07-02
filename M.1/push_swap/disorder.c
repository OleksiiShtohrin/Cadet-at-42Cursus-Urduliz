/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   disorder.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dzhambal <dzhambal@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/23 09:31:16 by dzhambal          #+#    #+#             */
/*   Updated: 2026/02/23 09:31:20 by dzhambal         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static long	count_for_i(t_node *i, int start, int size, long *total)
{
	t_node	*j;
	int		cj;
	long	mistakes;

	j = i->next;
	cj = start;
	mistakes = 0;
	while (cj < size)
	{
		(*total)++;
		if (i->value > j->value)
			mistakes++;
		j = j->next;
		cj++;
	}
	return (mistakes);
}

static long	count_mistakes(t_stack *a, long *total)
{
	t_node	*i;
	int		ci;
	long	mistakes;

	i = a->top;
	ci = 0;
	mistakes = 0;
	*total = 0;
	while (ci < a->size)
	{
		mistakes += count_for_i(i, ci + 1, a->size, total);
		i = i->next;
		ci++;
	}
	return (mistakes);
}

double	compute_disorder(t_stack *a)
{
	long	total;
	long	mistakes;

	if (!a || a->size < 2 || a->top == NULL)
		return (0.0);
	mistakes = count_mistakes(a, &total);
	if (total == 0)
		return (0.0);
	return ((double)mistakes / (double)total);
}
