*This project has been created as part of the 42 curriculum by oshtohri and dzhambal*

                                “Push_swap”
								 
## Contributors
- *oshtohri*: Parsing Logic & Dispatcher: Developed the robust multi-stage 
argument parser (parse_args, ps_parse_args_loop) capable of handling both 
individual arguments and quoted strings.
System Management: Implemented the main control flow, the algorithm dispatcher 
(run_with_strategy), and the "Early Exit" optimization for pre-sorted inputs.
Benchmarking Suite: Designed the entire t_bench framework, including real-time 
operation tracking (bench_inc), disorder measurement integration, and the 
adaptive formatting of technical reports.
String Utilities: Implemented essential library-level functions (ps_itoa, 
ps_strlcpy, ps_strncmp) and custom safe-I/O utilities for terminal reporting.

- *dzhambal*: Sorting Algorithms: Implemented the full suite of required 
strategies: Simple (O(n^2)), Medium (O(n*sqrt(n))), Complex (O(n log n)), and 
the Adaptive selector.
Stack Infrastructure: Developed the Circular Doubly-Linked List core, including 
node management and stack lifecycle (init, push, clear).
Operation Set: Implemented the 11 Push_swap atomic operations with integrated 
benchmarking hooks.
Algorithmic Utilities: Developed advanced helpers for the Medium/Complex 
strategies, including coordinate compression (indexing), bit-pass logic, 
and chunk calculation.

Both authors contributed equally to the optimization, debugging, and 
documentation of the project.
                                    
                                    
                               “Description”

**Push_swap** is a high-performance integer sorting project using two stacks
and a restricted set of operations (`sa`, `pb`, `ra`, etc.). This project 
analyzes input data (Disorder Coefficient) in real-time to choose the most 
efficient sorting algorithm.

The primary goal is to minimize the number of operations while strictly 
adhering to complexity limits:

- **100 numbers:**  < 2000 operations (Pass)
                    < 1500 operations (Good)
                    < 700 operations (Excellent)
- **500 numbers:**  < 12000 operations (Pass)
                    < 8000 operations (Good)
                    < 5500 operations (Excellent)


                            “Instructions”

# Compilation:
  A Makefile is a file that uses the make utility. This utility determines
which parts of a program should be compiled and sends them commands to do so.
Essentially, a makefile is used to automatically compile a project instead of
doing it manually.
  Makefile contains at least the rules $(NAME), all, clean, fclean and re.

make or make all - compiles the source files and generates the push_swap 
executable;
make clean - deletes all object files (.o);
make fclean - deletes all object files (.o) and the push_swap;
make re - recompiles all files of the project;

The program accepts a list of integers and supports flags for manual strategy 
selection:
# Default (Adaptive mode)
./push_swap 2 1 3 6 5 8
ARG="4 67 3 87 23"; ./push_swap --adaptive $ARG | wc -l

# Forced strategies
./push_swap --simple 5 4 3 2 1
ARG="4 67 3 87 23"; ./push_swap --complex $ARG

# Force the complex (O(n log n)) strategy and verify with the checker:
ARG="4 67 3 87 23"; ./push_swap --complex $ARG | ./checker_linux $ARG

# push_swap with a large input:
shuf -i 0-9999 -n 500 > args.txt ; ./push_swap $(cat args.txt) | wc -l

# Run with benchmark enabled; hide operations and show only metrics:
shuf -i 0-9999 -n 500 > args.txt ; ./push_swap --bench $(cat args.txt) 2>
bench.txt | ./checker_linux $(cat args.txt)

# Pipe operations to the checker while saving benchmark to a file:
ARG="4 67 3 87 23" ; ./push_swap --bench --adaptive $ARG 2> bench.txt |
./checker_linux $ARG

# Error management examples:
$> ./push_swap --adaptive 0 one 2 3
$> ./push_swap --simple 3 2 3


                       “Algorithm Selection & Justification”

1. ### Simple Strategy (O(n^2))
Method: Selection sort adaptation. Rationale: This method repeatedly identifies 
the minimum element in Stack A, rotates it to the top, and pushes it to Stack B. 
This approach is highly efficient for small datasets (n < 10) as it requires 
minimal logic and no complex indexing. For (n <= 5), the strategy is further 
optimized (O(1)) with hardcoded sequences to achieve the absolute minimum 
operation count.
##"Simple implements sequential minimum extraction: find the minimum element, rotate it upward, perform pb, repeat until the remaining 3 elements are sorted, and return via pa. In the push_swap model, this yields O(n^2) operations."

2. ### Medium Strategy (O(n*sqrt(n)))
Method: Optimized Chunk-based Sorting. Rationale: Dividing the stack into √n 
chunks (20 for n=100, 40 for n=500) provides the best balance between searching 
in Stack A and sorting in Stack B.

Proximity Search: Scans both top and bottom of Stack A to find the nearest chunk 
element.
B-Stack Hourglass: Elements smaller than the chunk median are sent to the bottom 
(rb), forming an "hourglass" structure to streamline the return process.
Smart Pull-back: An intelligent return mechanism that minimizes rotations when 
retrieving the next maximum.
##"Medium is a chunk algorithm: assign an index (rank), split the indices into chunks, and push suitable elements into b (using the rb heuristic for the chunk), then pull the maxima back. For a chunk size ≈ √n, this yields approximately O(n √n) operations."

3. ### Complex Strategy (O(n log n))
Method: Radix Sort (Bitwise Pass). Rationale: Chosen for its compact and elegant 
implementation within Norminette constraints (25 lines per function). It ensures 
a stable operation count on high-entropy (shuffled) data. To guarantee complexity, 
Coordinate Compression is used to normalize the input range to [0, N-1], 
fixing the bit-depth to exactly ⌈log₂N⌉.
##"Complex — radix (LSD) over indices: do bit passes (0..max_bits): for each bit, distribute (pb/ra), then return from b (pa). The number of passes is ≈ log n, each pass is O(n) ⇒ O(n log n)."

