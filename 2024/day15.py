import os
from utils import data_files_for

ROBOT = "@"
BOX = "O"
BIG_BOX_LEFT = "["
BIG_BOX_RIGHT = "]"
WALL = "#"
EMPTY = "."

def get_direction(direction):
    if direction == "<":
        return (-1, 0)
    elif direction == ">":
        return (1, 0)
    elif direction == "^":
        return (0, -1)
    elif direction == "v":
        return (0, 1)

def find_robot(ware_house_map):
    for y, row in enumerate(ware_house_map):
        for x, cell in enumerate(row):
            if cell == ROBOT:
                return (x, y)

def moved(position, direction):
    x, y = position
    dx, dy = direction
    return (x + dx, y + dy)


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


def can_move_big_boxes(big_warehouse_map, position, direction):
    next_to_move = moved(position, direction)
    if big_warehouse_map[next_to_move[1]][next_to_move[0]] == WALL:
        return False
    if direction[0] == 0:
        if big_warehouse_map[next_to_move[1]][next_to_move[0]] == BIG_BOX_LEFT:
            return (
                    can_move_big_boxes(big_warehouse_map, next_to_move, direction) and
                    can_move_big_boxes(big_warehouse_map, moved(next_to_move, (1, 0)), direction)
            )
        if big_warehouse_map[next_to_move[1]][next_to_move[0]] == BIG_BOX_RIGHT:
            return (
                    can_move_big_boxes(big_warehouse_map, next_to_move, direction) and
                    can_move_big_boxes(big_warehouse_map, moved(next_to_move, (-1, 0)), direction)
            )
    else:
        if big_warehouse_map[next_to_move[1]][next_to_move[0]] in [BIG_BOX_LEFT, BIG_BOX_RIGHT]:
            return can_move_big_boxes(big_warehouse_map, next_to_move, direction)
    return True


def move_big_boxes(big_warehouse_map, position, direction):
    next_to_move = moved(position, direction)
    if big_warehouse_map[next_to_move[1]][next_to_move[0]] == EMPTY:
        return big_warehouse_map

    if direction[0] == 0:
        if big_warehouse_map[next_to_move[1]][next_to_move[0]] == BIG_BOX_LEFT:
            next_to_move_other_side = moved(next_to_move, (1, 0))
        else:
            next_to_move_other_side = moved(next_to_move, (-1, 0))

        big_warehouse_map = move_big_boxes(big_warehouse_map, next_to_move, direction)
        big_warehouse_map = move_big_boxes(big_warehouse_map, next_to_move_other_side, direction)

        target = moved(next_to_move, direction)
        other_target = moved(next_to_move_other_side, direction)
        big_warehouse_map[target[1]][target[0]] = big_warehouse_map[next_to_move[1]][next_to_move[0]]
        big_warehouse_map[other_target[1]][other_target[0]] = big_warehouse_map[next_to_move_other_side[1]][next_to_move_other_side[0]]

        big_warehouse_map[next_to_move[1]][next_to_move[0]] = EMPTY
        big_warehouse_map[next_to_move_other_side[1]][next_to_move_other_side[0]] = EMPTY
    else:
        next_to_move_other_side = moved(next_to_move, direction)
        target = moved(next_to_move_other_side, direction)

        big_warehouse_map = move_big_boxes(big_warehouse_map, next_to_move_other_side, direction)

        big_warehouse_map[target[1]][target[0]] = big_warehouse_map[next_to_move_other_side[1]][next_to_move_other_side[0]]
        big_warehouse_map[next_to_move_other_side[1]][next_to_move_other_side[0]] = big_warehouse_map[next_to_move[1]][next_to_move[0]]
        big_warehouse_map[next_to_move[1]][next_to_move[0]] = EMPTY

    # draw_map(big_warehouse_map)

    return big_warehouse_map


def draw_map(big_warehouse_map):
    for line in big_warehouse_map:
        print(''.join(line))
    print('')


if __name__ == "__main__":
    for file, meta in data_files_for(os.path.basename(__file__)):

        raw_data = file.read()

        # print(raw_data)

        raw_ware_house_map, raw_moves = raw_data.split("\n\n")
        ware_house_map = [list(row.strip()) for row in raw_ware_house_map.split("\n")]
        big_warehouse_map = enlarge_warehouse(ware_house_map)
        moves = [get_direction(d) for d in ''.join(raw_moves.split()).strip()]

        print("\n--- Part one ---")

        robot_position = find_robot(ware_house_map)

        for direction in moves:
            target = moved(robot_position, direction)
            first_after_boxes = moved(robot_position, direction)

            while ware_house_map[first_after_boxes[1]][first_after_boxes[0]] == BOX:
                first_after_boxes = moved(first_after_boxes, direction)

            if ware_house_map[first_after_boxes[1]][first_after_boxes[0]] == WALL:
                continue

            ware_house_map[first_after_boxes[1]][first_after_boxes[0]] = BOX
            ware_house_map[robot_position[1]][robot_position[0]] = EMPTY
            ware_house_map[target[1]][target[0]] = ROBOT
            robot_position = target

        box_gps = [y*100+x for y, row in enumerate(ware_house_map) for x, cell in enumerate(row) if cell == BOX]
        print(sum(box_gps))

        print("\n--- Part two ---")

        robot_position = find_robot(big_warehouse_map)

        for direction in moves:
            if can_move_big_boxes(big_warehouse_map, robot_position, direction):

                # draw_map(big_warehouse_map)
                big_warehouse_map = move_big_boxes(big_warehouse_map, robot_position, direction)
                big_warehouse_map[robot_position[1]][robot_position[0]] = EMPTY
                robot_position = moved(robot_position, direction)
                big_warehouse_map[robot_position[1]][robot_position[0]] = ROBOT

        box_gps = [y*100+x for y, row in enumerate(big_warehouse_map) for x, cell in enumerate(row) if cell == BIG_BOX_LEFT]
        print(sum(box_gps))