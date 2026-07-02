from dataclasses import dataclass


@dataclass
class _Layout:
    """Container for computed layout metrics used by the visualizer.

    Attributes:
        width (int): Total window width in pixels.
        height (int): Total window height in pixels.
        board_x (int): X origin of the main board area.
        board_y (int): Y origin of the main board area.
        board_width (int): Width of the board area in pixels.
        board_height (int): Height of the board area in pixels.
        sidebar_x (int): X origin of the sidebar area.
        sidebar_y (int): Y origin of the sidebar area.
        sidebar_width (int): Width of the sidebar in pixels.
        sidebar_height (int): Height of the sidebar in pixels.
        board_padding (int): Inner padding inside the board area.
    """
    width: int
    height: int
    board_x: int
    board_y: int
    board_width: int
    board_height: int
    sidebar_x: int
    sidebar_y: int
    sidebar_width: int
    sidebar_height: int
    board_padding: int
