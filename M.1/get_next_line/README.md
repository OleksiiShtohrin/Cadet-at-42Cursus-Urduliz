*This project has been created as part of the 42 curriculum by oshtohri*
                                    
                                    
                                 Get Next Line


##Description:
  get_next_line (GNL) is a core programming project focused on implementing
a robust function that reads and returns a single complete line from
a specified file descriptor, managing the complexities of buffering, partial
reads, and multiple file accesses simultaneously. 

1. mandatory part:
Repeated calls (e.g., using a loop) to get_next_line() function should let
you read the text file pointed to by the file descriptor, one line at a time.
Function should return the line that was read.
If there is nothing left to read or if an error occurs, it should return NULL.

2. bonus:
get_next_line() can manage multiple file descriptors at the same time.
For example, if you are reading from file descriptors 3, 4, and 5, you should be able
to read from a different file descriptor with each call, without losing track of the
reading state of each file descriptor or returning a line from a different one.

##There are 2 sections:
Part 1 - Get Next Line functions
Part 2 - Libft functions (*_utils.c)
Part 3 - Get Next Line bonus functions


##Instructions:
cc -Wall -Wextra -Werror -D BUFFER_SIZE=42 get_next_line.c get_next_line_utils.c main.c for exequtable file;
cc -Wall -Wextra -Werror -D BUFFER_SIZE=42 get_next_line_bonus.c get_next_line_utils_bonus.c main.c for exequtable file;

valgrind --leak-check=full --show-leak-kinds=all --track-origins=yes ./a.out(or your name)

##Resources:
man function name
https://stackoverflow.com , https://www.geeksforgeeks.org
YouTube
https://42-cursus.gitbook.io/guide/1-rank-01/get_next_line



                      ---------------------------------------
                     |    Part 1 - Get Next Line functions   |
                      ---------------------------------------

get_next_line
###################################
char	*get_next_line(int fd);

 -------------- ------------------------------------------------------------- 
| Description  |   The get_next_line function is designed to read and return
|              | a single line from a given file descriptor. A "line" is defined
|              | as a sequence of characters ending with a newline character
|              | (\n) or the End Of File (EOF).
 -------------- -------------------------------------------------------------
| Parameters   | fd: The File Descriptor to read from. This can be a file
|              |     opened via open(), or a standard stream like 0 for stdin
 -------------- -------------------------------------------------------------
| Return Value |   char * A pointer to the string containing the line read,
|              | including the \n (if found). 
|              |   NULL Returned if there is nothing else to read, or if an
|              | error occurred (e.g., invalid fd, memory allocation failure,
|              | or read() error). 
 -------------- -------------------------------------------------------------


add_to_temp
######################################################
static char	*add_to_temp(int fd, char *st_temp);

 -------------- ------------------------------------------------------------- 
| Description  |   The add_to_temp function reads data from a file descriptor
|              | and appends it to the existing static storage until a newline
|              | character (\n) is encountered or the end of the file (EOF)
|              | is reached.
 -------------- -------------------------------------------------------------
| Parameters   |      fd: The file descriptor to read from
|              | st_temp: The current accumulated string (the "stash") from
|              |          previous reads
 -------------- -------------------------------------------------------------
| Return Value | char *	The updated string containing the previous content
|              | plus the newly read data.
|              | NULL Returned if a read() error occurs or if memory allocation fails.
 -------------- -------------------------------------------------------------


get_line
#########################################
static char	*get_line(char *st_temp);

 -------------- ------------------------------------------------------------- 
| Description  |   The get_line function extracts the current line from the
|              | accumulated static storage. It scans the "stash" and copies
|              | everything from the beginning up to and including the first
|              | newline character found.
 -------------- -------------------------------------------------------------
| Parameters   | st_temp: The accumulated string (the "stash") containing
|              | 	  the data read from the file descriptor
|              | 
 -------------- -------------------------------------------------------------
| Return Value | char *	A newly allocated string containing the line
|              | (ending with \n if present).
|              | NULL Returned if the input string is empty or null.
 -------------- -------------------------------------------------------------


clean_temp
############################################
static char	*clean_temp(char *st_temp);

 -------------- ------------------------------------------------------------- 
| Description  |   The clean_temp function trims the static storage string.
|              | It removes the line that has already been returned by get_next_line
|              | and preserves any leftover characters that were read after
|              | the newline character.
 -------------- -------------------------------------------------------------
| Parameters   | st_temp: The accumulated string (the "stash") containing both
|              | 	  the line just processed and the potential "leftover"
|              | 	  data
 -------------- -------------------------------------------------------------
| Return Value | char *	A new string containing only the characters following
|              | the first \n found.
|              | NULL Returned if there is no leftover data after the newline,
|              | if the string is empty, or if allocation fails. 
 -------------- -------------------------------------------------------------





                  ------------------------------------------
                 |    Part 2 - Libft functions (*_utils.c)   |
                  ------------------------------------------


