/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   bench.h                                            :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/17 14:52:15 by oshtohri          #+#    #+#             */
/*   Updated: 2026/02/23 14:50:34 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef BENCH_H
# define BENCH_H

# include <stdlib.h>
# include <unistd.h>

/* Bench public API and context type. */

typedef struct s_bench
{
	int		enabled;
	double	disorder;
	char	name[32];
	char	complexity[32];
	long	cnt[11];
}	t_bench;

void		bench_init(t_bench *b);
void		bench_enable(t_bench *b);
void		bench_set_disorder(t_bench *b, double d);
void		bench_set_strategy(t_bench *b, const char *name,
				const char *complexity);
void		bench_inc(t_bench *b, const char *op);
void		bench_finish_print(t_bench *b);

const char	**bench_ops_names(void);

/* small I/O helpers used by bench printing */
void		write_str_fd(const char *s, int fd);
void		write_int_fd(long v, int fd);

#endif
