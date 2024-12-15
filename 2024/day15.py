import os
from utils import data_files_for

ROBOT = "@"
BOX = "O"
BIG_BOX_LEFT = "["
BIG_BOX_RIGHT = "]"
WALL = "#"
EMPTY = "."


class WareHouseParser:
    def __init__(self, raw_data):
        self.raw_data = raw_data

    def parse(self):
        raw_ware_house_map, raw_moves = self.raw_data.split("\n\n")
        ware_house_map = [list(row.strip()) for row in raw_ware_house_map.split("\n")]
        moves = [self.__get_direction(d) for d in ''.join(raw_moves.split()).strip()]
        return moves, ware_house_map

    def __get_direction(self, direction):
        if direction == "<":
            return (-1, 0)
        elif direction == ">":
            return (1, 0)
        elif direction == "^":
            return (0, -1)
        elif direction == "v":
            return (0, 1)


def enlarge_warehouse(ware_house_map):
    conversion = {
        ROBOT: [ROBOT, EMPTY],
        BOX: [BIG_BOX_LEFT, BIG_BOX_RIGHT],
        WALL: [WALL, WALL],
        EMPTY: [EMPTY, EMPTY]
    }

    enlarged_map = []
    for row in ware_house_map:
        new_row = []
        for cell in row:
            new_row.extend(conversion[cell])
        enlarged_map.append(new_row)
    return enlarged_map


class WareHousePosition:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def add(self, direction):
        return WareHousePosition(self.x + direction[0], self.y + direction[1])

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return f"({self.x}, {self.y})"


class WareHouse:
    def __init__(self, ware_house_map):
        self.ware_house_map = [line.copy() for line in ware_house_map]
        self.robot_position = self.find_robot()

    def find_robot(self):
        for y, row in enumerate(self.ware_house_map):
            for x, cell in enumerate(row):
                if cell == ROBOT:
                    return WareHousePosition(x, y)
        raise ValueError("No robot found")

    def get_box_positions(self, position):
        if self.get_at(position) == BOX:
            return [position]
        if self.get_at(position) == BIG_BOX_LEFT:
            return [position, position.add((1, 0))]
        if self.get_at(position) == BIG_BOX_RIGHT:
            return [position.add((-1, 0)), position]
        raise ValueError("Not a box")

    def get_box_targets(self, position, direction):
        if self.get_at(position) == BOX:
            return [position.add(direction)]
        if self.is_vertical(direction):
            return [p.add(direction) for p in self.get_box_positions(position)]
        else:
            return [position.add(direction).add(direction)]

    def is_box_at(self, position):
        return self.get_at(position) in [BOX, BIG_BOX_LEFT, BIG_BOX_RIGHT]

    def can_move_box(self, position, direction):
        if self.get_at(position) == EMPTY:
            return True
        if self.get_at(position) == WALL:
            return False
        if self.is_box_at(position):
            return all(
                self.can_move_box(p, direction) for p in self.get_box_targets(position, direction)
            )
        raise ValueError("Unknown cell type " + self.get_at(position))

    def can_move_robot(self, direction):
        if self.get_at(self.robot_position.add(direction)) == WALL:
            return False
        if self.is_box_at(self.robot_position.add(direction)):
            return self.can_move_box(self.robot_position.add(direction), direction)
        return True

    def move_robot(self, direction):
        if self.can_move_robot(direction):
            self.move_box(self.robot_position.add(direction), direction)
            self.set_at(self.robot_position, EMPTY)
            self.robot_position = self.robot_position.add(direction)
            self.set_at(self.robot_position, ROBOT)

    def move_box(self, position, direction):
        if self.get_at(position) == WALL:
            raise ValueError("Cannot move box into wall")
        if self.is_box_at(position):
            for p in self.get_box_targets(position, direction):
                self.move_box(p, direction)
            self.move_one_box(position, direction)

    def move_one_box(self, position, direction):
        if self.get_at(position) == BOX:
            self.set_at(position.add(direction), BOX)
            self.set_at(position, EMPTY)
        else:
            big_box_positions = self.get_box_positions(position)
            if self.is_vertical(direction):
                for p in big_box_positions:
                    self.set_at(p.add(direction), self.get_at(p))
                    self.set_at(p, EMPTY)
            else:
                self.set_at(position.add(direction).add(direction), self.get_at(position.add(direction)))
                self.set_at(position.add(direction), self.get_at(position))
                self.set_at(position, EMPTY)

    def get_at(self, position):
        return self.ware_house_map[position.y][position.x]

    def set_at(self, position, value):
        self.ware_house_map[position.y][position.x] = value

    def apply_moves(self, moves):
        for direction in moves:
            self.move_robot(direction)

    def is_vertical(self, direction):
        return direction[0] == 0

    def box_gps(self):
        return [y * 100 + x for y, row in enumerate(self.ware_house_map) for x, cell in enumerate(row) if
                cell in [BOX, BIG_BOX_LEFT]]

    def __repr__(self):
        return "\n".join("".join(row) for row in self.ware_house_map)

    def draw(self):
        print(self, end="\n\n")


def get_expected_result(meta, part):
    if meta["type"] == "real":
        return expected_results["real"][f"part {part}"]
    else:
        return expected_results["tests"][int(meta["sequence_id"])][f"part {part}"]


if __name__ == "__main__":
    all_as_expected = True
    expected_results = {
        "tests":
            [
                {'part 1': 2028, 'part 2': 1751},
                {'part 1': 10092, 'part 2': 9021},
                {'part 1': 908, 'part 2': 618},
            ],
        "real": {'part 1': 1568399, 'part 2': 1575877}
    }

    for file, meta in data_files_for(os.path.basename(__file__)):
        raw_data = file.read()
        parser = WareHouseParser(raw_data)
        moves, ware_house_map = parser.parse()

        print("\n--- Part one ---")

        ware_house = WareHouse(ware_house_map)
        ware_house.apply_moves(moves)
        result = sum(ware_house.box_gps())

        expected_result = get_expected_result(meta, 1)
        all_as_expected = all_as_expected and result == expected_result
        print(f"Result: {result} ({'OK' if result == expected_result else 'ERROR, should be ' + str(expected_result)})")

        print("\n--- Part two ---")

        big_ware_house_map = enlarge_warehouse(ware_house_map)

        big_ware_house = WareHouse(big_ware_house_map)
        big_ware_house.apply_moves(moves)
        result = sum(big_ware_house.box_gps())

        expected_result = get_expected_result(meta, 2)
        all_as_expected = all_as_expected and result == expected_result
        print(f"Result: {result} ({'OK' if result == expected_result else 'ERROR, should be ' + str(expected_result)})")

    if all_as_expected:
        print("\nAll results as expected")
    else:
        print("\nSome results are not as expected")
