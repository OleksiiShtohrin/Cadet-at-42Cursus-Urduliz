/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lstadd_front.c                                  :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/24 12:59:59 by oshtohri          #+#    #+#             */
/*   Updated: 2026/01/27 16:42:46 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	ft_lstadd_front(t_list **lst, t_list *new)
{
	if (lst == 0 || new == 0)
		return ;
	new->next = *lst;
	*lst = new;
}
/*
#include <stdio.h>

int	main(void)
{
	t_list		*start = NULL;

	ft_lstadd_front(&start, ft_lstnew(ft_strdup("42")));
    ft_lstadd_front(&start, ft_lstnew(ft_strdup("de")));
    ft_lstadd_front(&start, ft_lstnew(ft_strdup("estudiante")));
    ft_lstadd_front(&start, ft_lstnew(ft_strdup("Hola")));

    t_list *tmp = start;
    while (tmp)
    {
        printf("%s ", (char *)tmp->content);
        tmp = tmp->next;
    }

	ft_lstclear(&start, free);

    return (0);
}*/