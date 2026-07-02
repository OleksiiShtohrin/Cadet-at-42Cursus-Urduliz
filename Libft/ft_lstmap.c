/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lstmap.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/24 15:23:53 by oshtohri          #+#    #+#             */
/*   Updated: 2026/01/27 16:47:21 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

t_list	*ft_lstmap(t_list *lst, void *(*f)(void *), void (*del)(void *))
{
	t_list	*list;
	t_list	*node;
	void	*cont;

	if (lst == 0 || f == 0 || del == 0)
		return (NULL);
	list = 0;
	while (lst)
	{
		cont = f(lst->content);
		node = ft_lstnew(cont);
		if (node == 0)
		{
			del(cont);
			ft_lstclear(&list, del);
			return (NULL);
		}
		ft_lstadd_back(&list, node);
		lst = lst->next;
	}
	return (list);
}
/*
#include <stdio.h>

void	*square_content(void *content)
{
	int	*new_val;

	new_val = malloc(sizeof(int));
	if (!new_val)
		return (NULL);
	*new_val = (*(int *)content) * (*(int *)content);
	return (new_val);
}

void	del_content(void *content)
{
	if (content == 0)
		return ;
	printf("Deleted: %d\n", *(int *)content);
	free(content);
}

int	main(void)
{
	t_list	*lst;
	t_list	*new_lst;
	int		*val;

	lst = NULL;
	for (int i = 1; i <= 3; i++)
	{
		val = malloc(sizeof(int));
		*val = i;
		ft_lstadd_back(&lst, ft_lstnew(val));
	}

	new_lst = ft_lstmap(lst, square_content, del_content);

	t_list *temp = new_lst;
	while (temp)
	{
		printf("%d ", *(int *)(temp->content));
		temp = temp->next;
	}
	printf("\n");

	ft_lstclear(&lst, del_content);
	ft_lstclear(&new_lst, del_content);

	return (0);
}*/