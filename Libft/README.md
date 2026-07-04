*This project has been created as part of the 42 curriculum by oshtohri*

# LIBFT
## Description:
This project involves coding a C library that will include numerous general purpose functions for your programs. In 42 that allows us to recreate some functions from the standard C library for future projects and gain a deeper 
understanding of data structures and basic algorithms.


### There are 3 sections:

* Part 1 - Libc functions
* Part 2 - Additional functions
* Part 3 - linked list


### Makefile:
  A Makefile is a file that uses the make utility. This utility determines which parts of a program should be compiled and sends them commands to do so. Essentially, a makefile is used to automatically compile a project instead of doing it manually.

  Makefile contains at least the rules $(NAME), all, clean, fclean and re.

Resources:
man function name
https://stackoverflow.com

https://www.geeksforgeeks.org

YouTube



### 
# Part 1 - Libc functions

### ft_isalpha
int	ft_isalpha(int c);
| | |
| :--- | :--- |
| **Description** | Checks for an alphabetic character; in the standard "C" locale, it is equivalent to (isupper(c) or islower(c)). In some locales, there may be additional characters for which ft_isalpha() is true—letters which are neither uppercase nor lowercase. |
| **Parameters**  | c: the character to look for |
| **Return Value** | 1 if the character matches the tested class |
|              | 0 if the character does not match|
 -------------- -------------------------------------------------------------


### ft_isdigit
int	ft_isdigit(int c);
| | |
| :--- | :--- |
| **Description** | Checks for a digit (0 through 9). |
| **Parameters**   | c: the character to look for |
| **Return Value** | 1 if the character matches the tested class |
|              | 0 if the character does not match |
 -------------- -------------------------------------------------------------


### ft_isalnum
int	ft_isalnum(int c);
| | |
| :--- | :--- |
| **Description** | Checks for an alphanumeric character; it is equivalent to (ft_isalpha(c) || ft_isdigit(c)). |
| **Parameters**   | c: the character to look for |
| **Return Value** | 1 if the character matches the tested class |
|              | 0 if the character does not match|
 -------------- -------------------------------------------------------------


### ft_isascii
int	ft_isascii(int c);
| | |
| :--- | :--- |
| **Description** | Checks whether c is a 7-bit unsigned char value that fits into the ASCII character set. |
| **Parameters**   | c: the character to look for|
| **Return Value** | 1 if the character matches the tested class |
|              | 0 if the character does not match |
 -------------- -------------------------------------------------------------


### ft_isprint
int	ft_isprint(int c);
| | |
| :--- | :--- |
| **Description** | Checks for any printable character including space. |
| **Parameters** | c: the character to look for|
| **Return Value** | 1 if the character matches the tested class |
|              | 0 if the character does not match | 
 -------------- -------------------------------------------------------------


### ft_strlen
size_t	ft_strlen(const char *s);
| | |
| :--- | :--- |
| **Description** | The ft_strlen() function calculates the length of the stringpointed to by s, excluding the terminating null byte ('\0').
| **Parameters** | s: it is the string whose length we are going to find.
| **Return Value** |  The ft_strlen() function returns the number of bytes in the string  pointed to by s.
 -------------- -------------------------------------------------------------


### ft_memset
void *ft_memset(void *s, int c, size_t n);
| | |
| :--- | :--- |
| **Description** | The ft_memset() function fills the first n bytes of the memory area pointed to by s with the constant byte c.
| **Parameters** | s: is the pointer to the memory area to be filled.
|              | c: the value (converted to an unsigned character) to be set.
|              | n: the number of bytes to be set in the value c.
| **Return Value** | The function returns a pointer to the memory area s.
 -------------- -------------------------------------------------------------


### ft_bzero
void ft_bzero(void *s, size_t n);
| | |
| :--- | :--- |
| **Description** | The function erases the data in the n bytes of the memory starting at the location pointed to by s, by writing zeros (bytes  containing '\0') to that area.
| **Parameters** | s: the pointer to the memory area to be filled.
|              | n: the number of bytes.
| **Return Value** |  None.
 -------------- -------------------------------------------------------------


