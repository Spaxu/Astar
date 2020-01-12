import math


def heuristic(first_point, second_point):
    return abs(first_point.x - second_point.x) + abs(first_point.y - second_point.y)


class Point:
    def __init__(self, x, y, blocked=False):
        self.x = x
        self.y = y
        self.blocked = blocked
        self.gScore = math.inf
        self.fScore = math.inf
        self.hScore = math.inf
        self.neighbours = []
        self.beginning = False
        self.target = False
        self.previous = None


class AStar:
    def __init__(self, start_point, end_point, map_array):
        self.width = len(map_array[0])
        self.height = len(map_array)
        self.collisions = self.parseCollisions(map_array)
        self.start = self.collisions[start_point.y][start_point.x]
        self.end = self.collisions[end_point.y][end_point.x]
        self.openSet = []
        self.closedSet = []
        self.init()

    def parseCollisions(self, map_array):
        newCollisions = []
        for h in range(self.height):
            newCollisions.append([])
            for w in range(self.width):
                newCollisions[h].append(Point(w, h, map_array[h][w] == 1))

        return newCollisions

    def addNeighbours(self):
        for h in range(self.height):
            for w in range(self.width):
                self.collisions[h][w] = self.addPointNeighbours(self.collisions[h][w])

    def addPointNeighbours(self, node):
        x = node.x
        y = node.y
        neighbours = []

        if x > 0:
            neighbours.append(self.collisions[y][x - 1])  # lewo
        if y > 0:
            neighbours.append(self.collisions[y - 1][x])  # góra
        if x < self.width - 1:
            neighbours.append(self.collisions[y][x + 1])  # prawo
        if y < self.height - 1:
            neighbours.append(self.collisions[y + 1][x])  # dół
        if x > 0 and y > 0:
            neighbours.append(self.collisions[y - 1][x - 1])  # lewo, góra
        if y > 0 and x < self.width - 1:
            neighbours.append(self.collisions[y - 1][x + 1])  # prawo, góra
        if x > 0 and y < self.height - 1:
            neighbours.append(self.collisions[y + 1][x - 1])  # lewo, dół
        if x < self.width - 1 and y < self.height - 1:
            neighbours.append(self.collisions[y + 1][x + 1])  # prawo, dół

        node.neighbours = neighbours

        return node

    def getLowestFScore(self):
        lowestIndex = 0
        for idx, node in enumerate(self.openSet):
            if node.fScore < self.openSet[lowestIndex].fScore:
                lowestIndex = idx

        return lowestIndex

    def reconstructPath(self):
        path = []
        currentNode = self.end

        while currentNode is not self.start:
            path.append(currentNode)
            currentNode = currentNode.previous

        path.append(self.start)
        path.reverse()
        return path

    def findPath(self):
        while len(self.openSet) > 0:
            currentIndex = self.getLowestFScore()
            currentNode = self.openSet[currentIndex]
            if currentNode == self.end:
                return self.reconstructPath()

            self.openSet.remove(self.openSet[currentIndex])
            self.closedSet.append(currentNode)

            for neighbour in currentNode.neighbours:
                if neighbour in self.closedSet:
                    continue

                isBetter = False
                tentativeScore = currentNode.gScore + 1

                if self.end is self.collisions[neighbour.y][neighbour.x]:
                    self.openSet.append(neighbour)
                    neighbour.hScore = heuristic(neighbour, self.end)
                    isBetter = True

                elif neighbour not in self.openSet and neighbour.blocked is False:
                    self.openSet.append(neighbour)
                    neighbour.hScore = heuristic(neighbour, self.end)
                    isBetter = True

                elif tentativeScore < neighbour.gScore and neighbour.blocked is False:
                    isBetter = True

                if isBetter:
                    neighbour.previous = currentNode
                    neighbour.gScore = tentativeScore
                    neighbour.fScore = neighbour.gScore + neighbour.hScore

        return []

    def init(self):
        self.start.beginning = True
        self.start.gScore = 0
        self.start.fScore = heuristic(self.start, self.end)

        self.end.target = True
        self.end.gScore = 0

        self.openSet.append(self.start)

        self.addNeighbours()


my_map = [
    [0, 0, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0, 1, 0],
    [0, 0, 1, 0, 0, 0, 1, 0],
    [0, 0, 1, 0, 0, 0, 1, 0],
    [0, 0, 1, 0, 0, 0, 1, 0],
    [0, 0, 1, 0, 1, 1, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0],
]

start = Point(0, 0)
end = Point(7, 7)

road = AStar(start, end, my_map).findPath()

if len(road) == 0:
    print("Nie znaleziono trasy.")
else:
    for index, point in enumerate(road):
        print(f"Krok {index + 1}: ({point.x}, {point.y})")