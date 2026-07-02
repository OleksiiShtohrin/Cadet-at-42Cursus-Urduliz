# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    Makefile                                           :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2026/02/23 14:50:16 by oshtohri          #+#    #+#              #
#    Updated: 2026/02/24 14:16:16 by oshtohri         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

NAME		= push_swap

CC			= cc
CFLAGS		= -Wall -Wextra -Werror

SRCS		= main.c \
			  ps_error.c \
			  ps_string.c \
			  ps_split.c \
			  ps_atoi_safe.c \
			  stack_init.c \
			  stack_node.c \
			  stack_clear.c \
			  parse_args.c \
			  parse_args_loop.c \
			  disorder.c \
			  op_swap.c \
			  op_push.c \
			  op_rotate.c \
			  op_rev_rotate.c \
			  alg_simple.c \
			  alg_medium.c \
			  alg_medium_find.c \
			  alg_medium_assign.c \
			  alg_medium_rotate.c \
			  alg_complex.c \
			  alg_complex_utils.c \
			  alg_adaptive.c \
			  alg_small.c \
			  alg_small_utils.c \
			  bench.c \
			  bench_utils.c \
			  bench_print.c \
			  ps_sort_three.c \
			  ps_itoa.c \
			  ps_strlcpy.c \
			  ps_strlen.c \
			  ps_strncmp.c

OBJS		= $(SRCS:.c=.o)

all: $(NAME)

$(NAME): $(OBJS)
	$(CC) $(CFLAGS) $(OBJS) -o $(NAME)

%.o: %.c
	$(CC) $(CFLAGS) -c $< -o $@

clean:
	rm -f $(OBJS)

fclean: clean
	rm -f $(NAME)

re: fclean all

.PHONY: all clean fclean re
