#DisAssembler for RISC-V hex
#やりたいこと: 32bitの16進数を入力 -> 2進数に変換 -> 上位から7,5,5,3,5,7bitずつ切り分ける -> 逆アセンブルする


import  sys

# --------Define OPCODEs--------
op_OP       = '0110011'
op_OP_Imm   = '0010011'
op_Load     = '0000011'
op_JALR     = '1100111'
op_Store    = '0100011'
op_Branch   = '1100011'
op_LUI      = '0110111'
op_AUIPC    = '0010111'
op_System   = '1110011'
op_MISC_MEM = '0001111'

op_Custom0  = '0001011'
op_Custom1  = '0101011'
op_Custom2  = '1011011' # rv128
op_Custom3  = '1111011' # rv128

# ^-------Define OPCODEs-------^


# Show a message when the instruction is not supported
def print_unsupported():
    print('This instruction is not supported.')
    print('Support: RV32IM')
    return()



# Convert hexadecimal to binary and align the instruction length
def conv_align(i):
    #convert hex to bin
    i_hex = bin(int('0x'+ i ,16))[2:]
    # print('bin      :', i_hex)    #check

    #align the instruction length to 32 bits
    hex_add_zero = '00000000000000000000000000000000' + i_hex
    inst = hex_add_zero[-32:]
    print('Inst     :', inst)     #check

    return (inst)



# Divide the instruction to funct7, rs2, rs1, funct3, rd, opcode
def divide_inst(inst):
    funct7  = inst[:7]
    rs2     = inst[7:12]
    rs1     = inst[12:17]
    funct3  = inst[17:20]
    rd      = inst[20:25]
    opcode  = inst[25:]
    print('Divided  :', funct7 + '|'+ rs2 + '|' + rs1 + '|' + funct3 + '|' + rd + '|' + opcode)

    return(funct7, rs2, rs1, funct3, rd, opcode)



# Select Instruction type
def sel_insttype(opcode):
    if opcode == op_OP:
        # R-Type
        return('R')

    elif opcode == op_OP_Imm or opcode == op_Load or opcode == op_JALR:
        # I-Type (ALU/shift,load,jalr)
        return('I')

    elif opcode == op_Store:
        # S-Type (store)
        return('S')

    elif opcode == op_Branch:
        # B-Type
        return('B')

    elif opcode == op_LUI or opcode == op_AUIPC:
        # U-Type
        return('U')
    
    elif opcode == '1101111':
        # J-Type
        return('J')
    
    elif opcode == op_System or opcode == op_MISC_MEM:
        # Other Type (ecall,ebrake,fence,fence.i)
        return('other')

    elif opcode == op_Custom0 or opcode == op_Custom1 or opcode == op_Custom2 or opcode == op_Custom3:
        # Custom Inst
        return('Custom')

    else:
        #error
        return('error')



# Select register name
def reg_name(regnum):
    reg=['zero','ra','sp','gp','tp','t0','t1','t2','s0/fp','s1','a0','a1','a2','a3','a4','a5',
            'a6','a7','s2','s3','s4','s5','s6','s7','s8','s9','s10','s11','t3','t4','t5','t6']

    regnum = int(regnum,2)

    regname = reg[regnum]

    return(regname)



# R-type Instruction
def Rtype(funct7, rs2, rs1, funct3, rd, opcode):
    if opcode == op_OP:

        # RV32I
        if funct7 == '0000000':
            if funct3 == '000':
                opname = 'ADD'

            elif funct3 == '001':
                opname = 'SLL'

            elif funct3 == '010':
                opname = 'SLT'

            elif funct3 == '011':
                opname = 'SLTU'

            elif funct3 == '100':
                opname = 'XOR'

            elif funct3 == '101':
                opname = 'SRL'

            elif funct3 == '110':
                opname = 'OR'

            elif funct3 == '111':
                opname = 'AND'

            else:
                print_unsupported()
                opname = 'XXX'

        elif funct7 == '0100000':
            if funct3 == '000':
                opname = 'SUB'

            elif funct3 == '101':
                opname = 'SRA'

            else:
                print_unsupported()
                opname = 'XXX'
                return()

        # -------- M extention --------
        elif funct7 == '0000001':
            if funct3 == '000':
                opname = 'MUL'

            elif funct3 == '001':
                opname = 'MULH'

            elif funct3 == '010':
                opname = 'MULHSU'

            elif funct3 == '011':
                opname = 'MULHU'

            elif funct3 == '100':
                opname = 'DIV'

            elif funct3 == '101':
                opname = 'DIVU'

            elif funct3 == '110':
                opname = 'REM'

            elif funct3 == '111':
                opname = 'REMU'

            else:
                print_unsupported()
                opname = 'XXX'
                return()
        # ^------- M extention -------^

        else:
            print_unsupported()
            opname = 'XXX'
            return()

    else:
        print_unsupported()
        opname = 'XXX'
        return()

    print('OP   rd, rs1, rs2')
    print(opname + '   ' + reg_name(rd) + ', ' + reg_name(rs1) + ', ' + reg_name(rs2) )
    return()



