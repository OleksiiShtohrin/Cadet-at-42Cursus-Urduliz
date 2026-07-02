/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lstnew.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/24 12:54:07 by oshtohri          #+#    #+#             */
/*   Updated: 2026/01/27 16:48:21 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

t_list	*ft_lstnew(void *content)
{
	t_list	*l_new;

	l_new = (t_list *) malloc(sizeof(t_list));
	if (l_new == 0)
		return (NULL);
	l_new->content = content;
	l_new->next = NULL;
	return (l_new);
}
/*
#include <stdio.h>

int	main(void)
{
	char    str[] = "HoLa estudiante de 42";
	t_list	*newlst;

	newlst = ft_lstnew(str);
	if (newlst)
	{
		printf("%s\n", (char *)newlst->content);
		printf("%p\n", newlst->next);
		free(newlst);
	}
    return (0);
}*/
