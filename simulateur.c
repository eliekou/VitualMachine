#include <stdlib.h> 
#include <stdio.h> 
#include <stdint.h>
#include <stdbool.h>
#define MEM_SIZE_WORDS 128



int mem[2084];//mémoire
int regs[32];//registre
int PC =0;
int IR;  //instruction register





int opcode;
int rd;
int rs = 0;
u_int32_t im;

int rs1;
int rs2;

int ra;

//Pour les branchements
int rs;
int addr;

//Pour les scalls
int n;


int go_on =1; //permet d'arréter en cas de stop
int loop();

void print_regs();
void print_mem();

int main(){//lire le fichier binaire en C ,le fichier binaire étant fourni par l'assembleur
    int to_read, nb_read, r, i;
    
    
    FILE *input_file = fopen("fichier.bin", "rb");
    if (input_file == NULL) {
        perror("fopen"); // print an error message (file not found, permission denied...) return EXIT_FAILURE;
    }
    to_read = MEM_SIZE_WORDS; 
    nb_read = 0;
    do {
        r = fread(&mem[nb_read], sizeof(uint32_t), to_read, input_file); 
        to_read -= r;
        nb_read += r;
    } while (to_read > 0 && r > 0 && nb_read < MEM_SIZE_WORDS);
    fclose(input_file);
    for (i = 0; i < nb_read; i++)
        printf("%i -> 0x%08x\n", i, mem[i]);
        
    
        
    
    loop();
    
        
    return EXIT_SUCCESS; 

}

void print_regs(){

    int i = 0;
    for(i=0;i<32;i++)
    {
        printf("Le registre %d est égal à %d\n",i,regs[i]);
    }
void print_mem(){
    int a =0;
    for (a =0;a<2048; i++)
    {
        printf("Le registre %d est égal à %d\n",a,mem[a]);
    }
}

}
void decode_R_instruction(uint32_t instr){
    //opcode = instr >> 26;
    rd = (instr >> 21) & 0x1f;
    rs1 = (instr >> 16) & 0x1f;
    rs2 = (instr >> 11) & 0x1f;
    printf("rd= %lu, rs1 = %lu, rs2 = %lu\n",rd,rs1,rs2);

}

void decode_I_instruction(uint32_t instr)
{
//va à partir de l'instruction nous ressortir l'opcode est les registre à utilisé pour réaliser l'opération dans un second temps

    //opcode = instr >> 26;
    rd = (instr >> 21) & 0x1f;
    rs = (instr >> 16) & 0x1f;
    im = instr & 0x0000ffff;
// immediate sign extention
    if ((im & 0x00008000) != 0)
        im |= 0xffff0000;
}

void decode_JR_instruction(uint32_t instr){
    
    rd =( instr >> 21) & 0x1f;
    ra =( instr >> 16)& 0x1f;
    printf("Le registre du jump est%lu\n",ra);
    //rd =0;
}
void decode_JI_instruction(uint32_t instr){
    rd = (instr >> 21) & 0x1f;
    addr = instr & 0x1fffff;
    //addr =( instr ) & 0x1f;
    printf("On va aller jump au registre %lu\n",addr);
    rd =0;
}

void decode_B_instruction(uint32_t instr){//Concerne les instructions de type branch
    rs = (instr >> 21) & 0x1f;
    addr = instr & 0x1fffff;
    printf("rs= %lu, addr = %lu\n",rs,addr);
    
}
void decode_scall_instruction(uint32_t instr){
    n =  instr & 0x3ffffff;
    printf("On fait un scall avec%d\n",n);
}
void write_register(int index, int value){

    if (index == 0){
        value = 0;
    }
    regs[index] = value;
}


// input, instruction word
// output, instruction opcode
// output, destination register number // output, source register number
// output, sign-extended immediate

void add(){

    printf("add r%d r%d r%d\n", rd, rs1, rs2);
    write_register(rd,regs[rs1]+regs[rs2]);//utiliser un pointeur ici?

}

void addi(){
    printf("add r%d r%d %d\n", rd, rs, im);
    write_register(rd,regs[rs]+ im);
}




void sub(){

    printf("sub r%d r%d r%d\n", rd, rs1, rs2);
    write_register(rd,regs[rs1]-regs[rs2]);
}

