# DONKEY KONG REBUILD IN PYTHON WITH THE PYGAME MODULE! (Est.720 Lines of Code)
import os
import random

import pygame

os.environ["SDL_VIDEO_CENTERED"] = "1"  # call before pygame.init()
pygame.init()
pygame.mixer.init()
info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h
window_width, window_height = screen_width - 800, screen_height - 150

timer = pygame.time.Clock()
fps = 60


pygame.display.set_caption("Classic Donkey Kong Rebuild!")
# pygame.display.set_icon('image file')

font = pygame.font.Font("freesansbold.ttf", 50)
font2 = pygame.font.Font("freesansbold.ttf", 30)

screen = pygame.display.set_mode([window_width, window_height])
section_width = window_width // 32
section_height = window_height // 32
slope = section_height // 8

# Dificuldade por nível: [barrel_spawn_time, max_flames_inicial]
level_difficulty = [
    {"barrel_spawn": 360, "initial_flames": 1},  # Fase 1
    {"barrel_spawn": 200, "initial_flames": 3},  # Fase 2 (mais difícil)
]
barrel_spawn_time = level_difficulty[0]["barrel_spawn"]
barrel_count = barrel_spawn_time / 2
barrel_time = barrel_spawn_time
barrel_img = pygame.transform.scale(
    pygame.image.load("assets/images/barrels/barrel.png"),
    (int(section_width * 1.5), section_height * 2),
)
# flames_img = pygame.transform.scale(pygame.image.load('assets/images/fire.png'),
#                                     (section_width * 2, section_height))
# ...existing code...
fornalha_repouso = pygame.image.load("assets/images/fornace/fornalha1.png")
fornalha_repouso = pygame.transform.scale(
    fornalha_repouso, (section_width * 3, int(section_height * 3.5))
)

fornalha_ativa = pygame.image.load("assets/images/fornace/fornalha2.png")
fornalha_ativa = pygame.transform.scale(
    fornalha_ativa, (section_width * 3, int(section_height * 3.5))
)

fornalha_atual = fornalha_repouso
timer_fornalha = 0
# ...existing code...

# Carrega as imagens das plataformas (fase 1 e fase 2)
try:
    platform_img = pygame.image.load("assets/images/platforms/platform.png")
    platform_img = pygame.transform.scale(platform_img, (section_width, section_height))
    use_platform_image = True
except Exception:
    use_platform_image = False
    print("Aviso: Imagem da plataforma não encontrada. Usando desenho de linhas.")

try:
    platform2_img = pygame.image.load("assets/images/platforms/platform2.png")
    platform2_img = pygame.transform.scale(
        platform2_img, (section_width, section_height)
    )
    use_platform2_image = True
except Exception:
    platform2_img = platform_img if use_platform_image else None
    use_platform2_image = use_platform_image
    print(
        "Aviso: Imagem 'platform2.png' não encontrada. Usando platform.png como fallback."
    )

barrel_side = pygame.transform.scale(
    pygame.image.load("assets/images/barrels/barrel.png"),
    (section_width * 2, int(section_height * 2.5)),
)
dk1 = pygame.transform.scale(
    pygame.image.load("assets/images/dk/dk1.png"),
    (section_width * 5, section_height * 5),
)
dk2 = pygame.transform.scale(
    pygame.image.load("assets/images/dk/dk2.png"),
    (section_width * 5, section_height * 5),
)
dk3 = pygame.transform.scale(
    pygame.image.load("assets/images/dk/dk3.png"),
    (section_width * 5, section_height * 5),
)
dk4 = pygame.transform.scale(
    pygame.image.load("assets/images/dk/dk4.png"),
    (section_width * 5, section_height * 5),
)
dk5 = pygame.transform.scale(
    pygame.image.load("assets/images/dk/dk5.png"),
    (section_width * 5, section_height * 5),
)
dk6 = pygame.transform.scale(
    pygame.image.load("assets/images/dk/dk6.png"),
    (section_width * 5, section_height * 5),
)
dk7 = pygame.transform.scale(
    pygame.image.load("assets/images/dk/dk7.png"),
    (section_width * 5, section_height * 5),
)
# ── Goblin sprites ───────────────────────────────────────────────────────────
try:
    _goblin_idle_orig = pygame.image.load("assets/images/goblin/goblin-walk.png").convert_alpha()
    _goblin_idle_orig.set_colorkey((255, 255, 255))
    goblin_idle_img = pygame.transform.scale(
        _goblin_idle_orig,
        (int(section_width * 2.5), int(section_height * 3)),
    )
    
    _goblin_walk1_orig = pygame.image.load("assets/images/goblin/goblin-walk1.png").convert_alpha()
    _goblin_walk1_orig.set_colorkey((255, 255, 255))
    goblin_walk1_img = pygame.transform.scale(
        _goblin_walk1_orig,
        (int(section_width * 2.5), int(section_height * 3)),
    )

    _goblin_walk2_orig = pygame.image.load("assets/images/goblin/goblin-walk2.png").convert_alpha()
    _goblin_walk2_orig.set_colorkey((255, 255, 255))
    goblin_walk2_img = pygame.transform.scale(
        _goblin_walk2_orig,
        (int(section_width * 2.5), int(section_height * 3)),
    )

    _goblin_throw_orig = pygame.image.load("assets/images/goblin/goblin_throw.png").convert_alpha()
    _goblin_throw_orig.set_colorkey((255, 255, 255))
    goblin_throw_img = pygame.transform.scale(
        _goblin_throw_orig,
        (int(section_width * 2.5), int(section_height * 3)),
    )

    _spear_orig = pygame.image.load("assets/images/goblin/spear.png").convert_alpha()
    _spear_orig.set_colorkey((255, 255, 255))
    spear_img = pygame.transform.scale(
        _spear_orig,
        (int(section_width * 3.6), int(section_height * 0.72)),
    )
    use_goblin = True
except Exception as _e:
    goblin_idle_img = goblin_walk1_img = goblin_walk2_img = goblin_throw_img = spear_img = None
    use_goblin = False
    print(f"Aviso: imagens do goblin não encontradas: {_e}")

# ── Backgounds ───────────────────────────────────────────────────────────────
try:
    bg1_img = pygame.transform.scale(
        pygame.image.load("assets/images/back-ground.png"), (window_width, window_height)
    )
    bg2_img = pygame.transform.scale(
        pygame.image.load("assets/images/back-ground1.png"), (window_width, window_height)
    )
    use_bg = True
except Exception as _e:
    bg1_img = bg2_img = None
    use_bg = False
    print(f"Aviso: imagens de background não encontradas: {_e}")

peach1 = pygame.transform.scale(
    pygame.image.load("assets/images/peach/peach1.png"),
    (2 * section_width, 3 * section_height),
)
peach2 = pygame.transform.scale(
    pygame.image.load("assets/images/peach/peach2.png"),
    (2 * section_width, 3 * section_height),
)
fireball = pygame.transform.scale(
    pygame.image.load("assets/images/fireball.png"),
    (int(1.5 * section_width), section_height * 2),
)
fireball2 = pygame.transform.scale(
    pygame.image.load("assets/images/fireball2.png"),
    (int(1.5 * section_width), section_height * 2),
)
hammer = pygame.transform.scale(
    pygame.image.load("assets/images/hammer.png"),
    (2 * section_width, 2 * section_height),
)
standing = pygame.transform.scale(
    pygame.image.load("assets/images/personagem/standing.png"),
    (section_width * 2, int(section_height * 2.5)),
)
jumping = pygame.transform.scale(
    pygame.image.load("assets/images/personagem/jumping.png"),
    (section_width * 2, int(section_height * 2.5)),
)
running = pygame.transform.scale(
    pygame.image.load("assets/images/personagem/running.png"),
    (section_width * 2, int(section_height * 2.5)),
)
climbing1 = pygame.transform.scale(
    pygame.image.load("assets/images/personagem/climbing1.png"),
    (section_width * 2, int(section_height * 2.5)),
)
climbing2 = pygame.transform.scale(
    pygame.image.load("assets/images/personagem/climbing2.png"),
    (section_width * 2, int(section_height * 2.5)),
)
hammer_stand = pygame.transform.scale(
    pygame.image.load("assets/images/personagem/hammer_stand.png"),
    (int(section_width * 2.5), int(section_height * 2.5)),
)
hammer_jump = pygame.transform.scale(
    pygame.image.load("assets/images/personagem/hammer_jump.png"),
    (int(section_width * 2.5), int(section_height * 2.5)),
)
hammer_overhead = pygame.transform.scale(
    pygame.image.load("assets/images/personagem/hammer_overhead.png"),
    (int(section_width * 2.5), int(section_height * 3.5)),
)

