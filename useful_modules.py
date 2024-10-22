import os
import sys
import termios
import time
import tty


def read_key():
  fd = sys.stdin.fileno()
  old_settings = termios.tcgetattr(fd)
  try:
    tty.setraw(fd)
    ch = sys.stdin.read(1)
  finally:
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
  return ch


def clear_console():
  os.system('cls' if os.name == 'nt' else 'clear')


def display_menu(menu_choices, selected_option):
  clear_console()
  for i, choice in enumerate(menu_choices):
    if i == selected_option:
      print(f"> {choice}")
    else:
      print(f"  {choice}")


def user_choice_select(menu_choices) -> str:
  if isinstance(menu_choices, dict):
      menu_choices = list(menu_choices.keys())
  user_choice_selection_loop = True
  selected_option_index = 0
  print(
      "Use the up and down arrow keys to navigate the menu and press enter to select an option."
  )
  time.sleep(2)
  while user_choice_selection_loop:
    display_menu(menu_choices, selected_option_index)
    key = read_key()
    if key == '\x1b':  # ESC sequence
      key += sys.stdin.read(2)
    if key == '\x1b[A':  # Up arrow
      selected_option_index = (selected_option_index - 1) % len(menu_choices)
    elif key == '\x1b[B':  # Down arrow
      selected_option_index = (selected_option_index + 1) % len(menu_choices)
    elif key == '\r':  # Enter key
        user_choice_selection_loop = False
    time.sleep(0.1)
  return menu_choices[selected_option_index]
