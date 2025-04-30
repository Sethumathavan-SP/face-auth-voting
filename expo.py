import pygame
import sys
import math
from pygame.locals import *

def voting_machine():
    pygame.init()
    screen_width, screen_height = pygame.display.Info().current_w, pygame.display.Info().current_h
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Smart Voting System")
    clock = pygame.time.Clock()
    bg_image = pygame.image.load("flag.jpg")
    bg_image = pygame.transform.scale(bg_image, (screen_width, screen_height))
    overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180)) 
    title_font = pygame.font.SysFont("Segoe UI", int(screen_height * 0.05), bold=True)
    button_font = pygame.font.SysFont("Segoe UI", 34)
    title1 = title_font.render("ST. JOSEPH'S INSTITUTE OF TECHNOLOGY", True, (255, 255, 255))
    title2 = title_font.render("SMART VOTING SYSTEM!", True, (0, 255, 200))
    title1_rect = title1.get_rect(center=(screen_width // 2, screen_height * 0.08))
    title2_rect = title2.get_rect(center=(screen_width // 2, screen_height * 0.15))
    total_buttons = 5
    button_data = []
    spacing = 90
    base_y = screen_height * 0.35
    for i in range(total_buttons):
        rect = pygame.Rect(0, 0, 320, 65)
        rect.center = (-400, base_y + i * spacing)
        button_data.append({
            "rect": rect,
            "label": f"PARTY {i + 1}",
            "hover": 0.0,
            "target_x": screen_width // 2,
            "delay": i * 4,
            "bounce": 0
        })
    fade_alpha = 255
    frame = 0
    clicked_button_index = None

    def draw_animated_overlay(surface, t):
        overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        for y in range(0, screen_height, 4):
            brightness = int(30 + 25 * math.sin(y * 0.02 + t * 2))
            brightness = max(0, min(255, brightness))
            color = (0, brightness, 100, 30)
            pygame.draw.line(overlay, color, (0, y), (screen_width, y))
        surface.blit(overlay, (0, 0))

    while True:
        frame += 1
        t = pygame.time.get_ticks() / 1000
        screen.blit(bg_image, (0, 0))
        screen.blit(overlay, (0, 0))     
        draw_animated_overlay(screen, t)         
        if fade_alpha > 0:
            fade_alpha -= 5
        title1.set_alpha(255 - fade_alpha)
        title2.set_alpha(255 - fade_alpha)
        screen.blit(title1, title1_rect)
        screen.blit(title2, title2_rect)
        mouse = pygame.mouse.get_pos()
        for i, btn in enumerate(button_data):
            rect = btn["rect"]
            is_hover = rect.collidepoint(mouse)
            target_scale = 1.1 if is_hover else 1.0
            btn["hover"] += (target_scale - btn["hover"]) * 0.1
            scale = btn["hover"]
            if frame > btn["delay"]:
                dx = (btn["target_x"] - rect.centerx) * 0.08
                rect.centerx += int(dx + math.sin(t * 5 + i) * 0.5)
            scaled_rect = rect.inflate(rect.width * (scale - 1), rect.height * (scale - 1))
            glow = pygame.Surface(scaled_rect.size, pygame.SRCALPHA)
            pygame.draw.rect(glow, (0, 255, 200, 70), glow.get_rect(), border_radius=18)
            screen.blit(glow, scaled_rect.topleft)
            pygame.draw.rect(screen, (15, 15, 15), scaled_rect, border_radius=18)
            pygame.draw.rect(screen, (0, 255, 200), scaled_rect, 2, border_radius=18)
            label_surf = button_font.render(btn["label"], True, (255, 255, 255))
            label_rect = label_surf.get_rect(center=scaled_rect.center)
            screen.blit(label_surf, label_rect)
        pygame.display.flip()
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == MOUSEBUTTONDOWN:
                for i, btn in enumerate(button_data):
                    if btn["rect"].collidepoint(event.pos):
                        clicked_button_index = i
                        pygame.quit()
                        return clicked_button_index
