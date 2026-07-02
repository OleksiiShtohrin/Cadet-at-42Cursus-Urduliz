/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   heap_ops.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/25 12:40:15 by oshtohri          #+#    #+#             */
/*   Updated: 2026/06/26 09:36:34 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

void	heap_swap(t_heap_node *a, t_heap_node *b)
{
	t_heap_node	tmp;

	tmp = *a;
	*a = *b;
	*b = tmp;
}

int	heap_compare(t_heap_node a, t_heap_node b, t_schedule_policy policy)
{
	if (a.priority < b.priority)
		return (1);
	if (a.priority > b.priority)
		return (0);
	if (policy == POLICY_EDF)
	{
		if (a.coder->id < b.coder->id)
			return (1);
		return (0);
	}
	else
	{
		if (a.arrival < b.arrival)
			return (1);
		return (0);
	}
}

int	heap_push(
	t_heap *heap, t_coder *coder, long priority, t_schedule_policy policy)
{
	if (heap->size >= heap->capacity)
		return (1);
	heap->nodes[heap->size].coder = coder;
	heap->nodes[heap->size].priority = priority;
	heap->nodes[heap->size].arrival = heap->arrival_counter;
	heap->arrival_counter++;
	heapify_up(heap, heap->size, policy);
	heap->size++;
	return (0);
}

t_coder	*heap_pop(t_heap *heap, t_schedule_policy policy)
{
	t_coder	*coder;

	if (heap->size == 0)
		return (NULL);
	coder = heap->nodes[0].coder;
	heap->size--;
	if (heap->size > 0)
	{
		heap->nodes[0] = heap->nodes[heap->size];
		heapify_down(heap, 0, policy);
	}
	return (coder);
}
