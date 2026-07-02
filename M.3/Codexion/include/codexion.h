/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   codexion.h                                         :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: oshtohri <oshtohri@student.42urduliz.com>  +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2026/06/16 11:35:51 by oshtohri          #+#    #+#             */
/*   Updated: 2026/06/26 09:31:13 by oshtohri         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#ifndef CODEXION_H
# define CODEXION_H

# include <pthread.h>
# include <stdio.h>
# include <stdlib.h>
# include <stdbool.h>
# include <string.h>
# include <sys/time.h>
# include <unistd.h>
# include <limits.h>

typedef struct s_simulation	t_simulation;
typedef struct s_coder		t_coder;
typedef struct s_dongle		t_dongle;
typedef struct s_heap_node	t_heap_node;
typedef struct s_heap		t_heap;
typedef struct s_scheduler	t_scheduler;

typedef enum e_parse_error
{
	PARSE_OK,
	PARSE_NULL_CONFIG,
	PARSE_INVALID_ARG_COUNT,
	PARSE_INVALID_CODER_COUNT,
	PARSE_INVALID_BURNOUT_TIME,
	PARSE_INVALID_COMPILE_TIME,
	PARSE_INVALID_DEBUG_TIME,
	PARSE_INVALID_REFACTOR_TIME,
	PARSE_INVALID_NUMBER_OF_COMPILES,
	PARSE_INVALID_COOLDOWN_TIME,
	PARSE_INVALID_POLICY
}	t_parse_error;

typedef enum e_coder_state
{
	CODER_WAITING,
	CODER_APPROVED,
	CODER_COMPILING,
	CODER_DEBUGGING,
	CODER_REFACTORING,
	CODER_FINISHED,
	CODER_BURNED_OUT
}	t_coder_state;

typedef enum e_dongle_state
{
	DONGLE_AVAILABLE,
	DONGLE_BUSY,
	DONGLE_COOLDOWN
}	t_dongle_state;

typedef enum e_schedule_policy
{
	POLICY_FIFO,
	POLICY_EDF
}	t_schedule_policy;

typedef struct s_config
{
	int					coder_count;
	int					number_of_compiles;
	long				burnout_time;
	long				compile_time;
	long				debug_time;
	long				refactor_time;
	long				cooldown_time;
	t_schedule_policy	policy;
}	t_config;

typedef struct s_coder
{
	int				id;
	t_simulation	*simulation;
	t_dongle		*left_dongle;
	t_dongle		*right_dongle;
	t_coder_state	status;
	int				compile_count;
	long			last_compile_start;
	pthread_t		thread;
	pthread_mutex_t	mutex;
	pthread_cond_t	cond;
}	t_coder;

typedef struct s_dongle
{
	int				id;
	t_coder			*owner;
	t_dongle_state	status;
	long			cooldown_end;
	pthread_mutex_t	mutex;
}	t_dongle;

typedef struct s_heap_node
{
	t_coder	*coder;
	long	priority;
	long	arrival;
}	t_heap_node;

typedef struct s_heap
{
	t_heap_node	*nodes;
	int			capacity;
	int			size;
	long		arrival_counter;
}	t_heap;

typedef struct s_scheduler
{
	t_heap				heap;
	t_schedule_policy	policy;
	pthread_mutex_t		mutex;
	pthread_t			thread;
	pthread_cond_t		cond;
}	t_scheduler;

typedef struct s_simulation
{
	t_config		config;
	t_coder			*coders;
	t_dongle		*dongles;
	t_scheduler		scheduler;
	pthread_t		monitor_thread;
	bool			stop;
	pthread_mutex_t	stop_mutex;
	long			start_time;
	pthread_mutex_t	log_mutex;
}	t_simulation;

/* parser */
t_parse_error	parse_args(int argc, char **argv, t_config *config);
void			print_parse_error(t_parse_error error);
t_parse_error	parse_policy(const char *str, t_schedule_policy *policy);
t_parse_error	parse_long_arg(
					const char *str, long *dst, t_parse_error error);
t_parse_error	parse_int_arg(
					const char *str, int *dst, t_parse_error error);
bool			parse_positive_long(const char *str, long *result);

/* init */
int				init_simulation(t_simulation *sim, t_config *config);
int				init_modules(t_simulation *sim);
int				init_scheduler(t_simulation *sim);
int				start_scheduler(t_simulation *sim);
void			join_scheduler(t_simulation *sim);
void			destroy_simulation(t_simulation *sim);
void			destroy_dongles(t_simulation *sim);
void			destroy_coders(t_simulation *sim);
void			destroy_scheduler(t_simulation *sim);

/* heap */
void			heap_swap(t_heap_node *a, t_heap_node *b);
int				heap_compare(
					t_heap_node a, t_heap_node b, t_schedule_policy policy);
int				heap_push(
					t_heap *heap, t_coder *coder,
					long priority, t_schedule_policy policy);
t_coder			*heap_pop(t_heap *heap, t_schedule_policy policy);
void			heapify_up(t_heap *heap, int idx, t_schedule_policy policy);
void			heapify_down(t_heap *heap, int idx, t_schedule_policy policy);

/* scheduler */
void			*scheduler_routine(void *arg);
void			approve_coder(t_coder *coder);
t_coder			*wait_for_next_coder(
					t_scheduler *scheduler, t_simulation *sim);
void			process_next_coder(t_scheduler *scheduler, t_simulation *sim);

/* coder */
void			*coder_routine(void *arg);
int				start_coders(t_simulation *sim);
void			join_coders(t_simulation *sim);
void			wait_for_approval(t_coder *coder);
void			request_compilation(t_coder *coder);
void			start_compiling(t_coder *coder);
void			start_debugging(t_coder *coder);
void			start_refactoring(t_coder *coder);

/* dongle */
int				take_dongles(t_coder *coder);
void			release_dongles(t_coder *coder);
int				is_dongle_ready(t_dongle *dongle);
t_dongle		*get_first_dongle(t_coder *coder);
t_dongle		*get_second_dongle(t_coder *coder);
int				take_single_dongle(t_coder *coder, t_dongle *first);
int				wait_for_first(t_coder *coder, t_dongle *first);
int				wait_for_second(
					t_coder *coder, t_dongle *first, t_dongle *second);

/* monitor */
void			*monitor_routine(void *arg);
int				start_monitor(t_simulation *sim);
int				join_monitor(t_simulation *sim);
int				check_burnout(t_simulation *sim);
int				all_coders_finished(t_simulation *sim);

/* utils */
long			get_timestamp(void);
long			get_elapsed_time(t_simulation *sim);
void			log_action(t_coder *coder, const char *msg);
void			log_burnout(t_coder *coder);
void			log_dongle(t_coder *coder);

/* simulation */
void			set_initial_compile_time(t_simulation *sim);
void			set_stop(t_simulation *sim, bool value);
bool			get_stop(t_simulation *sim);

#endif
