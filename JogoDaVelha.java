import java.util.Scanner;

public class JogoDaVelha {
    private static char[][] tabuleiro = {
        {'-', '-', '-'},
        {'-', '-', '-'},
        {'-', '-', '-'}
    };
    private static char jogadorAtual = 'X';

    public static void main(String[] args) {
        Scanner scanner = new Scanner(System.in);
        boolean jogoAtivo = true;

        while (jogoAtivo) {
            imprimirTabuleiro();
            System.out.println("Jogador " + jogadorAtual + ", insira a linha e a coluna (0, 1, ou 2):");
            int linha = scanner.nextInt();
            int coluna = scanner.nextInt();

            if (linha < 0 || linha > 2 || coluna < 0 || coluna > 2 || tabuleiro[linha][coluna] != '-') {
                System.out.println("Movimento inválido, tente novamente.");
                continue;
            }

            tabuleiro[linha][coluna] = jogadorAtual;

            if (verificarVitoria()) {
                imprimirTabuleiro();
                System.out.println("Parabéns! Jogador " + jogadorAtual + " venceu!");
                jogoAtivo = false;
                break;
            }

            if (verificarEmpate()) {
                imprimirTabuleiro();
                System.out.println("O jogo terminou em empate!");
                jogoAtivo = false;
                break;
            }

            jogadorAtual = (jogadorAtual == 'X') ? 'O' : 'X';
        }

        System.out.println("Deseja jogar novamente? (s/n)");
        char resposta = scanner.next().charAt(0);
        if (resposta == 's' || resposta == 'S') {
            reiniciarJogo();
            main(null);
        } else {
            System.out.println("Obrigado por jogar!");
        }

        scanner.close();
    }

    private static void imprimirTabuleiro() {
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                System.out.print(tabuleiro[i][j] + " ");
            }
            System.out.println();
        }
    }

    private static boolean verificarVitoria() {
        for (int i = 0; i < 3; i++) {
            if (tabuleiro[i][0] == jogadorAtual && tabuleiro[i][1] == jogadorAtual && tabuleiro[i][2] == jogadorAtual) {
                return true;
            }
            if (tabuleiro[0][i] == jogadorAtual && tabuleiro[1][i] == jogadorAtual && tabuleiro[2][i] == jogadorAtual) {
                return true;
            }
        }
        if (tabuleiro[0][0] == jogadorAtual && tabuleiro[1][1] == jogadorAtual && tabuleiro[2][2] == jogadorAtual) {
            return true;
        }
        if (tabuleiro[0][2] == jogadorAtual && tabuleiro[1][1] == jogadorAtual && tabuleiro[2][0] == jogadorAtual) {
            return true;
        }
        return false;
    }

    private static boolean verificarEmpate() {
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                if (tabuleiro[i][j] == '-') {
                    return false;
                }
            }
        }
        return true;
    }

    private static void reiniciarJogo() {
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                tabuleiro[i][j] = '-';
            }
        }
        jogadorAtual = 'X';
    }
}
