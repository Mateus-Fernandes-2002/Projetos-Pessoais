#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <locale.h>

#define MAX 100
struct ingresso {
    char nome[50];
    char cpf[15];
    int ano_nasc;
};


struct ingresso ingressos[MAX];


int contador = 0;


void vender_ingresso();
void listar_ingressos();
void validar_ingresso();
void sair();


int main() {
   
    setlocale(LC_ALL, "Portuguese");

    
    int opcao;

    
    while (1) {
        
        system("cls");

        
        printf("Sistema de venda de ingressos\n");
        printf("Escolha uma opcao:\n");
        printf("1 - Vender ingresso\n");
        printf("2 - Listar ingressos vendidos\n");
        printf("3 - Validar ingresso\n");
        printf("4 - Sair\n");

        
        scanf("%d", &opcao);

       
        switch (opcao) {
            case 1:
                vender_ingresso();
                break;
            case 2:
                listar_ingressos();
                break;
            case 3:
                validar_ingresso();
                break;
            case 4:
                sair();
                break;
            default:
                printf("Opcao invalida!\n");
                system("pause");
                break;
        }
    }

    return 0;
}


void vender_ingresso() {
    
    if (contador < MAX) {
        
        system("cls");

        
        printf("Vender ingresso\n");

        
        printf("Digite o nome do comprador: ");
        fflush(stdin);
        gets(ingressos[contador].nome);
        printf("Digite o CPF do comprador: ");
        fflush(stdin);
        gets(ingressos[contador].cpf);
        printf("Digite o ano de nascimento do comprador: ");
        scanf("%d", &ingressos[contador].ano_nasc);

        
        contador++;

        
        printf("Ingresso vendido com sucesso!\n");
        system("pause");
    }
    else {
       
        printf("Nao ha mais ingressos disponiveis!\n");
        system("pause");
    }
}


void listar_ingressos() {
    
    if (contador > 0) {
        
        system("cls");

        
        printf("Listar ingressos vendidos\n");

       
        int i;

        
        for (i = 0; i < contador; i++) {
            printf("Nome: %s\n", ingressos[i].nome);
            printf("CPF: %s\n", ingressos[i].cpf);
            printf("Ano de nascimento: %d\n", ingressos[i].ano_nasc);
            printf("===============================\n");
        }

        
        system("pause");
    }
    else {
        
        printf("Nao ha ingressos vendidos!\n");
        system("pause");
    }
}


void validar_ingresso() {
    
    if (contador > 0) {
        
        system("cls");

        
        printf("Validar ingresso\n");

        
        char cpf[15];

        
        printf("Digite o CPF do comprador: ");
        fflush(stdin);
        gets(cpf);

        
        int i;

        
        int encontrado = 0;

        
        for (i = 0; i < contador; i++) {
            
            if (strcmp(cpf, ingressos[i].cpf) == 0) {
                
                printf("Ingresso valido!\n");
                printf("Nome: %s\n", ingressos[i].nome);
                printf("CPF: %s\n", ingressos[i].cpf);
                printf("Ano de nascimento: %d\n", ingressos[i].ano_nasc);
                printf("===============================\n");

                
                encontrado = 1;

                
                break;
            }
        }

  
        if (encontrado == 0) {
  
            printf("Ingresso invalido!\n");
            printf("CPF nao cadastrado!\n");
            printf("===============================\n");
        }

       
        system("pause");
    }
    else {
    
         printf("Nao ha ingressos vendidos!\n");
         system("pause");
    }
}


void sair() {
 
    system("cls");


    printf("Obrigado por usar o sistema de venda de ingressos!\n");
    printf("Ate mais!\n");


    exit(0);
}
