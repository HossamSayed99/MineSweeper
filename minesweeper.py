import itertools
import random
import copy


class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        if self.count == len(self.cells):
           return self.cells
        return  None 
        # raise NotImplementedErrors

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        if self.count == 0:
            return self.cells
        return None
        # raise NotImplementedError

    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        if cell in self.cells:
            self.cells.remove(cell)
            self.count -= 1
        return
        # raise NotImplementedError

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        if cell in self.cells:
            self.cells.remove(cell)
        return 
        # raise NotImplementedError


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # Marking the cell as a move that has been made
        self.moves_made.add(cell)
        # Marking the cell as safe
        self.mark_safe(cell)
        
        # Getting all the neighbors of the current cell to construct the new statment 
        neighbors  = set()
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue
                
                if 0 <= i < self.height and 0 <= j < self.width:
                    ncell = (i, j)
                    if ncell not in self.moves_made:
                        neighbors.add((i, j))
        sentence = Sentence(neighbors, count)
        if sentence not in self.knowledge:
            self.knowledge.append(sentence)

        # Marking additional cells as safe or as mines
        # looping over statments in Knowledge Bank and removing statements that are no longer important
        for sentence in self.knowledge:
            # Getting all safe cells in a statment and marking as safe
            safecells = copy.deepcopy(sentence.known_safes())
            if safecells != None:
                for safecell in safecells:
                    self.mark_safe(safecell)

            badcells = copy.deepcopy(sentence.known_mines())
            if badcells != None:
                for badcell in badcells:
                    self.mark_mine(badcell)
    

            
        # Adding the final inference 
        # If statment1 is a subset of statment two then statment3  = st2 - st1  = count2 - count1

        new_sentences = []
        for sentence1 in self.knowledge:
            # Check if setence 1 is a subset of sentence2
            for sentence2 in self.knowledge:
                if sentence1 == sentence2 or len(sentence1.cells) == 0 or len(sentence2.cells) <= len(sentence1.cells):
                    continue
                # First we assume that it is indeed a subset
                v = all(cell in sentence2.cells for cell in sentence1.cells)
                # if indeed subset get sentence2 - sentence1
                if v:
                    uncommmon_cells = set()
                    for cell in sentence2.cells:
                        if not cell in sentence1.cells:
                            uncommmon_cells.add(cell)
                    if len(uncommmon_cells) != 0:
                        new_sentence = Sentence(uncommmon_cells, sentence2.count - sentence1.count)
                        print('Sentence1')
                        print(sentence1)
                        print('Sentence2')
                        print(sentence2)
                        print("New Sentence from intersection: ")
                        print(new_sentence)
                        new_sentences.append(new_sentence)


        for s in new_sentences:
            safecells = copy.deepcopy(s.known_safes())
            if safecells != None:
                for safecell in safecells:
                    self.mark_safe(safecell)
                break
            badcells = copy.deepcopy(sentence.known_mines())
            if badcells != None:
                for badcell in badcells:
                    self.mark_mine(badcell)
                break
            if s not in self.knowledge:
                self.knowledge.append(s)
        return 

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """
        for cell in self.safes:
            if cell not in self.moves_made:
                return cell
        return None
        # raise NotImplementedError

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        print ('Known Mines' , self.mines)
        cells = []
        for i in range(self.height):
            for j in range(self.width):
                if not ((i, j) in self.moves_made) and not((i,j) in self.mines):
                    cells.append((i,j))

        if len(cells) != 0:
            cell = cells[random.randint(0, len(cells)-1)]
            print(cell)
            return cell
        return None 
        # raise NotImplementedError
