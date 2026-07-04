*This project has been created as part of the 42 curriculum by oshtohri*

#  ft_printf


## Description:
  The goal of this project is to recode the standard printf() function.
Through this assignment, variadic functions were implemented in C, and
a variable number of arguments were handled. Once completed, ft_printf()
will be integrated into the libft to be used in future 42 Network projects.
  The project could involve parsing format specifiers: cspdiuxX%
(like %s, %d, or %x).


## There are 2 sections:

Part 1 - ft_printf function

Part 2 - Additional functions

## Makefile:
  A Makefile is a file that uses the make utility. This utility determines
which parts of a program should be compiled and sends them commands to do so.
Essentially, a makefile is used to automatically compile a project instead of
doing it manually.
  Makefile contains at least the rules $(NAME), all, clean, fclean and re.

## Instructions:
make all - compiles object files (.o) and the libftprintf.a library;
make clean - deletes all object files (.o);
make fclean - deletes all object files (.o) and the libftprintf.a library;
make re - recompiles all object files (.o) and the libftprintf.a library;


## Resources:
man function name
https://stackoverflow.com

https://www.geeksforgeeks.org

YouTube
https://42-cursus.gitbook.io/guide/1-rank-01/ft_printf

https://csnotes.medium.com/ft-printf-tutorial-42project-f09b6dc1cd0e





## Part 1 - ft_printf function


### ft_printf.c
int printf(const char *format, ...);
| | |
| :--- | :--- |
| **Description** | Replicates the standard printf behavior. It parses the format string character by character: if it encounters a %, it treats the next character as a specifier; otherwise, it prints the character as a literal. Prints the format string, interpreting ‘%’ directives and ‘\’ escapes to format numeric and string arguments in a way that is mostly similar to the C ‘printf’ function, and C language escape sequence processing. This function has to handle the following conversions: cspdiuxX% |
| **Parameters** | format: the mandatory first argument. It is a format string that acts as a template for the output. The initial string containing text and/or format specifiers |
| |  ...:  (Ellipsis) this represents variadic arguments, meaning the function can take a variable number of additional parameters A variable number of arguments to be formatted and printed |
| **Return Value** | Upon successful return, these functions return the number of characters printed (excluding the null byte used to end output to strings) |
| **Logic** | The while loop scans the string. When format[i] == '%' is found, it increments i to pass the specifier character to print_format. It accumulates the return values from write and print_format into res to keep an accurate count of total characters printed. |


### print_format
static int	print_format(char specifier, va_list ap);
| | |
| :--- | :--- |
| **Description** | This function evaluates a single format specifier (the character following a %) and retrieves the next argument from the variadic list (ap) to print it in the correct format. |
| **Parameters** | specifier: the character identifying the data type (e.g., 'd', 's', 'x') ap: the va_list structure containing the variable arguments passed to the main printf function |
| **Return Value** | The total number of characters printed by whichever helper function was triggered. |
| **Logic** | 'c': fetches an int (promoted from char) and calls ft_putchar
|              | 's': fetches a char * and calls ft_putstr
|              | 'p': fetches an unsigned long and calls ft_print_ptr
|              | 'd' or 'i': fetches an int and calls ft_putnbr
|              | 'u': fetches an unsigned int and calls ft_putunsigned
|              | 'x' or 'X': Fetches an unsigned int and calls ft_puthex, passing the specifier to determine the case (upper or lower). |
|              | '%': Simply prints a literal percent sign
|              | Default: If the specifier isn't recognized, it prints the character itself as a fallback |


###

# Part 2 - Additional functions

### ft_putchar.c
int	ft_putchar(int c);
| | |
| :--- | :--- |
| **Description** | Writes a single character to the standard output (file descriptor 1). |
| **Parameters**   | c: the integer representation of the character to be printed |
| **Return Value** |   The number of bytes successfully written (usually 1), or -1 if an error occurs. |

### ft_putstr.c
int	ft_putstr(char *s);
| | |
| :--- | :--- |
| **Description** | Prints a null-terminated string to the standard output. If the string pointer is NULL, it prints "(null)". |
| **Parameters** | s: a pointer to the string of characters |
| **Return Value** | The total number of characters printed from the string. |

### ft_putnbr.c
int	ft_putnbr(int num);
| | |
| :--- | :--- |
| **Description** | Recursively prints a signed integer in decimal format. It includes special handling for the minimum possible integer (-2147483648) to avoid overflow when converting to a positive number. |
| **Parameters**   | num: the signed integer to print |
| **Return Value** | The total count of digits and signs (-) printed. |
 
### ft_putunsigned.c
int	ft_putunsigned(unsigned int u);
| | |
| :--- | :--- |
| **Description** | Recursively prints an unsigned integer in decimal format. |
| **Parameters**   | u: the unsigned integer to print |
| **Return Value** | The total count of digits printed. |

### ft_putptr.c
int	ft_putptr(unsigned long long ptr);
| | |
| :--- | :--- |
| **Description** | A recursive helper function that converts a memory address into a lowercase hexadecimal string. |
| **Parameters** | ptr: the raw memory address as an unsigned long long |
| **Return Value** | The number of hexadecimal characters printed. |

### ft_print_ptr.c
int	ft_print_ptr(void *ptr);
| | |
| :--- | :--- |
| **Description** | Formats and prints a pointer. It adds the "0x" prefix and calls ft_putptr for the hexadecimal conversion. If the pointer is NULL (0), it prints "(nil)". |
| **Parameters**   | ptr: the memory address to print |
| **Return Value** | Total characters printed (including the 0x prefix). |

### ft_puthex.c
int	ft_puthex(unsigned int hex, char specifier);
| | |
| :--- | :--- |
| **Description** | Converts and prints an unsigned integer into hexadecimal. |
| **Parameters** | hex: the number to convert |
| | specifier: either 'x' for lowercase or any other character (usually 'X') for uppercase |
| **Return Value** | The number of hexadecimal digits printed. |
