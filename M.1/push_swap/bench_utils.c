/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   bench_utils.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/17 14:54:11 by oshtohri          #+#    #+#             */
/*   Updated: 2026/02/22 17:12:31 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

const char	**bench_ops_names(void)
{
	static const char	*names[11] = {
		"sa", "sb", "ss",
		"pa", "pb",
		"ra", "rb", "rr",
		"rra", "rrb", "rrr"
	};

	return ((const char **)names);
}

void	write_str_fd(const char *s, int fd)
{
	if (s == NULL)
		return ;
	(void)write(fd, s, ps_strlen(s));
}

void	write_int_fd(long v, int fd)
{
	char	*s;

	s = ps_itoa((int)v);
	if (s == NULL)
		return ;
	write_str_fd(s, fd);
	free(s);
}

void	bench_set_disorder(t_bench *b, double d)
{
	if (!b)
		return ;
	b->disorder = d;
}