### ft_memcpy
void	*ft_memcpy(void *dest, const void *src, size_t n);
| | |
| :--- | :--- |
| **Description** | The ft_memcpy() function copies n bytes from memory area src to memory area dest. The memory areas must not overlap. Use ft_memmove() if the memory areas do overlap.
| **Parameters** | dest: memory area.
|              | src: the source string.
|              | n: the number of bytes to copy.
| **Return Value** | The ft_memcpy() function returns a pointer to dest.
 -------------- -------------------------------------------------------------


### ft_memmove
void	*ft_memmove(void *dest, const void *src, size_t n);
| | |
| :--- | :--- |
| **Description** | The function copies n bytes from memory area src to memory area dest. The memory areas may overlap: copying takes place as though the bytes in src are first copied into a temporary array that does not overlap src or dest, and the bytes are then copied from the temporary array to dest.
| **Parameters** | dest: this is the destination array where the content,
|              |       converted to a pointer, will be copied.
|              | src: the source string.
|              | n: the number of bytes to copy.
| **Return Value** |  The ft_memmove() function returns a pointer to dest.
 -------------- -------------------------------------------------------------


### ft_strlcpy
size_t	ft_strlcpy(char *dst, const char *src, size_t size);
| | |
| :--- | :--- |
| **Description** | The ft_strlcpy() function copies up to size - 1 characters from the NUL-terminated string src to dst, NUL-terminating the result.
| **Parameters** | dst: this is the destination string.
|              | src: the string to be copied.
|              | size: number of characters to copy from src.
| **Return Value** | Total length of string to create (src length)
 -------------- -------------------------------------------------------------


### ft_strlcat
size_t	ft_strlcat(char *dst, const char *src, size_t size);
| | |
| :--- | :--- |
| **Description** | The ft_strlcat() function appends the NUL-terminated string src to the end of dst. It will append at most size - strlen(dst) - 1 bytes, NUL-terminating the result.
| **Parameters** | dst: this is the destination string.
|              | src: String to be appended to dst.
|              | size: Maximum number of characters to append.
| **Return Value** |  The length of the string you attempted to create in dst. That means the initial length of dst plus the length of src.
 -------------- -------------------------------------------------------------


### ft_toupper
int		ft_toupper(int c);
| | |
| :--- | :--- |
| **Description** | If c is a lowercase letter, it returns its uppercase equivalent, if an uppercase representation exists in the current locale. Otherwise, it returns c.
| **Parameters** | c: the character to be converted.
| **Return Value** | The value returned is that of the converted letter, or c if the conversion was not possible.
 -------------- -------------------------------------------------------------


### ft_tolower
int		ft_tolower(int c);
| | |
| :--- | :--- |
| **Description** | If c is an uppercase letter, it returns its lowercase equivalent, if a lowercase representation exists in the current locale. Otherwise, it returns c.
| **Parameters** | c: the character to be converted.
| **Return Value** | The value returned is that of the converted letter, or c if the conversion was not possible.
 -------------- -------------------------------------------------------------


### ft_strchr
char	*ft_strchr(const char *s, int c);
| | |
| :--- | :--- |
| **Description** | The  ft_strchr() function returns a pointer to the firstoccurrence of the character c in the string s.
| **Parameters** | s: pointer to string.
|              | c: character to search for.
| **Return Value** |  The functions return a pointer to the matched character or NULL if the character is not found. The terminating null byte is considered part of the string, so that if c is specified as '\0', these functions return a pointer to the terminator.
 -------------- -------------------------------------------------------------


### ft_strrchr
char	*ft_strrchr(const char *s, int c);
| | |
| :--- | :--- |
| **Description** | The ft_strrchr() function returns a pointer to the last occurrence  of the character c in the string s.
| **Parameters** | s: pointer to string.
|              | c: character to search for.
| **Return Value** | The functions return a pointer to the matched character or NULL if the character is not found. The terminating null byte is considered part of the string, so that if c is specified as '\0', these functions return a pointer to the terminator.
 -------------- -------------------------------------------------------------


