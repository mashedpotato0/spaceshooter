import numpy as np
import tkinter as tk
import random


class SpaceShooterGame:
    def __init__(self):
        self.space = np.zeros((16, 16), dtype=int)
        self.player_position = [15, 8]  # Starting position at the bottom center
        self.player_health = 3
        self.space[self.player_position[0], self.player_position[1]] = 1
        self.enemies = []
        self.bullets = []
        self.powerups = []

    def move_player(self, direction):
        if self.player_health <= 0:
            return

        # Remove the player from the current position
        self.space[self.player_position[0], self.player_position[1]] = 0

        if direction == 'left' and self.player_position[1] > 0:
            self.player_position[1] -= 1
        elif direction == 'right' and self.player_position[1] < 15:
            self.player_position[1] += 1
        elif direction == 'up' and self.player_position[0] > 0:
            self.player_position[0] -= 1
        elif direction == 'down' and self.player_position[0] < 15:
            self.player_position[0] += 1

        # Place the player in the new position
        self.space[self.player_position[0], self.player_position[1]] = 1

    def spawn_enemy(self):
        x = random.randint(0, 5)
        y = random.randint(0, 15)
        enemy_type = random.choice(['weak', 'strong'])
        health = 1 if enemy_type == 'weak' else 2
        self.enemies.append([x, y, enemy_type, health])
        self.space[x, y] = 2  # 2 represents an enemy

    def move_enemies(self):
        for enemy in self.enemies:
            self.space[enemy[0], enemy[1]] = 0
            enemy[0] += 1
            if enemy[0] > 15:
                self.enemies.remove(enemy)
            else:
                if [enemy[0], enemy[1]] == self.player_position:
                    self.player_health -= 1
                    self.enemies.remove(enemy)
                else:
                    self.space[enemy[0], enemy[1]] = 2

    def shoot_bullet(self, bullet_type):
        if self.player_health > 0:
            power = 1 if bullet_type == 'normal' else 2
            self.bullets.append([self.player_position[0] - 1, self.player_position[1], power])
            self.space[self.player_position[0] - 1, self.player_position[1]] = 3  # 3 represents a bullet

    def move_bullets(self):
        for bullet in self.bullets:
            self.space[bullet[0], bullet[1]] = 0
            bullet[0] -= 1
            if bullet[0] < 0:
                self.bullets.remove(bullet)
            else:
                for enemy in self.enemies:
                    if [bullet[0], bullet[1]] == [enemy[0], enemy[1]]:
                        enemy[3] -= bullet[2]
                        if enemy[3] <= 0:
                            self.drop_powerup(enemy[0], enemy[1])
                            self.enemies.remove(enemy)
                        self.bullets.remove(bullet)
                        break
                else:
                    self.space[bullet[0], bullet[1]] = 3

    def drop_powerup(self, x, y):
        if random.random() < 0.1:  # 10% chance to drop a power-up
            self.powerups.append([x, y])
            self.space[x, y] = 4  # 4 represents a power-up

    def collect_powerups(self):
        for powerup in self.powerups:
            if self.player_position == powerup:
                self.powerups.remove(powerup)
                self.space[powerup[0], powerup[1]] = 0

    def get_space(self):
        return self.space


class GameGUI:
    def __init__(self, root, game):
        self.root = root
        self.game = game

        self.canvas = tk.Canvas(root, width=320, height=320, bg="black")
        self.canvas.pack()

        self.draw_grid()
        self.update_canvas()
        self.game_loop()

        root.bind("<Left>", self.handle_keypress)
        root.bind("<Right>", self.handle_keypress)
        root.bind("<Up>", self.handle_keypress)
        root.bind("<Down>", self.handle_keypress)
        root.bind("a", self.handle_keypress)
        root.bind("d", self.handle_keypress)
        root.bind("w", self.handle_keypress)
        root.bind("s", self.handle_keypress)
        root.bind("<space>", self.handle_keypress)

    def draw_grid(self):
        self.rects = []
        for i in range(16):
            row = []
            for j in range(16):
                rect = self.canvas.create_rectangle(j * 20, i * 20, (j + 1) * 20, (i + 1) * 20, outline="white",
                                                    fill="black")
                row.append(rect)
            self.rects.append(row)

    def update_canvas(self):
        space = self.game.get_space()
        for i in range(16):
            for j in range(16):
                if space[i, j] == 1:
                    color = "white"  # Player
                elif space[i, j] == 2:
                    color = "red"  # Enemy
                elif space[i, j] == 3:
                    color = "yellow"  # Bullet
                elif space[i, j] == 4:
                    color = "blue"  # Power-up
                else:
                    color = "black"
                self.canvas.itemconfig(self.rects[i][j], fill=color)

    def handle_keypress(self, event):
        if event.keysym in ['Left', 'a']:
            self.game.move_player('left')
        elif event.keysym in ['Right', 'd']:
            self.game.move_player('right')
        elif event.keysym in ['Up', 'w']:
            self.game.move_player('up')
        elif event.keysym in ['Down', 's']:
            self.game.move_player('down')
        elif event.keysym == 'space':
            self.game.shoot_bullet('normal')  # Add different bullet types here

        self.update_canvas()

    def game_loop(self):
        if self.game.player_health > 0:
            self.game.move_enemies()
            self.game.move_bullets()
            self.game.collect_powerups()
            if random.random() < 0.1:  # Adjust spawn rate
                self.game.spawn_enemy()

            self.update_canvas()
            self.root.after(500, self.game_loop)  # Adjust game speed
        else:
            self.canvas.create_text(160, 160, text="Game Over", fill="white", font=("Helvetica", 24))


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Space Shooter Game")

    game = SpaceShooterGame()
    gui = GameGUI(root, game)

    root.mainloop()