# Carregar som do martelo
try:
    hammer_sound = pygame.mixer.Sound("assets/sounds/marretada-do-galego.mp3")
except Exception:
    hammer_sound = None
    print("Aviso: Arquivo de áudio 'marretada-do-galego.mp3' não encontrado.")

# Carregar som do barril
try:
    barrel_sound = pygame.mixer.Sound("assets/sounds/bowler.mp3")
except Exception:
    barrel_sound = None
    print("Aviso: Arquivo de áudio 'bowler.mp3' não encontrado.")

# Carregar som de introdução
try:
    intro_sound = pygame.mixer.Sound("assets/sounds/intro-clash-royale.mp3")
except Exception:
    intro_sound = None
    print("Aviso: Arquivo de áudio 'intro-clash-royale.mp3' não encontrado.")

# Carregar imagem da tela inicial
try:
    start_screen_img = pygame.image.load("assets/images/tela-jogo.png")
    start_screen_img = pygame.transform.scale(
        start_screen_img, (window_width, window_height)
    )
    use_start_screen = True
except Exception:
    use_start_screen = False
    print("Aviso: Imagem 'tela-jogo.png' não encontrada. Usando tela inicial padrão.")


start_y = window_height - 2 * section_height
row2_y = start_y - 4 * section_height
row3_y = row2_y - 7 * slope - 3 * section_height
row4_y = row3_y - 4 * section_height
row5_y = row4_y - 7 * slope - 3 * section_height
row6_y = row5_y - 4 * section_height
row6_top = row6_y - 4 * slope
row5_top = row5_y - 8 * slope
row4_top = row4_y - 8 * slope
row3_top = row3_y - 8 * slope
row2_top = row2_y - 8 * slope
row1_top = start_y - 5 * slope
fireball_trigger = False
active_level = 0
counter = 0
score = 0
high_score = 0
lives = 3
bonus = 6000
first_fireball_trigger = False
victory = False
reset_game = False
game_started = False  # Controle da tela inicial
intro_played = False  # Controle para tocar intro apenas uma vez
levels = [
    # ==================== FASE 1 ====================
    {
        "bridges": [
            (1, start_y, 15),
            (16, start_y - slope, 3),
            (19, start_y - 2 * slope, 3),
            (22, start_y - 3 * slope, 3),
            (25, start_y - 4 * slope, 3),
            (28, start_y - 5 * slope, 3),
            (25, row2_y, 3),
            (22, row2_y - slope, 3),
            (19, row2_y - 2 * slope, 3),
            (16, row2_y - 3 * slope, 3),
            (13, row2_y - 4 * slope, 3),
            (10, row2_y - 5 * slope, 3),
            (7, row2_y - 6 * slope, 3),
            (4, row2_y - 7 * slope, 3),
            (2, row2_y - 8 * slope, 2),
            (4, row3_y, 3),
            (7, row3_y - slope, 3),
            (10, row3_y - 2 * slope, 3),
            (13, row3_y - 3 * slope, 3),
            (16, row3_y - 4 * slope, 3),
            (19, row3_y - 5 * slope, 3),
            (22, row3_y - 6 * slope, 3),
            (25, row3_y - 7 * slope, 3),
            (28, row3_y - 8 * slope, 2),
            (25, row4_y, 3),
            (22, row4_y - slope, 3),
            (19, row4_y - 2 * slope, 3),
            (16, row4_y - 3 * slope, 3),
            (13, row4_y - 4 * slope, 3),
            (10, row4_y - 5 * slope, 3),
            (7, row4_y - 6 * slope, 3),
            (4, row4_y - 7 * slope, 3),
            (2, row4_y - 8 * slope, 2),
            (4, row5_y, 3),
            (7, row5_y - slope, 3),
            (10, row5_y - 2 * slope, 3),
            (13, row5_y - 3 * slope, 3),
            (16, row5_y - 4 * slope, 3),
            (19, row5_y - 5 * slope, 3),
            (22, row5_y - 6 * slope, 3),
            (25, row5_y - 7 * slope, 3),
            (28, row5_y - 8 * slope, 2),
            (25, row6_y, 3),
            (22, row6_y - slope, 3),
            (19, row6_y - 2 * slope, 3),
            (16, row6_y - 3 * slope, 3),
            (2, row6_y - 4 * slope, 14),
            (13, row6_y - 4 * section_height, 6),
            (10, row6_y - 3 * section_height, 3),
        ],
        "ladders": [
            (12, row2_y + 6 * slope, 2),
            (12, row2_y + 26 * slope, 2),
            (25, row2_y + 11 * slope, 4),
            (6, row3_y + 11 * slope, 3),
            (14, row3_y + 8 * slope, 4),
            (10, row4_y + 6 * slope, 1),
            (10, row4_y + 24 * slope, 2),
            (16, row4_y + 6 * slope, 5),
            (25, row4_y + 9 * slope, 4),
            (6, row5_y + 11 * slope, 3),
            (11, row5_y + 8 * slope, 4),
            (23, row5_y + 4 * slope, 1),
            (23, row5_y + 24 * slope, 2),
            (25, row6_y + 9 * slope, 4),
            (13, row6_y + 5 * slope, 2),
            (13, row6_y + 25 * slope, 2),
            (18, row6_y - 27 * slope, 4),
            (12, row6_y - 17 * slope, 2),
            (10, row6_y - 17 * slope, 2),
            (12, -5, 13),
            (10, -5, 13),
        ],
        "hammers": [
            (4, row6_top + section_height + 30),
            (4, row4_top + section_height + 40),
        ],
        "target": (13, row6_y - 4 * section_height, 3),
    },
    # ==================== FASE 2 ====================
    # Layout inspirado no dk2.png: plataformas HORIZONTAIS (sem inclinação),
    # com 5 andares, escadas mais esparsas e caminhos mais desafiadores.
    {
        "bridges": [
            # Chão / andar térreo
            (1, start_y, 30),
            # Andar 2 – esquerda separada | centro + direita UNIDAS (circulo azul)
            (1, row2_y, 10),
            (14, row2_y, 16),
            # Andar 3 – esquerda+centro UNIDAS (circulo azul) | direita separada
            (3, row3_y, 17),
            (24, row3_y, 6),
            # Andar 4 – esquerda separada | centro+direita UNIDAS (circulo azul)
            (1, row4_y, 12),
            (17, row4_y, 13),
            # Andar 5 – esquerda separada | centro+direita UNIDAS (circulo azul)
            (5, row5_y, 6),
            (14, row5_y, 15),
            # Topo – plataforma do DK e da Pauline
            (2, row6_y - 4 * slope, 26),
            (2, row6_y - 4 * section_height, 26),
        ],
        "ladders": [
            # y_pos = row_X + section_height + section_height//2
            # → body top fica meio bloco ABAIXO da plataforma → sem overshoot
            # ----- Chão para Andar 2 -----
            (15, row2_y + section_height + section_height // 6, 5),
            # (25) → quebrada (círculo 4)
            # ----- Andar 2 para Andar 3 -----
            (17, row3_y + section_height + section_height // 6, 5),
            (27, row3_y + section_height + section_height // 6, 5),
            # ----- Andar 3 para Andar 4 -----
            (8, row4_y + section_height + section_height // 6, 5),
            (25, row4_y + section_height + section_height // 6, 5),
            # ----- Andar 4 para Andar 5 -----
            (6, row5_y + section_height + section_height // 6, 5),
            # (18) → quebrada (círculo 3)
            (26, row5_y + section_height + section_height // 6, 5),

            # ----- Andar 5 para Topo DK -----
            # (8) → quebrada (círculo 2)
            (
                16,
                row6_y - 4 * slope + section_height + section_height // 2,
                5,
            ),  # círculo 1
            # ----- Topo DK para Pauline (WIN) -----
            (10, row6_y - 4 * section_height + section_height + section_height // 2, 5),
            (20, row6_y - 4 * section_height + section_height + section_height // 2, 5),
        ],
        "broken_ladders": [
            # círculo 2 – escada quebrada onde estava a única subida para o DK
            (8, row6_y - 4 * slope + section_height, 5),
            # círculo 3 – escada quebrada entre andar 4 e andar 5 (centro)
            (18, row5_y + section_height, 5),
            # círculo 4 – escada quebrada chão→andar 2 (direita)
            (25, row2_y + section_height, 5),
            # círculo 5 – escada quebrada andar 2→3 (esquerda)
            (6, row3_y + section_height, 5),
        ],
        "hammers": [
            # Martelos em posições diferentes da fase 1
            (23, row5_top + section_height + 30),
            (2, row3_top + section_height + 40),
            # Martelo na plataforma do DK (para a batalha)
            (14, row6_y - 4 * section_height + section_height + 10),
        ],
        "goblins": [
            # (x_section, platform_y, patrol_left_section, patrol_right_section)
            (26, row6_y - 4 * slope, 22, 27),  # topo direito – plataforma DK
            (3, row3_y, 3, 9),  # esquerda – plataforma row3
            (26, row4_y, 23, 28),  # direita   – plataforma row4
        ],
        "blocked_ladders": [8, 9],  # escadas bloqueadas até derrotar o DK
        "target": (10, row6_y - 4 * section_height, 6),
    },
]

# ── DK walking state (Fase 2) ──────────────────────────────────────────────────
dk_home_x = int(3.5 * section_width)  # posição inicial do DK
dk_walk_x = dk_home_x  # posição atual do DK (pixels)
dk_walk_state = "idle"  # "idle" | "walking_out" | "dropping" | "walking_back"
dk_walk_target = dk_home_x  # destino aleatório escolhido
dk_drop_timer = 0  # contador de espera na posição de drop
dk_idle_timer = 120  # espera inicial antes de começar a andar
dk_dir = 1  # direção: 1=direita, -1=esquerda
dk_drop_signal = False  # sinal para spawnar barril no loop principal
dk_drop_x = 0  # X do barril a ser solto
DK_WALK_SPEED = 2  # pixels por frame
DK_DROP_WAIT = 45  # frames parado antes de retornar

dk_falling_victory = False
dk_fall_y = 0
victory_dk_fall_done = False
victory_timer = 0
peach_y_offset = 0

# ── Boss fight state (Fase 2) ─────────────────────────────────────────────────
dk_boss_mode = False      # ativado quando o jogador chega no nível do DK
dk_health = 3             # vida do DK (3 marteladas para matar)
dk_defeated = False       # DK derrotado?
dk_invincible_timer = 0   # invencibilidade pós-martelada (piscar)
dk_stun_timer = 0         # atordoamento pós-knockback


class Player(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        pygame.sprite.Sprite.__init__(self)
        self.y_change = 0
        self.x_speed = 3
        self.x_change = 0
        self.landed = False
        self.pos = 0
        self.dir = 1
        self.count = 0
        self.climbing = False
        self.image = standing
        self.hammer = False
        self.max_hammer = 450
        self.hammer_len = self.max_hammer
        self.hammer_pos = 1
        self.hammer_swing_timer = 0
        self.boss_hp = 3       # corações na batalha contra o DK
        self.boss_iframe = 0   # invencibilidade pós-dano do DK
        self.rect = self.image.get_rect()
        self.hitbox = self.rect
        self.hammer_box = self.rect
        self.rect.center = (x_pos, y_pos)
        self.over_barrel = False
        self.bottom = pygame.rect.Rect(
            self.rect.left, self.rect.bottom - 20, self.rect.width, 20
        )

    def update(self):
        self.landed = False
        for i in range(len(plats)):
            if self.bottom.colliderect(plats[i]):
                self.landed = True
                if not self.climbing:
                    self.rect.centery = plats[i].top - self.rect.height / 2 + 1
        if not self.landed and not self.climbing:
            self.y_change += 0.25
        self.rect.move_ip(self.x_change * self.x_speed, self.y_change)
        self.bottom = pygame.rect.Rect(
            self.rect.left, self.rect.bottom - 20, self.rect.width, 20
        )
        if self.x_change != 0 or (self.climbing and self.y_change != 0):
            if self.count < 3:
                self.count += 1
            else:
                self.count = 0
                if self.pos == 0:
                    self.pos += 1
                else:
                    self.pos = 0
        else:
            self.pos = 0
        if self.boss_iframe > 0:
            self.boss_iframe -= 1
        if self.hammer:
            if active_level != 1:
                # Fase 1: alterna automático e decai
                self.hammer_pos = (self.hammer_len // 30) % 2
                self.hammer_len -= 1
                if self.hammer_len == 0:
                    self.hammer = False
                    self.hammer_len = self.max_hammer
            else:
                # Fase 2: baseado em clique (mouse)
                if self.hammer_swing_timer > 0:
                    self.hammer_swing_timer -= 1
                # Ataque só nos primeiros ~10 frames (timer > 50)
                self.hammer_pos = 0 if self.hammer_swing_timer > 50 else 1

    def draw(self):
        # Piscar quando toma dano do DK
        if self.boss_iframe > 0 and self.boss_iframe // 3 % 2 == 0:
            return
        if not self.hammer:
            if not self.climbing and self.landed:
                if self.pos == 0:
                    self.image = standing
                else:
                    self.image = running
            if not self.landed and not self.climbing:
                self.image = jumping
            if self.climbing:
                if self.pos == 0:
                    self.image = climbing1
                else:
                    self.image = climbing2
        else:
            if self.hammer_pos == 0:
                self.image = hammer_jump
            else:
                self.image = hammer_overhead
        if self.dir == -1:
            self.image = pygame.transform.flip(self.image, True, False)
        else:
            self.image = self.image
        self.calc_hitbox()
        if self.hammer_pos == 1 and self.hammer:
            screen.blit(self.image, (self.rect.left, self.rect.top - section_height))
        else:
            screen.blit(self.image, self.rect.topleft)

    def calc_hitbox(self):
        if not self.hammer:
            self.hitbox = pygame.rect.Rect(
                (self.rect[0] + 15, self.rect[1] + 5),
                (self.rect[2] - 30, self.rect[3] - 10),
            )
        elif self.hammer_pos == 0:
            if self.dir == 1:
                self.hitbox = pygame.rect.Rect(
                    (self.rect[0], self.rect[1] + 5),
                    (self.rect[2] - 30, self.rect[3] - 10),
                )
                self.hammer_box = pygame.rect.Rect(
                    (self.hitbox[0] + self.hitbox[2], self.rect[1] + 5),
                    (self.hitbox[2], self.rect[3] - 10),
                )
            else:
                self.hitbox = pygame.rect.Rect(
                    (self.rect[0] + 40, self.rect[1] + 5),
                    (self.rect[2] - 30, self.rect[3] - 10),
                )
                self.hammer_box = pygame.rect.Rect(
                    (self.hitbox[0] - self.hitbox[2], self.rect[1] + 5),
                    (self.hitbox[2], self.rect[3] - 10),
                )
        else:
            self.hitbox = pygame.rect.Rect(
                (self.rect[0] + 15, self.rect[1] + 5),
                (self.rect[2] - 30, self.rect[3] - 10),
            )
            self.hammer_box = pygame.rect.Rect(
                (self.hitbox[0], self.hitbox[1] - section_height),
                (self.hitbox[2], section_height),
            )


class Hammer(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = hammer
        self.rect = self.image.get_rect()
        self.rect.top = y_pos
        self.rect.left = x_pos * section_width
        self.used = False

    def draw(self):
        if not self.used:
            screen.blit(self.image, (self.rect[0], self.rect[1]))
            if self.rect.colliderect(player.hitbox):
                self.kill()
                player.hammer = True
                player.hammer_len = player.max_hammer
                self.used = True
                # Tocar som do martelo
                if hammer_sound:
                    hammer_sound.play()


class Barrel(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, falls_straight=False):
        pygame.sprite.Sprite.__init__(self)
        self.image = barrel_img
        self.rect = self.image.get_rect()
        self.rect.center = (x_pos, y_pos)
        self.y_change = 0
        self.x_change = 3
        self.pos = 0
        self.count = 0
        self.oil_collision = False
        self.falling = False
        self.check_lad = False
        self.forced_fall = False
        self.drop_fall = False
        self.was_on_platform = False
        self.fall_start_y = 0
        self.falls_straight = falls_straight
        self.bottom = pygame.rect.Rect(
            (self.rect[0], self.rect.bottom), (self.rect[2], 3)
        )

    # ...existing code...
    def update(self, fire_trig):
        if self.falls_straight:
            if self.y_change < 12:
                self.y_change += 0.4
            self.rect.move_ip(0, self.y_change)
            if self.count < 10:
                self.count += 1
            else:
                self.count = 0
                self.pos = (self.pos + 1) % 4
            self.bottom = pygame.rect.Rect(
                (self.rect[0], self.rect.bottom), (self.rect[2], 3)
            )
            if self.rect.top > screen_height:
                self.kill()
            return fire_trig

        # Gravidade: rapida no chao (+2/frame, cap 8), lenta no ar (+0.3/frame, cap 5)
        if self.falling or self.forced_fall:
            if self.y_change < 5:
                self.y_change += 0.3
        else:
            if self.y_change < 8:
                self.y_change += 2

        # Colisao com plataformas
        on_platform = False
        for i in range(len(plats)):
            if self.bottom.colliderect(plats[i]):
                if self.forced_fall:
                    pass
                else:
                    if self.drop_fall:
                        fall_dist = self.rect.bottom - self.fall_start_y
                        if fall_dist > section_height:
                            self.x_change = 3 if self.x_change < 0 else -3
                        self.drop_fall = False
                    self.y_change = 0
                    self.falling = False
                    self.check_lad = False
                    self.was_on_platform = True
                    if self.x_change >= 0:
                        self.x_change = 3
                    else:
                        self.x_change = -3
                on_platform = True

        # Forced_fall: apos atravessar a plataforma, ativa drop_fall
        if self.forced_fall and not on_platform:
            self.forced_fall = False
            self.fall_start_y = self.rect.bottom
            self.drop_fall = True

        # Caiu da borda: entra em queda
        if not on_platform and not self.falling and not self.forced_fall:
            self.falling = True
            self.fall_start_y = self.rect.bottom
            if self.was_on_platform:
                self.drop_fall = True

        # Fornalha
        if self.rect.colliderect(oil_drum):
            if not self.oil_collision:
                self.oil_collision = True
                if random.randint(0, 4) == 4:
                    global fornalha_atual, timer_fornalha
                    fire_trig = True
                    fornalha_atual = fornalha_ativa
                    timer_fornalha = 180
                    self.kill()

        # Movimento: velocidade cheia rolando, metade caindo, zero no forced_fall
        if self.falling:
            if self.x_change > 0:
                self.x_change = 1.5
            elif self.x_change < 0:
                self.x_change = -1.5
        elif self.forced_fall:
            self.x_change = 0

        self.rect.move_ip(self.x_change, self.y_change)

        if self.rect.top > screen_height:
            self.kill()

        # Animacao
        if self.count < 15:
            self.count += 1
        else:
            self.count = 0
            if self.x_change > 0:
                self.pos = (self.pos + 1) % 4
            else:
                self.pos = (self.pos - 1) % 4

        self.bottom = pygame.rect.Rect(
            (self.rect[0], self.rect.bottom), (self.rect[2], 3)
        )

        return fire_trig

    def check_fall(self):
        already_collided = False
        below = pygame.rect.Rect(
            (self.rect[0], self.rect[1] + section_height),
            (self.rect[2], section_height),
        )
        for lad in lads:
            if below.colliderect(lad) and not self.falling and not self.check_lad:
                self.check_lad = True
                already_collided = True
                if random.randint(0, 200) == 200:
                    self.falling = True
                    self.forced_fall = True
                    self.drop_fall = True
                    self.y_change = 2
                    self.fall_start_y = self.rect.bottom
        if not already_collided:
            self.check_lad = False

    def draw(self):
        screen.blit(
            pygame.transform.rotate(barrel_img, 90 * self.pos), self.rect.topleft
        )


class Flame(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos):
        pygame.sprite.Sprite.__init__(self)
        self.image = fireball
        self.rect = self.image.get_rect()
        self.rect.center = (x_pos, y_pos)
        self.pos = 1
        self.count = 0
        self.x_count = 0
        self.x_change = 2
        self.x_max = 4
        self.y_change = 0
        self.row = 1
        self.check_lad = False
        self.climbing = False

    def update(self):
        if self.y_change < 3 and not self.climbing:
            self.y_change += 0.25
        for i in range(len(plats)):
            if self.rect.colliderect(plats[i]):
                self.climbing = False
                self.y_change = -4
        # if flame collides with players hitbox - trigger reset of the game (also do this to barrels)
        if self.count < 15:
            self.count += 1
        else:
            self.count = 0
            self.pos *= -1
            if self.x_count < self.x_max:
                self.x_count += 1
            else:  # row 1,3 and 5 - go further right than left overall, otherwise flip it
                self.x_count = 0
                if self.x_change > 0:
                    if self.row in [1, 3, 5]:
                        self.x_max = random.randint(3, 6)
                    else:
                        self.x_max = random.randint(6, 10)
                else:
                    if self.row in [1, 3, 5]:
                        self.x_max = random.randint(6, 10)
                    else:
                        self.x_max = random.randint(3, 6)
                self.x_change *= -1
        if self.pos == 1:
            if self.x_change > 0:
                self.image = fireball
            else:
                self.image = pygame.transform.flip(fireball, True, False)
        else:
            if self.x_change > 0:
                self.image = fireball2
            else:
                self.image = pygame.transform.flip(fireball2, True, False)
        self.rect.move_ip(self.x_change, self.y_change)
        if self.rect.top > screen_height or self.rect.top < 0:
            self.kill()

    def check_climb(self):
        already_collided = False
        for lad in lads:
            if self.rect.colliderect(lad) and not self.climbing and not self.check_lad:
                self.check_lad = True
                already_collided = True
                if random.randint(0, 120) == 120:
                    self.climbing = True
                    self.y_change = -4
        if not already_collided:
            self.check_lad = False
        if self.rect.bottom < row6_y:
            self.row = 6
        elif self.rect.bottom < row5_y:
            self.row = 5
        elif self.rect.bottom < row4_y:
            self.row = 4
        elif self.rect.bottom < row3_y:
            self.row = 3
        elif self.rect.bottom < row2_y:
            self.row = 2
        else:
            self.row = 1


# ── Spear (lança do goblin) ───────────────────────────────────────────────────
class Spear(pygame.sprite.Sprite):
    SPEED = 7
    GRAVITY = 0.18

    def __init__(self, x, y, direction):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface((1, 1), pygame.SRCALPHA)
        self.rect = pygame.Rect(
            x, y, int(section_width * 3.6), int(section_height * 0.72)
        )
        self.direction = direction  # 1 = direita, -1 = esquerda
        self.vx = self.SPEED * direction
        self.vy = -2.0  # leve arco inicial

    def update(self):
        self.vy += self.GRAVITY
        self.rect.move_ip(self.vx, self.vy)
        if (
            self.rect.right < 0
            or self.rect.left > window_width
            or self.rect.top > window_height
        ):
            self.kill()

    def draw(self):
        if use_goblin and spear_img:
            img = (
                spear_img
                if self.direction == 1
                else pygame.transform.flip(spear_img, True, False)
            )
            screen.blit(img, self.rect.topleft)
        else:
            pygame.draw.line(
                screen, (139, 90, 43), self.rect.midleft, self.rect.midright, 4
            )


# ── Goblin (guardião de plataforma) ──────────────────────────────────────────
class Goblin(pygame.sprite.Sprite):
    PATROL_SPEED = 1
    THROW_INTERVAL = 200  # frames entre lançamentos
    THROW_ANIM_LEN = 50  # frames da animação de arremesso

    def __init__(self, x_section, platform_y, patrol_left, patrol_right):
        pygame.sprite.Sprite.__init__(self)
        gw = int(section_width * 2.5)
        gh = int(section_height * 3)
        self.image = pygame.Surface((gw, gh), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x_section * section_width, int(platform_y) + int(section_height * 0.5))
        self.x = float(self.rect.x)
        self.patrol_left = patrol_left * section_width
        self.patrol_right = patrol_right * section_width
        self.direction = -1  # -1 = esquerda (pose padrão da imagem)
        self.throw_timer = random.randint(60, self.THROW_INTERVAL)
        self.throwing = False
        self.throw_frame = 0
        self.walk_frame = 0  # animation control

    def update(self, spears_group):
        if self.throwing:
            self.throw_frame += 1
            # Metade da animação: spawna a lança
            if self.throw_frame == self.THROW_ANIM_LEN // 2:
                sx = self.rect.right if self.direction == 1 else self.rect.left
                sy = self.rect.centery
                spears_group.add(Spear(sx, sy, self.direction))
            if self.throw_frame >= self.THROW_ANIM_LEN:
                self.throwing = False
                self.throw_frame = 0
                self.throw_timer = self.THROW_INTERVAL
        else:
            # Patrulha
            self.x += self.PATROL_SPEED * self.direction
            if self.x <= self.patrol_left:
                self.x = float(self.patrol_left)
                self.direction = 1
            elif self.x >= self.patrol_right:
                self.x = float(self.patrol_right)
                self.direction = -1
            self.rect.x = int(self.x)
            # Conta regressiva para o próximo lançamento
            self.throw_timer -= 1
            if self.throw_timer <= 0:
                self.throwing = True
                self.throw_frame = 0

            self.walk_frame += 1

    def draw(self):
        if not use_goblin:
            pygame.draw.rect(screen, (0, 180, 0), self.rect)
            return

        if self.throwing:
            base_img = goblin_throw_img
        else:
            tick = (self.walk_frame // 15) % 2
            base_img = goblin_walk1_img if tick == 0 else goblin_walk2_img
            
        img = (
            base_img
            if self.direction == 1
            else pygame.transform.flip(base_img, True, False)
        )
        screen.blit(img, self.rect.topleft)


class Bridge:
    def __init__(self, x_pos, y_pos, length):
        self.x_pos = x_pos * section_width
        self.y_pos = y_pos
        self.length = length
        self.top = self.draw()

    def draw(self):
        if use_platform_image:
            # Seleciona a imagem da plataforma de acordo com a fase ativa
            if active_level == 1 and use_platform2_image:
                img = platform2_img
            else:
                img = platform_img
            for i in range(self.length):
                x = self.x_pos + (section_width * i)
                y = self.y_pos
                screen.blit(img, (x, y))
        else:
            # Desenho original com linhas
            line_width = 7
            platform_color = (225, 51, 129)
            for i in range(self.length):
                bot_coord = self.y_pos + section_height
                left_coord = self.x_pos + (section_width * i)
                mid_coord = left_coord + (section_width * 0.5)
                right_coord = left_coord + section_width
                top_coord = self.y_pos
                # draw 4 lines, top, bot, left diag, right diag
                pygame.draw.line(
                    screen,
                    platform_color,
                    (left_coord, top_coord),
                    (right_coord, top_coord),
                    line_width,
                )
                pygame.draw.line(
                    screen,
                    platform_color,
                    (left_coord, bot_coord),
                    (right_coord, bot_coord),
                    line_width,
                )
                pygame.draw.line(
                    screen,
                    platform_color,
                    (left_coord, bot_coord),
                    (mid_coord, top_coord),
                    line_width,
                )
                pygame.draw.line(
                    screen,
                    platform_color,
                    (mid_coord, top_coord),
                    (right_coord, bot_coord),
                    line_width,
                )
        # get the top platform 'surface'
        top_line = pygame.rect.Rect(
            (self.x_pos, self.y_pos), (self.length * section_width, 2)
        )
        # pygame.draw.rect(screen, 'blue', top_line)
        return top_line


class Ladder:
    def __init__(self, x_pos, y_pos, length):
        self.x_pos = x_pos * section_width
        self.y_pos = y_pos
        self.length = length
        self.body = self.draw()

    def draw(self):
        line_width = 3
        lad_color = (139, 69, 19) if active_level == 0 else "light blue"  # Madeira na 1ª fase, light blue na 2ª
        lad_height = 0.6
        for i in range(self.length):
            top_coord = self.y_pos + lad_height * section_height * i
            bot_coord = top_coord + lad_height * section_height
            mid_coord = (lad_height / 2) * section_height + top_coord
            left_coord = self.x_pos
            right_coord = left_coord + section_width
            pygame.draw.line(
                screen,
                lad_color,
                (left_coord, top_coord),
                (left_coord, bot_coord),
                line_width,
            )
            pygame.draw.line(
                screen,
                lad_color,
                (right_coord, top_coord),
                (right_coord, bot_coord),
                line_width,
            )
            pygame.draw.line(
                screen,
                lad_color,
                (left_coord, mid_coord),
                (right_coord, mid_coord),
                line_width,
            )
        body = pygame.rect.Rect(
            (self.x_pos, self.y_pos - section_height),
            (
                section_width,
                (lad_height * self.length * section_height + section_height),
            ),
        )
        return body


class BrokenLadder:
    """Escada quebrada: visual diferenciado, o jogador NÃO pode escalar."""

    def __init__(self, x_pos, y_pos, length):
        self.x_pos = x_pos * section_width
        self.y_pos = y_pos
        self.length = length
        self.draw()

    def draw(self):
        line_width = 3
        rail_color = (139, 69, 19) if active_level == 0 else "light blue"
        rung_color = (139, 69, 19) if active_level == 0 else "light blue"
        lad_height = 0.6
        gap_start = max(1, self.length // 3)
        gap_end = max(gap_start + 1, self.length - self.length // 3)
        for i in range(self.length):
            if gap_start <= i < gap_end:
                continue
            top_coord = self.y_pos + lad_height * section_height * i
            bot_coord = top_coord + lad_height * section_height
            mid_coord = (lad_height / 2) * section_height + top_coord
            left_coord = self.x_pos
            right_coord = left_coord + section_width
            pygame.draw.line(
                screen,
                rail_color,
                (left_coord, top_coord),
                (left_coord, bot_coord),
                line_width,
            )
            pygame.draw.line(
                screen,
                rail_color,
                (right_coord, top_coord),
                (right_coord, bot_coord),
                line_width,
            )
            pygame.draw.line(
                screen,
                rung_color,
                (left_coord, mid_coord),
                (right_coord, mid_coord),
                line_width,
            )


# function to draw platforms and ladders
def draw_screen():
    platforms = []
    climbers = []
    ladder_objs = []
    bridge_objs = []

    ladders = levels[active_level]["ladders"]
    bridges = levels[active_level]["bridges"]
    broken_ladders = levels[active_level].get("broken_ladders", [])
    blocked_ladders = levels[active_level].get("blocked_ladders", [])

    for i, ladder in enumerate(ladders):
        ladder_objs.append(Ladder(*ladder))
        # Escadas bloqueadas: só ficam acessíveis depois de derrotar o DK
        if i in blocked_ladders and not dk_defeated:
            continue
        if ladder[2] >= 3:
            climbers.append(ladder_objs[-1].body)
    for bridge in bridges:
        bridge_objs.append(Bridge(*bridge))
        platforms.append(bridge_objs[-1].top)
    # Escadas quebradas: apenas visuais, não entram em lads/climbers
    for bl in broken_ladders:
        BrokenLadder(*bl)

    return platforms, climbers


def draw_extras():
    # put lives, levels, bonus text etc in here
    screen.blit(
        font.render(f"I•{score}", True, "white"),
        (3 * section_width, 2 * section_height),
    )
    screen.blit(
        font.render(f"TOP•{high_score}", True, "white"),
        (14 * section_width, 2 * section_height),
    )
    screen.blit(
        font.render(f"[  ][        ][  ]", True, "white"),
        (20 * section_width, 4 * section_height),
    )
    screen.blit(
        font2.render(f"  M    BONUS     L ", True, "white"),
        (20 * section_width + 5, 4 * section_height),
    )
    screen.blit(
        font2.render(
            f"  {lives}       {bonus}        {active_level + 1}  ", True, "white"
        ),
        (20 * section_width + 5, 5 * section_height),
    )
    # draw peach
    peach_render_y = row6_y - 6 * section_height + peach_y_offset
    if barrel_count < barrel_spawn_time / 2:
        screen.blit(peach1, (10 * section_width, peach_render_y))
    else:
        screen.blit(peach2, (10 * section_width, peach_render_y))
    # draw oil drum
    oil = draw_oil()
    # draw stationary barrels
    draw_barrels()
    # draw donkey kong
    draw_kong()
    return oil


def draw_oil():
    global fornalha_atual, timer_fornalha

    x_coord = 4 * section_width
    y_coord = int(window_height - 5.5 * section_height)

    # Lógica do temporizador: decrementa ou reseta a imagem
    if timer_fornalha > 0:
        timer_fornalha -= 1
        # Garante que a imagem seja a ativa enquanto o timer roda
        fornalha_atual = fornalha_ativa
    else:
        # Quando o tempo acaba, volta para a fornalha 1
        fornalha_atual = fornalha_repouso

    # Desenha a fornalha atual
    screen.blit(fornalha_atual, (x_coord - section_width, y_coord))

    # Hitbox para colisão com os barris
    oil_hitbox = pygame.Rect(
        x_coord, y_coord + 2 * section_height, 2 * section_width, int(2.5 * section_height)
    )

    return oil_hitbox


# ...existing code...


def draw_barrels():
    screen.blit(
        pygame.transform.rotate(barrel_side, 90),
        (int(section_width * 1.2), int(7.7 * section_height)),
    )
    screen.blit(
        pygame.transform.rotate(barrel_side, 90),
        (int(section_width * 2.5), int(7.7 * section_height)),
    )
    screen.blit(
        pygame.transform.rotate(barrel_side, 90),
        (int(section_width * 1.85), int(5.4 * section_height)),
    )


def draw_kong():
    global dk_walk_x, dk_walk_state, dk_walk_target, dk_drop_timer
    global dk_idle_timer, dk_dir, dk_drop_signal, dk_drop_x
    global dk_falling_victory, dk_fall_y, victory_dk_fall_done
    global dk_boss_mode, dk_defeated, dk_invincible_timer, dk_stun_timer

    dk_y = int(row6_y - 5.5 * section_height)
    
    if dk_falling_victory:
        dk_draw_img = dk7
        dk_fall_y += 4
        screen.blit(dk_draw_img, (dk_walk_x, dk_fall_y))
        if dk_fall_y > window_height:
            victory_dk_fall_done = True
        return

    if active_level == 1:
        # ── Boss mode: DK anda agressivamente, sem soltar barris ──────────
        if dk_boss_mode and not dk_defeated:
            DK_BOSS_SPEED = 3
            if dk_stun_timer > 0:
                DK_BOSS_SPEED = 1  # lento enquanto atordoado
                dk_stun_timer -= 1
            boss_left = int(3 * section_width)
            boss_right = int(25 * section_width)
            dk_walk_x += DK_BOSS_SPEED * dk_dir
            if dk_walk_x >= boss_right:
                dk_walk_x = boss_right
                dk_dir = -1
            elif dk_walk_x <= boss_left:
                dk_walk_x = boss_left
                dk_dir = 1
            tick = pygame.time.get_ticks() // 120
            base_img = [dk1, dk4][tick % 2]
            dk_draw_img = pygame.transform.flip(base_img, True, False) if dk_dir == 1 else base_img
            # Piscar quando toma dano
            if dk_invincible_timer > 0:
                dk_invincible_timer -= 1
                if dk_invincible_timer // 3 % 2 == 0:
                    screen.blit(dk_draw_img, (dk_walk_x, dk_y))
                else:
                    pass  # invisível no flash
            else:
                screen.blit(dk_draw_img, (dk_walk_x, dk_y))
            return

        # ── Fase 2 modo normal: DK anda aleatoriamente e solta barris ───
        if dk_walk_state == "idle":
            dk_idle_timer -= 1
            if dk_idle_timer <= 0:
                # Escolhe posição aleatória dentro da plataforma do topo
                dk_walk_target = random.randint(
                    int(6 * section_width), int(22 * section_width)
                )
                dk_dir = 1 if dk_walk_target > dk_walk_x else -1
                dk_walk_state = "walking_out"

        elif dk_walk_state == "walking_out":
            dk_walk_x += DK_WALK_SPEED * dk_dir
            if (dk_dir == 1 and dk_walk_x >= dk_walk_target) or (
                dk_dir == -1 and dk_walk_x <= dk_walk_target
            ):
                dk_walk_x = dk_walk_target
                dk_drop_timer = DK_DROP_WAIT
                dk_drop_signal = True  # sinaliza: spawnar barril!
                dk_drop_x = dk_walk_x
                dk_walk_state = "dropping"

        elif dk_walk_state == "dropping":
            dk_drop_timer -= 1
            if dk_drop_timer <= 0:
                # Volta para casa
                dk_dir = 1 if dk_home_x > dk_walk_x else -1
                dk_walk_state = "walking_back"

        elif dk_walk_state == "walking_back":
            dk_walk_x += DK_WALK_SPEED * dk_dir
            if (dk_dir == 1 and dk_walk_x >= dk_home_x) or (
                dk_dir == -1 and dk_walk_x <= dk_home_x
            ):
                dk_walk_x = dk_home_x
                dk_idle_timer = random.randint(60, 180)  # espera aleatória
                dk_walk_state = "idle"

        # Escolha de imagem (anima DK andando)
        tick = pygame.time.get_ticks() // 180
        if dk_walk_state == "walking_out":
            base_img = [dk5, dk6][tick % 2]  # indo com pedra: dk5 + dk6
        elif dk_walk_state == "walking_back":
            base_img = [dk1, dk4][tick % 2]  # voltando: dk1 + dk4 (sem pedra)
        elif dk_walk_state == "dropping":
            base_img = dk2  # DK segurando barril
        else:
            base_img = dk1  # DK parado

        # walking_out: sempre flip (direita) | walking_back/idle: original (esquerda)
        if dk_walk_state == "walking_out":
            dk_draw_img = pygame.transform.flip(base_img, True, False)
        elif dk_walk_state in ("walking_back", "idle"):
            dk_draw_img = base_img
        elif dk_dir == -1:
            dk_draw_img = pygame.transform.flip(base_img, True, False)
        else:
            dk_draw_img = base_img
        screen.blit(dk_draw_img, (dk_walk_x, dk_y))

    else:
        # ── Fase 1: comportamento original ──────────────────────────────────
        phase_time = barrel_time // 4
        if barrel_spawn_time - barrel_count > 3 * phase_time:
            dk_img = dk2
        elif barrel_spawn_time - barrel_count > 2 * phase_time:
            dk_img = dk1
        elif barrel_spawn_time - barrel_count > phase_time:
            dk_img = dk3
        else:
            dk_img = pygame.transform.flip(dk1, True, False)
            screen.blit(barrel_img, (int(6 * section_width), int(row6_y - 4 * slope - 2 * section_height)))
        screen.blit(dk_img, (int(3.5 * section_width), int(row6_y - 5.5 * section_height)))


def check_climb():
    can_climb = False
    climb_down = False
    under = pygame.rect.Rect(
        (player.rect[0], player.rect[1] + 2 * section_height),
        (player.rect[2], player.rect[3]),
    )
    for lad in lads:
        if player.hitbox.colliderect(lad) and not can_climb:
            can_climb = True
        if under.colliderect(lad):
            climb_down = True
    if (not can_climb and (not climb_down or player.y_change < 0)) or (
        player.landed and can_climb and player.y_change > 0 and not climb_down
    ):
        player.climbing = False
    return can_climb, climb_down


def barrel_collide(reset):
    global score
    under = pygame.rect.Rect(
        (player.rect[0], player.rect[1] + 2 * section_height),
        (player.rect[2], player.rect[3]),
    )
    for brl in barrels:
        if brl.rect.colliderect(player.hitbox):
            reset = True
        elif not player.landed and not player.over_barrel and under.colliderect(brl):
            player.over_barrel = True
            score += 100
    if player.landed:
        player.over_barrel = False

    return reset


def reset():
    """Reseta o nível atual (morte do jogador). Perde uma vida."""
    global player, barrels, flames, hammers, hammers_list, first_fireball_trigger
    global victory, lives, bonus, barrel_spawn_time, barrel_count, barrel_time
    global dk_walk_x, dk_walk_state, dk_idle_timer, dk_drop_signal, dk_dir
    global dk_falling_victory, dk_fall_y, victory_dk_fall_done
    global victory_timer, peach_y_offset
    global dk_boss_mode, dk_health, dk_defeated, dk_invincible_timer, dk_stun_timer
    pygame.time.delay(1000)
    for bar in barrels:
        bar.kill()
    for flam in flames:
        flam.kill()
    for hams in hammers:
        hams.kill()
    hammers_list = levels[active_level]["hammers"]
    for hams in hammers_list:
        hammers.add(Hammer(*hams))
    lives -= 1
    bonus = 6000
    player.kill()
    player = Player(250, window_height - 130)
    first_fireball_trigger = False
    barrel_spawn_time = level_difficulty[active_level]["barrel_spawn"]
    barrel_count = barrel_spawn_time / 2
    barrel_time = barrel_spawn_time
    victory = False
    victory_timer = 0
    peach_y_offset = 0
    # Reseta o estado do DK
    dk_walk_x = dk_home_x
    dk_walk_state = "idle"
    dk_idle_timer = 120
    dk_drop_signal = False
    dk_dir = 1
    dk_falling_victory = False
    dk_fall_y = int(window_height - section_height * 34)
    victory_dk_fall_done = False
    # Reseta estado da batalha (DK reseta HP quando morre)
    dk_boss_mode = False
    dk_health = 3
    dk_defeated = False
    dk_invincible_timer = 0
    dk_stun_timer = 0
    # Reinicia goblins e lanças
    for g in goblins:
        g.kill()
    for s in spears:
        s.kill()
    for g in levels[active_level].get("goblins", []):
        goblins.add(Goblin(*g))


def advance_level():
    """Avança para o próximo nível sem perder vida."""
    global player, barrels, flames, hammers, hammers_list, first_fireball_trigger
    global victory, bonus, barrel_spawn_time, barrel_count, barrel_time, active_level
    global dk_walk_x, dk_walk_state, dk_idle_timer, dk_drop_signal, dk_dir
    global dk_falling_victory, dk_fall_y, victory_dk_fall_done
    global victory_timer, peach_y_offset
    global dk_boss_mode, dk_health, dk_defeated, dk_invincible_timer, dk_stun_timer
    pygame.time.delay(1500)
    active_level += 1
    for bar in barrels:
        bar.kill()
    for flam in flames:
        flam.kill()
    for hams in hammers:
        hams.kill()
    hammers_list = levels[active_level]["hammers"]
    for hams in hammers_list:
        hammers.add(Hammer(*hams))
    bonus = 6000
    player.kill()
    player = Player(250, window_height - 130)
    first_fireball_trigger = False
    barrel_spawn_time = level_difficulty[active_level]["barrel_spawn"]
    barrel_count = barrel_spawn_time / 2
    barrel_time = barrel_spawn_time
    victory = False
    victory_timer = 0
    peach_y_offset = 0
    # Reseta o estado do DK para a nova fase
    dk_walk_x = dk_home_x
    dk_walk_state = "idle"
    dk_idle_timer = 90  # espera um pouco antes de começar a andar
    dk_drop_signal = False
    dk_dir = 1
    dk_falling_victory = False
    dk_fall_y = int(window_height - section_height * 34)
    victory_dk_fall_done = False
    dk_boss_mode = False
    dk_health = 3
    dk_defeated = False
    dk_invincible_timer = 0
    dk_stun_timer = 0
    # Fase 2: começa já com múltiplas flames para aumentar dificuldade
    n_flames = level_difficulty[active_level]["initial_flames"]
    for _ in range(n_flames):
        f = Flame(
            random.randint(3, 10) * section_width,
            window_height - random.randint(3, 5) * section_height,
        )
        flames.add(f)
    # Reinicia goblins e lanças para o novo nível
    for g in goblins:
        g.kill()
    for s in spears:
        s.kill()
    for g in levels[active_level].get("goblins", []):
        goblins.add(Goblin(*g))


def check_victory():
    target = levels[active_level]["target"]
    target_rect = pygame.rect.Rect(
        (target[0] * section_width, target[1]), (section_width * target[2], 1)
    )
    return player.bottom.colliderect(target_rect)


def draw_start_screen():
    """Desenha a tela inicial do jogo com instruções"""
    # Desenha a imagem de fundo se disponível
    if use_start_screen:
        screen.blit(start_screen_img, (0, 0))
    else:
        screen.fill("black")

    # Título do jogo
    title = font.render("DONKEY KONG", True, "red")
    title_rect = title.get_rect(center=(window_width // 2, window_height // 4))
    screen.blit(title, title_rect)

    # Instruções de controle
    instructions_y = window_height // 2 - 100
    instructions = [
        "COMO JOGAR:",
        "",
        "SETAS <- -> : Mover",
        "SETA CIMA : Subir escadas",
        "SETA BAIXO : Descer escadas",
        "ESPACO : Pular",
        "",
        "OBJETIVO: Resgatar a princesa!",
    ]

    for i, line in enumerate(instructions):
        if line == "COMO JOGAR:":
            text = font2.render(line, True, "yellow")
        else:
            text = font2.render(line, True, "white")
        text_rect = text.get_rect(center=(window_width // 2, instructions_y + i * 35))
        screen.blit(text, text_rect)

    # Mensagem piscante para iniciar
    if counter % 60 < 30:  # Pisca a cada meio segundo
        start_text = font.render("PRESSIONE QUALQUER TECLA", True, "green")
        start_rect = start_text.get_rect(
            center=(window_width // 2, window_height - 100)
        )
        screen.blit(start_text, start_rect)


barrels = pygame.sprite.Group()
flames = pygame.sprite.Group()
hammers = pygame.sprite.Group()
spears = pygame.sprite.Group()
goblins = pygame.sprite.Group()
hammers_list = levels[active_level]["hammers"]
for ham in hammers_list:
    hammers.add(Hammer(*ham))
for g in levels[active_level].get("goblins", []):
    goblins.add(Goblin(*g))
player = Player(250, window_height - 130)

run = True
while run:
    if use_bg:
        if active_level == 0:
            screen.blit(bg1_img, (0, 0))
        elif active_level == 1:
            screen.blit(bg2_img, (0, 0))
        else:
            screen.fill("black")
    else:
        screen.fill("black")

    timer.tick(fps)
    if counter < 60:
        counter += 1
    else:
        counter = 0
        if bonus > 0 and game_started:
            bonus -= 100

    # Se o jogo não começou, mostra a tela inicial
    if not game_started:
        # Toca o som de introdução apenas uma vez
        if not intro_played and intro_sound:
            intro_sound.play()
            intro_played = True

        draw_start_screen()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                # Qualquer tecla inicia o jogo
                game_started = True

        pygame.display.flip()
        continue  # Pula o resto do loop até o jogo começar

    # draw platforms and ladders on the screen in dedicated function
    plats, lads = draw_screen()
    oil_drum = draw_extras()
    climb, down = check_climb()
    if not victory:  # Não sobrescreve depois que já foi ativado
        if active_level == 1 and not dk_defeated:
            victory = False
        else:
            victory = check_victory()
    if barrel_count < barrel_spawn_time:
        barrel_count += 1
    else:
        barrel_count = random.randint(0, 120)
        barrel_time = barrel_spawn_time - barrel_count
        if active_level == 0:
            platform_y = int(row6_y - 4 * slope)
            spawn_x = int(5.0 * section_width)
            spawn_y = platform_y - section_height
            barrel = Barrel(spawn_x, spawn_y)
            barrels.add(barrel)
            if barrel_sound:
                barrel_sound.play()
        # Fase 2: barril é criado pelo sinal dk_drop_signal (ver abaixo)
        if not first_fireball_trigger:
            flame = Flame(5 * section_width, window_height - 4 * section_height)
            flames.add(flame)
            first_fireball_trigger = True
            # Ativa a animação da fornalha na primeira fireball
            fornalha_atual = fornalha_ativa
            timer_fornalha = 180  # 3 segundos (60 fps * 3)

    # ── Fase 2: spawn do barril quando DK o solta ────────────────────────────
    if active_level == 1 and dk_drop_signal and not dk_boss_mode:
        drop_px = int(dk_drop_x + 2 * section_width)  # centro do barril
        drop_py = int(row6_y - 3 * section_height)  # logo abaixo do DK
        barrel_lvl2 = Barrel(drop_px, drop_py, falls_straight=True)
        barrels.add(barrel_lvl2)
        if barrel_sound:
            barrel_sound.play()
        dk_drop_signal = False
    for barrel in barrels:
        barrel.draw()
        barrel.check_fall()
        fireball_trigger = barrel.update(fireball_trigger)
        if barrel.rect.colliderect(player.hammer_box) and player.hammer:
            barrel.kill()
            score += 500

    if fireball_trigger:
        flame = Flame(5 * section_width, window_height - 4 * section_height)
        flames.add(flame)
        fireball_trigger = False
        # Ativa a animação da fornalha quando a fireball spawna
        fornalha_atual = fornalha_ativa
        timer_fornalha = 180  # 3 segundos (60 fps * 3)

    for flame in flames:
        flame.check_climb()
        if flame.rect.colliderect(player.hitbox):
            reset_game = True
    flames.draw(screen)
    flames.update()
    player.update()
    player.draw()
    for ham in hammers:
        ham.draw()

    # ── Boss fight DK (Fase 2) ──────────────────────────────────────────────
    if active_level == 1:
        dk_rect = pygame.Rect(dk_walk_x, int(row6_y - 5.5 * section_height), section_width * 5, section_height * 5)
        dk_rect.y = dk_rect.y + section_height * 2  # ajuste fino da hitbox
        dk_rect.h = section_height * 3

        # Ativar boss mode quando o jogador chega no nível do DK
        if not dk_boss_mode and not dk_defeated:
            if player.rect.centery <= dk_rect.centery + section_height * 4:
                dk_boss_mode = True

        if dk_boss_mode and not dk_defeated and not dk_falling_victory:
            # DK acerta o jogador: perde 1 coração (se não tiver martelo ou martelo pra cima)
            dano = False
            if player.hammer and player.hammer_pos == 1:
                dano = True
            if not player.hammer:
                dano = True
            if dano and player.hitbox.colliderect(dk_rect) and player.boss_iframe <= 0:
                player.boss_hp -= 1
                player.boss_iframe = 45  # 0.75s invencível + piscando
                if player.boss_hp <= 0:
                    reset_game = True

        # Martelo pra baixo (hammer_pos == 0): acerta o DK
        if dk_boss_mode and not dk_defeated and player.hammer and player.hammer_pos == 0 and dk_invincible_timer <= 0:
            if player.hammer_box.colliderect(dk_rect):
                dk_health -= 1
                dk_invincible_timer = 30  # 0.5s piscando
                # Knockback no DK (empurrão forte + atordoamento)
                push_dir = 1 if player.rect.centerx < dk_rect.centerx else -1
                dk_walk_x += push_dir * 200
                dk_dir = -push_dir
                dk_stun_timer = 60  # 1s andando devagar
                if dk_health <= 0:
                    dk_defeated = True
                    dk_falling_victory = True
                    dk_fall_y = int(row6_y - 5.5 * section_height)

        # Martelo acerta goblins (só com hammer_pos == 0)
        if player.hammer and player.hammer_pos == 0:
            for goblin in list(goblins):
                if player.hammer_box.colliderect(goblin.rect):
                    goblin.kill()
                    score += 200

    # ── Goblins e lanças (fase 2) ─────────────────────────────────────────
    if active_level == 1:
        for goblin in goblins:
            goblin.update(spears)
            goblin.draw()
        for spear in list(spears):
            spear.update()
            spear.draw()
            if spear.rect.colliderect(player.hitbox):
                reset_game = True
                spear.kill()

    reset_game = barrel_collide(reset_game)
    if reset_game:
        if lives > 0:
            reset()
            reset_game = False
        else:
            run = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            # ESC na tela final da fase 2
            if victory and active_level == 1 and victory_dk_fall_done:
                if event.key == pygame.K_ESCAPE:
                    game_started = False
                    if score > high_score:
                        high_score = score
                    lives = 5
                    score = 0
                    active_level = 0
                    reset()
            if not victory:
                if (event.key == pygame.K_RIGHT or event.key == pygame.K_d) and not player.climbing:
                    player.x_change = 1
                    player.dir = 1
                if (event.key == pygame.K_LEFT or event.key == pygame.K_a) and not player.climbing:
                    player.x_change = -1
                    player.dir = -1
                if event.key == pygame.K_SPACE and player.landed:
                    player.landed = False
                    player.y_change = -6
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    if climb:
                        player.y_change = -2
                        player.x_change = 0
                        player.climbing = True
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if down:
                        player.y_change = 2
                        player.x_change = 0
                        player.climbing = True
            if event.key == pygame.K_F2:
                if active_level == 0 and len(levels) > 1:
                    advance_level()
        if event.type == pygame.KEYUP:
            if not victory:  # Bloqueia soltar teclas de movimento durante vitória
                if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    player.x_change = 0
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    player.x_change = 0
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    if climb:
                        player.y_change = 0
                    if player.climbing and player.landed:
                        player.climbing = False
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    if climb:
                        player.y_change = 0
                    if player.climbing and player.landed:
                        player.climbing = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1 and player.hammer and not victory:
                if player.hammer_swing_timer <= 0:
                    player.hammer_swing_timer = 60
    if victory:
        victory_timer += 1

        # Controla o personagem automaticamente durante a vitória
        player.x_change = 0
        target_x = 12 * section_width

        # FASE 1 estágio 3: personagem e Peach sobem pelas escadas
        if active_level == 0 and victory_timer > 150:
            player.climbing = True
            player.y_change = -4
            player.x_change = 0
            player.rect.x = target_x
            player.dir = 1
            peach_y_offset -= 4  # Peach sobe escada (10, -5, 13)
            screen.blit(
                font.render("VICTORY!", True, "yellow"),
                (window_width // 2 - 150, window_height // 2),
            )
            screen.blit(
                font2.render("PROXIMO NIVEL!", True, "cyan"),
                (window_width // 2 - 170, window_height // 2 + 70),
            )
            # Quando o personagem sair pelo topo da tela -> avança de fase
            if player.rect.bottom < 0:
                score += bonus
                if score > high_score:
                    high_score = score
                advance_level()

        else:
            # Estágio 1/2: caminhar até a Peach e pular (comemoração)
            player.climbing = False

            if player.rect.x < target_x - 5:
                player.x_change = 1
                player.dir = 1
            elif player.rect.x > target_x + 5:
                player.x_change = -1
                player.dir = -1
            else:
                player.x_change = 0
                player.rect.x = target_x
                player.dir = -1  # De frente para a Peach

                # Pulos de comemoração
                if victory_timer % 30 < 15:
                    peach_y_offset = -10
                    if player.landed:
                        player.y_change = -4
                else:
                    peach_y_offset = 0

            # Mostra VICTORY! a partir do frame 60
            if victory_timer > 60:
                screen.blit(
                    font.render("VICTORY!", True, "yellow"),
                    (window_width // 2 - 150, window_height // 2),
                )

            # FASE 2: espera DK cair (se já não caiu) e mostra ESC
            if active_level == 1 and victory_timer > 120:
                if victory_dk_fall_done:
                    screen.blit(
                        font2.render("Pressione ESC para voltar ao Inicio", True, "white"),
                        (window_width // 2 - 260, window_height // 2 + 70),
                    )
                    # ESC handling já está no KEYDOWN acima

    pygame.display.flip()
pygame.quit()
