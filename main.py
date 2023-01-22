# -*- coding: utf-8 -*-
"""
Python State Machine v0.1

Copyright (C) 2023 Yannis Maragos.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License version 2 only,
as published by the Free Software Foundation.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
import config
import pygame
import sys
import time


class States(object):
    def __init__(self):
        self.done = False
        self.quit = False
        self.target = None

    def get_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_F1:
                self.done = True
                self.target = 'state1'
            elif event.key == pygame.K_F2:
                self.done = True
                self.target = 'state2'
            elif event.key == pygame.K_SPACE:
                self.done = True
                self.target = 'menu'
            elif event.key == pygame.K_ESCAPE:
                self.done = True
                self.target = 'exit'

    def update(self):
        pass

    def draw(self):
        pass


class Menu(States):
    def __init__(self):
        States.__init__(self)

    def get_event(self, event):
        super(Menu, self).get_event(event)

    def cleanup(self):
        pass

    def startup(self):
        pass

    def ready(self):
        print('\nPress:')
        print('\'F1\' to run State1')
        print('\'F2\' to run State2')
        print('\'Space\' to show menu')
        print('\'Esc\' to exit program\n')

    def update(self):
        self.draw()
        super(Menu, self).update()

    def draw(self):
        super(Menu, self).draw()


class State1(States):
    def __init__(self):
        States.__init__(self)

    def get_event(self, event):
        super(State1, self).get_event(event)

    def cleanup(self):
        print('\n\n- Stopping State1')

    def startup(self):
        print('+ Starting State1')

    def ready(self):
        print('> Running State1 ', end='', flush=True)

    def update(self):
        self.draw()
        super(State1, self).update()

    def draw(self):
        print('.', end='', flush=True)
        super(State1, self).draw()


class State2(States):
    def __init__(self):
        States.__init__(self)

    def get_event(self, event):
        super(State2, self).get_event(event)

    def cleanup(self):
        print('\n\n- Stopping State2')

    def startup(self):
        print('+ Starting State2')

    def ready(self):
        print('> Running State2 ', end='', flush=True)

    def update(self):
        self.draw()
        super(State2, self).update()

    def draw(self):
        print('.', end='', flush=True)
        super(State2, self).draw()


class Exit(States):
    def __init__(self):
        States.__init__(self)

    def get_event(self, event):
        super(Exit, self).get_event(event)

    def cleanup(self):
        pass

    def startup(self):
        pass

    def ready(self):
        print('- Exiting program')
        self.quit = True

    def update(self):
        pass

    def draw(self):
        pass


class Control:
    """
    Controls the entire program.
    Switches between states.
    Contains:
        - current state
        - main game loop
        - main event loop
        - main update
        - main change state
    """

    def __init__(self, **settings):
        self.__dict__.update(settings)
        self.program_start = True
        self.quit = False

    def setup_states(self, state_dict, start_state):
        self.state_dict = state_dict
        self.state = self.state_dict[start_state]
        self.state.target = start_state

    def change_state(self):
        self.state.done = False  # reset current state otherwise it remains done forever
        self.state.cleanup()
        self.state = self.state_dict[self.state.target]  # set new state
        self.state.startup()
        self.state.ready()

    def update(self):
        if self.program_start == True:
            print('\nPress:')
            print('\'F1\' to run State1')
            print('\'F2\' to run State2')
            print('\'Space\' to show menu')
            print('\'Esc\' to exit program\n')

            self.program_start = False

        if self.state.quit:
            self.quit = True
        elif self.state.done:
            self.change_state()

        self.state.update()

    def event_loop(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit = True

            self.state.get_event(event)

    def main_loop(self):
        time_per_frame = 1 / self.fps

        print('+ Starting program')

        while not self.quit:
            # Start the timer
            start_time = time.time()

            # Perform the loop's operations
            self.event_loop()
            self.update()

            # Calculate the time taken for this iteration
            elapsed_time = time.time() - start_time

            # Calculate the time to sleep
            time_to_sleep = time_per_frame - elapsed_time

            # Sleep for the remaining time
            if time_to_sleep > 0:
                time.sleep(time_to_sleep)


def start():
    # Initialize pygame
    pygame.init()

    # In order to capture keyboard events using Pygame, you must initialize the Pygame display module (pygame.display) and create a window.
    # This window does not have to be visible, but it must be created in order for Pygame to receive and process keyboard events.
    window = pygame.display.set_mode(
        (config.WINDOW_WIDTH, config.WINDOW_HEIGHT))

    # Create dictionary of control settings
    settings = {
        'fps': config.FPS
    }

    # Start control
    app = Control(**settings)

    # Setup dictionary of states, so that we can reference objects when setting states
    state_dict = {
        'menu': Menu(),
        'state1': State1(),
        'state2': State2(),
        'exit': Exit(),
    }

    # Set initial state
    app.setup_states(state_dict, 'menu')

    # Start main loop
    app.main_loop()

    # Exit
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    start()
