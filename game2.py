import pyxel
import random

WINDOW_W = 160
WINDOW_H = 120
PLAYER_W = 10
PLAYER_H = 10
BULLET_W = 2
BULLET_H = 4
BLOCK_W = 16
BLOCK_H = 16

class Player:
    def __init__(self):
        self.x = WINDOW_W // 2 - PLAYER_W // 2
        self.y = WINDOW_H - 20
        self.bullets = []

    def update(self):
        if pyxel.btn(pyxel.KEY_LEFT):
            self.x = max(self.x - 2, 0)
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.x = min(self.x + 2, WINDOW_W - PLAYER_W)
        if pyxel.btn(pyxel.KEY_UP):
            self.y = max(self.y - 2, 0)
        if pyxel.btn(pyxel.KEY_DOWN):
            self.y = min(self.y + 2, WINDOW_H - PLAYER_H)
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.bullets.append([self.x + PLAYER_W // 2, self.y])

    def draw(self):
        pyxel.rect(self.x, self.y, PLAYER_W, PLAYER_H, 11)
        for bullet in self.bullets:
            pyxel.rect(bullet[0], bullet[1], BULLET_W, BULLET_H, 10)

class Block:
    def __init__(self, x, y, letter=""):
        self.x = x
        self.y = y
        self.letter = letter

    def draw(self):
        pyxel.rect(self.x, self.y, BLOCK_W, BLOCK_H, 14)
        pyxel.text(self.x + 4, self.y + 4, self.letter, 7)

class Game:
    def __init__(self):
        pyxel.init(WINDOW_W, WINDOW_H, title="Block Breaker Quiz")
        self.reset_game()
        pyxel.run(self.update, self.draw)

    def reset_game(self):
        self.player = Player()
        self.blocks = []
        self.stage = 1
        self.stage_clear = False
        self.quiz_started = False
        self.target_word = "NEW-GROWTH"
        self.current_word = ""
        self.wrong_hits = 0
        self.game_clear = False
        self.show_intro = False
        self.intro_timer = 0
        self.reset_message = ""
        self.reset_message_timer = 0
        self.setup_stage()

    def setup_stage(self):
        self.blocks = []
        if self.stage == 1:
            for i in range(10):
                x = random.randint(0, WINDOW_W - BLOCK_W)
                y = random.randint(0, WINDOW_H // 2)
                self.blocks.append(Block(x, y))
        elif self.stage == 2:
            for i, letter in enumerate(self.target_word):
                x = (i % 4) * (BLOCK_W + 8) + 20
                y = (i // 4) * (BLOCK_H + 8) + 20
                self.blocks.append(Block(x, y, letter))
        elif self.stage == 3:
            letters = list("HEART")
            for i in range(5):
                x = i * (BLOCK_W + 8) + 20
                y = WINDOW_H // 2
                self.blocks.append(Block(x, y, random.choice(letters)))

    def update(self):
        if self.reset_message_timer > 0:
            self.reset_message_timer -= 1
            if self.reset_message_timer == 0:
                self.reset_message = ""
                self.setup_stage()
                self.current_word = ""
        elif self.show_intro:
            self.intro_timer += 1
            if self.intro_timer > 180 and pyxel.btnp(pyxel.KEY_RETURN):
                self.show_intro = False
                self.stage = 2
                self.setup_stage()
        elif self.game_clear:
            if pyxel.btnp(pyxel.KEY_RETURN):
                pyxel.quit()
        elif self.stage_clear:
            if pyxel.btnp(pyxel.KEY_RETURN):
                if self.stage == 1:
                    self.stage = 2
                    self.setup_stage()
                    self.stage_clear = False
                    self.quiz_started = False
                elif self.stage == 2:
                    self.stage = 3
                    self.setup_stage()
                    self.stage_clear = False
                    self.quiz_started = False
                elif self.stage == 3:
                    self.game_clear = True
        elif not self.quiz_started:
            if pyxel.btnp(pyxel.KEY_RETURN):
                self.quiz_started = True
        else:
            self.player.update()
            self.update_bullets()
            self.check_collision()

    def update_bullets(self):
        for bullet in self.player.bullets:
            bullet[1] -= 2
        self.player.bullets = [b for b in self.player.bullets if b[1] > 0]

    def check_collision(self):
        for bullet in self.player.bullets[:]:
            for block in self.blocks[:]:
                if (block.x < bullet[0] < block.x + BLOCK_W and
                    block.y < bullet[1] < block.y + BLOCK_H):
                    if self.stage == 1:
                        self.blocks.remove(block)
                    elif self.stage == 2:
                        if block.letter == self.target_word[len(self.current_word)]:
                            self.current_word += block.letter
                            self.blocks.remove(block)
                        else:
                            self.reset_message = "Wrong order! Restarting..."
                            self.reset_message_timer = 60
                    elif self.stage == 3:
                        block.letter = random.choice("HEART")
                    if bullet in self.player.bullets:
                        self.player.bullets.remove(bullet)
                    break

        if self.stage == 1 and len(self.blocks) == 0:
            self.stage_clear = True
        elif self.stage == 2 and self.current_word == self.target_word:
            self.stage_clear = True
        elif self.stage == 3 and all(block.letter == "HEART"[i] for i, block in enumerate(self.blocks)):
            self.stage_clear = True

    def draw(self):
        pyxel.cls(0)
        if self.show_intro:
            for i in range(20):
                x = random.randint(0, WINDOW_W)
                y = random.randint(0, WINDOW_H)
                pyxel.pset(x, y, 7)
            pyxel.text(10, 50, "NICE TO MEET YOU!", 7)
            pyxel.text(10, 60, "THANK YOU FOR", 7)
            pyxel.text(10, 70, "THIS OPPORTUNITY.", 7)
            pyxel.text(10, 100, "PRESS ENTER TO CONTINUE", 7)
        elif not self.quiz_started:
            if self.stage == 1:
                pyxel.text(10, 50, "STAGE 1: DESTROY ALL BLOCKS", 7)
            elif self.stage == 2:
                pyxel.text(10, 50, "STAGE 2: SPELL 'NEW_GROWTH'", 7)
                pyxel.text(10, 60, "SHOOT IN THE CORRECT ORDER!", 7)
                pyxel.text(10, 70, "WRONG ORDER WILL RESET!", 7)
            elif self.stage == 3:
                pyxel.text(10, 50, "FINAL QUESTION!", 7)
                pyxel.text(10, 60, "WHEN HIRING A NEW PERSON,", 7)
                pyxel.text(10, 70, "SKILLS AND POTENTIAL ARE IMPORTANT.", 7)
                pyxel.text(10, 80, "BUT WHAT'S THE MOST IMPORTANT?", 7)
            pyxel.text(10, 100, "PRESS ENTER TO START", 7)
        else:
            self.player.draw()
            for block in self.blocks:
                block.draw()
            pyxel.text(5, 5, f"STAGE: {self.stage}", 7)
            pyxel.text(5, WINDOW_H - 10, "SPACE: SHOOTING", 7)
            if self.stage == 2:
                pyxel.text(5, WINDOW_H - 20, f"WORD: {self.current_word}", 7)

        if self.reset_message:
            pyxel.text(WINDOW_W // 2 - 50, WINDOW_H // 2, self.reset_message, 8)

        if self.stage_clear:
            pyxel.text(WINDOW_W // 2 - 30, WINDOW_H // 2, f"STAGE {self.stage} CLEAR!", 7)
            pyxel.text(WINDOW_W // 2 - 50, WINDOW_H // 2 + 20, "PRESS ENTER FOR NEXT STAGE", 7)

        if self.game_clear:
            pyxel.cls(0)
            for i in range(20):
                x = random.randint(0, WINDOW_W)
                y = random.randint(0, WINDOW_H)
                pyxel.pset(x, y, 7)
            pyxel.text(WINDOW_W // 2 - 50, WINDOW_H // 2 - 20, "CONGRATULATIONS!", 7)
            pyxel.text(WINDOW_W // 2 - 40, WINDOW_H // 2, "GAME CLEAR!", 7)
            pyxel.text(WINDOW_W // 2 - 50, WINDOW_H // 2 + 20, "THE ANSWER IS HEART.", 7)
            pyxel.text(WINDOW_W // 2 - 60, WINDOW_H // 2 + 30, "AND I HAVE IT.", 7)
            pyxel.text(WINDOW_W // 2 - 70, WINDOW_H // 2 + 50, "PRESS ENTER TO EXIT", 7)

Game()
