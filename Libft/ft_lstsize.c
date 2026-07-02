/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_lstsize.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/24 13:06:46 by oshtohri          #+#    #+#             */
/*   Updated: 2026/01/27 16:48:39 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

int	ft_lstsize(t_list *lst)
{
	int	count;

	count = 0;
	while (lst)
	{
		count++;
		lst = lst->next;
	}
	return (count);
}
/*
#include <stdio.h>

int	main(void)
{
	t_list node3 = {"3", NULL};
	t_list node2 = {"2", &node3};
	t_list node1 = {"1", &node2};

	printf("3: %d\n", ft_lstsize(&node1));
	printf("1: %d\n", ft_lstsize(&node3));
	printf("0: %d\n", ft_lstsize(NULL));

    return (0);
}*/
