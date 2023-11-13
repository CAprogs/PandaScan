import tkinter as tk
from foundation.core.essentials import INACTIVE_CURSOR, ACTIVE_CURSOR


def button_hover(button, button_image_1, button_image_2, Download_state=False):
    """Activer le Hover d'un bouton

    Args:
        button (Any): bouton de référence
        button_image_1 (Any): image par defaut
        button_image_2 (Any): image alternative
        Download_state (bool): état du bouton Download
    """
    def set_button_color(event, button, button_image, Download_state):
        """Associer une image à un bouton

        Args:
            event (Any): l'événement qui déclenche la fonction
            button (Any): bouton de référence
            button_image (Any): image à associer
            Download_state (bool): état du bouton Download
        """
        if Download_state is True:
            None
        else:
            button.configure(image=button_image)

    button.bind("<Enter>", lambda event: set_button_color(event, button, button_image_2, Download_state))
    button.bind("<Leave>", lambda event: set_button_color(event, button, button_image_1, Download_state))


def deactivate_button_hover(button):
    """Désactiver le Hover d'un bouton.

    Args:
        button (Any): bouton de référence
    """
    button.unbind("<Enter>")
    button.unbind("<Leave>")


def activate_button(button, button_image_1, button_image_2):
    """Activer un bouton

    Args:
        button (Any): bouton de référence
        button_image_1 (Any): image par défaut
        button_image_2 (Any): image alternative
    """
    button.config(image=button_image_1, state=tk.NORMAL, cursor=ACTIVE_CURSOR)
    button_hover(button, button_image_1, button_image_2)


def deactivate_button(button, button_image_2):
    """Désactiver un bouton

    Args:
        button (Any): bouton de référence
        button_image_2 (Any): image alternative
    """
    button.config(image=button_image_2, state=tk.DISABLED, cursor=INACTIVE_CURSOR)
    deactivate_button_hover(button)
