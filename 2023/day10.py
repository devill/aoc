import unittest

def print_table(table):
    print('\n'.join([''.join(row) for row in table]))

# Constants for pipe shapes
NS = "|"
WE = "-"
NE = "L"
NW = "J"
WS = "7"
SE = "F"
GROUND = "."
START = "S"

HEADING_SOUTH = (0, 1)
HEADING_EAST = (1, 0)
HEADING_NORTH = (0, -1)
HEADING_WEST = (-1, 0)
BLOCKED = (0, 0)

class TestMazeSolver(unittest.TestCase):
    def test_parse_input(self):
        input_str = (
            ".F-7.\n"
            ".S-7.\n"
            ".|.|.\n"
            ".L-J.\n"
            "....."
        )
        expected_output = [
            [".", "F", "-", "7", "."],
            [".", "S", "-", "7", "."],
            [".", "|", ".", "|", "."],
            [".", "L", "-", "J", "."],
            [".", ".", ".", ".", "."]
        ]
        self.assertEqual(parse_input(input_str), expected_output)

    def test_next_direction(self):
        self.assertEqual(next_direction(HEADING_SOUTH, NS), HEADING_SOUTH)
        self.assertEqual(next_direction(HEADING_NORTH, NS), HEADING_NORTH)
        self.assertEqual(next_direction(HEADING_EAST, WE), HEADING_EAST)
        self.assertEqual(next_direction(HEADING_WEST, WE), HEADING_WEST)
        self.assertEqual(next_direction(HEADING_SOUTH, NE), HEADING_EAST)
        self.assertEqual(next_direction(HEADING_WEST, NE), HEADING_NORTH)
        self.assertEqual(next_direction(HEADING_SOUTH, NW), HEADING_WEST)
        self.assertEqual(next_direction(HEADING_EAST, NW), HEADING_NORTH)
        self.assertEqual(next_direction(HEADING_EAST, WS), HEADING_SOUTH)
        self.assertEqual(next_direction(HEADING_NORTH, WS), HEADING_WEST)
        self.assertEqual(next_direction(HEADING_NORTH, SE), HEADING_EAST)
        self.assertEqual(next_direction(HEADING_WEST, SE), HEADING_SOUTH)

    def test_invalid_direction(self):
        self.assertEqual(next_direction(HEADING_EAST, NS), BLOCKED)
        self.assertEqual(next_direction(HEADING_WEST, NS), BLOCKED)
        self.assertEqual(next_direction(HEADING_NORTH, WE), BLOCKED)
        self.assertEqual(next_direction(HEADING_SOUTH, WE), BLOCKED)
        self.assertEqual(next_direction(HEADING_NORTH, GROUND), BLOCKED)
        self.assertEqual(next_direction(HEADING_EAST, GROUND), BLOCKED)
        self.assertEqual(next_direction(HEADING_SOUTH, GROUND), BLOCKED)
        self.assertEqual(next_direction(HEADING_WEST, GROUND), BLOCKED)

    def test_entering_start_tile(self):
        self.assertEqual(next_direction(HEADING_NORTH, START), HEADING_NORTH)
        self.assertEqual(next_direction(HEADING_SOUTH, START), HEADING_SOUTH)
        self.assertEqual(next_direction(HEADING_EAST, START), HEADING_EAST)
        self.assertEqual(next_direction(HEADING_WEST, START), HEADING_WEST)

    def test_find_starting_point(self):
        maze = [
            [".", "F", "-", "7", "."],
            [".", "S", "-", "7", "."],
            [".", "|", ".", "|", "."],
            [".", "L", "-", "J", "."],
            [".", ".", ".", ".", "."]
        ]
        expected_start = (1, 1)  # Row 1, Column 1
        solver = MazeSolver(maze)
        self.assertEqual(solver.starting_point, expected_start)

    def test_next_coordinate_and_heading(self):
        maze = [
            [".", "F", "-", "7", "."],
            ["7", "S", "-", "7", "L"],
            [".", "|", ".", "|", "."],
            [".", "L", "-", "J", "."],
            [".", ".", ".", ".", "."]
        ]
        solver = MazeSolver(maze)

        # Starting from S and heading east
        next_coord_heading = solver.next_coordinate_and_heading(solver.starting_point, HEADING_EAST)
        expected = ((1, 2), HEADING_EAST)  # Should move to the right and keep heading east
        self.assertEqual(next_coord_heading, expected)

    def test_find_furthest_point(self):
        maze = [
            [".", "F", "-", "7", "."],
            ["7", "S", "-", "7", "L"],
            [".", "|", ".", "|", "."],
            [".", "L", "-", "J", "."],
            [".", ".", ".", ".", "."]
        ]
        solver = MazeSolver(maze)
        furthest_steps = solver.find_furthest_point()
        expected_steps = 4  # Expected number of steps to the furthest point
        self.assertEqual(furthest_steps, expected_steps)

    def test_mark_loop_tiles(self):
        maze = [
            [".", "F", "-", "7", "."],
            ["7", "S", "-", "7", "L"],
            [".", "|", ".", "|", "."],
            [".", "L", "-", "J", "."],
            [".", ".", ".", ".", "."]
        ]
        solver = MazeSolver(maze)
        expected_loop = [
            [".", ".", ".", ".", "."],
            [".", "X", "X", "X", "."],
            [".", "X", ".", "X", "."],
            [".", "X", "X", "X", "."],
            [".", ".", ".", ".", "."]
        ]
        self.assertEqual(solver.loop, expected_loop)

    def test_identify_enclosed_tiles(self):

        maze = [
            [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", "S", "-", "-", "-", "-", "-", "-", "-", "7", "."],
            [".", "|", "F", "-", "-", "-", "-", "-", "7", "|", "."],
            [".", "|", "|", ".", ".", ".", ".", ".", "|", "|", "."],
            [".", "|", "|", ".", ".", ".", ".", ".", "|", "|", "."],
            [".", "|", "L", "-", "7", ".", "F", "-", "J", "|", "."],
            [".", "|", ".", ".", "|", ".", "|", ".", ".", "|", "."],
            [".", "L", "-", "-", "J", ".", "L", "-", "-", "J", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."]
        ]
        solver = MazeSolver(maze)
        enclosed_tiles = solver.identify_enclosed_tiles()
        expected_enclosed = [
            [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", "X", "X", ".", ".", ".", "X", "X", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."]
        ]
        self.assertEqual(enclosed_tiles, expected_enclosed)


    def test_enclosed_area(self):

        maze = [
            [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
            [".", "S", "-", "-", "-", "-", "-", "-", "-", "7", "."],
            [".", "|", "F", "-", "-", "-", "-", "-", "7", "|", "."],
            [".", "|", "|", ".", ".", ".", ".", ".", "|", "|", "."],
            [".", "|", "|", ".", ".", ".", ".", ".", "|", "|", "."],
            [".", "|", "L", "-", "7", ".", "F", "-", "J", "|", "."],
            [".", "|", ".", ".", "|", ".", "|", ".", ".", "|", "."],
            [".", "L", "-", "-", "J", ".", "L", "-", "-", "J", "."],
            [".", ".", ".", ".", ".", ".", ".", ".", ".", ".", "."]
        ]
        solver = MazeSolver(maze)
        enclosed_tiles = solver.enclosed_area()
        expected_enclosed = 4
        self.assertEqual(enclosed_tiles, expected_enclosed)

    def test_process_single_line(self):
        solver = MazeSolver([])
        maze_row = list(".F--J..L-7..F--7.|..LJ.|..")
        loop_row = list(".XXXX..XXX..XXXX.X..XX.X..")
        expected = list(".....XX...........XX..X...")

        enclosed_tiles = solver.process_single_line(maze_row, loop_row)
        self.assertEqual(enclosed_tiles, expected)

    def test_infer_start_tile_shape(self):
        solver = MazeSolver([])  # Empty maze for testing purposes

        # Test different scenarios
        self.assertEqual(solver.infer_start_tile_shape(HEADING_NORTH, HEADING_WEST), NE)
        self.assertEqual(solver.infer_start_tile_shape(HEADING_SOUTH, HEADING_WEST), SE)
        self.assertEqual(solver.infer_start_tile_shape(HEADING_NORTH, HEADING_EAST), NW)

    def test_real_input(self):
        with open("input10.txt", 'r') as file:
            puzzle_input = file.read()

            # Parsing the puzzle input
            puzzle_maze = parse_input(puzzle_input)

            # Creating an instance of MazeSolver with the puzzle maze
            solver = MazeSolver(puzzle_maze)

            # Finding the result of find_furthest_point
            furthest_point_steps = solver.find_furthest_point()
            self.assertEqual(furthest_point_steps, 6754)

            enclosed_area = solver.enclosed_area()
            self.assertEqual(enclosed_area, 567)

def parse_input(input_str):
    return [list(line) for line in input_str.split('\n') if line]

direction_map = {
    (HEADING_SOUTH, NS): HEADING_SOUTH,
    (HEADING_NORTH, NS): HEADING_NORTH,
    (HEADING_EAST, WE): HEADING_EAST,
    (HEADING_WEST, WE): HEADING_WEST,
    (HEADING_SOUTH, NE): HEADING_EAST,
    (HEADING_WEST, NE): HEADING_NORTH,
    (HEADING_SOUTH, NW): HEADING_WEST,
    (HEADING_EAST, NW): HEADING_NORTH,
    (HEADING_EAST, WS): HEADING_SOUTH,
    (HEADING_NORTH, WS): HEADING_WEST,
    (HEADING_NORTH, SE): HEADING_EAST,
    (HEADING_WEST, SE): HEADING_SOUTH
}
def next_direction(current_direction, pipe_shape):
    if pipe_shape == START:
        return current_direction
    return direction_map.get((current_direction, pipe_shape), BLOCKED)

class MazeSolver:
    def __init__(self, maze):
        self.maze = maze
        self.starting_point = self.find_starting_point()
        if len(self.maze) > 0:
            self.process_maze()

    def process_maze(self):
        for heading in [HEADING_NORTH, HEADING_EAST, HEADING_SOUTH, HEADING_WEST]:
            self.loop_length = 0
            self.loop = [["."] * len(row) for row in self.maze]
            current = (self.starting_point, heading)

            while True:
                coord, head = self.next_coordinate_and_heading(*current)
                if head == BLOCKED:
                    break
                x, y = coord
                self.loop[x][y] = 'X'
                current = (coord, head)
                self.loop_length += 1

                if coord == self.starting_point:
                    start_shape = self.infer_start_tile_shape(heading, head)
                    self.maze[x][y] = start_shape
                    return

    def infer_start_tile_shape(self, heading, head):
        return {
            (HEADING_NORTH, HEADING_NORTH): NS,
            (HEADING_NORTH, HEADING_EAST): NW,
            (HEADING_NORTH, HEADING_WEST): NE,
            (HEADING_EAST, HEADING_NORTH): SE,
            (HEADING_EAST, HEADING_EAST): WE,
            (HEADING_EAST, HEADING_SOUTH): NE,
            (HEADING_SOUTH, HEADING_EAST): WS,
            (HEADING_SOUTH, HEADING_SOUTH): NS,
            (HEADING_SOUTH, HEADING_WEST): SE,
            (HEADING_WEST, HEADING_NORTH): WS,
            (HEADING_WEST, HEADING_SOUTH): NW,
            (HEADING_WEST, HEADING_WEST): WE
        }[heading, head]

    def find_starting_point(self):
        for i, row in enumerate(self.maze):
            for j, cell in enumerate(row):
                if cell == START:
                    return (i, j)

    def next_coordinate_and_heading(self, coordinate, heading):
        x, y = coordinate
        dx, dy = heading

        next_x, next_y = x + dy, y + dx

        if 0 <= next_x < len(self.maze) and 0 <= next_y < len(self.maze[0]):
            next_cell = self.maze[next_x][next_y]
            new_heading = next_direction(heading, next_cell)
        else:
            new_heading = BLOCKED

        return (next_x, next_y), new_heading

    def find_furthest_point(self):
        return int(self.loop_length / 2)

    def identify_enclosed_tiles(self):
        if not self.loop:
            return None

        result = []  # Initialize result with empty tiles

        for i, row in enumerate(self.loop):
            result.append(self.process_single_line(self.maze[i], row))


        return result

    def process_single_line(self, maze_row, loop_row):
        is_inside = False
        result_row = ["." for _ in maze_row]
        boundary_from = None

        for i, (tile, loop_tile) in enumerate(zip(maze_row, loop_row)):
            if loop_tile == 'X':  # Boundary tile
                if tile == NS:
                    is_inside = not is_inside
                elif tile == NE:
                    boundary_from = "North"
                elif tile == SE:
                    boundary_from = "South"
                elif tile == NW:
                    if boundary_from == "South":
                        is_inside = not is_inside
                    boundary_from = None
                elif tile == WS:
                    if boundary_from == "North":
                        is_inside = not is_inside
                    boundary_from = None
                elif tile == WE:
                    pass
                else:
                    raise Exception("Impossible case", tile, is_inside, boundary_from)
            else:
                if is_inside and boundary_from == None:
                    result_row[i] = 'X'

        return result_row

    def enclosed_area(self):
        enclosed_tiles = self.identify_enclosed_tiles()
        if not enclosed_tiles:
            return 0
        return sum(row.count('X') for row in enclosed_tiles)

    def illustrate(self, enclosed):
        result = []
        for i, enclosed_row in enumerate(enclosed):
            result_row = []
            for j, enclosed_tile in enumerate(enclosed_row):
                if self.loop[i][j] == 'X':
                    result_row.append(self.maze[i][j])
                elif enclosed_tile == 'X':
                    result_row.append('.')
                else:
                    result_row.append(' ')
            result.append(result_row)
        return result

if __name__ == '__main__':
    unittest.main()