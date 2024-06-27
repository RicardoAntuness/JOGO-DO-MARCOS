import pygame
import random
import os
from tkinter import simpledialog

# Henrique Ibiaçá e Ricardo Tupanci
pygame.init()

relogio = pygame.time.Clock()
icone = pygame.image.load("assets/marcos.png")
iron = pygame.image.load("assets/marcos.png")
fundo = pygame.image.load("assets/fundo.jpeg")
fundoStart = pygame.image.load("assets/fundoStart.jpg")
fundoDead = pygame.image.load("assets/fundoDead.jpg")

missel = pygame.image.load("assets/copodechopp.png")
controle = pygame.image.load("assets/controle.png")
controle = pygame.transform.scale(controle, (60, 30))
pizza = pygame.image.load("assets/pizza.png")

tamanho = (800, 600)
tela = pygame.display.set_mode(tamanho)
pygame.display.set_caption("Jogo do Marcão")
pygame.display.set_icon(icone)
missileSound = pygame.mixer.Sound("assets/somm.mp3")
explosaoSound = pygame.mixer.Sound("assets/derrota.mp3")
fonte = pygame.font.SysFont("comicsans", 28)
fonteStart = pygame.font.SysFont("comicsans", 55)
fonteMorte = pygame.font.SysFont("arial", 120)
pygame.mixer.music.load("assets/fundo.mp3")
petroski
branco = (255, 255, 255)
preto = (0, 0, 0)
azul = (0, 255, 255)

def jogar(nome):
    pygame.mixer.Sound.play(missileSound)
    pygame.mixer.music.play(-1)
    posicaoXPersona = 400
    posicaoYPersona = 300
    movimentoXPersona = 0
    movimentoYPersona = 0
    posicaoXMissel = 400
    posicaoYMissel = -240
    velocidadeMissel = 1
    posicaoXPizza = random.randint(0, 800)
    posicaoYPizza = -240
    velocidadePizza = 1
    pontos = 0
    larguraPersona = 91
    alturaPersona = 125
    larguaMissel = 50
    alturaMissel = 70
    larguraPizza = 50
    alturaPizza = 50
    dificuldade = 15
    raio = 20
    aumentando = True

    # Posição inicial e movimento do controle de videogame
    posicaoXControle = random.randint(0, tamanho[0] - 50)
    posicaoYControle = random.randint(0, tamanho[1] - 50)
    movimentoXControle = random.choice([-1, 1])
    movimentoYControle = random.choice([-1, 1])

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_RIGHT:
                movimentoXPersona = 10
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_LEFT:
                movimentoXPersona = -10
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_RIGHT:
                movimentoXPersona = 0
            elif evento.type == pygame.KEYUP and evento.key == pygame.K_LEFT:
                movimentoXPersona = 0

        posicaoXPersona = posicaoXPersona + movimentoXPersona

        if posicaoXPersona < 0:
            posicaoXPersona = 0
        elif posicaoXPersona > tamanho[0] - larguraPersona:
            posicaoXPersona = tamanho[0] - larguraPersona

        tela.fill(branco)
        tela.blit(fundo, (0, 0))
        tela.blit(iron, (posicaoXPersona, posicaoYPersona))

        posicaoYMissel = posicaoYMissel + velocidadeMissel
        if posicaoYMissel > 600:
            posicaoYMissel = -240
            pontos = pontos - 1
            velocidadeMissel = velocidadeMissel + 1
            posicaoXMissel = random.randint(0, 800)
            pygame.mixer.Sound.play(missileSound)

        tela.blit(missel, (posicaoXMissel, posicaoYMissel))

        posicaoYPizza = posicaoYPizza + velocidadePizza
        if posicaoYPizza > 600:
            posicaoYPizza = -240
            pontos = pontos - 1  # Reduz um ponto se a pizza passar
            posicaoXPizza = random.randint(0, 800)
            pygame.mixer.Sound.play(missileSound)

        tela.blit(pizza, (posicaoXPizza, posicaoYPizza))

        texto = fonte.render(nome + "- Pontos: " + str(pontos), True, branco)
        tela.blit(texto, (10, 10))

        pixelsPersonaX = list(range(posicaoXPersona, posicaoXPersona + larguraPersona))
        pixelsPersonaY = list(range(posicaoYPersona, posicaoYPersona + alturaPersona))
        pixelsMisselX = list(range(posicaoXMissel, posicaoXMissel + larguaMissel))
        pixelsMisselY = list(range(posicaoYMissel, posicaoYMissel + alturaMissel))
        pixelsPizzaX = list(range(posicaoXPizza, posicaoXPizza + larguraPizza))
        pixelsPizzaY = list(range(posicaoYPizza, posicaoYPizza + alturaPizza))

        if len(list(set(pixelsMisselY).intersection(set(pixelsPersonaY)))) > dificuldade:
            if len(list(set(pixelsMisselX).intersection(set(pixelsPersonaX)))) > dificuldade:
                pontos = pontos + 1
                posicaoYMissel = -240
                velocidadeMissel = velocidadeMissel + 1
                posicaoXMissel = random.randint(0, 800)

        if len(list(set(pixelsPizzaY).intersection(set(pixelsPersonaY)))) > dificuldade:
            if len(list(set(pixelsPizzaX).intersection(set(pixelsPersonaX)))) > dificuldade:
                pontos = pontos + 1
                posicaoYPizza = -240
                velocidadePizza = velocidadePizza + 1
                posicaoXPizza = random.randint(0, 800)

        if pontos < 0:
            dead(nome, pontos)

        # Atualizar a posição do controle de videogame
        posicaoXControle += movimentoXControle
        posicaoYControle += movimentoYControle

        # Verificar limites da tela para o controle
        if posicaoXControle <= 0 or posicaoXControle >= tamanho[0] - 50:
            movimentoXControle = -movimentoXControle
        if posicaoYControle <= 0 or posicaoYControle >= tamanho[1] - 50:
            movimentoYControle = -movimentoYControle

        # Desenhar o controle de videogame
        tela.blit(controle, (posicaoXControle, posicaoYControle))

        # Desenhar o círculo neon azul no canto superior direito
        pygame.draw.circle(tela, azul, (750, 50), raio)
        if aumentando:
            raio += 0.15
            if raio >=40:
                aumentando = False
        else:
            raio -= 0.15
            if raio <=10:
                aumentando = True

        pygame.display.update()
        relogio.tick(60)


