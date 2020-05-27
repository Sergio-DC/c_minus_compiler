#Transalting c- fragment to assembler code, sample of c- code:
# int suma(int p, int q) {
#   return q + p;
# }
#
# void main(void) {
#   int x;
#   int y;
#   x = 3;
#   y = 2;
#   x = suma(x, y);
#   output(x);
# }
.data 
    var_x: .word 12
    var_y: .word 3

# Making Room for a function
.text

.globl main

#Calle Part
suma:
    move $fp $sp #move the pointer of the $fp to point to $sp
    sw $ra 0($sp) #save the return address in the activation record
    addiu $sp $sp -4
    # Calculate the sum of the 2 arguments
    # Val Left
    # Search in ST the offset of valIzq
    li $t7 2 ## Num 2 represent the logical_offset of 'y' variable
    # Calculate physical offset
    li $t6 4
    mult $t7 $t6  # Num 4 is the byte_alignment
    mflo $t6 # <- It has the physical offset
    # Load the param value from stack to $t0
    addu $t6 $fp $t6
    lw $t0 ($t6) #This line takes advantage of $fp as pivot to search for 'y' param 
    # 
    # Val Right
    # Search in ST the offset of valDer
    li $t7 1 ## Num 2 represent the logical_offset of 'x' variable
    # Calculate physical offset
    li $t6 4
    mult $t7 $t6  # Num 4 is the byte_alignment
    mflo $t6 # <- It has the physical offset
    # Load the param value from stack to $t1
    addu $t6 $fp $t6
    lw $t1 ($t6) #This line takes advantage of $fp as pivot to search for 'x' param
    #Calculate the sum
    add $a0 $t0 $t1

    # Load return address to register $ra
    lw $ra 4($sp)
    # The stack-pointer will do a deep pop to restore to the pevious activation-frame top 
    #Get from the ST the count of parameters
    li $t0 2 # Num 2 represents the number of total params obtained from ST
    #deep offset = z
    li $t6 4
    mult $t0 $t6 #  4 * N
    mflo $t0 
    addi $t0 $t0 8 # z = 4*n + 8
    addu $sp $sp $t0
    lw $fp 0($sp) # Restore the $fp to the old Frame pointer  

    jr $ra

main:
    #1 Set %fp to the bottom
    move $fp $sp
    addiu $sp $sp -4 # Move stack_pointer to the next empty position
    #2 Reserve space for local variables
        #2.1 Determine how many local variables the main function will have
            #On the python side: Count the number of local variables(using ST) and save that num in register %t7
            li $t7 2 #The number 2 represent the number of local variables in main function
        #2.2 Reserve space for the local variables
            li $t6 4
            mult $t7 $t6 # n_number_of_local_variables   4_byte_alignment (n * 4)
            mflo $t6 # physical offset that is going to use to reserve space in stack for local variables
            sub $sp $sp $t6
    #3 Update local variables
        #3.1 When a EXPRESSION_1 is reached update the local_variable value (this is for vaiable X)
            # On the python side: scan value:int and store in the register $a0
            lw $a0 var_x # Number 3 represent the value assigned to X
            #On the python side: Search variable in ST and get the logical_offset of that, save the logical_offset in register $t7
            li $t7 1 # Number 1 represent the logical offset of variable 'x'
            #Calculte the physical offset
            li $t6 4
            mult $t7 $t6 # Num 4 is the byte-alignment
            mflo $t6 #$t6 has the physical offset
            # Search the variable 'x' using the physical offset and store the value in the stack
            subu $t6 $fp $t6
            sw $a0 ($t6) # the follwing line is taking advantage of $fp to search the 'X' variable
        #3.2 When a EXPRESSION_1 is reached update the local_variable value (this is for variable Y)
            # On the python side: scan int and store in the register $a0
            lw $a0 var_y # Number 2 represent the value assigned to Y
            #On the python side: Search variable in ST and get the logical_offset of that, save the logical_offset in register $t7
            li $t7 2 # Number 2 represent the logical offset of variable 'y'
            #Calculte the physical offset
            li $t6 4
            mult $t7 $t6 # Num 4 is the byte-alignment
            mflo $t6 #$t6 has the physical offset
            # Search the variable 'y' using the physical offset and store the value in the stack
            subu $t6 $fp $t6
            sw $a0 ($t6)# the follwing line is taking advantage of $fp to search the 'Y' variable
    #4 Call sum function
    # Caller part: 
        #4.1 Store the Old FramePointer, at this point a new Activation Record is created
        sw $fp 0($sp)
        addiu $sp $sp -4
        #4.2 save the params in a reverse manner
        # On the python side: When a NodeType.CALL is reached, save the params in a list in a reverse manner
        # traverse this list and and get the logical offset of the current param by searching in the ST
        # Search variable in ST and get the logical_offset of that, save the logical_offset in register $t7
        
            #Param Y        
            li $t7 2 # Number 2 represent the logical offset of variable 'Y', that number is obtained by ST
            # Calculate the physical offset
            li $t6 4
            mult $t7 $t6 #Num 4 is the byte-alignment
            mflo $t6 # <- it has the physical offset
            # Search the variable 'Y' using the physical offset and load the value from memory to register $a0
                subu $t6 $fp $t6
                lw $a0 ($t6) # the following line is taking advantage of $fp to search the 'Y' variable
                sw $a0 0($sp) #Store param in the param section of the new Activation Record
                addiu $sp $sp -4
            #Param X        
            li $t7 1 # Number 1 represent the logical offset of variable 'X', that number is obtained by ST
            # Calculate the physical offset
            li $t6 4
            mult $t7 $t6 #Num 4 is the byte-alignment
            mflo $t6 # <- it has the physical offset
            # Search the variable 'X' using the physical offset and load the value from memory to register $a0
                subu $t6 $fp $t6
                lw $a0 ($t6) # the following line is taking advantage of $fp to search the 'X' variable
                sw $a0 0($sp)#Store param in the param section of the new Activation Record
                addiu $sp $sp -4
        
        # 4.3 Jump to the 'suma' prodecure and save the return address
        jal suma
        
    #5 Save the returned value in the corresponding variable, in this case 'x', Remember that the returned value is in $a0
        #On the pyhton side: search in ST logical_offset of variable x 
        li $t7 1 #Num 1 represent logical offset of variable 'x' obtained from ST
        #Calculate the physical offset
        li $t6 4
        mult $t7 $t6 # Num 4 is the byte-alignment
        mflo $t6 # <- Physical offset
        subu $t6 $fp $t6
        sw $a0 ($t6) #the following line is taking advantage of $fp to save the retured value in the stack (That position in stack is variable 'x')

    #Print the x value
    #. Search the variable in ST that is gonna printed 
    #Get the logical offset of the variable
    li $t7 1 # 1 represent the logical offset of some variable
    li $t6 4 # 4 byte-alignment
    mult $t7 $t6#calculate physical offset
    mflo $t6
    subu $t6 $fp $t6
    lw $a0 ($t6)

    li $v0 1
    syscall

    #Finish Program
    li $v0 10
    syscall