# I-type Instruction
def Itype(funct7, rs2, rs1, funct3, rd, opcode):
    if opcode == op_OP_Imm:
        if funct3 == '000':
            if rs1 == '00000':
                if rd == '00000':
                    opname = 'NOP'
                    print('OP')
                    print(opname)
                    return()

                else:
                    opname = 'LI'
                    print('OP   rd, imm')
                    print(opname + '   '+ reg_name(rd) + ', ' + hex(int(funct7 + rs2,2)))
                    return()

            else:
                opname = 'ADDI'

        elif funct3 == '010':
            opname = 'SLTI'
        
        elif funct3 == '011':
            opname = 'SLTIU'

        elif funct3 == '100':
            opname = 'XORI'

        elif funct3 == '110':
            opname = 'ORI'

        elif funct3 == '111':
            opname = 'ANDI'

        elif funct3 == '001':
            opname = 'SLLI'

        elif funct3 == '101':
            if funct7 == '0000000':
                opname = 'SRLI'

            elif funct7 == '0100000':
                opname = 'SRAI'

            else:
                print_unsupported()
                opname = 'XXX'
                return()

        else:
            print_unsupported()
            opname = 'XXX'
            return()

    elif opcode == op_Load:
        if funct3 == '000':
            opname = 'LB'

        elif funct3 == '001':
            opname = 'LH'

        elif funct3 == '010':
            opname = 'LW'

        elif funct3 == '100':
            opname = 'LBU'

        elif funct3 == '101':
            opname = 'LHU'

        else:
            print_unsupported()
            opname = 'XXX'
            return()

    elif opcode == op_JALR:
        if (funct7 + rs2) == '000000000000' and rd == '00000':
            if rs1 == '00001':
                opname = 'RET'
                print('OP')
                print(opname)
                return()

            else:
                opname = 'JR'
                print('OP   rs1')
                print(opname + '   ' + reg_name(rs1))
                return()

        else:
            opname = 'JALR'

    else:
        print_unsupported()
        opname = 'XXX'
        return()


    if funct7[:1] == '0':       #正
        imm_I = int(funct7 + rs2,2)

    elif funct7[:1] == '1':     #負
        imm_I = ~( int(funct7 + rs2,2) ^ 0xfff )   # 2の補数



    if opcode == op_OP_Imm and  (funct3 == '001' or funct3 == '101'):
        print('OP   rd, rs1, shamt')
        print(opname + '   ' + reg_name(rd) + ', ' + reg_name(rs1) + ', ' + hex(int(rs2,2)))
        return()

    elif opcode == op_Load:
        print('OP   rd, offset(rs1)')
        print(opname + '   ' + reg_name(rd) + ', ' + hex(imm_I) + '(' + reg_name(rs1) + ')' )
        return()

    else:
        print('OP   rd, rs1, imm')
        print(opname + '   ' + reg_name(rd) + ', ' + reg_name(rs1) + ', ' + hex(imm_I))
        return()



# S-type Instruction
def Stype(funct7, rs2, rs1, funct3, rd, opcode):
    if opcode == op_Store:
        if funct3 == '000':
            opname = 'SB'

        elif funct3 == '001':
            opname = 'SH'

        elif funct3 == '010':
            opname = 'SW'

        else:
            print_unsupported()
            opname = 'XXX'
            return()

    else:
        print_unsupported()
        opname = 'XXX'
        return()

    print('OP   rs2, offset(rs1)')
    print(opname + '   ' + reg_name(rs2) + ', ' + hex(int(funct7 + rd,2)) + '(' + reg_name(rs1) + ')' )
    return()



# B-type Instruction
def Btype(funct7, rs2, rs1, funct3, rd, opcode):
    if funct7[:1] == '0':       #正
        imm_B = int(funct7[:1] + rd[-1:] + funct7[1:] + rd[:-1] +'0',2)

    elif funct7[:1] == '1':     #負
        imm_B = ~( int(funct7[:1] + rd[-1:] + funct7[1:] + rd[:-1] +'0',2) ^ 0x1fff )   # 2の補数

    if opcode == op_Branch:
        if funct3 == '000':
            opname = 'BEQ'

        elif funct3 == '001':
            opname = 'BNE'

        elif funct3 == '100':
            opname = 'BLT'

        elif funct3 == '101':
            opname = 'BGE'

        elif funct3 == '110':
            opname = 'BTLU'

        elif funct3 == '111':
            opname = 'BGEU'

        else:
            print_unsupported()
            opname = 'XXX'
            return()

    else:
        print_unsupported()
        opname = 'XXX'
        return()

    print('OP   rs1, rs2, offset')
    print(opname + '   ' + reg_name(rs1) + ', ' + reg_name(rs2) + ', ' + hex(imm_B))
    return()