### ft_strncmp
int		ft_strncmp(const char *s1, const char *s2, size_t n);
| | |
| :--- | :--- |
| **Description** | The ft_strncmp() function compares only the first (at most) n bytes of s1 and s2.
| **Parameters** | s1: the first string to be compared.
|              | s2: the string to compare.
|              | n: the maximum number of characters to compare.
| **Return Value** | The difference between the first two characters that differ in the strings being compared.
 -------------- -------------------------------------------------------------


### ft_memchr
void	*ft_memchr(const void *s, int c, size_t n);
| | |
| :--- | :--- |
| **Description** | The ft_memchr() function scans the initial n bytes of the memory area pointed to by s for the first instance of c. Both c and the bytes of the memory area pointed to by s are interpreted as unsigned char.
| **Parameters** | s: the string to search for.
|              | c: character to search for.
|              | n: the number of bytes to search for.
| **Return Value** | The ft_memchr() function returns a pointer to the matching byte or NULL if the character does not occur in the given memory area.
 -------------- -------------------------------------------------------------


### ft_memcmp
int		ft_memcmp(const void *s1, const void *s2, size_t n);
| | |
| :--- | :--- |
| **Description** |  The ft_memcmp() function compares the first n bytes (each interpreted as unsigned char) of the memory areas s1 and s2.
| **Parameters** | s1: the first string to compare.
|              | s2: the string to compare.
|              | n: the number of bytes to compare.
| **Return Value** | The function returns an integer less than, equal to, or greater than zero if the first n bytes of s1 is found, respectively, to be less than, to match, or be greater than the first n bytes of s2.
 -------------- -------------------------------------------------------------


### ft_strnstr
char	*ft_strnstr(const char *big, const char *little, size_t len);
| | |
| :--- | :--- |
| **Description** | The function locates the first occurrence of the null-terminated string little in the string big, where not more than len characters are searched. Characters that appear after a ‘\0’ character are not searched.
| **Parameters** | big: the string to search for.
|              | little: the string to search for within the 'haystack' string.
|              | len: the maximum number of characters to search for.
| **Return Value** | If little is an empty string, big is returned; if little occurs nowhere in big, NULL is returned; otherwise a pointer to the first character of the first occurrence of little is returned.
 -------------- -------------------------------------------------------------


### ft_atoi
int		ft_atoi(char *str);
| | |
| :--- | :--- |
| **Description** | The ft_atoi() function converts the initial portion of the string pointed to by nptr to int.
| **Parameters** | str: the string we are converting into a whole number.
| **Return Value** | The converted value or 0 on error.
 -------------- -------------------------------------------------------------


### ft_calloc
void	*ft_calloc(size_t nmemb, size_t size);
| | |
| :--- | :--- |
| **Description** | The function allocates memory for an array of nmemb elements of size bytes each and returns a pointer to the allocated memory. The memory is set to zero. If nmemb or size is 0, then ft_calloc() returns either NULL, or a unique pointer value that can later be successfully passed to free().
| **Parameters** | nmemb: specifies the number of elements in an array for which memory is being requested.
|              | size: specifies the size (in bytes) of each individual element.
| **Return Value** | The function returns a pointer to the allocated memory, which is suitably aligned for any built-in type. On error,  these functions return NULL. NULL may also be returned by a successful call to ft_calloc() with nmemb or size equal to zero.
 -------------- -------------------------------------------------------------


### ft_strdup
char	*ft_strdup(const char *s);
| | |
| :--- | :--- |
| **Description** | The function returns a pointer to a new string which is a duplicate of the string s. Memory for the new string is obtained with malloc(3), and can be freed with free(3).
| **Parameters** | s: the pointer to the source string that you wish to duplicate.
| **Return Value** | On success, the function returns a pointer to the duplicated string. It returns NULL if insufficient memory was available, with errno set to indicate the cause of the error.
 -------------- -------------------------------------------------------------


###
# Part 2 - Additional functions

