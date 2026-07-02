# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/01/31 13:27:04 by oshtohri          #+#    #+#              #
#    Updated: 2026/02/03 13:00:01 by oshtohri         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

NAME = libftprintf.a

CC = cc
FLAGS = -Wall -Wextra -Werror

MY_PRINTF = ft_printf.c \
			ft_putchar.c \
			ft_putstr.c \
			ft_print_ptr.c \
			ft_putnbr.c \
			ft_puthex.c \
			ft_putunsigned.c

OBJS = $(MY_PRINTF:.c=.o)

all: $(NAME)

$(NAME) : $(OBJS)
	@ar rcs $(NAME) $(OBJS)

%.o: %.c ft_printf.h
	@$(CC) $(FLAGS) -c $< -o $@

clean:
	@rm -f $(OBJS)

fclean: clean
	@rm -f $(NAME)

re: fclean all

.PHONY: all clean fclean re
