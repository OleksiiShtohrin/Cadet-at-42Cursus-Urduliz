/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   heapify.c                                          :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/25 12:43:09 by oshtohri          #+#    #+#             */
/*   Updated: 2026/06/26 09:36:13 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "codexion.h"

void	heapify_up(t_heap *heap, int idx, t_schedule_policy policy)
{
	int	parent;

	while (idx > 0)
	{
		parent = (idx - 1) / 2;
		if (heap_compare(heap->nodes[idx], heap->nodes[parent], policy))
		{
			heap_swap(&heap->nodes[idx], &heap->nodes[parent]);
			idx = parent;
		}
		else
			break ;
	}
}

void	heapify_down(t_heap *heap, int idx, t_schedule_policy policy)
{
	int	left;
	int	right;
	int	smallest;

	while (1)
	{
		left = 2 * idx + 1;
		right = 2 * idx + 2;
		smallest = idx;
		if (left < heap->size
			&& heap_compare(heap->nodes[left], heap->nodes[smallest], policy))
			smallest = left;
		if (right < heap->size
			&& heap_compare(heap->nodes[right], heap->nodes[smallest], policy))
			smallest = right;
		if (smallest != idx)
		{
			heap_swap(&heap->nodes[idx], &heap->nodes[smallest]);
			idx = smallest;
		}
		else
			break ;
	}
}
