/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lstdelone.c                                     :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/24 13:43:08 by oshtohri          #+#    #+#             */
/*   Updated: 2026/01/27 16:43:31 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	ft_lstdelone(t_list *lst, void (*del)(void *))
{
	if (lst == 0 || del == 0)
		return ;
	del(lst->content);
	free(lst);
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
	t_list		*elem1;
	t_list		*elem2;
	t_list		*elem3;
	char		*str1 = ft_strdup("Hello");
	char		*str2 = ft_strdup("world");
	char		*str3 = ft_strdup("2026!");

	elem1 = ft_lstnew(str1);
	elem2 = ft_lstnew(str2);
	elem3 = ft_lstnew(str3);

	printf("Node 1: %s\n", (char *)elem1->content);
	printf("Node 2: %s\n", (char *)elem2->content);
	printf("Node 3: %s\n", (char *)elem3->content);

	ft_lstdelone(elem1, del_content);
	ft_lstdelone(elem2, del_content);
	ft_lstdelone(elem3, del_content);

	printf("All clean.\n");
	return (0);
}*/