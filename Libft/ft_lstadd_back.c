/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lstadd_back.c                                   :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/24 13:42:39 by oshtohri          #+#    #+#             */
/*   Updated: 2026/01/27 16:42:18 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	ft_lstadd_back(t_list **lst, t_list *new)
{
	t_list	*last;

	if (lst == 0 || new == 0)
		return ;
	if (*lst == 0)
	{
		*lst = new;
		return ;
	}
	last = ft_lstlast(*lst);
	last->next = new;
}
/*
#include <stdio.h>

void	print_list(t_list *lst)
{
	if (!lst)
	{
		printf("(Null)\n");
		return ;
	}
	while (lst)
	{
		printf("[%s] -> ", (char *)lst->content);
		lst = lst->next;
	}
	printf("NULL\n");
}

int	main(void)
{
	t_list	*head = NULL;
	t_list	*new_node;

	new_node = ft_lstnew("Node 1");
	ft_lstadd_back(&head, new_node);
	print_list(head);

	ft_lstadd_back(&head, ft_lstnew("Node 2"));
	print_list(head);

	ft_lstadd_back(&head, ft_lstnew("Node 3"));
	print_list(head);

	t_list *tmp;
	while (head)
	{
		tmp = head->next;
		free(head);
		head = tmp;
	}
	return (0);
}*/