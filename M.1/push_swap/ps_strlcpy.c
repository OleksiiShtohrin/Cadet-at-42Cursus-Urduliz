/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ps_strlcpy.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/15 12:40:51 by oshtohri          #+#    #+#             */
/*   Updated: 2026/02/21 15:45:22 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

size_t	ps_strlcpy(char *dst, const char *src, size_t size)
{
	size_t	s_len;
	size_t	i;

	s_len = 0;
	while (src[s_len] != '\0')
		s_len++;
	if (size == 0)
		return (s_len);
	i = 0;
	while (src[i] && i < size - 1)
	{
		dst[i] = src[i];
		i++;
	}
	dst[i] = '\0';
	return (s_len);
}
