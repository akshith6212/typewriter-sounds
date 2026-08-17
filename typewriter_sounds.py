import sys
import os
from pynput import keyboard
import pygame


class TypeWriterSounds:
    """
    Typewriter sounds emulator for Python
    =====================================

    This program plays typewriter sounds each time a key is pressed, giving
    the user the vintage experience of an old typewriter machine.

    Listens for global keyboard events using pynput (cross-platform) and
    plays sounds via pygame.

    Sound samples come from https://www.freesound.org/, some were modified
    for this project.

    Requirements
    ------------

    -  Python 3.8+
    -  pynput (https://github.com/moses-palmer/pynput)
    -  pygame 2.x (https://pygame.org)

    Usage
    -----

    cd into the project's directory and type::

        $ python typewriter_sounds.py

    To stop the program, type CTRL-C.

    Author
    ------

    Manuel Arturo Izquierdo aizquier@gmail.com
    """

    SHIFT_KEYS = frozenset([
        keyboard.Key.up, keyboard.Key.down, keyboard.Key.left, keyboard.Key.right,
        keyboard.Key.ctrl_l, keyboard.Key.ctrl_r,
        keyboard.Key.shift_l, keyboard.Key.shift_r,
        keyboard.Key.alt_l, keyboard.Key.alt_r,
        keyboard.Key.tab, keyboard.Key.caps_lock,
        keyboard.Key.f1, keyboard.Key.f2, keyboard.Key.f3, keyboard.Key.f4,
        keyboard.Key.f5, keyboard.Key.f6, keyboard.Key.f7, keyboard.Key.f8,
        keyboard.Key.f9, keyboard.Key.f10, keyboard.Key.f11, keyboard.Key.f12,
        keyboard.Key.cmd_l, keyboard.Key.cmd_r,
        keyboard.Key.esc,
    ])

    LOAD_KEYS = frozenset([
        keyboard.Key.page_up, keyboard.Key.page_down,
        keyboard.Key.home, keyboard.Key.end,
    ])

    def __init__(self):
        pygame.mixer.init(buffer=512)

        self.bellcount = 0

        samples_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'samples')
        self.keysounds = {
            'load': pygame.mixer.Sound(os.path.join(samples_dir, 'manual_load_long.wav')),
            'shift': pygame.mixer.Sound(os.path.join(samples_dir, 'manual_shift.wav')),
            'delete': pygame.mixer.Sound(os.path.join(samples_dir, 'manual_backspace.wav')),
            'space': pygame.mixer.Sound(os.path.join(samples_dir, 'manual_space.wav')),
            'key': pygame.mixer.Sound(os.path.join(samples_dir, 'manual_key.wav')),
            'enter': pygame.mixer.Sound(os.path.join(samples_dir, 'manual_return.wav')),
            'bell': pygame.mixer.Sound(os.path.join(samples_dir, 'manual_bell.wav')),
        }

        print("TypeWriter Sounds Emulator. v1.0")
        print("type now and enjoy the vintage experience!...")
        self.keysounds['bell'].play()
        self.keysounds['enter'].play()

        with keyboard.Listener(on_press=self.on_key_press) as listener:
            try:
                listener.join()
            except KeyboardInterrupt:
                print('\nbye!')
                sys.exit(0)

    def on_key_press(self, key):
        if key == keyboard.Key.enter:
            self.keysounds['enter'].play()
            self.bellcount = 0
        elif key == keyboard.Key.space:
            self.keysounds['space'].play()
            self.bellcount += 1
        elif key in (keyboard.Key.delete, keyboard.Key.backspace):
            self.keysounds['delete'].play()
            self.bellcount = max(0, self.bellcount - 1)
        elif key in self.SHIFT_KEYS:
            self.keysounds['shift'].play()
        elif key in self.LOAD_KEYS:
            self.keysounds['load'].play()
        else:
            self.keysounds['key'].play()
            self.bellcount += 1

        if self.bellcount == 70:
            self.keysounds['bell'].play()
            self.bellcount = 0


if __name__ == '__main__':
    TypeWriterSounds()
