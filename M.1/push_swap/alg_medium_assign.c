/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   alg_medium_assign.c                                :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dzhambal <dzhambal@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/22 21:52:10 by dzhambal          #+#    #+#             */
/*   Updated: 2026/02/22 21:52:15 by dzhambal         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static int	fill_vals(int *vals, char *used, t_stack *a, int n)
{
	t_node	*cur;
	int		i;

	if (!a || n <= 0)
		return (1);
	cur = a->top;
	i = 0;
	while (i < n)
	{
		vals[i] = cur->value;
		used[i] = 0;
		i++;
		cur = cur->next;
	}
	return (1);
}

static int	get_min_pos(int *vals, char *used, int n)
{
	int	i;
	int	min;
	int	pos;
	int	first;

	i = 0;
	first = 1;
	pos = -1;
	min = 0;
	while (i < n)
	{
		if (!used[i] && (first || vals[i] < min))
		{
			min = vals[i];
			pos = i;
			first = 0;
		}
		i++;
	}
	return (pos);
}

static void	mark_index_for_value(t_stack *a, int value, int idx)
{
	t_node	*cur;
	int		i;

	if (!a || a->size <= 0)
		return ;
	cur = a->top;
	i = 0;
	while (i < a->size)
	{
		if (cur->value == value && cur->index == -1)
		{
			cur->index = idx;
			return ;
		}
		cur = cur->next;
		i++;
	}
}

static int	init_buffers(t_stack *a, int **vals, char **used, int *n)
{
	*n = a->size;
	if (*n <= 0)
		return (1);
	*vals = (int *)malloc(sizeof(int) * (*n));
	*used = (char *)malloc(sizeof(char) * (*n));
	if (!*vals || !*used)
	{
		free(*vals);
		free(*used);
		return (0);
	}
	if (!fill_vals(*vals, *used, a, *n))
	{
		free(*vals);
		free(*used);
		return (0);
	}
	return (1);
}

int	ps_assign_indices(t_stack *a)
{
	int		n;
	int		*vals;
	char	*used;
	int		idx;
	int		min_pos;

	if (!a)
		return (0);
	vals = NULL;
	used = NULL;
	if (!init_buffers(a, &vals, &used, &n))
		return (0);
	if (n <= 0)
		return (1);
	idx = 0;
	while (idx < n)
	{
		min_pos = get_min_pos(vals, used, n);
		mark_index_for_value(a, vals[min_pos], idx);
		used[min_pos] = 1;
		idx++;
	}
	free(vals);
	free(used);
	return (1);
}
