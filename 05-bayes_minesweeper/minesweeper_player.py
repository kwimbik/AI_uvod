import numpy
from minesweeper_common import UNKNOWN, MINE, get_neighbors

RUN_TESTS = False

"""
    TODO: Improve the strategy for playing Minesweeper provided in this file.
    The provided strategy simply counts the number of unexplored mines in the neighborhood of each cells.
    If this couting concludes that a cell has to contain a mine, then it is marked.
    If it concludes that a cell cannot contain a mine, then it is explored; i.e. function Player.preprocessing returns its coordinates.
    If the simple couting algorithm does not find a unexplored cell provably without a mine,
     function Player.probability_player is called to find an unexplored cell with the minimal probability having a mine.
    A recommended approach is implementing the function Player.get_each_mine_probability.
    You can adopt this file as you like but you have to keep the interface so that your player properly works on recodex; i.e.
        * Player.__init__ is called in the beginning of every game.
        * Player.turn is called to explore one cell.
"""

class Player:
    def __init__(self, rows, columns, game, mine_prb):
        # Initialize a player for a game on a board of given size with the probability of a mine on each cell.
        self.rows = rows
        self.columns = columns
        self.game = game
        self.mine_prb = mine_prb

        # Matrix of all neighbor cells for every cell.
        self.neighbors = get_neighbors(rows, columns)

        # Matrix of numbers of missing mines in the neighborhood of every cell.
        # -1 if a cell is unexplored.
        self.mines = numpy.full(rows*columns, -1).reshape((rows, columns))

        # Matrix of the numbers of unexplored neighborhood cells, excluding known mines.
        self.unknown = numpy.full(rows*columns, 0).reshape((rows, columns))
        for i in range(self.rows):
            for j in range(self.columns):
                self.unknown[i,j] = len(self.neighbors[i,j])

        # A set of cells for which the precomputed values self.mines and self.unknown need to be updated.
        self.invalid = set()


    def turn(self):
        # Returns the position of one cell to be explored.
        pos = self.preprocessing()
        if not pos:
            pos = self.probability_player()
        self.invalidate_with_neighbors(pos)
        return pos

    def probability_player(self):
        # Return an unexplored cell with the minimal probability of mine
        mineFound = True
        while mineFound:
            prb,mineFound  = self.get_each_mine_probability()

        min_prb = 1
        for i in range(self.rows):
            for j in range(self.columns):
                if self.game[i,j] == UNKNOWN:
                    if prb[i,j] > 0.9999: # Float-point arithmetics may not be exact.
                        self.game[i,j] = MINE
                        self.invalidate_with_neighbors((i,j))
                    if min_prb > prb[i,j]:
                        min_prb = prb[i,j]
                        best_position = (i,j)
        return best_position

    def invalidate_with_neighbors(self, pos):
        # Insert a given position and its neighborhood to the list of cell requiring update of precomputed information.
        self.invalid.add(pos)
        for neigh in self.neighbors[pos]:
            self.invalid.add(neigh)

    def preprocess_all(self):
        # Preprocess all cells
        self.invalid = set((i,j) for i in range(self.rows) for j in range(self.columns))
        pos = self.preprocessing()
        assert(pos == None) # Preprocessing is incomplete

    def preprocessing(self):
        """
            Update precomputed information of cells in the set self.invalid.
            Using a simple counting, check cells which have to contain a mine.
            If this simple counting finds a cell which cannot contain a mine, then returns its position.
            Otherwise, returns None.
        """
        while self.invalid:
            pos = self.invalid.pop()

            # Count the numbers of unexplored neighborhood cells, excluding known mines.
            self.unknown[pos] = sum(1 if self.game[neigh] == UNKNOWN else 0 for neigh in self.neighbors[pos])

            if self.game[pos] >= 0:
                # If the cell pos is explored, count the number of missing mines in its neighborhood.
                self.mines[pos] = self.game[pos] - sum(1 if self.game[neigh] == MINE else 0 for neigh in self.neighbors[pos])
                assert(0 <= self.mines[pos] and self.mines[pos] <= self.unknown[pos])

                if self.unknown[pos] > 0:
                    if self.mines[pos] == self.unknown[pos]:
                        # All unexplored neighbors have to contain a mine, so mark them.
                        for neigh in self.neighbors[pos]:
                            if self.game[neigh] == UNKNOWN:
                                self.game[neigh] = MINE
                                self.invalidate_with_neighbors(neigh)

                    elif self.mines[pos] == 0:
                        # All mines in the neighborhood was found, so explore the rest.
                        self.invalid.add(pos) # There may be other unexplored neighbors.
                        for neigh in self.neighbors[pos]:
                            if self.game[neigh] == UNKNOWN:
                                return neigh
                        assert(False) # There has to be at least one unexplored neighbor.

        if not RUN_TESTS:
            return None

        # If the invalid list is empty, so self.unknown and self.mines should be correct.
        # Verify it to be sure.
        for i in range(self.rows):
            for j in range(self.columns):
                assert(self.unknown[i,j] == sum(1 if self.game[neigh] == UNKNOWN else 0 for neigh in self.neighbors[i,j]))
                if self.game[i,j] >= 0:
                    assert(self.mines[i,j] == self.game[i,j] - sum(1 if self.game[neigh] == MINE else 0 for neigh in self.neighbors[i,j]))

    def get_each_mine_probability(self):

        
        # Returns a matrix of probabilities of a mine of each cell
        probability = numpy.zeros((self.rows,self.columns))
        foundMineCell = False  #If found mine
        for i in range(self.rows):
            for j in range(self.columns):
                if self.game[i,j] == MINE:
                    probability[i,j] = 1
                #here enter bayas modificitaion of pribability
                elif self.game[i,j] >= 0:
                    probability[i,j] = 0 
                 #All combinations across all neigbour valid 
                else: 
                    nonZeroCells = getNonZeroCells(self.neighbors[i,j], self)
                    possibleMineCells = []
                    if len(nonZeroCells) == 0:
                        probability[i,j] = self.mine_prb
                    else:
                        possibleMineCells = getUnknownCells(nonZeroCells, self)
                        combNumber = generateMineCombination(self, possibleMineCells, (i,j), nonZeroCells) #positiveResults/allValidresults
                        # debug
                        if combNumber > 0.999:
                            self.game[i,j] = MINE
                            self.invalidate_with_neighbors((i,j))
                            probability[i,j] = 1
                            foundMineCell = True
                            for u in self.neighbors[i,j]:
                                if self.mines[u] > 0:
                                    self.mines[u] -= 1
                            return probability, foundMineCell
                        else:
                           probability[i,j] = combNumber
        return probability, foundMineCell


