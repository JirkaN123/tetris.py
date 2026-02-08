import pygame


class Tetris:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((400, 600))
        pygame.display.set_caption("Tetris")
        self.clock = pygame.time.Clock()
        self.running = True
        self.death = False
        self.death_zone = 0
        self.map = [[0 for _ in range(10)] for _ in range(20)]
        self.blocks = [
            [[1, 1, 1, 1]],  # I
            [[1, 1], [1, 1]],  # O
            [[0, 1, 0], [1, 1, 1]],  # T
            [[1, 0, 0], [1, 1, 1]],  # L
            [[0, 0, 1], [1, 1, 1]],  # J
            [[0, 1, 1], [1, 1, 0]],  # S
            [[1, 1, 0], [0, 1, 1]]   # Z
        ]
        self.current_piece = None
        self.next_piece = None
        self.colorlist= [
            (255, 0, 0),    # Red
            (0, 255, 0),    # Green
            (0, 0, 255),    # Blue
            (255, 255, 0),  # Yellow
            (255, 0, 255),  # Magenta
            (0, 255, 255),  # Cyan
            (255, 165, 0)   # Orange
        ]
        self.keys = {
            "left": pygame.K_LEFT,
            "right": pygame.K_RIGHT,
            "down": pygame.K_DOWN,
            "rotate": pygame.K_UP,
            "drop": pygame.K_SPACE,
            "reset": pygame.K_r,
            "pause": pygame.K_ESCAPE

        }

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(10)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == self.keys["left"]:
                    self.move_piece(-1, 0)
                elif event.key == self.keys["right"]:
                    self.move_piece(1, 0)
                elif event.key == self.keys["down"]:
                    self.move_piece(0, 1)
                elif event.key == self.keys["rotate"]:
                    self.rotate_piece()
                elif event.key == self.keys["drop"]:
                    while self.is_valid_position(self.piece_x, self.piece_y + 1):
                        self.move_piece(0, 1)
                    self.lock_piece()
                    self.current_piece = None
                elif event.key == self.keys["reset"]:
                    self.reset_game()
                elif event.key == self.keys["pause"]:
                    self.pause_game()

    def update(self):
        if self.current_piece is None:
            self.spawn_piece()
        else:
            self.move_piece(0, 1)

    def draw(self):
        self.screen.fill((0, 0, 0))
        for y in range(20):
            for x in range(10):
                if self.map[y][x] == 1:
                    pygame.draw.rect(self.screen, (255, 255, 255), (x * 20, y * 20, 20, 20))
        if self.current_piece is not None:
            for y in range(len(self.current_piece)):
                for x in range(len(self.current_piece[y])):
                    if self.current_piece[y][x] == 1:
                        pygame.draw.rect(self.screen, (255, 0, 0), ((self.piece_x + x) * 20, (self.piece_y + y) * 20, 20, 20))
        pygame.display.flip()

    def spawn_piece(self):
        import random
        self.colorlist.append(self.colorlist.pop(0))
        self.current_piece = random.choice(self.blocks)
        self.piece_x = 3
        self.piece_y = 0


    def move_piece(self, dx, dy):
        new_x = self.piece_x + dx
        new_y = self.piece_y + dy
        if self.is_valid_position(new_x, new_y):
            self.piece_x = new_x
            self.piece_y = new_y
        else:
            if dy == 1: 
                self.lock_piece()
                self.current_piece = None
    
    def rotate_piece(self):
        rotated_piece = [list(row) for row in zip(*self.current_piece[::-1])]
        if self.is_valid_position(self.piece_x, self.piece_y, rotated_piece):
            self.current_piece = rotated_piece

    def is_valid_position(self, x, y, piece=None):
        if piece is None:
            piece = self.current_piece
        try:
            for py in range(len(piece)):
                for px in range(len(piece[py])):
                    if piece[py][px] == 1:
                        if x + px < 0 or x + px >= 10 or y + py >= 20:
                            return False
                        if self.map[y + py][x + px] == 1:
                            return False
            return True
        except IndexError:
            return False
            
    
    def lock_piece(self):
        for y in range(len(self.current_piece)):
            for x in range(len(self.current_piece[y])):
                if self.current_piece[y][x] == 1:
                    self.map[self.piece_y + y][self.piece_x + x] = 1
        self.clear_lines()

    def clear_lines(self):
        new_map = [row for row in self.map if any(cell == 0 for cell in row)]
        lines_cleared = 20 - len(new_map)
        self.map = [[0 for _ in range(10)] for _ in range(lines_cleared)] + new_map

    def check_death(self):
        for x in range(10):
            if self.map[0][x] == 1:
                self.death = True
                break
    
    def check_death_zone(self):
        for x in range(10):
            if self.map[0][x] == 1:
                self.death_zone += 1
            else:
                self.death_zone = 0
                break
        if self.death_zone >= 2:
            self.death = True

    def reset_game(self):
        self.map = [[0 for _ in range(10)] for _ in range(20)]
        self.current_piece = None
        self.next_piece = None
        self.death = False
        self.death_zone = 0
    
    def pause_game(self):
        paused = True
        while paused:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    paused = False
                elif event.type == pygame.KEYDOWN and event.key == self.keys["pause"]:
                    paused = False

if __name__ == "__main__":
    game = Tetris()
    game.run()