ft_strlen
######################################
size_t	ft_strlen(const char *str);

 -------------- ------------------------------------------------------------- 
| Description  |   The ft_strlen() function calculates the length of the string
|              | pointed to by s, excluding the terminating null byte ('\0').
|              | 
 -------------- -------------------------------------------------------------
| Parameters   | str: it is the string whose length we are going to find.
|              | 
 -------------- -------------------------------------------------------------
| Return Value |   The ft_strlen() function returns the number of bytes in the
|              | string  pointed to by s.
 -------------- -------------------------------------------------------------


ft_strchr
#############################################
char	*ft_strchr(const char *s, int c);

 -------------- ------------------------------------------------------------- 
| Description  |   The  ft_strchr() function returns a pointer to the first
|              | occurrence of the character c in the string s.
|              | 
 -------------- -------------------------------------------------------------
| Parameters   | s: pointer to string.
|              | c: character to search for.
 -------------- -------------------------------------------------------------
| Return Value |   The functions return a pointer to the matched character
|              | or NULL if the character is not found.
|              |   The terminating null byte is considered part of the string,
|              | so that if c is specified as '\0', these functions return
|              | a pointer to the terminator.
 -------------- -------------------------------------------------------------


ft_strdup
#####################################
char	*ft_strdup(const char *s);

 -------------- ------------------------------------------------------------- 
| Description  |   The function returns a pointer to a new string which
|              | is a duplicate of the string s. Memory for the new string
|              | is obtained with malloc(3), and can be freed with free(3).
 -------------- -------------------------------------------------------------
| Parameters   | s: the pointer to the source string that you wish to duplicate.
|              | 
 -------------- -------------------------------------------------------------
| Return Value |   On success, the function returns a pointer to the
|              | duplicated string. It returns NULL if insufficient memory was
|              | available, with errno set to indicate the cause of the error.
 -------------- -------------------------------------------------------------


ft_substr
#############################################################
char *ft_substr(char *s, unsigned int start, size_t len);

 -------------- ------------------------------------------------------------- 
| Description  |   Allocates memory (using malloc(3)) and returns a substring 
|              | from the string ’s’. The substring starts at index ’start’ 
|              | and has a maximum length of ’len’.
 -------------- -------------------------------------------------------------
| Parameters   | s: The original string from which to create the substring.
|              | start: The starting index of the substring within ’s’.
|              | len: The maximum length of the substring.
 -------------- -------------------------------------------------------------
| Return Value | The substring.
|              | NULL if the allocation fails.
 -------------- -------------------------------------------------------------


ft_strjoin
##########################################
char *ft_strjoin(char *s1, char *s2);

 -------------- ------------------------------------------------------------- 
| Description  |   Allocates memory (using malloc(3)) and returns a new
|              | string, which is the result of concatenating ’s1’ and ’s2’.
 -------------- -------------------------------------------------------------
| Parameters   | s1: The prefix string.
|              | s2: The suffix string.
 -------------- -------------------------------------------------------------
| Return Value | The new string.
|              | NULL if the allocation fails.
 -------------- -------------------------------------------------------------



                      ------------------------------------
                     |    Part 3 - Get Next Line bonus    |
                      ------------------------------------

I don't change anything in other functions.

get_next_line_bonus
###################################
char	*get_next_line(int fd);

Static Array of Strings:
static char *st_temp[1024];
 -------------- ------------------------------------------------------------- 
| Description  |   The primary difference in the bonus version is the replacement
|              | of a single pointer with an array of pointers. This allows the
|              | function to store a unique "stash" for every possible file descriptor.
|              |   The get_next_line function is designed to read and return
|              | a single line from a given file descriptor. A "line" is defined
|              | as a sequence of characters ending with a newline character
|              | (\n) or the End Of File (EOF).
 -------------- -------------------------------------------------------------
| Parameters   | fd: The specific File Descriptor to read from.
|              | 
 -------------- -------------------------------------------------------------
| Return Value |   char * The line read from the specific fd provided.
|              |   NULL Returned if the fd is out of range, a read error
|              | occurs, or the end of the file is reached.
 -------------- -------------------------------------------------------------


add_to_temp
######################################################
static char	*add_to_temp(int fd, char *st_temp);

Add in while: if (ft_strchr(buffer, '\n')) break ;
 -------------- ------------------------------------------------------------- 
| Description  |   The add_to_temp function reads data from a file descriptor
|              | and appends it to the existing static storage until a newline
|              | character (\n) is encountered or the end of the file (EOF)
|              | is reached.
 -------------- -------------------------------------------------------------
| Parameters   |      fd: The file descriptor to read from
|              | st_temp: The current accumulated string (the "stash") from
|              |          previous reads
 -------------- -------------------------------------------------------------
| Return Value | char *	The updated string containing the previous content
|              | plus the newly read data.
|              | NULL Returned if a read() error occurs or if memory allocation fails.
 -------------- -------------------------------------------------------------