def getNonZeroCells(cells, self):
        DiscoveredCells = []
        for u in cells:
            if self.mines[u] > 0:
                DiscoveredCells.append(u)
        return DiscoveredCells

def getUnknownCells(cells, self):
        DiscoveredCells = []
        for u in cells:
            for k in self.neighbors[u]:
                if self.game[k] == -1 and not k in DiscoveredCells:
                    DiscoveredCells.append(k)
        return DiscoveredCells



def combinations(iterable, r):
    # combinations('ABCD', 2) --> AB AC AD BC BD CD
    # combinations(range(4), 3) --> 012 013 023 123
    pool = tuple(iterable)
    n = len(pool)
    if r > n:
        return
    indices = list(range(r))
    yield tuple(pool[i] for i in indices)
    while True:
        for i in reversed(range(r)):
            if indices[i] != i + n - r:
                break
        else:
            return
        indices[i] += 1
        for j in range(i+1, r):
            indices[j] = indices[j-1] + 1
        yield tuple(pool[i] for i in indices)


def generateMineCombination(self, mineCells, objectiveCell, masterCells):
    #pokud validni, pripsat jako overall kombinaci a pokud zaroven mina na objective policku, pripsat jeden bod tam
    
    mineField = {}
    allValidCombinations = 0
    allValidCombinationsWithObjectiveCell = 0
    for k in range(len(mineCells)):
        mineArrangements = combinations(mineCells, k)
        for combination in mineArrangements:
            for i in combination:
                mineField[i] = 1
            if validateMineCombinations(self, mineField, masterCells):
                if objectiveCell in mineField:
                    allValidCombinationsWithObjectiveCell += 1 #adds one to combination with objective cell
                allValidCombinations += 1       #adds one to overall valid combinations
            mineField.clear()
    if allValidCombinations == 0:
        return 0
    return allValidCombinationsWithObjectiveCell / allValidCombinations
                

def validateMineCombinations(self, mineField, masterCells):
    for MC in masterCells:
        value = self.mines[MC]
        for n in self.neighbors[MC]:
            if n in mineField:
                value -= 1
        if value != 0:
            return False
    return True








    

   
