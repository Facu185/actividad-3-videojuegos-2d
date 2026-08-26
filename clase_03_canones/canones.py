import math
import sys
import pygame

pygame.init()
ANCHO, ALTO = 900, 600
pantalla = pygame.display.set_mode((ANCHO, ALTO))
reloj = pygame.time.Clock()

GRAVEDAD = 0.25
POTENCIA = 22
origen = (90, ALTO - 30)  # posición del cañón
balas = []  # cada bala es un dict: x, y, vx, vy
blancos = [{"x": x, "ancho": 60, "alto": 40} for x in range(350, 850, 90)]
puntos = 0
ganaste = False


def disparar(angulo):
    rad = math.radians(angulo)
    vx = POTENCIA * math.cos(rad)
    vy = -POTENCIA * math.sin(rad)
    balas.append({"x": origen[0], "y": origen[1], "vx": vx, "vy": vy})


fuente = pygame.font.SysFont(None, 72)

ejecutando = True
while ejecutando:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if not ganaste:
                disparar(angulo)

    mx, my = pygame.mouse.get_pos()
    angulo = math.degrees(math.atan2(origen[1] - my, mx - origen[0]))

    # Física de cada bala
    for b in balas:
        b["x"] += b["vx"]
        b["y"] += b["vy"]
        b["vy"] += GRAVEDAD
        if b["y"] > ALTO - 10:  # rebote en el piso
            b["vy"] *= -0.7
            b["y"] = ALTO - 10

    # Detección de impacto: bala contra blanco
    for b in balas[:]:
        for blanco in blancos[:]:
            if (blanco["x"] <= b["x"] <= blanco["x"] + blanco["ancho"] and
                    ALTO - 90 <= b["y"] <= ALTO - 90 + blanco["alto"]):
                blancos.remove(blanco)
                balas.remove(b)
                puntos += 10
                break

    if not blancos:
        ganaste = True

    # Dibujar
    pantalla.fill((25, 25, 45))
    pygame.draw.rect(pantalla, (80, 220, 120), (0, ALTO - 10, ANCHO, 10))
    for blanco in blancos:
        pygame.draw.rect(pantalla, (220, 80, 80),
                          (blanco["x"], ALTO - 90, blanco["ancho"], blanco["alto"]))

    rad = math.radians(angulo)
    pygame.draw.line(pantalla, (240, 200, 60), origen,
                      (origen[0] + 60 * math.cos(rad),
                       origen[1] - 60 * math.sin(rad)), 6)

    for b in balas:
        pygame.draw.circle(pantalla, (240, 240, 240),
                            (int(b["x"]), int(b["y"])), 8)

    if ganaste:
        texto = fuente.render("Ganaste", True, (255, 220, 60))
        rect = texto.get_rect(center=(ANCHO // 2, ALTO // 2))
        pantalla.blit(texto, rect)

    pygame.display.set_caption(f"Cañones - Puntos: {puntos}")
    pygame.display.flip()
    reloj.tick(60)

pygame.quit()
sys.exit()
