/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_calloc.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/18 14:44:12 by oshtohri          #+#    #+#             */
/*   Updated: 2026/01/21 17:23:53 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	*ft_calloc(size_t nmemb, size_t size)
{
	size_t			i;
	unsigned char	*ptr;

	if (nmemb != 0 && size > ((size_t)-1) / nmemb)
		return (NULL);
	ptr = (unsigned char *) malloc(nmemb * size);
	if (ptr == 0)
		return (NULL);
	i = 0;
	while (i < nmemb * size)
	{
		ptr[i] = 0;
		i++;
	}
	return ((void *) ptr);
}
/*
#include <stdio.h>
#include <string.h>

int main(void)
{
    int i, *ptr, sum = 0;
    ptr = (int*)ft_calloc(10, sizeof(int));
    
    if (ptr == NULL)
    {
        printf("Error");
        exit(0);
    }
    printf("\n");

    for (i = 0; i < 10; ++i)
    {
        *(ptr + i) = i;
        sum += *(ptr + i);
    }
    printf("Sum = %d\n", sum);
    free(ptr);

    char* numb = (char*)ft_calloc(8, sizeof(char));
    size_t j = 0;
    while (j < 8)
    {
        printf("%d,", numb[j]);
        ++j;
    }
    printf("\n");

    memset(numb, 65, 8);

    j = 0;
    while (j < 8)
    {
        printf("%d,", numb[j]);
        ++j;
    }
    printf("\n");
    free(numb);
    return (0);
}*/
