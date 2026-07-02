/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lstclear.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/24 13:44:43 by oshtohri          #+#    #+#             */
/*   Updated: 2026/01/26 17:49:11 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	ft_lstclear(t_list **lst, void (*del)(void *))
{
	t_list	*temp;

	if (lst == 0 || del == 0 || *lst == 0)
		return ;
	while (*lst)
	{
		temp = (*lst)->next;
		ft_lstdelone(*lst, del);
		*lst = temp;
	}
	*lst = NULL;
}
/*
#include <stdio.h>

void	del_content(void *content)
{
	if (content == 0)
		return ;
	printf("Deleted: %s\n", (char *)content);
	free(content);
}

int	main(void)
{
	t_list	*elem1;
	t_list	*elem2;
	t_list	*elem3;

	elem1 = ft_lstnew(ft_strdup("Node 1"));
	elem2 = ft_lstnew(ft_strdup("Node 2"));
	elem3 = ft_lstnew(ft_strdup("Node 3"));

	elem1->next = elem2;
	elem2->next = elem3;

	printf("Start: %p\n", elem1);

	ft_lstclear(&elem1, del_content);

	if (elem1 == NULL)
		printf("Start: %p\n", elem1);
	else
		printf("error not free\n");

	return (0);
}*/