import pygame
import sys
from config import *
from persistence import *
from ui_elements import Button, TextInput
from game import RaceSession

class RacerApp:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Racer TSIS 3")
        self.clock = pygame.time.Clock()
        self.running = True
        
        self.settings = load_settings()
        self.leaderboard = load_leaderboard()
        
        self.state = GameState.MENU
        self.username = ""
        self.race_session = None
        
        self._init_ui()
        
    def _init_ui(self):
        # menu UI
        self.btn_play = Button(100, 200, 200, 50, "Play")
        self.btn_lead = Button(100, 270, 200, 50, "Leaderboard")
        self.btn_set = Button(100, 340, 200, 50, "Settings")
        self.btn_quit = Button(100, 410, 200, 50, "Quit")
        
        # username UI
        self.username_input = TextInput(100, 300, 200, 40)
        self.btn_start_race = Button(100, 370, 200, 50, "Start")
        self.btn_cancel_name = Button(100, 440, 200, 50, "Back")
        
        # settings UI
        self.btn_color = Button(100, 200, 200, 50, f"Color: {self.settings['car_color']}")
        self.btn_diff = Button(100, 270, 200, 50, f"Diff: {self.settings['difficulty']}")
        snd_txt = "Sound: ON" if self.settings.get("sound_enabled", True) else "Sound: OFF"
        self.btn_sound = Button(100, 340, 200, 50, snd_txt)
        self.btn_back_set = Button(100, 410, 200, 50, "Back")
        
        # leaderboard UI
        self.btn_back_lead = Button(100, 500, 200, 50, "Back")
        
        # game Over UI
        self.btn_retry = Button(100, 350, 200, 50, "Retry")
        self.btn_menu = Button(100, 420, 200, 50, "Main Menu")

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.update()
            self.clock.tick(FPS)
        pygame.quit()
        sys.exit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            if self.state == GameState.MENU:
                if self.btn_play.is_clicked(event):
                    self.state = GameState.USERNAME
                elif self.btn_lead.is_clicked(event):
                    self.state = GameState.LEADERBOARD
                elif self.btn_set.is_clicked(event):
                    self.state = GameState.SETTINGS
                elif self.btn_quit.is_clicked(event):
                    self.running = False
            
            elif self.state == GameState.USERNAME:
                self.username_input.handle_event(event)
                if self.btn_start_race.is_clicked(event):
                    self.username = self.username_input.text if self.username_input.text else "Player"
                    self.race_session = RaceSession(self.settings)
                    self.state = GameState.PLAY
                elif self.btn_cancel_name.is_clicked(event):
                    self.state = GameState.MENU
                    
            elif self.state == GameState.SETTINGS:
                if self.btn_color.is_clicked(event):
                    colors = ["RED", "BLUE", "YELLOW", "GREEN", "MAGENTA"]
                    idx = (colors.index(self.settings["car_color"]) + 1) % len(colors)
                    self.settings["car_color"] = colors[idx]
                    self.btn_color.text = f"Color: {self.settings['car_color']}"
                elif self.btn_diff.is_clicked(event):
                    diffs = ["Easy", "Normal", "Hard"]
                    idx = (diffs.index(self.settings["difficulty"]) + 1) % len(diffs)
                    self.settings["difficulty"] = diffs[idx]
                    self.btn_diff.text = f"Diff: {self.settings['difficulty']}"
                elif self.btn_sound.is_clicked(event):
                    self.settings["sound_enabled"] = not self.settings.get("sound_enabled", True)
                    self.btn_sound.text = "Sound: ON" if self.settings["sound_enabled"] else "Sound: OFF"
                elif self.btn_back_set.is_clicked(event):
                    save_settings(self.settings)
                    self.state = GameState.MENU
                    
            elif self.state == GameState.LEADERBOARD:
                if self.btn_back_lead.is_clicked(event):
                    self.state = GameState.MENU
                    
            elif self.state == GameState.PLAY:
                self.race_session.handle_event(event)
                
            elif self.state == GameState.GAMEOVER:
                if self.btn_retry.is_clicked(event):
                    self.race_session = RaceSession(self.settings)
                    self.state = GameState.PLAY
                elif self.btn_menu.is_clicked(event):
                    self.state = GameState.MENU

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.state == GameState.MENU:
            self.btn_play.update(mouse_pos)
            self.btn_lead.update(mouse_pos)
            self.btn_set.update(mouse_pos)
            self.btn_quit.update(mouse_pos)
        elif self.state == GameState.USERNAME:
            self.btn_start_race.update(mouse_pos)
            self.btn_cancel_name.update(mouse_pos)
        elif self.state == GameState.SETTINGS:
            self.btn_color.update(mouse_pos)
            self.btn_diff.update(mouse_pos)
            self.btn_sound.update(mouse_pos)
            self.btn_back_set.update(mouse_pos)
        elif self.state == GameState.LEADERBOARD:
            self.btn_back_lead.update(mouse_pos)
        elif self.state == GameState.PLAY:
            self.race_session.update()
            if self.race_session.game_over:
                # save score
                self.leaderboard.append({"name": self.username, "score": self.race_session.score, "dist": int(self.race_session.distance)})
                save_leaderboard(self.leaderboard)
                self.state = GameState.GAMEOVER
        elif self.state == GameState.GAMEOVER:
            self.btn_retry.update(mouse_pos)
            self.btn_menu.update(mouse_pos)

    def draw(self):
        self.screen.fill(Colors.ROAD.value)
        
        font_title = pygame.font.SysFont("Verdana", 40, bold=True)
        font_norm = pygame.font.SysFont("Verdana", 24)
        
        if self.state == GameState.MENU:
            title = font_title.render("RACER TSIS 3", True, Colors.WHITE.value)
            self.screen.blit(title, (60, 80))
            self.btn_play.draw(self.screen)
            self.btn_lead.draw(self.screen)
            self.btn_set.draw(self.screen)
            self.btn_quit.draw(self.screen)
            
        elif self.state == GameState.USERNAME:
            title = font_title.render("Enter Name:", True, Colors.WHITE.value)
            self.screen.blit(title, (80, 200))
            self.username_input.draw(self.screen)
            self.btn_start_race.draw(self.screen)
            self.btn_cancel_name.draw(self.screen)
            
        elif self.state == GameState.SETTINGS:
            title = font_title.render("SETTINGS", True, Colors.WHITE.value)
            self.screen.blit(title, (100, 80))
            self.btn_color.draw(self.screen)
            self.btn_diff.draw(self.screen)
            self.btn_sound.draw(self.screen)
            self.btn_back_set.draw(self.screen)
            
        elif self.state == GameState.LEADERBOARD:
            title = font_title.render("TOP 10", True, Colors.WHITE.value)
            self.screen.blit(title, (120, 50))
            self.leaderboard.sort(key=lambda x: x.get("score", 0), reverse=True)
            for i, entry in enumerate(self.leaderboard[:10]):
                txt = f"{i+1}. {entry['name']} - {entry['score']} pts"
                surf = font_norm.render(txt, True, Colors.WHITE.value)
                self.screen.blit(surf, (50, 120 + i * 30))
            self.btn_back_lead.draw(self.screen)
            
        elif self.state == GameState.PLAY:
            self.race_session.draw(self.screen)
            
        elif self.state == GameState.GAMEOVER:
            self.race_session.draw(self.screen) # draw background frozen
            # draw overlay
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.set_alpha(180)
            overlay.fill(Colors.BLACK.value)
            self.screen.blit(overlay, (0, 0))
            
            title = font_title.render("GAME OVER", True, Colors.RED.value)
            self.screen.blit(title, (70, 100))
            
            s1 = font_norm.render(f"Score: {self.race_session.score}", True, Colors.WHITE.value)
            s2 = font_norm.render(f"Dist: {int(self.race_session.distance)} / {FINISH_LINE_DISTANCE}", True, Colors.WHITE.value)
            if self.race_session.distance >= FINISH_LINE_DISTANCE:
                title = font_title.render("YOU WIN!", True, Colors.YELLOW.value)
                self.screen.blit(title, (90, 50))
                
            self.screen.blit(s1, (120, 200))
            self.screen.blit(s2, (100, 250))
            
            self.btn_retry.draw(self.screen)
            self.btn_menu.draw(self.screen)
