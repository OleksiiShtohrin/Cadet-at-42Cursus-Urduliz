/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   bench_print.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/17 14:54:23 by oshtohri          #+#    #+#             */
/*   Updated: 2026/02/22 17:13:37 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static void	print_disorder_percent(double disorder)
{
	int		tmp;
	int		int_part;
	int		frac;
	char	buf[3];

	tmp = (int)(disorder * 10000.0 + 0.5);
	int_part = tmp / 100;
	frac = tmp % 100;
	write_str_fd("[bench] disorder: ", 2);
	write_int_fd(int_part, 2);
	write_str_fd(".", 2);
	buf[0] = '0' + (char)(frac / 10);
	buf[1] = '0' + (char)(frac % 10);
	buf[2] = '\0';
	write_str_fd(buf, 2);
	write_str_fd("%\n", 2);
}

static void	print_header(t_bench *p, long total)
{
	if (!p)
		return ;
	print_disorder_percent(p->disorder);
	write_str_fd("[bench] strategy: ", 2);
	write_str_fd(p->name, 2);
	write_str_fd(" / ", 2);
	write_str_fd(p->complexity, 2);
	write_str_fd("\n", 2);
	write_str_fd("[bench] total ops: ", 2);
	write_int_fd(total, 2);
	write_str_fd("\n", 2);
}

static void	print_counts_part(t_bench *p, int start, int end)
{
	const char	**names;
	int			i;

	if (!p)
		return ;
	names = bench_ops_names();
	write_str_fd("[bench] ", 2);
	i = start;
	while (i <= end)
	{
		write_str_fd(names[i], 2);
		write_str_fd(": ", 2);
		write_int_fd(p->cnt[i], 2);
		if (i < end)
			write_str_fd("  ", 2);
		i++;
	}
	write_str_fd("\n", 2);
}

void	print_counts(t_bench *p)
{
	if (!p)
		return ;
	print_counts_part(p, 0, 4);
	print_counts_part(p, 5, 10);
}

void	bench_finish_print(t_bench *p)
{
	int		i;
	long	total;

	if (!p || !p->enabled)
		return ;
	total = 0;
	i = 0;
	while (i < 11)
	{
		total += p->cnt[i];
		i++;
	}
	print_header(p, total);
	print_counts(p);
}
