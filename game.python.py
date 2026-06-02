import pygame
import random
import sys

# Inicializar Pygame
pygame.init()

# Dimensiones de la ventana

ANCHO = 800
ALTO = 600
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption(" Space Shooter")

# Colores
NEGRO = (0, 0, 0)
BLANCO = (255, 255, 255)
ROJO = (255, 0, 0)

# FPS
FPS = 60
clock = pygame.time.Clock()

# Cargar imágenes 
nave_img = pygame.Surface((50, 40))
nave_img.fill((0, 255, 255))

meteorito_img = pygame.Surface((40, 40))
meteorito_img.fill((255, 100, 0))

bala_img = pygame.Surface((5, 10))
bala_img.fill((255, 255, 0))

# Clases del juego
class Nave(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = nave_img
        self.rect = self.image.get_rect()
        self.rect.centerx = ANCHO // 2
        self.rect.bottom = ALTO - 10
        self.velocidad = 5

    def update(self):
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocidad
        if teclas[pygame.K_RIGHT] and self.rect.right < ANCHO:
            self.rect.x += self.velocidad

    def disparar(self):
        bala = Bala(self.rect.centerx, self.rect.top)
        todas_sprites.add(bala)
        balas.add(bala)

class Meteorito(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = meteorito_img
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, ANCHO - self.rect.width)
        self.rect.y = random.randint(-100, -40)
        self.velocidady = random.randint(3, 8)

    def update(self):
        self.rect.y += self.velocidady
        if self.rect.top > ALTO:
            self.rect.x = random.randint(0, ANCHO - self.rect.width)
            self.rect.y = random.randint(-100, -40)
            self.velocidady = random.randint(3, 8)

class Bala(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bala_img
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.velocidady = -10

    def update(self):
        self.rect.y += self.velocidady
        if self.rect.bottom < 0:
            self.kill()
# Grupos de sprites
todas_sprites = pygame.sprite.Group()
meteoritos = pygame.sprite.Group()
balas = pygame.sprite.Group()

# NUEVO: Función para reiniciar el juego
def reiniciar_juego():
    global puntaje, nave
    puntaje = 0
    # Vaciar los grupos de sprites
    todas_sprites.empty()
    meteoritos.empty()
    balas.empty()
    
    # Recrear la nave
    nave = Nave()
    todas_sprites.add(nave)
    
    # Recrear los meteoritos
    for i in range(8):
        meteorito = Meteorito()
        todas_sprites.add(meteorito)
        meteoritos.add(meteorito)

# Iniciar por primera vez
reiniciar_juego()

# NUEVO: Control de estados del juego
ejecutando = True # Controla si la ventana está abierta
jugando = True    # Controla si estamos en la partida o en la pantalla de Game Over

while ejecutando:
    clock.tick(FPS)
    
    # --- Eventos ---
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
            
        # Controles si estamos jugando
        if jugando:
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE:
                    nave.disparar()
                    
        # Controles si estamos en Game Over (esperando clic)
        else:
            if evento.type == pygame.MOUSEBUTTONDOWN:
                # Obtener posición del mouse
                mouse_pos = pygame.mouse.get_pos()
                # Verificar si el clic fue dentro del botón
                if boton_rect.collidepoint(mouse_pos):
                    reiniciar_juego()
                    jugando = True

    # --- Lógica y Dibujo dependiendo del estado ---
    if jugando:
        # Actualizar
        todas_sprites.update()

        # Colisiones bala - meteorito
        impactos = pygame.sprite.groupcollide(meteoritos, balas, True, True)
        for impacto in impactos:
            puntaje += 10
            nuevo_meteorito = Meteorito()
            todas_sprites.add(nuevo_meteorito)
            meteoritos.add(nuevo_meteorito)

        # Colisiones nave - meteorito
        colision = pygame.sprite.spritecollideany(nave, meteoritos)
        if colision:
            jugando = False # Cambiamos el estado a Game Over

        # Dibujar Juego
        VENTANA.fill(NEGRO)
        todas_sprites.draw(VENTANA)

        # Mostrar puntaje
        fuente = pygame.font.SysFont(None, 36)
        texto = fuente.render(f"Puntaje: {puntaje}", True, BLANCO)
        VENTANA.blit(texto, (10, 10))

    else:
        # Dibujar pantalla de GAME OVER
        VENTANA.fill(NEGRO)
        fuente_final = pygame.font.SysFont(None, 64)
        texto_final = fuente_final.render(f"GAME OVER", True, ROJO)
        texto_puntaje = fuente.render(f"Puntaje Final: {puntaje}", True, BLANCO)
        
        # Coordenadas de los textos
        VENTANA.blit(texto_final, (ANCHO//2 - 140, ALTO//2 - 100))
        VENTANA.blit(texto_puntaje, (ANCHO//2 - 100, ALTO//2 - 30))
        
        # NUEVO: Dibujar el botón
        # pygame.Rect(x, y, ancho, alto)
        boton_rect = pygame.Rect(ANCHO//2 - 100, ALTO//2 + 50, 200, 50)
        pygame.draw.rect(VENTANA, VERDE, boton_rect)
        
        # Texto del botón
        fuente_boton = pygame.font.SysFont(None, 36)
        texto_boton = fuente_boton.render("Reintentar", True, NEGRO)
        VENTANA.blit(texto_boton, (ANCHO//2 - 60, ALTO//2 + 62))

    # Actualizar pantalla
    pygame.display.flip()

pygame.quit()
sys.exit()