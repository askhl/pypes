# -*- coding: utf-8 -*-
from __future__ import print_function, unicode_literals
from optparse import OptionParser
import random
from itertools import count

connections2unicode = '·╶╵└╴─┘┴╷┌│├┐┬┤┼'

def tounicode(connections):
    i = connections[0] + 2 * connections[1] + 4 * connections[2] \
        + 8 * connections[3]
    return connections2unicode[i]

class Direction(int):
    def __init__(self, num):
        int.__init__(self, num)
        self.num = num
        self.next = None
        self.prev = None
        self.opposite = None
    
    def __add__(self, num):
        return DIRECTIONS[(self.num + num) % NDIRS]

    def __sub__(self, num):
        return self.__add__(-num)

NDIRS = 4
DIRECTIONS = [Direction(i) for i in range(NDIRS)]
for num, dir in enumerate(DIRECTIONS):
    dir.next = DIRECTIONS[(num + 1) % NDIRS]
    dir.prev = DIRECTIONS[(num - 1) % NDIRS]
    dir.opposite = DIRECTIONS[(num + NDIRS // 2) % NDIRS]

RIGHT, UP, LEFT, DOWN = DIRECTIONS

class Tile:
    def __init__(self):
        self.connections = [False] * 4
        self.neighbours = [None] * 4
        self.colour = 0

    def set_neighbour(self, tile, direction):
        assert self.neighbours[direction] is None
        self.neighbours[direction] = tile
        tile.neighbours[direction.opposite] = self

    def connect(self, direction):
        self.connections[direction] = True
        self.neighbours[direction].connections[direction.opposite] = True

    def get_neighbour(self, direction):
        return self.neighbours[direction]

    def tostring(self):
        return tounicode(self.connections)

    def floodfill(self, colour):
        previous_colour = self.colour
        self.colour = colour
        peers = [self]
        while peers:
            tile = peers.pop()
            tile.colour = colour
            for neighbour in tile.neighbours:
                if neighbour.colour == previous_colour:
                    peers.append(neighbour)


class Board:
    def __init__(self, nx, ny):
        self.nx = nx
        self.ny = ny

        tiles = []
        for y in range(ny):
            row = []
            for x in range(nx):
                row.append(Tile())
            tiles.append(row)
        self.tiles = tiles

    def __getitem__(self, xy):
        x, y = xy
        return self.tiles[y][x]

    def tostring(self):
        lines = []
        for y in range(self.ny):
            lines.append(''.join([tile.tostring() for tile in self.tiles[y]]))
        return '\n'.join(lines)

def set_neighbours_periodic(board):
    colour = count()
    for y in range(board.ny):
        for x in range(board.nx):
            tile = board[x, y]
            tile.colour = next(colour)
            tile.set_neighbour(board[x, (y + 1) % board.ny], DOWN)
            tile.set_neighbour(board[(x + 1) % board.nx, y], RIGHT)

def generate(board, allow_tetravalent=True):
    ntiles = board.nx * board.ny
    possible_connections = []
    for y in range(board.ny):
        for x in range(board.nx):
            for direction in [RIGHT, DOWN]:
                possible_connections.append((board[x, y], direction))

    random.shuffle(possible_connections)
    for tile, direction in possible_connections:
        tile2 = tile.neighbours[direction]
        if tile.colour == tile2.colour:
            continue
        tile.connect(direction)
        tile2.floodfill(tile.colour)

def main():
    p = OptionParser()
    opts, args = p.parse_args()
    
    nx = 79
    ny = 22

    board = Board(nx, ny)

    set_neighbours_periodic(board)

    generate(board)

    print(board.tostring())

if __name__ == '__main__':
    main()
