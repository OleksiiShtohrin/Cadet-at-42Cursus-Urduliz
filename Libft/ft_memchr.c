/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memchr.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/18 10:29:36 by oshtohri          #+#    #+#             */
/*   Updated: 2026/01/21 17:24:06 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	*ft_memchr(const void *s, int c, size_t n)
{
	const unsigned char	*ptr;
	unsigned char		x;
	size_t				i;

	ptr = (const unsigned char *)s;
	x = (unsigned char)c;
	i = 0;
	while (i < n)
	{
		if (ptr[i] == x)
			return ((void *)(ptr + i));
		i++;
	}
	return (NULL);
}
/*
#include <string.h>
#include <stdio.h>

int main(void)
{
    char    data[] = {'a', 'b', 'c', 'd', 'e', 'f', 'g'};

    char    *pos = ft_memchr(data, 'd', 5);

    if (pos == NULL)
        printf("Not found!\n");
    else
    {
        printf("pos[0] = %c\n", pos[0]);
        printf("pos[1] = %c\n", pos[1]);
    }

    int arr1[] = {3, 4};

    if (ft_memchr(arr1, 0, sizeof(int) * 2) != NULL)
        printf("Found!\n");
    else
        printf("Not found!\n");

    char    str[] = "student.osh@42urduliz.com";
    char    *domain = ft_memchr(str, '@', strlen(str));
    domain++;
    printf("Domain: %s\n", domain);

    const int   arr[5] = {0x1021, 0x8988, 0x706, 0x50, 0x22};
    int *ptr;

    ptr = ft_memchr(arr, 0x00, sizeof(arr));
    printf("arr: %p ptr %p\n", arr, ptr);
    return (0);
}*/
