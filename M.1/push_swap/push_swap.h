/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   push_swap.h                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/17 15:07:25 by oshtohri          #+#    #+#             */
/*   Updated: 2026/02/23 14:50:30 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef PUSH_SWAP_H
# define PUSH_SWAP_H

# include "bench.h"
# include <limits.h>
# include <stddef.h>
# include <string.h>
# include <stdlib.h>
# include <unistd.h>

typedef struct s_node
{
	int				value;
	int				index;
	struct s_node	*prev;
	struct s_node	*next;
}	t_node;

typedef struct s_stack
{
	t_node	*top;
	int		size;
	t_bench	*bench;
}	t_stack;

typedef enum e_strategy
{
	STRAT_ADAPTIVE = 0,
	STRAT_SIMPLE = 1,
	STRAT_MEDIUM = 2,
	STRAT_COMPLEX = 3
}	t_strategy;

typedef struct s_parse_ctx
{
	t_stack		*a;
	t_strategy	*strategy;
	int			strategy_seen;
	int			bench_seen;
}	t_parse_ctx;

/* error / output */
int		ps_error(void);

/* small string utils */
int		ps_isdigit(int c);
int		ps_isspace(int c);
int		ps_strcmp(char *s1, char *s2);
int		ps_streq(const char *a, const char *b);

/* split and parsing numbers */
char	**ps_split_spaces(const char *s);
void	ps_split_free(char **parts);
int		ps_atoi_safe(const char *s, int *out);

/* stack basics */
void	stack_init(t_stack *s);
t_node	*node_new(int value);
int		stack_push_top(t_stack *s, t_node *n);
int		stack_push_bottom(t_stack *s, t_node *n);
void	stack_clear(t_stack *s);

/* parse argv -> stack a, strategy flags */
int		parse_args(int argc, char **argv, t_stack *a,
			t_strategy *strategy);
int		ps_parse_args_loop(int argc, char **argv, t_stack *a,
			t_strategy *strategy);
int		ps_add_arg_as_tokens(t_stack *a, const char *arg);

/* disorder */
double	compute_disorder(t_stack *a);

/* operations (print to stdout) */
void	op_sa(t_stack *a);
void	op_sb(t_stack *b);
void	op_ss(t_stack *a, t_stack *b);
void	op_pa(t_stack *a, t_stack *b);
void	op_pb(t_stack *a, t_stack *b);
void	op_ra(t_stack *a);
void	op_rb(t_stack *b);
void	op_rr(t_stack *a, t_stack *b);
void	op_rra(t_stack *a);
void	op_rrb(t_stack *b);
void	op_rrr(t_stack *a, t_stack *b);

/* algorithms */
void	run_simple(t_stack *a, t_stack *b);
void	run_medium(t_stack *a, t_stack *b);
void	run_complex(t_stack *a, t_stack *b);
void	run_adaptive(t_stack *a, t_stack *b);
void	ps_sort_three(t_stack *s);

/* adaptive and small*/
int		ps_choose_strategy(double disorder);
void	run_2(t_stack *a, t_stack *b);
void	run_3(t_stack *a, t_stack *b);
void	run_4(t_stack *a, t_stack *b);
void	run_5(t_stack *a, t_stack *b);
void	ps_rotate_min_to_top(t_stack *a);

/* utils for medium */
int		ps_assign_indices(t_stack *a);
int		ps_calc_chunk(int n);
int		ps_find_best_pos(t_stack *s, int target);
int		ps_find_max_pos(t_stack *s);
int		ps_find_pos_eq(t_stack *s, int target);
void	ps_rotate_to_top(t_stack *s, int pos, int is_a);

/* utils for complex */
int		ps_get_max_bits(int n);
void	ps_do_bit_pass(t_stack *a, t_stack *b, int bit);

/* Libc functions */
char	*ps_itoa(int n);
size_t	ps_strlcpy(char *dst, const char *src, size_t size);
size_t	ps_strlen(const char *s);
int		ps_strncmp(const char *s1, const char *s2, size_t n);

#endif
