/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memcmp.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/18 13:16:00 by oshtohri          #+#    #+#             */
/*   Updated: 2026/01/21 17:24:11 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

int	ft_memcmp(const void *s1, const void *s2, size_t n)
{
	const unsigned char	*ch_s1;
	const unsigned char	*ch_s2;
	size_t				i;

	ch_s1 = s1;
	ch_s2 = s2;
	i = 0;
	while (i < n)
	{
		if (ch_s1[i] != ch_s2[i])
		{
			return (ch_s1[i] - ch_s2[i]);
		}
		i++;
	}
	return (0);
}
/*
#include <string.h>
#include <stdio.h>

int main(void)
{
    int arr1[] = {2, 2, 3, 4};
    int arr2[] = {1, 2, 3};
    int res;

    res = ft_memcmp(arr1+1, arr2+1, 2 * sizeof(int));
    if (res > 0)
        printf("Greater: %d\n", res);
    else if (res < 0)
        printf("Less: %d\n", res);
    else
        printf("Same! %d\n", res);

    const char  *s1 = "Hello";
    const char  *s2 = "Hey";
    const char  *s3 = "Help";

    int a = ft_memcmp(s1, s2, 3);
    int b = ft_memcmp(s1, s3, 3);
    int c = ft_memcmp(s2, s3, 3);
    printf("a: %s = %s? %d\n", s1, s2, a);
    printf("b: %s = %s? %d\n", s1, s3, b);
    printf("c: %s = %s? %d\n", s2, s3, c);

    return 0;
}*/
