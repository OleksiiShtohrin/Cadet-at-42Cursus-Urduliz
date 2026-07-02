/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   stack_node.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dzhambal <dzhambal@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/23 09:38:01 by dzhambal          #+#    #+#             */
/*   Updated: 2026/02/23 09:38:04 by dzhambal         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

t_node	*node_new(int value)
{
	t_node	*n;

	n = (t_node *)malloc(sizeof(t_node));
	if (!n)
		return (NULL);
	n->value = value;
	n->index = -1;
	n->prev = NULL;
	n->next = NULL;
	return (n);
}

static void	link_single(t_stack *s, t_node *n)
{
	n->next = n;
	n->prev = n;
	s->top = n;
	s->size = 1;
}

int	stack_push_top(t_stack *s, t_node *n)
{
	t_node	*tail;

	if (!s || !n)
		return (0);
	if (s->top == NULL)
		return (link_single(s, n), 1);
	tail = s->top->prev;
	n->next = s->top;
	n->prev = tail;
	tail->next = n;
	s->top->prev = n;
	s->top = n;
	s->size++;
	return (1);
}

int	stack_push_bottom(t_stack *s, t_node *n)
{
	t_node	*tail;

	if (!s || !n)
		return (0);
	if (s->top == NULL)
		return (link_single(s, n), 1);
	tail = s->top->prev;
	n->next = s->top;
	n->prev = tail;
	tail->next = n;
	s->top->prev = n;
	s->size++;
	return (1);
}