4. ### Adaptive Strategy (Custom Design)
Switches regimes based on the Disorder Coefficient (disorder) 
Low (disorder < 0.2): Simple Strategy. 
Medium (0.2 <= disorder < 0.5): Medium Strategy (Chunks). 
High (disorder <= 0.5): Complex Strategy (Radix).


                            “Technical Evolution”

1. Migration to Circular Doubly-Linked List
The initial linear stack was replaced by a Circular Doubly-Linked List. This 
change allowed rotate and reverse rotate operations to run in O(1), eliminated 
NULL-pointer edge cases (tail management), and made min/max searching 
significantly cleaner.
2. Removal of Global State
In compliance with Norm v4, the project was stripped of hidden global 
variables. The benchmark context (--bench) is now passed explicitly via the 
t_stack->bench structure. 
This ensures:
- Zero side-effects and safe memory deallocation.
- Compatibility with multi-run environments and modular unit tests.
3. Strengths & Trade-offs
- Strengths: Modular architecture, zero memory leaks (Valgrind-clean), and 
optimized circular stack rotations.
- Trade-offs: At certain n, Radix sort might be less efficient than Chunks 
("algorithmic regret").


                            “Resources:”
https://stackoverflow.com , 
https://www.geeksforgeeks.org
https://proproprogs.ru/structure_data
https://www.youtube.com/watch?v=98r9uhjPveE&t=5921s
https://42-cursus.gitbook.io/guide/2-rank-02/push_swap

AI was utilized in this project for the following tasks:
- **Architectural Refactoring:** Brainstorming the transition from global 
variables to a pointer-based context to satisfy Norm requirements.
- **Verifying Data Structures:** AI helped in analyzing why a Circular Stack is 
faster than a linear one for operations like ra and rra.
- **Technical Documentation:** Assisting in structuring and translating this 
README to meet 42’s strict formatting standards.


                      ----------------------------
                     |     Push_swap functions    |
                      ----------------------------
/* error / output */
int		ps_error(void);

/* small string utils */
int		ps_isdigit(int c);
int		ps_isspace(int c);
int		ps_strcmp(char *s1, char *s2);
int		ps_streq(const char *a, const char *b);

/* split and parsing numbers */
char	**ps_split_spaces(const char *s);
void	ps_split_free(char **parts);
int		ps_atoi_safe(const char *s, int *out);

/* stack basics */
void	stack_init(t_stack *s);
t_node	*node_new(int value);
int		stack_push_top(t_stack *s, t_node *n);
int		stack_push_bottom(t_stack *s, t_node *n);
void	stack_clear(t_stack *s);

/* parse argv -> stack a, strategy flags */
int		parse_args(int argc, char **argv, t_stack *a,
			t_strategy *strategy);
int		ps_parse_args_loop(int argc, char **argv, t_stack *a,
			t_strategy *strategy);
int		ps_add_arg_as_tokens(t_stack *a, const char *arg);

/* disorder */
double	compute_disorder(t_stack *a);

/* operations (print to stdout) */
void	op_sa(t_stack *a);
void	op_sb(t_stack *b);
void	op_ss(t_stack *a, t_stack *b);
void	op_pa(t_stack *a, t_stack *b);
void	op_pb(t_stack *a, t_stack *b);
void	op_ra(t_stack *a);
void	op_rb(t_stack *b);
void	op_rr(t_stack *a, t_stack *b);
void	op_rra(t_stack *a);
void	op_rrb(t_stack *b);
void	op_rrr(t_stack *a, t_stack *b);

/* algorithms */
void	run_simple(t_stack *a, t_stack *b);
void	run_medium(t_stack *a, t_stack *b);
void	run_complex(t_stack *a, t_stack *b);
void	run_adaptive(t_stack *a, t_stack *b);
void	ps_sort_three(t_stack *s);

/* adaptive and small*/
int		ps_choose_strategy(double disorder);
void	run_2(t_stack *a, t_stack *b);
void	run_3(t_stack *a, t_stack *b);
void	run_4(t_stack *a, t_stack *b);
void	run_5(t_stack *a, t_stack *b);
void	ps_rotate_min_to_top(t_stack *a);

/* utils for medium */
int		ps_assign_indices(t_stack *a);
int		ps_calc_chunk(int n);
int		ps_find_best_pos(t_stack *s, int target);
int		ps_find_max_pos(t_stack *s);
int		ps_find_pos_eq(t_stack *s, int target);
void	ps_rotate_to_top(t_stack *s, int pos, int is_a);

/* utils for complex */
int		ps_get_max_bits(int n);
void	ps_do_bit_pass(t_stack *a, t_stack *b, int bit);

/* Libc functions */
char	*ps_itoa(int n);
size_t	ps_strlcpy(char *dst, const char *src, size_t size);
size_t	ps_strlen(const char *s);
int		ps_strncmp(const char *s1, const char *s2, size_t n);


                      -----------------------
                     |    Bench functions    |
                      -----------------------


void		bench_init(t_bench *b);
void		bench_enable(t_bench *b);
void		bench_set_disorder(t_bench *b, double d);
void		bench_set_strategy(t_bench *b, const char *name,
				const char *complexity);
void		bench_inc(t_bench *b, const char *op);
void		bench_finish_print(t_bench *b);

const char	**bench_ops_names(void);

/* small I/O helpers used by bench printing */
void		write_str_fd(const char *s, int fd);
void		write_int_fd(long v, int fd);
