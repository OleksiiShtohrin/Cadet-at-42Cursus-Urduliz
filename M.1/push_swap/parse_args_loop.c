/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   parse_args_loop.c                                  :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/23 12:49:30 by oshtohri          #+#    #+#             */
/*   Updated: 2026/02/23 14:50:39 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static void	ctx_init(t_parse_ctx *ctx, t_stack *a, t_strategy *strategy)
{
	ctx->a = a;
	ctx->strategy = strategy;
	ctx->strategy_seen = 0;
	ctx->bench_seen = 0;
}

static int	set_bench(t_parse_ctx *ctx)
{
	if (ctx->bench_seen)
		return (0);
	ctx->bench_seen = 1;
	bench_enable(ctx->a->bench);
	return (1);
}

static int	set_strategy(char *arg, t_parse_ctx *ctx)
{
	if (ctx->strategy_seen)
		return (0);
	ctx->strategy_seen = 1;
	if (ps_streq(arg, "--simple"))
		*(ctx->strategy) = STRAT_SIMPLE;
	else if (ps_streq(arg, "--medium"))
		*(ctx->strategy) = STRAT_MEDIUM;
	else if (ps_streq(arg, "--complex"))
		*(ctx->strategy) = STRAT_COMPLEX;
	else
		*(ctx->strategy) = STRAT_ADAPTIVE;
	return (1);
}

static int	parse_one_arg(char *arg, t_parse_ctx *ctx)
{
	if (ps_strcmp(arg, "--bench") == 0)
		return (set_bench(ctx));
	if (ps_streq(arg, "--simple") || ps_streq(arg, "--medium")
		|| ps_streq(arg, "--complex") || ps_streq(arg, "--adaptive"))
		return (set_strategy(arg, ctx));
	return (ps_add_arg_as_tokens(ctx->a, arg));
}

int	ps_parse_args_loop(int argc, char **argv, t_stack *a, t_strategy *strategy)
{
	int			i;
	t_parse_ctx	ctx;

	ctx_init(&ctx, a, strategy);
	i = 1;
	while (i < argc)
	{
		if (!parse_one_arg(argv[i], &ctx))
			return (0);
		i++;
	}
	return (1);
}
