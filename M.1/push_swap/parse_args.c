/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   parse_args.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/23 12:49:43 by oshtohri          #+#    #+#             */
/*   Updated: 2026/02/23 15:02:36 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static int	add_token(t_stack *a, const char *token)
{
	int		value;
	t_node	*n;

	if (!ps_atoi_safe(token, &value))
		return (0);
	n = node_new(value);
	if (!n)
		return (0);
	if (!stack_push_bottom(a, n))
	{
		free(n);
		return (0);
	}
	return (1);
}

int	ps_add_arg_as_tokens(t_stack *a, const char *arg)
{
	char	**parts;
	size_t	i;

	parts = ps_split_spaces(arg);
	if (!parts)
		return (0);
	if (parts[0] == NULL)
	{
		ps_split_free(parts);
		return (0);
	}
	i = 0;
	while (parts[i])
	{
		if (!add_token(a, parts[i]))
		{
			ps_split_free(parts);
			return (0);
		}
		i++;
	}
	ps_split_free(parts);
	return (1);
}

static int	has_duplicate(t_stack *a)
{
	t_node	*x;
	t_node	*y;
	int		i;
	int		j;

	if (!a || a->size < 2)
		return (0);
	i = 0;
	x = a->top;
	while (i < a->size)
	{
		j = i + 1;
		y = x->next;
		while (j < a->size)
		{
			if (x->value == y->value)
				return (1);
			y = y->next;
			j++;
		}
		x = x->next;
		i++;
	}
	return (0);
}

int	parse_args(int argc, char **argv, t_stack *a, t_strategy *strategy)
{
	if (!a || !strategy)
		return (0);
	*strategy = STRAT_ADAPTIVE;
	if (!ps_parse_args_loop(argc, argv, a, strategy))
		return (0);
	if (has_duplicate(a))
		return (0);
	return (1);
}
