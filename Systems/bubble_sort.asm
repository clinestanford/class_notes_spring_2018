
.data
#first need to store the array
myarray: .word 12, 15
mysize: .word 2

.text
j main #jump to the main part of the program

printfunc: #print function
   #need to initialize a few of the variables
   #make sure the $a0 contains the starting address of the array
   #make sure the $ra is set as well
   #a1 must be the size of the array
   
   add $t0 $0 $a0	#load starting position into $a0
   move $t1 $a1		#load int size into $a1
   
   add $t9 $0 $0	#start the counter from 0
   printloop:
      sll $t2 $t9 2 	#multiply index by 4 to get memory location offset
      add $t2 $t0 $t2	#move memory locator to the ith index
      lw  $a0 0($t2)	#load value at index into $t2
      
      li $v0 1		#load instruction
      syscall
      
      li $v0 11
      addi $a0 $0 0x20 	#loads the ascii " "
      syscall
      
      addi $t9 $t9 1	#increments value of $t9
      slt  $t8 $t9 $t1	#set less than, compares $t9 to $t1 and stores comparison in $t8
      bne  $t8 $0 printloop	#loop will break if $t8 is equal to $t0
   
   li $v0 11
   addi $a0 $0 0x0D	#prints character return at the end of the line
   syscall
   jr $ra		#jumps back to return address unconditionally
   
main:#starts the main portion of the program
   li $v0 4	#load system instruction 4(print string) into v0 register
   
   la $a0 myarray
   lw $a1 mysize
   jal printfunc
   
   jal printfunc
   
leave:
   li $v0 10
   syscall