void subi(){
    printf("sub r%d r%d %d\n", rd, rs, im);
    write_register(rd,regs[rs]- im);
}

void mul(){
    printf("mul  r%d r%d r%d\n", rd, rs1, rs2);
    write_register(rd,regs[rs1]*regs[rs2]);
}

void muli(){
    printf("mul r%d r%d %d\n", rd, rs, im);
    write_register(rd,regs[rs]* im);
}
void div_(){
    printf("div  r%d r%d r%d\n", rd, rs1, rs2);
    write_register(rd,regs[rs1]/regs[rs2]);
}
void divi(){
    printf("div r%d r%d %d\n", rd, rs, im);
    write_register(rd,regs[rs]/ im);
}
void and(){
    printf("and r%d r%d r%d\n", rd, rs1, rs2);
    write_register(rd,regs[rs1]&regs[rs2]);
}
void andi(){
    printf("and r%d r%d %d\n", rd, rs, im);
    write_register(rd,regs[rs]& im);
}
void or(){
    printf("or  r%d r%d r%d\n", rd, rs1, rs2);
    write_register(rd,regs[rs1]||regs[rs2]);
}

void ori(){
    printf("or r%d r%d %d\n", rd, rs, im);
    write_register(rd,regs[rs]||im);
}

void xor(){
    printf("xor  r%d r%d r%d\n", rd, rs1, rs2);
    write_register(rd,regs[rs1] ^ regs[rs2]);
}

void xori(){
    printf("xori  r%d r%d %d\n", rd, rs, im);
    write_register(rd,regs[rs] ^ im);
}
void shl(){
    printf("shl  r%d r%d r%d\n", rd, rs1, rs2);
    write_register(rd,regs[rs1] << regs[rs2]);
}
void shli(){
    printf("shl r%d r%d %d\n", rd, rs, im);
    write_register(rd,regs[rs] << im);
}
void shr(){
    printf("shr  r%d r%d r%d\n", rd, rs1, rs2);
    write_register(rd,regs[rs1]>>regs[rs2]);
}
void shri(){
    printf("shr r%d r%d %d\n", rd, rs, im);
    write_register(rd,regs[rs]>>im);
}
void slt(){
    printf("slt r%d r%d r%d\n", rd, rs1, rs2);
    write_register(rd,regs[rs1]<regs[rs2]);
}
void slti(){
    printf("slt r%d r%d %d\n", rd, rs, im);
    write_register(rd,regs[rs]<im);
}
void sle(){
    printf("sle r%d r%d r%d\n", rd, rs1, rs2);
    write_register(rd,regs[rs1] <= regs[rs2]);
}
void slei(){
    printf("sle r%d r%d %d\n", rd, rs, im);
    
    write_register(rd,regs[rs] <= im);
}
void seq(){
    printf("seq r%d r%d r%d\n", rd, rs1, rs2);
    write_register(rd,regs[rs1]==regs[rs2]);
}
//différence entre seq et seqi?
void seqi(){
    printf("seq r%d r%d %d\n", rd, rs, im);
    write_register(rd,(regs[rs]==im));
}
//Rd,rs et im n'ont plus forcément autant de sens mais c'est le meme type I
void load(){
    printf("load r%d r%d %d\n", rd, rs, im);
    if ((rs + im) > 2048){
        printf("Error: superior to memory_size");

    }
    else{
        printf("MEMORY_SIZE: OK-> proceed to load");
        write_register(rd,mem[regs[rs]+im]);
        printf("On a écrit dans le registre %d la valeur%d\n",rd,mem[regs[rs]+im]);
    }
    /*write_register(rd,mem[regs[rs]+im]);
    printf("On a écrit dans le registre %d la valeur%d\n",rd,mem[regs[rs]+im]);*/
}
void store(){
    printf("store r%d r%d %d\n",rd,rs,im);
    if ((regs[rs]+im)> 2048 && (regs[rs]+im)<0){
        printf("Error: impossible to store");
    }
    else{
        mem[regs[rs]+im]=regs[rd];
        printf("la  mem %d est égale à %d\n",regs[rs]+im,regs[rd]);
    }

    
}
void jump(){
    printf("jump r%d r%d\n",ra,rd);
    printf("Le programme counter est maintenant à la valeur%lu\n",ra);
    rd = PC;//On garde dans rd la valeur actuel du register
    PC = regs[ra];//PC=3??
    printf("Le programme counter 1 est maintenant à la valeur%lu\n",ra);
}
void jumpi(){
    printf("jumpi r%d %d\n",rd,addr);
    printf("Le programme counter est ici avant le jump à la valeur%lu\n",PC);
    rd = PC;
    PC = addr;//PC=3??
    printf("Le programme counter est maintenant à la valeur%lu\n",addr);
}
//Puis viennent les branchements
void braz(){
    printf("braz  r%d %d",rs,addr);
    if (regs[rs]==0){
        PC = addr - 1;
        printf("Le branchement if a fonctionné\n");
        printf("On va maintenant aller à l'adresse du branchement, le programme counter revient à%d\n",PC);
    }
    else{
        printf("Le branchement if n'a pas fonctionné\n");
    }
}
void branz(){
    printf("branz ubdubdirucbe r%d %d\n",rs,addr);
    if (regs[rs]!=0){
        PC = addr - 1;
        printf("Le branchement if not a fonctionné\n");
        printf("On va maintenant aller à l'adresse du branchement, le programme counter revient à%d\n",PC);
    }
    else{
        printf("Branz ne fait rien car la condition n'est pas remplie\n");
    }
}
void scall(){
    int userInput;
    switch(n){
        case 0:
            printf("Input a number: ");
            scanf("%d", &userInput);
            write_register(20, userInput);
            break;
        case 1:
            printf("r20 est égal à %lu\n",regs[20]);
            break;
        case 3:
            printf("%c\n", regs[20] & 0x7f);
            break;
    }
    
}