def dead(nome, pontos):
    pygame.mixer.music.stop()
    pygame.mixer.Sound.play(explosaoSound)

    jogadas = {}
    try:
        arquivo = open("historico.txt", "r", encoding="utf-8")
        jogadas = eval(arquivo.read())
        arquivo.close()
    except:
        arquivo = open("historico.txt", "w", encoding="utf-8")
        arquivo.close()

    jogadas[nome] = pontos
    arquivo = open("historico.txt", "w", encoding="utf-8")
    arquivo.write(str(jogadas))
    arquivo.close()

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.KEYDOWN and evento.key == pygame.K_RETURN:
                jogar(nome)

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if buttonStart.collidepoint(evento.pos):
                    jogar(nome)
        tela.fill(branco)
        tela.blit(fundoDead, (0, 0))
        buttonStart = pygame.draw.rect(tela, preto, (35, 482, 750, 100), 0)
        textoStart = fonteStart.render("RESTART", True, branco)
        tela.blit(textoStart, (400, 482))
        textoEnter = fonte.render("Press enter to continue...", True, branco)
        tela.blit(textoEnter, (60, 482))


        pygame.display.update()
        relogio.tick(60)


def ranking():
    estrelas = {}
    try:
        arquivo = open("historico.txt", "r", encoding="utf-8")
        estrelas = eval(arquivo.read())
        arquivo.close()
    except:
        pass

    nomes = sorted(estrelas, key=estrelas.get, reverse=True)
    print(estrelas)
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if buttonStart.collidepoint(evento.pos):
                    start()

        tela.fill(preto)
        buttonStart = pygame.draw.rect(tela, preto, (35, 482, 750, 100), 0)
        textoStart = fonteStart.render("BACK TO START", True, branco)
        tela.blit(textoStart, (330, 482))

        posicaoY = 50
        for key, nome in enumerate(nomes):
            if key == 13:
                break
            textoJogador = fonte.render(nome + " - " + str(estrelas[nome]), True, branco)
            tela.blit(textoJogador, (300, posicaoY))
            posicaoY = posicaoY + 30

        pygame.display.update()
        relogio.tick(60)


def start():
    nome = simpledialog.askstring("JOGO DO MARCÃOA", "Nome Completo:")

    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                quit()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if buttonStart.collidepoint(evento.pos):
                    jogar(nome)
                elif buttonRanking.collidepoint(evento.pos):
                    ranking()

        tela.fill(branco)
        tela.blit(fundoStart, (0, 0))
        buttonStart = pygame.draw.rect(tela, preto, (35, 482, 750, 100), 0)
        buttonRanking = pygame.draw.rect(tela, preto, (35, 50, 200, 50), 0, 30)
        textoRanking = fonte.render("Ranking", True, branco)
        tela.blit(textoRanking, (90, 50))
        textoStart = fonteStart.render("START", True, branco)
        tela.blit(textoStart, (330, 482))

        pygame.display.update()
        relogio.tick(60)


start()