#!/usr/bin/env python3
"""
Vertex Pursuit: Motor Skill Assessment Game
===========================================

A low-fidelity surgical training simulator that challenges participants to trace
a star pentagon trajectory while performing concurrent spacebar tasks.

This experiment collects high-precision mouse trajectory data for motor skill
assessment research, capturing both movement patterns and dual-task performance.

Author: Arash Iranfar
License: MIT
"""

import pygame
import csv
import os
import time
import sys
from pathlib import Path
from pygame.locals import *

class VertexPursuitGame:
    """Main game class for the Vertex Pursuit motor skill assessment."""
    
    def __init__(self):
        """Initialize game components and settings."""
        pygame.init()
        
        # Game constants
        self.SCREEN_WIDTH = 1000
        self.SCREEN_HEIGHT = 1000
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.WHITE = (255, 255, 255)
        
        # Initialize display
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Vertex Pursuit: Motor Skill Assessment")
        
        # Load background image
        self._load_background()
        
        # Game state variables
        self.tracking = False
        self.mouse_positions = []
        self.space_event = 0
        self.start_time = 0
        self.save_prompt = False
        self.next_participant = False
        
        # Participant and trial management
        self.participant_number = self._get_next_participant_number()
        self.trial_number = 1
        self.max_trials = 5
        
        # Font for UI elements
        self.font = pygame.font.Font(None, 36)
    
    def _load_background(self):
        """Load and scale the background image."""
        background_path = Path(__file__).parent / "assets" / "background.jpg"
        
        try:
            self.background = pygame.image.load(str(background_path)).convert()
            self.background = pygame.transform.scale(
                self.background, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT)
            )
        except pygame.error as e:
            print(f"Warning: Could not load background image from {background_path}")
            print(f"Error: {e}")
            # Create a simple black background as fallback
            self.background = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
            self.background.fill(self.BLACK)
    
    def _get_next_participant_number(self):
        """Determine the next available participant number based on existing files."""
        data_dir = Path(__file__).parent / "data" / "raw" / "trajectories"
        data_dir.mkdir(parents=True, exist_ok=True)
        
        existing_files = list(data_dir.glob("SHSA_*.csv"))
        
        if not existing_files:
            return 1
        
        existing_numbers = []
        for file in existing_files:
            try:
                # Extract participant number from filename: SHSA_X_Y.csv
                parts = file.stem.split("_")
                if len(parts) >= 2:
                    existing_numbers.append(int(parts[1]))
            except (ValueError, IndexError):
                continue
        
        return max(existing_numbers, default=0) + 1
    
    def _display_message(self, message, color=None):
        """Display a message on screen."""
        if color is None:
            color = self.RED
        
        text_surface = self.font.render(message, True, color)
        # Center the text horizontally
        text_rect = text_surface.get_rect()
        text_rect.centerx = self.SCREEN_WIDTH // 2
        text_rect.y = 50
        self.screen.blit(text_surface, text_rect)
    
    def _save_trajectory_data(self):
        """Save collected mouse trajectory data to CSV file."""
        if not self.mouse_positions:
            print("Warning: No trajectory data to save")
            return False
        
        # Create data directory if it doesn't exist
        data_dir = Path(__file__).parent / "data" / "raw" / "trajectories"
        data_dir.mkdir(parents=True, exist_ok=True)
        
        filename = f"SHSA_{self.participant_number}_{self.trial_number}.csv"
        filepath = data_dir / filename
        
        try:
            with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['Timestamp', 'X', 'Y', 'Event'])
                
                for timestamp, x, y, event in self.mouse_positions:
                    writer.writerow([timestamp, x, y, event])
            
            print(f"✓ Saved trial data: {filename}")
            return True
            
        except IOError as e:
            print(f"Error saving file {filepath}: {e}")
            return False
    
    def _handle_keydown(self, key):
        """Process keyboard input events."""
        if key == K_s and not self.next_participant:
            # Start tracking
            self.tracking = True
            self.start_time = time.time()
            self.mouse_positions = []
            print(f"Started tracking - Participant {self.participant_number}, Trial {self.trial_number}")
            
        elif key == K_q:
            # Stop tracking and prompt for save
            self.tracking = False
            self.save_prompt = True
            print("Tracking stopped - Save prompt displayed")
            
        elif key == K_y and self.save_prompt:
            # Confirm save
            if self._save_trajectory_data():
                self.trial_number += 1
                if self.trial_number > self.max_trials:
                    self.next_participant = True
                    print(f"All trials completed for participant {self.participant_number}")
            
            self.save_prompt = False
            
        elif key == K_n and self.save_prompt:
            # Cancel save
            print("Trial discarded")
            self.save_prompt = False
            
        elif key == K_y and self.next_participant:
            # Move to next participant
            self.participant_number += 1
            self.trial_number = 1
            self.next_participant = False
            print(f"Moving to participant {self.participant_number}")
            
        elif key == K_n and self.next_participant:
            # Stay with current participant
            self.next_participant = False
            print("Continuing with current participant")
            
        elif key == K_SPACE:
            # Spacebar press event
            self.space_event = 1
            
        elif key == K_ESCAPE:
            # Quick exit
            return False
            
        return True
    
    def _handle_keyup(self, key):
        """Process key release events."""
        if key == K_SPACE:
            self.space_event = 0
    
    def _handle_mouse_motion(self, pos):
        """Process mouse movement during tracking."""
        if self.tracking:
            x, y = pos
            timestamp = time.time() - self.start_time
            self.mouse_positions.append((timestamp, x, y, self.space_event))
    
    def _render_trajectory(self):
        """Draw the current trajectory on screen."""
        if self.tracking and len(self.mouse_positions) > 1:
            points = [(pos[1], pos[2]) for pos in self.mouse_positions]
            pygame.draw.lines(self.screen, self.RED, False, points, width=3)
    
    def _render_ui(self):
        """Render user interface elements."""
        # Status information
        status_text = f"Participant: {self.participant_number} | Trial: {self.trial_number}/{self.max_trials}"
        status_surface = pygame.font.Font(None, 24).render(status_text, True, self.WHITE)
        self.screen.blit(status_surface, (10, 10))
        
        # Show prompts
        if self.save_prompt:
            self._display_message("Save this trial? (Y/N)")
        elif self.next_participant:
            self._display_message("Move to next participant? (Y/N)")
        elif not self.tracking:
            self._display_message("Press 'S' to start tracking | 'Q' to stop | ESC to quit", self.WHITE)
    
    def run(self):
        """Main game loop."""
        clock = pygame.time.Clock()
        running = True
        
        print("=== Vertex Pursuit Motor Skill Assessment ===")
        print("Controls:")
        print("  S - Start tracking")
        print("  Q - Stop tracking")
        print("  SPACE - Event marker")
        print("  Y/N - Confirm/Cancel prompts")
        print("  ESC - Quit")
        print("=" * 45)
        
        while running:
            # Handle events
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                    
                elif event.type == KEYDOWN:
                    if not self._handle_keydown(event.key):
                        running = False
                        
                elif event.type == KEYUP:
                    self._handle_keyup(event.key)
                    
                elif event.type == MOUSEMOTION:
                    self._handle_mouse_motion(event.pos)
            
            # Render frame
            self.screen.blit(self.background, (0, 0))
            self._render_trajectory()
            self._render_ui()
            
            pygame.display.flip()
            clock.tick(60)  # 60 FPS
        
        pygame.quit()
        print("Game session ended.")


def main():
    """Entry point for the Vertex Pursuit game."""
    try:
        game = VertexPursuitGame()
        game.run()
    except KeyboardInterrupt:
        print("\nGame interrupted by user")
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()