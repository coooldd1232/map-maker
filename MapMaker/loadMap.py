from rect import Rect

from reusableClasses.vector2 import Vector2

def LoadMap(file):
    walls = []

    with open(file, 'r') as f:
        for line in f:
            line = line.strip('\n')
            line = line.replace(' ', '')

            wallProperties = line.split(',')

            for i, prop in enumerate(wallProperties):
                wallProperties[i] = int(prop)

            walls.append(
                Rect(Vector2(wallProperties[0], wallProperties[1]), wallProperties[2], wallProperties[3]))

    # return list of walls
    return walls