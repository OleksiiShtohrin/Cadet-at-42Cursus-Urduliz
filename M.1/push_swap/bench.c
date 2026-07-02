/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   bench.c                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/17 14:52:45 by oshtohri          #+#    #+#             */
/*   Updated: 2026/02/22 17:12:47 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

void	bench_init(t_bench *b)
{
	int	i;

	if (!b)
		return ;
	b->enabled = 0;
	b->disorder = 0.0;
	b->name[0] = '\0';
	b->complexity[0] = '\0';
	i = 0;
	while (i < 11)
	{
		b->cnt[i] = 0;
		i++;
	}
}

void	bench_enable(t_bench *b)
{
	if (!b)
		return ;
	b->enabled = 1;
}

void	bench_set_strategy(t_bench *b, const char *name, const char *complexity)
{
	if (!b)
		return ;
	if (name != NULL)
		(void)ps_strlcpy(b->name, name, sizeof(b->name));
	if (complexity != NULL)
		(void)ps_strlcpy(b->complexity, complexity, sizeof(b->complexity));
}

static int	op_index(const char *op)
{
	int			i;
	const char	**names;

	if (!op)
		return (-1);
	names = bench_ops_names();
	i = 0;
	while (i < 11)
	{
		if (ps_strncmp(op, names[i], ps_strlen(names[i]) + 1) == 0)
			return (i);
		i++;
	}
	return (-1);
}

void	bench_inc(t_bench *b, const char *op)
{
	int	i;

	if (!b || !b->enabled || !op)
		return ;
	i = op_index(op);
	if (i < 0)
		return ;
	b->cnt[i] += 1;
}
