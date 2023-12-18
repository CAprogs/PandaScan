import tkinter as tk
from src.foundation.core.essentials import INACTIVE_CURSOR, ACTIVE_CURSOR


def button_hover(button, button_image_1, button_image_2, Download_state=False):
    """Enable button hover.

    Args:
        button (Any): the widget button
        button_image_1 (Any): default image
        button_image_2 (Any): alternative image
        Download_state (bool): download button state
    """
    def set_button_color(event, button, button_image, Download_state):
        """Associate an image with a button

        Args:
            event (Any): the event triggering the function
            button (Any): the widget button
            button_image (Any): the image to set
            Download_state (bool): download button state
        """
        if Download_state is True:
            None
        else:
            button.configure(image=button_image)

    button.bind("<Enter>", lambda event: set_button_color(event, button, button_image_2, Download_state))
    button.bind("<Leave>", lambda event: set_button_color(event, button, button_image_1, Download_state))


def deactivate_button_hover(button):
    """Disable button hover.

    Args:
        button (Any): the widget button
    """
    button.unbind("<Enter>")
    button.unbind("<Leave>")


def activate_button(button, button_image_1, button_image_2):
    """Activate a button

    Args:
        button (Any): the widget button
        button_image_1 (Any): default image
        button_image_2 (Any): alternative image
    """
    button.config(image=button_image_1, state=tk.NORMAL, cursor=ACTIVE_CURSOR)
    button_hover(button, button_image_1, button_image_2)


def deactivate_button(button, button_image_2):
    """Deactivate a button

    Args:
        button (Any): the widget button
        button_image_2 (Any): alternative image
    """
    button.config(image=button_image_2, state=tk.DISABLED, cursor=INACTIVE_CURSOR)
    deactivate_button_hover(button)


def manage_menu(menu, menu_list, menu_list_var):
    """Manage menu displayed items

    Args:
        menu (Any): the menu
        menu_list (list): menu's elements
        menu_list_var (str): element selected in the menu
    """

    menu['menu'].delete(0, 'end')
    for element in menu_list:
        if element != menu_list_var.get():
            menu['menu'].add_command(label=element, command=tk._setit(menu_list_var, element))
