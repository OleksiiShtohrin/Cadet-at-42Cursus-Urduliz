/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_split.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/01/22 17:12:27 by oshtohri          #+#    #+#             */
/*   Updated: 2026/01/26 16:28:58 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"

static int	ft_count(char const *s, char c);
static char	*ft_word(char const **s, char c);
static void	ft_free_split(char **res, int i);

char	**ft_split(char const *s, char c)
{
	char	**res;
	int		count;
	int		i;

	if (s == 0)
		return (NULL);
	count = ft_count(s, c);
	res = (char **) malloc(sizeof(char *) * (count + 1));
	if (res == 0)
		return (NULL);
	i = 0;
	while (i < count)
	{
		res[i] = ft_word(&s, c);
		if (res[i] == 0)
		{
			ft_free_split(res, i);
			return (NULL);
		}
		i++;
	}
	res[i] = NULL;
	return (res);
}

static int	ft_count(char const *s, char c)
{
	int	count;
	int	i;

	count = 0;
	i = 0;
	while (s[i])
	{
		while (s[i] == c)
			i++;
		if (s[i])
		{
			count++;
			while (s[i] && s[i] != c)
				i++;
		}
	}
	return (count);
}

static char	*ft_word(char const **s, char c)
{
	char	*word;
	int		len;
	int		i;

	while (**s && **s == c)
		(*s)++;
	len = 0;
	while ((*s)[len] && (*s)[len] != c)
		len++;
	word = (char *) malloc(sizeof(char) * (len + 1));
	if (word == 0)
		return (NULL);
	i = 0;
	while (i < len)
	{
		word[i] = (*s)[i];
		i++;
	}
	word[i] = '\0';
	*s += len;
	return (word);
}

static void	ft_free_split(char **res, int i)
{
	while (i > 0)
	{
		i--;
		free(res[i]);
	}
	free(res);
}
/*
#include <stdio.h>
void print_split(char **res)
{
    int i = 0;

    if (!res)
    {
        printf("NULL\n");
        return;
    }
    if (!res[0])
    {
        printf("Empty Array (NULL)\n");
    }
    while (res[i])
    {
        printf("[%d]: %s\n", i, res[i]);
        free(res[i]);
        i++;
    }
    printf("\n");
    free(res);
}
	
int	main(void)
{
    int     i;
    char    **str;
    char    **str1;
    char    **str2;
    char    **res;
    
    str = ft_split("     ", ' ');
    if (str)
    {
        if (str[0] == NULL)
        {
            printf("NULL\n");
        }
        else
        {
            for (i = 0; str[i]; i++)
            {
                printf("str: %s\n", str[i]);
                free(str[i]);
            }
        }
        free(str);
    }
    printf("\n");

    str1 = ft_split("Hola estudiante de 42 cursus en 2026!", ' ');
    i = 0;
    while (str1 && str1[i])
    {
        printf("str1: %s\n", str1[i]);
        free(str1[i]);
        i++;
    }
    free(str1);
    printf("\n");

    str2 = ft_split("  Hola  estudiante  42 cursus   2026  ", ' ');
    if (str2)
    {
        for (i = 0; str2[i]; i++)
            printf("str2: %s\n", str2[i]);
        ft_free_split(str2, i);
    }
    printf("\n");
    
    res = ft_split("Hola estudiante de 42 cursus en 2026!", 's');
    print_split(res);

    res = ft_split("Hola estudiante", 'y');
    print_split(res);
    
    res = ft_split("", 'a');
    print_split(res);
    // for (i = 0; res && res[i]; i++) free(res[i]); free(res);
    
    return (0);
}*/