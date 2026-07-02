/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lstlast.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/24 13:09:29 by oshtohri          #+#    #+#             */
/*   Updated: 2026/01/27 16:45:14 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

t_list	*ft_lstlast(t_list *lst)
{
	if (lst == 0)
		return (0);
	while (lst->next)
		lst = lst->next;
	return (lst);
}
/*
#include <stdio.h>

int	main(void)
{
	t_list	*elem1 = ft_lstnew("Node 1");
	t_list	*elem2 = ft_lstnew("Node 2");
	t_list	*elem3 = ft_lstnew("Node last");
	t_list	*last;

	elem1->next = elem2;
	elem2->next = elem3;

	last = ft_lstlast(elem1);
	if (last)
		printf("Last: '%s'\n", (char *)last->content);
	else
		printf("error: NULL\n");

	last = ft_lstlast(elem3);
	if (last)
		printf("Last: '%s'\n", (char *)last->content);

	last = ft_lstlast(NULL);
	if (last == NULL)
		printf("ok\n");
	else
		printf("error\n");

	free(elem1);
	free(elem2);
	free(elem3);

	return (0);
}*/