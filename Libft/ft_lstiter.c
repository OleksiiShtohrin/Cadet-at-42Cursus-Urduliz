/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lstiter.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/24 15:12:39 by oshtohri          #+#    #+#             */
/*   Updated: 2026/01/27 16:43:57 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	ft_lstiter(t_list *lst, void (*f)(void *))
{
	if (lst == 0 || f == 0)
		return ;
	while (lst)
	{
		f(lst->content);
		lst = lst->next;
	}
}
/*
#include <stdio.h>

void	toupper_content(void *content)
{
	char	*str;
	int		i;

	str = (char *)content;
	i = 0;
	while (str[i])
	{
		str[i] = ft_toupper(str[i]);
		i++;
	}
}

void	print_content(void *content)
{
	printf("%s\n", (char *)content);
}

int	main(void)
{
	t_list	*head;
	t_list	*elem1;
	t_list	*elem2;

	elem1 = ft_lstnew(ft_strdup("hello"));
	elem2 = ft_lstnew(ft_strdup("world"));
	head = elem1;
	elem1->next = elem2;

	ft_lstiter(head, print_content);
	ft_lstiter(head, toupper_content);

	printf("\nAfter ft_lstiter (toupper):\n");
	ft_lstiter(head, print_content);

	ft_lstclear(&head, free);

	return (0);
}*/