# Hello, World! .data 
## Data declaration section 
## String to be printed: 
.data
out_string: .asciiz "\nHello, World!\n"

     .text ## Assembly language instructions go in text segment 
main: ## Start of code section
  li $v0, 4          # load system instruction 4 (print string) into v0 register 
  la $a0, out_string # load address of string to be printed into $a0
  syscall            # call operating system to perform operation 
                         # specified by contents of $v0 
                         # syscall takes its arguments from registers $a0, $a1, . .. 

  li $v0, 10         # load system instruction 10 (terminate program) into v0 register
  syscall