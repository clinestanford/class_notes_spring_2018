## Data declaration section 
.data
# these are globals
  # String to be printed: 
  endline: .asciiz "\n"
  test_string: .asciiz "I zig and Zag"
  compare_string: .asciiz "J!ajh!boe!Abh"
  
  # array of word long ints
  myarray:    .word 23, 4, 34, 55, 87, 23, 99, 12, 233, 45, 40003245, 23, 45, 68, 69
  mysize:     .word 15

.text ## Assembly language instructions go in text segment 
j main # very first, goto main.

# input values are really globals and could be used by the printfunc, but to demonstrate modularization,
#   they are passed 
printfunc:
   # inputs:
   # ra must be set before calling this and contain the location to where this will return after execution
   # a0 must be the base address of the array of integers to print
   # a1 must be the size of the array to print (or the number of elements in the array to print)
   # outputs: only output is the system "display", no return values
   # saved registers: no need as this internally only uses t registers
   #
   # internal register uses
   # t0 = address of base of myarray from input $a0
   # t1 = value of mysize from input $a1
   # t2 is used to put address, once calculated of array[index]
   # t8 is used to hold comparison result
   # t9 = index into array 
  add $t0 $0 $a0  # move a0 to t0 via an add statement
  move $t1 $a1    # move a1 to t1 via the move command
  # either of the above commands work. Before you choose, look at the 
  #   assembled version of each command
  
  add $t9 $0 $0   # initialize the counter before the loop
  printloop:
    sll $t2 $t9 2   # multiply index by 4
    add $t2 $t0 $t2 # add base address of array to 4*index
    lw $a0 0($t2) # put value of myarray[index] into t2
    
    li $v0, 1         # load instruction 1 (print an int whose value is in a0)
    syscall
    
    li $v0, 11        #load instruction 11 (print single char whose value is in a0)
    addi $a0, $0, 0x20  #load ascii char 32 = 0x20 = 'space'
    syscall
    
    
    addi $t9 $t9 1  # increment counter
    slt $t8 $t9 $t1  # compare counter t9 to size t1
    bne $t8 $0 printloop # loop if $t9 < size
    
  li $v0 11 #load instruction 11 (print single char whose value is in a0)
  addi $a0 $0 0x0D # ascii char 13 = 0x0D = carriage return
  syscall  # print newline at the end of printing array so whatever comes next is on next line
  jr $ra #leave function

strencode:
   #string address is stored in a0. Need to check to see if the value of the string is z or Z
   add $t9 $a0 $0 	#gives t0 the same address as the point to the first character in the array
   li  $t8 'z'		#initializes t8 to be able to compare later
   li  $t7 'Z'		#initializes t7 to be able to compare later
   li  $t6 'a'
   li  $t5 'A'
   
   loop:
     lb $t0 0($t9)	#load current byte into t0
     beqz $t0 exit_encode	#exits loop if we are at the end of the string
     beq  $t0 $t8 lowerz
     beq  $t0 $t7 upperz
     addi $t0 $t0 1	#adds 1 to current char if it isn't z or Z
     sb   $t0 0($t9)	#store the value of $t0 into address $t9
     addi $t9 $t9 1	#increments the memory address by one

     j    loop
     
   lowerz:		#saves byte a to z
     sb   $t6 0($t9)
     addi $t9 $t9 1
     j    loop
   
   upperz:		#saves byte A to Z
     sb   $t5 0($t9)
     addi $t9 $t9 1
     j    loop
     
   exit_encode:
   jr $ra

strcmp:
   #this compares the string in a0 and a1
   sw   $ra 0($sp)	#stores the return address onto the stack
   addi $sp $sp 4
   
   jal strencode	#will jump to the string encode function
   
   add $t9 $a0 $0	#first spot in a0->t9
   add $t8 $a1 $0	#first spot in a1->t9
   
   cmploop:
     lb   $t0 0($t9)
     lb   $t1 0($t8)	#load each of the first elements into t0 and t1
     beqz $t0 good_exit	#will branch if we have reached the null terminator
     beqz $t1 good_exit
     bne  $t1 $t0 bad_exit
     addi $t9 $t9 1	#add one to the pointer location
     addi $t8 $t8 1
     j    cmploop
     
   good_exit:
     addi $v0 $0 0 	#stores the value of 0 into v0 
     j    strcmpexit
     
   bad_exit:
     addi $v0 $0 1	#stores the value of 1 into v0
     j    strcmpexit
   
   strcmpexit:
   addi $sp $sp -4	#decrements stack pointer, and loads $ra
   lw $ra 0($sp)
   jr $ra

main: ## Start of code section
  li $v0 4
  la $a0 test_string
  syscall     
  
  la $a0 endline
  syscall
  
  la $a0 compare_string
  syscall
  
  la $a0 endline
  syscall
  
  la $a0 test_string
  la $a1 compare_string
  
  jal strcmp 	#should jump to the string encode function, and return
  
  add $a0 $v0 $0	#get the return value from string compare
  li  $v0 1
  syscall
  
  li $v0, 11		#load instruction 11 (print single char whose value is in a0)
  addi $a0 $0 0x0D
  syscall
  syscall
                             

  j leave

leave:
  li $v0, 10         # load system instruction 10 (terminate program) into v0 register
  syscall
