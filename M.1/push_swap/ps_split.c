/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ps_split.c                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: dzhambal <dzhambal@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/23 09:35:26 by dzhambal          #+#    #+#             */
/*   Updated: 2026/02/23 09:35:30 by dzhambal         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "push_swap.h"

static size_t	count_words(const char *s)
{
	size_t	i;
	size_t	count;

	i = 0;
	count = 0;
	while (s[i])
	{
		while (s[i] && ps_isspace(s[i]))
			i++;
		if (s[i])
			count++;
		while (s[i] && !ps_isspace(s[i]))
			i++;
	}
	return (count);
}

void	ps_split_free(char **parts)
{
	size_t	i;

	if (!parts)
		return ;
	i = 0;
	while (parts[i])
	{
		free(parts[i]);
		i++;
	}
	free(parts);
}

static int	add_word(char **parts, size_t *k, const char *start_ptr, size_t len)
{
	char	*word;
	size_t	j;

	word = (char *)malloc(len + 1);
	if (!word)
		return (0);
	j = 0;
	while (j < len)
	{
		word[j] = start_ptr[j];
		j++;
	}
	word[j] = '\0';
	parts[*k] = word;
	(*k)++;
	return (1);
}

char	**ps_split_spaces(const char *s)
{
	char	**parts;
	size_t	i;
	size_t	k;
	size_t	start;

	if (!s)
		return (NULL);
	parts = (char **)malloc(sizeof(char *) * (count_words(s) + 1));
	if (!parts)
		return (NULL);
	i = 0;
	k = 0;
	while (s[i])
	{
		while (s[i] && ps_isspace(s[i]))
			i++;
		start = i;
		while (s[i] && !ps_isspace(s[i]))
			i++;
		if (start < i && !add_word(parts, &k, s + start, i - start))
			return (ps_split_free(parts), NULL);
	}
	parts[k] = NULL;
	return (parts);
}