int loop(){
    while(go_on){
        //ir = mem[PC];
        //déterminer le type de l'instruction
        
        IR = mem[PC];
        printf("mem %u = %lu\n", PC, IR);
        opcode = (IR >> 26) & 0x3f;
        printf("L'opcode est%d\n",opcode);

        if(opcode < 26)
        {
                if ((opcode & 1) == 0){//regarde si l'opcode est pair, s'il l'ait c'est une instruction de type R
                    decode_R_instruction(IR);
                    //printf("ggggg");
                }
                else{
                    decode_I_instruction(IR);
                    //printf("ffff");
                }

        }
        if (opcode ==30){
            //Cas du jump I
            decode_JR_instruction(IR);

        }
        if (opcode ==31){
            //Cas du jump I
            decode_JI_instruction(IR);

        }
        if((opcode ==27)||(opcode ==29)){
            //Cas du load immediate et du store
            decode_I_instruction(IR);
        }

        if((opcode == 32)||(opcode == 33)){
            decode_B_instruction(IR);
        }

        if((opcode == 34)){
            decode_scall_instruction(IR);
        }

        switch(opcode){

            case 2:
                add();
                break;
            case 3:
                addi();
                break;
            case 4:
                sub();
                break;
            case 5:
                subi();
                break;
            case 6:
                mul();
                break;
            case 7:
                muli();
                break;
            case 8:
                div_();
                break;
            case 9:
                divi();
                break;
            case 10:
                and();
                break;
            case 11:
                andi();
                break;
            case 12:
                or();
                break;
            case 13:
                ori();
                break;
            case 14:
                xor();
                break;
            case 15:
                xori();
                break;
            case 16:
                shl();
                break;
            case 17:
                shli();
                break;
            case 18:
                shr();
                break;
            case 19:
                shri();
                break;
            case 20:
                slt();
                break;
            case 21:
                slti();
                break;
            case 22:
                sle();
                break;
            case 23:
                slei();
                break;
            case 24:
                seq();
                break;
            case 25:
                seqi();
                break;
            case 27:
                load();
                break;
            case 28:
                store();
                break;
            case 29:
                store();
                break;
            case 30:
                jump();
                break;
            case 31:
                jumpi();
                break;
            case 32:
                braz();
                break;
            case 33:
                branz();
                break;
            case 34:
                scall();
            case 35:
                
                printf("INSTRUCTION STOP\n");
                go_on = 0;
                break;
            default:
                printf("Error: unknown opcode (%d)\n",opcode);
                go_on = 0;
                break;
        }
        print_regs();
        printf("PROGRAMME COUNTER PLACE %lu\n",PC);
        PC++;
    }


    return 0;
}