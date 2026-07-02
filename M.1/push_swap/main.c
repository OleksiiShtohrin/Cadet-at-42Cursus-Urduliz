/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   main.c                                             :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/17 15:06:31 by oshtohri          #+#    #+#             */
/*   Updated: 2026/02/24 14:16:47 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static int	is_sorted(t_stack *a)
{
	t_node	*n;
	int		i;

	if (!a || a->size < 2)
		return (1);
	n = a->top;
	i = 1;
	while (i < a->size)
	{
		if (n->value > n->next->value)
			return (0);
		n = n->next;
		i++;
	}
	return (1);
}

static int	bench_print_if_sorted(t_stack *a, t_stack *b,
				t_strategy strategy)
{
	if (!is_sorted(a))
		return (0);
	if (strategy == STRAT_SIMPLE)
		bench_set_strategy(a->bench, "Simple", "O(n^2)");
	else if (strategy == STRAT_MEDIUM)
		bench_set_strategy(a->bench, "Medium", "O(n*sqrt(n))");
	else if (strategy == STRAT_COMPLEX)
		bench_set_strategy(a->bench, "Complex", "O(n log n)");
	else
		bench_set_strategy(a->bench, "Adaptive", "O(n)");
	bench_finish_print(a->bench);
	stack_clear(a);
	stack_clear(b);
	return (1);
}

static void	run_with_strategy(t_stack *a, t_stack *b, t_strategy strategy)
{
	if (strategy == STRAT_SIMPLE)
	{
		bench_set_strategy(a->bench, "Simple", "O(n^2)");
		run_simple(a, b);
		return ;
	}
	if (strategy == STRAT_MEDIUM)
	{
		bench_set_strategy(a->bench, "Medium", "O(n*sqrt(n))");
		run_medium(a, b);
		return ;
	}
	if (strategy == STRAT_COMPLEX)
	{
		bench_set_strategy(a->bench, "Complex", "O(n log n)");
		run_complex(a, b);
		return ;
	}
	run_adaptive(a, b);
}

int	main(int argc, char **argv)
{
	t_stack		a;
	t_stack		b;
	t_strategy	strategy;
	t_bench		bench;

	if (argc < 2)
		return (0);
	stack_init(&a);
	stack_init(&b);
	bench_init(&bench);
	a.bench = &bench;
	b.bench = &bench;
	if (!parse_args(argc, argv, &a, &strategy))
		return (stack_clear(&a), ps_error(), 1);
	bench_set_disorder(&bench, compute_disorder(&a));
	if (bench_print_if_sorted(&a, &b, strategy))
		return (0);
	run_with_strategy(&a, &b, strategy);
	bench_finish_print(&bench);
	stack_clear(&a);
	stack_clear(&b);
	return (0);
}
