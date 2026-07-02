/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   get_next_line.c                                    :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/02/12 11:04:12 by oshtohri          #+#    #+#             */
/*   Updated: 2026/03/04 12:55:29 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "get_next_line.h"

static char	*get_line(char *st_temp)
{
	size_t	i;

	if (!st_temp || !st_temp[0])
		return (NULL);
	i = 0;
	while (st_temp[i] && st_temp[i] != '\n')
		i++;
	if (st_temp[i] == '\n')
		i++;
	return (ft_substr(st_temp, 0, i));
}

static char	*clean_temp(char *st_temp)
{
	size_t	i;
	char	*new_temp;

	if (!st_temp)
		return (NULL);
	i = 0;
	while (st_temp[i] && st_temp[i] != '\n')
		i++;
	if (!st_temp[i])
	{
		free(st_temp);
		return (NULL);
	}
	if (st_temp[i + 1] == '\0')
	{
		free(st_temp);
		return (NULL);
	}
	new_temp = ft_strdup(st_temp + i + 1);
	free(st_temp);
	return (new_temp);
}

static char	*add_to_temp(int fd, char *st_temp)
{
	char	*buffer;
	char	*tmp;
	int		num;

	buffer = malloc(BUFFER_SIZE + 1);
	if (!buffer)
		return (free(st_temp), NULL);
	num = 1;
	while (num > 0)
	{
		num = read(fd, buffer, BUFFER_SIZE);
		if (num == -1)
			return (free(buffer), free(st_temp), NULL);
		if (num == 0)
			break ;
		buffer[num] = '\0';
		tmp = ft_strjoin(st_temp, buffer);
		if (!tmp)
			return (free(buffer), NULL);
		st_temp = tmp;
		if (ft_strchr(buffer, '\n'))
			break ;
	}
	free(buffer);
	return (st_temp);
}

char	*get_next_line(int fd)
{
	static char	*st_temp;
	char		*line;

	if (fd < 0 || BUFFER_SIZE <= 0)
		return (NULL);
	st_temp = add_to_temp(fd, st_temp);
	if (!st_temp)
		return (NULL);
	line = get_line(st_temp);
	st_temp = clean_temp(st_temp);
	return (line);
}
