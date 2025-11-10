import re
import csv
import matplotlib.pyplot as plt

# -----------------------------
# Função para registrar módulos
# -----------------------------
def registrar_modulo(nome, largura, altura, nivel, pos_x, pos_y, writer):
    writer.writerow([nome, largura, altura, nivel, pos_x, pos_y])

# -----------------------------
# Função para desenhar bloco
# -----------------------------
def desenhar_bloco(ax, x, y, largura, altura, nome):
    rect = plt.Rectangle((x - largura / 2, y), largura, altura, fill=True, color="skyblue", ec="black")
    ax.add_patch(rect)
    ax.text(x, y + altura / 2, nome, ha='center', va='center', fontsize=8)

# -----------------------------
# Função principal recursiva
# -----------------------------
def interpretar_linhas(linhas, ax, writer, nivel=0, altura_atual=0, x=0):
    i = 0
    while i < len(linhas):
        linha = linhas[i].strip()
        if not linha:
            i += 1
            continue

        # BLOCO(nome, largura, altura)
        if linha.startswith("BLOCO"):
            info = re.findall(r'\((.*?)\)', linha)[0].split(',')
            nome = info[0].strip()
            largura = int(info[1])
            altura = int(info[2])
            desenhar_bloco(ax, x, altura_atual, largura, altura, nome)
            registrar_modulo(nome, largura, altura, nivel, x, altura_atual, writer)
            altura_atual += altura

        # TOPO(largura, altura)
        elif linha.startswith("TOPO"):
            info = re.findall(r'\((.*?)\)', linha)[0].split(',')
            nome = "TOPO"
            largura = int(info[0])
            altura = int(info[1])
            desenhar_bloco(ax, x, altura_atual, largura, altura, nome)
            registrar_modulo(nome, largura, altura, nivel, x, altura_atual, writer)
            altura_atual += altura

        # REPITA(N){...}
        elif linha.startswith("REPITA"):
            repeticoes = int(re.findall(r'REPITA\((\d+)\)', linha)[0])
            bloco_interno = []
            i += 1
            # Coleta o conteúdo entre { }
            while i < len(linhas) and not linhas[i].strip().startswith('}'):
                bloco_interno.append(linhas[i])
                i += 1
            # Recursão
            for _ in range(repeticoes):
                altura_atual = interpretar_linhas(bloco_interno, ax, writer, nivel + 1, altura_atual, x)

        i += 1

    return altura_atual


# -----------------------------
# Função principal
# -----------------------------
def main():
    with open("projeto.txt", "r", encoding="utf-8") as f:
        linhas = f.readlines()

    fig, ax = plt.subplots(figsize=(6, 8))
    ax.set_xlim(-150, 150)
    ax.set_ylim(0, 300)
    ax.set_aspect('equal')
    ax.set_title("Construção Modular")

    with open("log_construcao.csv", "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Nome", "Largura", "Altura", "Nivel", "Posição X", "Posição Y"])

        interpretar_linhas(linhas, ax, writer)

    plt.show()
    print("✅ Construção concluída! Arquivo 'log_construcao.csv' gerado com sucesso.")


if __name__ == "__main__":
    main()