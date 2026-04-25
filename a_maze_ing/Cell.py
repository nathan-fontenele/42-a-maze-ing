class Cell:
    """Represents a single cell in the maze grid."""
    def __init__(
        self,
        walls: int = 15,
        static: bool = False,
        visited: bool = False
    ) -> None:
        """Initialize the cell with all walls up by default."""
        self.walls: int = walls
        self.visited: bool = visited
        self.static: bool = static
        self.entrance: bool = False
        self.exit: bool = False
