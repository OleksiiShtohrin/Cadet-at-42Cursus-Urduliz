NAME = codexion

CC = cc
CFLAGS = -Wall -Wextra -Werror -pthread

INCLUDES = -Iinclude

SRC = src/main.c \
      src/parser/parse_args.c \
      src/parser/parse_utils.c \
      src/parser/print_parse_error.c \
      src/init/init_simulation.c \
      src/init/init_modules.c \
      src/init/destroy_simulation.c \
      src/init/init_scheduler.c \
      src/queue/heap_ops.c \
      src/queue/heapify.c \
      src/scheduler/scheduler_routine.c \
      src/coder/coder_routine.c \
      src/coder/coder_utils.c \
      src/coder/coder_actions.c \
      src/dongles/dongle_ops.c \
      src/dongles/dongle_utils.c \
      src/monitor/monitor_routine.c \
      src/monitor/monitor_checks.c \
      src/utils/get_timestamp.c \
      src/utils/log_action.c \
      src/simulation/simulation_utils.c

OBJ = $(SRC:.c=.o)

all: $(NAME)

$(NAME): $(OBJ)
	$(CC) $(CFLAGS) $(OBJ) -o $(NAME)

%.o: %.c
	$(CC) $(CFLAGS) $(INCLUDES) -c $< -o $@

clean:
	rm -f $(OBJ)

fclean: clean
	rm -f $(NAME)

re: fclean all

.PHONY: all clean fclean re