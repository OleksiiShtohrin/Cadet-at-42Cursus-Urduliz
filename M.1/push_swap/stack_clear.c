/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   stack_clear.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dzhambal <dzhambal@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/23 09:37:27 by dzhambal          #+#    #+#             */
/*   Updated: 2026/02/23 09:37:29 by dzhambal         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static void	remove_top(t_stack *s)
{
	t_node	*n;
	t_node	*tail;
	t_node	*new_top;

	n = s->top;
	if (s->size == 1)
	{
		s->top = NULL;
		s->size = 0;
		free(n);
		return ;
	}
	tail = n->prev;
	new_top = n->next;
	tail->next = new_top;
	new_top->prev = tail;
	s->top = new_top;
	s->size--;
	free(n);
}

void	stack_clear(t_stack *s)
{
	if (!s)
		return ;
	while (s->size > 0)
		remove_top(s);
}
