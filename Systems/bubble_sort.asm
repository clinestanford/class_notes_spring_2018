
.data
#first need to store the array
myarray: .word 15, 23, 12, 5, 8, 15, 6, 28, 4
mysize: .word 10

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
   addi $a0 $0 0x0D
   syscall
   jr $ra		#jumps back to return address unconditionally
   
swap:
			#don't forgot a2 is the i index, and a3 is the j
   sll $t0 $a2 2
   add $t0 $a0 $t0	#adds the offset from the index to the array position for i
   lw  $t2 0($t0)
   lw  $t3 4($t0)	#loads each of the words into registers t0 and t1
   sw  $t3 0($t0)
   sw  $t2 4($t0)	#places the value from i into j, and j into i
   jr $ra
   
   
sort:
   move $s0 $a0		#s0 is the beginning of the array
   move $s1 $a1		#s1 is the size of the array
   addi $s2 $s1 -1	#s2 stores the value for n-1
   addi $t9 $0 0
   addi $t8 $0 0	#starts i = j = 0
   addi $sp $sp -4
   sw   $ra 0($sp)	#push the return address to the stack, we will be linking with other functions
   outer:
      add  $t8 $0 $0
      slt  $t0 $t9 $s2
      beq  $t0 $0 exit	#should exit if i == size
      inner:
         neg $t0 $t9
         add $t0 $t0 $s2
         slt $t1 $t8 $t0
         beq $t1 $0 exit1
         sll $t0 $t8 2
         add $t1 $t0 $s0
         lw $t2 0($t1)
         lw $t3 4($t1)
         slt $t4 $t2 $t3
         bne $t4 $0 incj
         move $a2 $t8
         jal swap
         j incj
        
   exit1:
   addi $t9 $t9 1	#increment i+1
   j outer
   
   incj:
   addi $t8 $t8 1
   j inner
        
   exit:   
   lw   $ra 0($sp)
   addi $sp $sp 4
   jr $ra
   
   
main:#starts the main portion of the program
   li $v0 4	#load system instruction 4(print string) into v0 register
   
   la $a0 myarray
   lw $a1 mysize
   jal printfunc
    
   #remember to reset the variables
   la $a0 myarray
   lw $a1 mysize
   
   jal sort
   
   jal printfunc
   
leave:
   li $v0 10
   syscall