# U-type Instruction
def Utype(imm, rd, opcode):
    if opcode == op_LUI:
        opname = 'LUI'
    
    elif opcode == op_AUIPC:
        opname = 'AUIPC'

    else:
        print_unsupported()
        opname = 'XXX'
        return()

    print('OP   rd, imm')
    print(opname + '   ' + reg_name(rd) + ', ' + hex(int(imm,2)))
    return()



# J-type Instruction
def Jtype(imm, rd, opcode):
    if imm[:1] == '0':      #正
        imm_J = int(imm[:1] + imm[12:20] + imm[11:12] + imm[1:11] + '0',2)

    elif imm[:1] == '1':    #負
        imm_J = ~( int(imm[:1] + imm[12:20] + imm[11:12] + imm[1:11] + '0',2) ^ 0x1fffff )  # 2の補数

    if opcode == '1101111':
        if rd == '00000':
            opname = 'J'
            print('OP   offset')
            print(opname + '   ' + hex(imm_J))
            return()

        else:
            opname = 'JAL'

    else:
        print_unsupported()
        opname = 'XXX'
        return()
    
    print('OP   rd, offset')
    print(opname + '   ' + reg_name(rd) + ', ' + hex(imm_J))
    return()



# Other-type Instruction
def Othertype(funct7, rs2, rs1, funct3, rd, opcode):
    if opcode == op_System:
        if rs2 == '00000':
            opname = 'ECALL'

        elif rs2 == '00001':
            opname = 'EBREAK'

        else:
            print_unsupported()
            opname = 'XXX'
            return()

    elif opcode == op_MISC_MEM:
        if funct3 == '000':
            opname = 'FENCE'

        elif funct3 == '001':
            opname = 'FENCE.I'

        else:
            print_unsupported()
            opname = 'XXX'
            return()

    else:
        print_unsupported()
        opname = 'XXX'
        return()

    if opcode == op_MISC_MEM and funct3 == '000':
        print('OP   pred, succ')
        pred = funct7[-3:] + rs2[:1]
        succ = rs2[1:]
        print(opname + '   ' + hex(int(pred,2)) + ', ' + hex(int(succ,2)))
        return()

    else:
        print('OP')
        print(opname)
        return()



# RV32C/64C Instruction
def C_Inst(inst):
    inst_c = inst[-16:]         # Align the instruction length to 16 bits
    print('\ninst_c   :', inst_c)   # Check
    print('RV32/64C is not supported.')
    return()



# Custom Instruction
def CustomInst(funct7, rs2, rs1, funct3, rd, opcode):

    if opcode == op_Custom2:
        opname = 'prngrolf'
        print('Type: U')
        print('OP   rd')
        print(opname + '   ' + reg_name(rd))

    else:
        # print('No custom instruction available.')
        print('Only "prngrolf" is available among the custom instructions.')
        print_unsupported()
        opname = 'XXX'

    return()



# -------- Fullsize Inst --------
def Full_Inst(inst):

    # Divide the instruction to funct7, rs2, rs1, funct3, rd, opcode
    funct7, rs2, rs1, funct3, rd, opcode = divide_inst(inst)

    # Select Instruction type
    InstType = sel_insttype(opcode)

    print('InstType : ' + InstType + '\n')

    # Show Assembly
    if   InstType == 'R':
        Rtype(funct7, rs2, rs1, funct3, rd, opcode)

    elif InstType == 'I':
        Itype(funct7, rs2, rs1, funct3, rd, opcode)

    elif InstType == 'S':
        Stype(funct7, rs2, rs1, funct3, rd, opcode)

    elif InstType == 'B':
        Btype(funct7, rs2, rs1, funct3, rd, opcode)

    elif InstType == 'U':
        Utype(inst[:20], rd, opcode)

    elif InstType == 'J':
        Jtype(inst[:20], rd, opcode)

    elif InstType == 'other':       # Other Type (ecall,ebrake,fence,fence.i)
        Othertype(funct7, rs2, rs1, funct3, rd, opcode)

    elif InstType == 'Custom':
        CustomInst(funct7, rs2, rs1, funct3, rd, opcode)

    else:
        print_unsupported()


    return()



# -------- main --------
def main():
    print('\nDisAssembler for RV32I\n')

    while True:

        i = input('input(hex) : ')
        if i == '':   # Null Check
            print('Fill input with 0 since the input is null.')
            i = '00000000000000000000000000000000'
        else:
            pass

        print('\ninput    :',i)     # Input Check

        inst = conv_align(i)

        # Check RV**C
        op_c = inst[-2:]
        if op_c != '11':    # If RV**C
            C_Inst(inst)

        else:               # else
            Full_Inst(inst)

        print('\n')


        while True: # Continue Check

            l = input('Continue? (y or n):')

            if l == 'y':
                next = 'Continue'
                break

            elif l == 'n':
                next = 'Finish'
                break

            else:
                print('Answer in y or n.')


        if next == 'Finish':
            break
        else:
            print('\n')


    return()

# ^--------------- main ---------------^



if __name__ == "__main__":
    main()

