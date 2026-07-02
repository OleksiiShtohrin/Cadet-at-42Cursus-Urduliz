/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   alg_adaptive.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dzhambal <dzhambal@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/22 21:34:48 by dzhambal          #+#    #+#             */
/*   Updated: 2026/02/22 21:34:55 by dzhambal         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

int	ps_choose_strategy(double disorder)
{
	if (disorder < 0.2)
		return (0);
	if (disorder < 0.5)
		return (1);
	return (2);
}

static void	run_small(t_stack *a, t_stack *b)
{
	if (a->size == 2)
	{
		bench_set_strategy(a->bench, "Adaptive", "O(n)");
		run_2(a, b);
	}
	else if (a->size == 3)
	{
		bench_set_strategy(a->bench, "Adaptive", "O(n)");
		run_3(a, b);
	}
	else if (a->size == 4)
	{
		bench_set_strategy(a->bench, "Adaptive", "O(n)");
		run_4(a, b);
	}
	else if (a->size == 5)
	{
		bench_set_strategy(a->bench, "Adaptive", "O(n)");
		run_5(a, b);
	}
}

static void	run_strategy(int s, t_stack *a, t_stack *b)
{
	if (s == 0)
	{
		bench_set_strategy(a->bench, "Adaptive", "O(n^2)");
		run_simple(a, b);
	}
	else if (s == 1)
	{
		bench_set_strategy(a->bench, "Adaptive", "O(n*sqrt(n))");
		run_medium(a, b);
	}
	else
	{
		bench_set_strategy(a->bench, "Adaptive", "O(n log n)");
		run_complex(a, b);
	}
}

void	run_adaptive(t_stack *a, t_stack *b)
{
	double	dis;
	int		s;

	if (!a || !b)
		return ;
	if (a->size < 2)
		return ;
	if (a->size <= 5)
	{
		run_small(a, b);
		return ;
	}
	if (a->bench != NULL)
		dis = a->bench->disorder;
	else
		dis = compute_disorder(a);
	s = ps_choose_strategy(dis);
	run_strategy(s, a, b);
}
