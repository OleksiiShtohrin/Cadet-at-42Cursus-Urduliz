/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_memcpy.c                                        :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/17 11:31:41 by oshtohri          #+#    #+#             */
/*   Updated: 2026/01/21 17:24:18 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

void	*ft_memcpy(void *dest, const void *src, size_t n)
{
	size_t	i;
	char	*ch_dest;
	char	*ch_src;

	if (dest == 0 && src == 0)
		return (NULL);
	ch_dest = (char *) dest;
	ch_src = (char *) src;
	i = 0;
	while (i < n)
	{
		ch_dest[i] = ch_src[i];
		i++;
	}
	return (dest);
}
/*
#include <string.h>
#include <stdio.h>

typedef struct
{
	char	name[256];
	int	age;
	double	average;
} Student;

int	main(void)
{
	char	csrc[100] = "Geeksfor"; 
	memcpy(csrc+5, csrc, strlen(csrc)+1); 
	printf("%s\n", csrc);

	char	src[] = "Hello world!";
	char	dest[20];

	char	*dest_ptr = ft_memcpy(dest, src, strlen(src) + 1);
	printf("src: %s\n", src);
	printf("dest: %s\n", dest);

	printf("dest_ptr: %p\n", dest_ptr);
	printf("    dest: %p\n\n", dest);

	double	src_arr[5] = {1.1, 2.2, 3.3, 4.4, 5.5};
	double	dest_arr[5];

	ft_memcpy(dest_arr, src_arr, sizeof(src_arr));
		for (int i = 0; i < 5; i++)
			printf("dest_arr[%d] = %f\n", i, dest_arr[i]);
	printf("\n");

	Student student1;
	strcpy(student1.name, "Alex");
	student1.age = 38;
	student1.average = 77.6;

	Student	student2;

	ft_memcpy(&student2, &student1, sizeof(Student));
	printf("Name: %s\n", student2.name);
	printf("Age: %d\n", student2.age);
	printf("Average, kg: %f\n", student2.average);
	return 0;
}*/