### ft_substr
char *ft_substr(char const *s, unsigned int start, size_t len);
| | |
| :--- | :--- |
| **Description** |  Allocates memory (using malloc(3)) and returns a substring  from the string ’s’. The substring starts at index ’start’ and has a maximum length of ’len’.
| **Parameters** | s: The original string from which to create the substring.
|              | start: The starting index of the substring within ’s’.
|              | len: The maximum length of the substring.
| **Return Value** | The substring.
|              | NULL if the allocation fails.
 -------------- -------------------------------------------------------------


### ft_strjoin
char *ft_strjoin(char const *s1, char const *s2);
| | |
| :--- | :--- |
| **Description** |  Allocates memory (using malloc(3)) and returns a new
|              | string, which is the result of concatenating ’s1’ and ’s2’.
| **Parameters** | s1: The prefix string.
|              | s2: The suffix string.
| **Return Value** | The new string.
|              | NULL if the allocation fails.
 -------------- -------------------------------------------------------------


### ft_strtrim
char *ft_strtrim(char const *s1, char const *set);
| | |
| :--- | :--- |
| **Description** |  Allocates memory (using malloc(3)) and returns a copy of ’s1’ with characters from ’set’ removed from the beginning and the end.
| **Parameters** | s1: The string to be trimmed.
|              | set: The string containing the set of characters to be removed.
| **Return Value** |  The trimmed string.
|              | NULL if the allocation fails.
 -------------- -------------------------------------------------------------


### ft_split
char **ft_split(char const *s, char c);
| | |
| :--- | :--- |
| **Description** |  Allocates memory (using malloc(3)) and returns an array of strings obtained by splitting ’s’ using the character ’c’ as a delimiter. The array must end with a NULL pointer.
| **Parameters** | s: The string to be split.
|              | c: The delimiter character.
| **Return Value** | The array of new strings resulting from the split.
|              | NULL if the allocation fails.
 -------------- -------------------------------------------------------------


### ft_itoa
char *ft_itoa(int n);
| | |
| :--- | :--- |
| **Description** |  Allocates memory (using malloc(3)) and returns a string representing the integer received as an argument. Negative numbers must be handled.
| **Parameters** |  n: The integer to convert.
| **Return Value** | The string representing the integer.
|              | NULL if the allocation fails.
 -------------- -------------------------------------------------------------


### ft_strmapi
char *ft_strmapi(char const *s, char (*f)(unsigned int, char));
| | |
| :--- | :--- |
| **Description** | Applies the function f to each character of the string s, passing its index as the first argument and the character itself as the second. A new string is created (using malloc(3)) to store the results from the successive applications of f.
| **Parameters** | s: The string to iterate over.
|              | f: The function to apply to each character.
| **Return Value** | The string created from the successive applications of ’f’.
|              | Returns NULL if the allocation fails.
 -------------- -------------------------------------------------------------


### ft_striteri
void ft_striteri(char *s, void (*f)(unsigned int, char*));
| | |
| :--- | :--- |
| **Description** | Applies the function ’f’ to each character of the string passed as argument, passing its index as the first argument. Each character is passed by address to ’f’ so it can be modified if necessary.
| **Parameters** | s: The string to iterate over.
|              | f: The function to apply to each character.
| **Return Value** | None
 -------------- -------------------------------------------------------------


### ft_putchar_fd
void ft_putchar_fd(char c, int fd);
| | |
| :--- | :--- |
| **Description** |  Outputs the character ’c’ to the specified file descriptor.
| **Parameters** | c: The character to output.
|              | fd: The file descriptor on which to write.
| **Return Value** | None
 -------------- -------------------------------------------------------------


### ft_putstr_fd
void ft_putstr_fd(char *s, int fd);
| | |
| :--- | :--- |
| **Description** | Outputs the string ’s’ to the specified file descriptor.
| **Parameters** | s: The string to output.
|              | fd: The file descriptor on which to write.
| **Return Value** | None
 -------------- -------------------------------------------------------------


### ft_putendl_fd
void ft_putendl_fd(char *s, int fd);
| | |
| :--- | :--- |
| **Description** | Outputs the string ’s’ to the specified file descriptor followed by a newline.
| **Parameters** | s: The string to output.
|              | fd: The file descriptor on which to write.
| **Return Value** | None
 -------------- -------------------------------------------------------------


