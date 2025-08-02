#!/usr/bin/env python3
"""
Vertex Pursuit: Replay Viewer
=============================

A replay system for reviewing recorded Vertex Pursuit trials, allowing evaluators
to analyze participant performance with visual feedback including trajectory paths
and spacebar event markers.

Features:
- Real-time trajectory playback with original timing
- Persistent spacebar event visualization (red circles)
- Pause/resume functionality for detailed analysis
- File selection interface for reviewing specific trials

Authors: [Your names here]
License: MIT
"""

import pygame
import csv
import os
import time
import sys
from pathlib import Path
from pygame.locals import *

class VertexPursuitReplay:
    """Replay viewer for Vertex Pursuit motor skill assessment trials."""
    
    def __init__(self):
        """Initialize replay system components."""
        pygame.init()
        
        # Display constants
        self.SCREEN_WIDTH = 1000
        self.SCREEN_HEIGHT = 1000
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.WHITE = (255, 255, 255)
        self.BLUE = (0, 0, 255)
        self.GREEN = (0, 255, 0)
        
        # Initialize display
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Vertex Pursuit: Replay Viewer")
        
        # Load background
        self._load_background()
        
        # Initialize fonts
        self.font_small = pygame.font.Font(None, 24)
        self.font_medium = pygame.font.Font(None, 32)
        
        # Replay state
        self.is_paused = True
        self.spacebar_events = []  # Store all spacebar event positions for persistent display
        
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
            print(f"Using white background as fallback")
            # Create white background as fallback
            self.background = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
            self.background.fill(self.WHITE)
    
    def _get_data_file_path(self, participant_number, trial_number):
        """Construct file path for trajectory data."""
        data_dir = Path(__file__).parent / "data" / "raw" / "trajectories"
        filename = f"SHSA_{participant_number}_{trial_number}.csv"
        return data_dir / filename
    
    def _display_status_message(self, message, color=None):
        """Display status message in bottom-left corner."""
        if color is None:
            color = self.BLACK
            
        text_surface = self.font_small.render(message, True, color)
        # Position in bottom-left corner with padding
        self.screen.blit(text_surface, (10, self.SCREEN_HEIGHT - 30))
    
    def _load_trial_data(self, filepath):
        """Load and validate trial data from CSV file."""
        try:
            with open(filepath, 'r', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                header = next(reader)  # Skip header
                
                # Validate header format
                expected_header = ['Timestamp', 'X', 'Y', 'Event']
                if header != expected_header:
                    print(f"Warning: Unexpected header format: {header}")
                
                # Load and validate data
                events_data = []
                for row_num, row in enumerate(reader, start=2):
                    try:
                        timestamp = float(row[0])
                        x = int(row[1])
                        y = int(row[2])
                        event = int(row[3])
                        events_data.append((timestamp, x, y, event))
                    except (ValueError, IndexError) as e:
                        print(f"Warning: Invalid data in row {row_num}: {row}")
                        continue
                
                if not events_data:
                    raise ValueError("No valid data found in file")
                    
                return events_data
                
        except FileNotFoundError:
            raise FileNotFoundError(f"Trial data file not found: {filepath}")
        except Exception as e:
            raise Exception(f"Error loading trial data: {e}")
    
    def _draw_trajectory_segment(self, start_pos, end_pos):
        """Draw a single trajectory segment."""
        if start_pos != (-1, -1):
            pygame.draw.line(self.screen, self.RED, start_pos, end_pos, width=5)
    
    def _draw_spacebar_events(self):
        """Draw all recorded spacebar event positions as persistent circles."""
        for pos in self.spacebar_events:
            # Draw filled circle for spacebar events
            pygame.draw.circle(self.screen, self.RED, pos, 10)
            # Draw outline for better visibility
            # pygame.draw.circle(self.screen, self.BLACK, pos, 10, 2)
    
    def _replay_trial(self, filepath):
        """Replay a single trial with trajectory and event visualization."""
        try:
            # Load trial data
            events_data = self._load_trial_data(filepath)
            print(f"✓ Loaded {len(events_data)} data points from {filepath.name}")
            
            # Initialize replay state
            counter = 0
            previous_position = (-1, -1)
            previous_timestamp = 0
            self.spacebar_events = []  # Reset spacebar events for new trial
            clock = pygame.time.Clock()
            
            # Clear screen and show initial message
            self.screen.blit(self.background, (0, 0))
            self._display_status_message("Press P to start replay")
            pygame.display.flip()
            
            # Main replay loop
            while counter < len(events_data):
                # Handle events
                for event in pygame.event.get():
                    if event.type == QUIT:
                        return -1
                    elif event.type == KEYDOWN:
                        if event.key == K_p:
                            self.is_paused = not self.is_paused
                            status = "Paused" if self.is_paused else "Playing"
                            print(f"Replay {status}")
                        elif event.key == K_q:
                            print("Replay stopped by user")
                            return -1
                        elif event.key == K_r:
                            print("Restarting replay...")
                            return 1
                
                # Process current data point if not paused
                if not self.is_paused:
                    timestamp, x, y, spacebar_event = events_data[counter]
                    current_position = (x, y)
                    
                    # Draw trajectory segment
                    self._draw_trajectory_segment(previous_position, current_position)
                    
                    # Record spacebar events for persistent display
                    if spacebar_event == 1:
                        self.spacebar_events.append(current_position)
                    
                    # Draw all spacebar events (persistent)
                    self._draw_spacebar_events()
                    
                    # Calculate and apply timing delay
                    if counter > 0:
                        delay = timestamp - previous_timestamp
                        if delay > 0:
                            time.sleep(min(delay, 0.1))  # Cap delay to prevent long pauses
                    
                    previous_position = current_position
                    previous_timestamp = timestamp
                    counter += 1
                
                # Update display and status
                progress = f"Progress: {counter}/{len(events_data)} ({counter/len(events_data)*100:.1f}%)"
                status = "PAUSED - Press P to resume" if self.is_paused else "PLAYING - Press P to pause"
                
                self._display_status_message(f"{status} | {progress} | Q: Quit | R: Restart")
                pygame.display.flip()
                clock.tick(60)  # Maintain smooth frame rate
            
            # Replay completed
            self._display_status_message("Replay completed - Press R for new trial")
            pygame.display.flip()
            print("✓ Replay completed successfully")
            return 0
            
        except Exception as e:
            print(f"Error during replay: {e}")
            return -1
    
    def _get_trial_selection(self):
        """Get participant and trial numbers from user input."""
        try:
            print("\n" + "="*50)
            print("TRIAL SELECTION")
            print("="*50)
            
            participant_num = input("Enter participant number (1-24): ").strip()
            trial_num = input("Enter trial number (1-5): ").strip()
            
            # Validate input
            participant_number = int(participant_num)
            trial_number = int(trial_num)
            
            if not (1 <= participant_number <= 24):
                raise ValueError("Participant number must be between 1 and 24")
            if not (1 <= trial_number <= 5):
                raise ValueError("Trial number must be between 1 and 5")
                
            return participant_number, trial_number
            
        except ValueError as e:
            print(f"Invalid input: {e}")
            return None, None
        except KeyboardInterrupt:
            print("\nSelection cancelled by user")
            return None, None
    
    def run(self):
        """Main application loop."""
        print("=== Vertex Pursuit Replay Viewer ===")
        print("Controls:")
        print(" R - Load new trial")
        print(" P - Play/Pause replay")
        print(" Q - Stop current replay")
        print(" ESC/Close - Quit application")
        print("="*37)
        
        running = True
        clock = pygame.time.Clock()
        
        # Initial screen setup
        self.screen.blit(self.background, (0, 0))
        self._display_status_message("Press R to load a trial for replay")
        pygame.display.flip()
        
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_r:
                        # Load and replay new trial
                        participant_num, trial_num = self._get_trial_selection()
                        
                        if participant_num is not None and trial_num is not None:
                            filepath = self._get_data_file_path(participant_num, trial_num)
                            
                            if filepath.exists():
                                print(f"Loading trial: Participant {participant_num}, Trial {trial_num}")
                                self.is_paused = True  # Reset pause state
                                
                                # Clear screen for new replay
                                self.screen.blit(self.background, (0, 0))
                                pygame.display.flip()
                                
                                result = self._replay_trial(filepath)
                                if result == -1:
                                    running = False
                            else:
                                print(f"✗ File not found: {filepath}")
                                print("Please check participant and trial numbers")
                    
                    elif event.key == K_ESCAPE:
                        running = False
            
            clock.tick(60)
        
        pygame.quit()
        print("Replay viewer closed")


def main():
    """Entry point for the Vertex Pursuit replay viewer."""
    try:
        viewer = VertexPursuitReplay()
        viewer.run()
    except KeyboardInterrupt:
        print("\nApplication interrupted by user")
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()