### ft_putnbr_fd
void ft_putnbr_fd(int n, int fd);
| | |
| :--- | :--- |
| **Description** | Outputs the integer ’n’ to the specified file descriptor.
| **Parameters** | n: The integer to output.
|              | fd: The file descriptor on which to write.
| **Return Value** | None
 -------------- -------------------------------------------------------------



### 
# Part 3 - linked list

### ft_lstnew
t_list *ft_lstnew(void *content);
| | |
| :--- | :--- |
| **Description** | Allocates memory (using malloc(3)) and returns a new node. The ’content’ member variable is initialized with the given parameter ’content’. The variable ’next’ is initialized to NULL.
| **Parameters** | content: The content to store in the new node.
| **Return Value** | A pointer to the new node
 -------------- -------------------------------------------------------------


### ft_lstadd_front
void ft_lstadd_front(t_list **lst, t_list *new);
| | |
| :--- | :--- |
| **Description** | Adds the node ’new’ at the beginning of the list.
| **Parameters** | lst: The address of a pointer to the first node of a list.
|              | new: The address of a pointer to the node to be added.
| **Return Value** | None
 -------------- -------------------------------------------------------------


### ft_lstsize
int ft_lstsize(t_list *lst);
| | |
| :--- | :--- |
| **Description** | Counts the number of nodes in the list.
| **Parameters** | lst: The beginning of the list.
| **Return Value** | The length of the list
 -------------- -------------------------------------------------------------


### ft_lstlast
t_list *ft_lstlast(t_list *lst);
| | |
| :--- | :--- |
| **Description** | Returns the last node of the list.
| **Parameters** |  lst: The beginning of the list.
| **Return Value** |  Last node of the list
 -------------- -------------------------------------------------------------


### ft_lstadd_back
void ft_lstadd_back(t_list **lst, t_list *new);
| | |
| :--- | :--- |
| **Description** | Adds the node ’new’ at the end of the list.
| **Parameters** | lst: The address of a pointer to the first node of a list.
|              | new: The address of a pointer to the node to be added.
| **Return Value** |  None
 -------------- -------------------------------------------------------------


### ft_lstdelone
void ft_lstdelone(t_list *lst, void (*del)(void *));
| | |
| :--- | :--- |
| **Description** | Takes a node as parameter and frees its content using the function ’del’. Free the node itself but does NOT free the next node.
| **Parameters** | lst: The node to free.
|              | del: The address of the function used to delete the content.
| **Return Value** | None
 -------------- -------------------------------------------------------------


### ft_lstclear
void ft_lstclear(t_list **lst, void (*del)(void *));
| | |
| :--- | :--- |
| **Description** |  Deletes and frees the given node and all its successors, using the function ’del’ and free(3). Finally, set the pointer to the list to NULL.
| **Parameters** |  lst: The address of a pointer to a node.
|              | del: The address of the function used to delete the content of the node.
| **Return Value** | None
 -------------- -------------------------------------------------------------


### ft_lstiter
void ft_lstiter(t_list *lst, void (*f)(void *));
| | |
| :--- | :--- |
| **Description** | Iterates through the list ’lst’ and applies the function ’f’ to the content of each node.
| **Parameters** |  lst: The address of a pointer to a node.
|              | f: The address of the function to apply to each node’s content.
| **Return Value** | None
 -------------- -------------------------------------------------------------


### ft_lstmap
t_list *ft_lstmap(t_list *lst, void *(*f)(void *), void (*del)(void *));
| | |
| :--- | :--- |
| **Description** | Iterates through the list ’lst’, applies the function ’f’ to each node’s content, and creates a new list resulting of the successive applications of the function ’f’. The ’del’ function is used to delete the content of a node if needed.
| **Parameters** |  lst: The address of a pointer to a node.
|              | f: The address of the function applied to each node’s content.
|              | del: The address of the function used to delete a node’s content if needed.
| **Return Value** | The new list.
|              | NULL if the allocation fails.
 -------------- -------------------------------------------------------------

