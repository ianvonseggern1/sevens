from functools import reduce
from random import randint

SIZE = 7
PIECES_PER_ROUND = 5

# TODO deal with not having enough of these figured out
CHAIN_MULTIPLIERS = [7, 39, 109, 224, 391, 617, 907, 1267, 1701, 2213, 2809, 3491, 4265, 5133, 6099, 7168, 8341, 9622]

# TODO add 70000 point bonus for clearing the screen

# Some implementation details
#
# Board is always a square unless its game over and then the piece(s) that bust are still on those columns
class Game:
  # Implementation assumptions rely on empty being 0, grays being less than 0 and pieces being greater
  EMPTY = 0
  GRAY = -1
  DGRAY = -2

  # TODO drop some pieces initially
  def __init__(self):
      self.board = []  # indexed board[column][row]
      for i in range(SIZE):
          self.board.append([self.EMPTY] * SIZE)
      self.nextPiece = self.getPiece()
      self.score = 0
      self.piecesInRound = PIECES_PER_ROUND

  def getPiece(self):
      return randint(1, 7)

  # Returns true if placing a piece in that column is a legal move
  def canMove(self, column):
      return self.EMPTY in self.board[column]

  # TODO game is also over if there are no places left to place a piece
  def isGameOver(self):
      return max([len(col) for col in self.board]) > SIZE

  def move(self, column):
      if self.isGameOver():
          # TODO throw?
          return
      if not self.canMove(column):
          # TODO throw?
          return

      # Drop piece
      newPieceRow = self.board[column].index(self.EMPTY)
      self.board[column][newPieceRow] = self.nextPiece

      totalPopLoops = self.doPopLoop()

      # TODO I don't think you get the 17000 if you take the last spot before the game is over. Probably not a big deal
      # Decrement piecesInRound, if 0, bump bottom, remove empties on top, keep updating score
      self.piecesInRound -= 1
      if self.piecesInRound == 0:
          self.score += 17000

          self.piecesInRound = PIECES_PER_ROUND
          for c in range(SIZE):
              self.board[c].insert(self.DGRAY, 0)
              if self.board[c][-1] == self.EMPTY:
                  self.board[c].pop()

          self.doPopLoop(totalPopLoops)

      # Select new next piece
      self.nextPiece = self.getPiece()
  
  # While pieces to pop, pop pieces, decrement grays, drop remaining, keep updating score    
  def doPopLoop(self, priorLoopCount=0):
      loopCount = priorLoopCount
      popMask = self.getPopMask()
      popCount = self.countTrue(popMask)
      while popCount > 0:
          decrementMask = self.getDecrementMap(popMask)
          
          self.pop(popMask)
          self.decrement(decrementMask)
          self.dropPieces()

          loopCount += 1
          this.score += popCount * CHAIN_MULTIPLIERS[loopCount]

          popMask = self.getPopMask()
          popCount = self.countTrue(popMask)

      return loopCount

  # Performs a single pop by removing pieces anywhere popMask is true
  def pop(self, popMask):
      for c in range(SIZE):
          for r in range(SIZE):
              if popMask[c][r]:
                  self.board[c][r] = self.EMPTY

  def decrement(self, decrementMask):
      for c in range(SIZE):
          for r in range(SIZE):
              decCount = decrementMask[c][r]
              if decCount == 1 and self.board[c][r] == self.DGRAY:
                  self.board[c][r] = self.GRAY
              elif decCount > 0 and self.board[c][r] < 0:
                  self.board[c][r] = self.getPiece()

  def dropPieces(self):
      for c in range(SIZE):
          newCol = []
          for piece in self.board[c]:
              if piece != self.EMPTY:
                  newCol.append(piece)
          while len(newCol) < SIZE:
              newCol.append(self.EMPTY)
          self.board[c] = newCol

  def countTrue(self, mask):
      return sum([sum([1 if x else 0 for x in col]) for col in mask])

  # Returns a bool mask of the current board where true indicates that piece should pop
  def getPopMask(self):
      rtn = [[False] * SIZE for i in range(SIZE)]
      for c in range(SIZE):
          for r in range(SIZE):
              # Only numeric pieces can pop
              pieceVal = self.board[c][r]
              if pieceVal <= 0:
                  continue

              if pieceVal == self.getPiecesInCol(c, r) or pieceVal == self.getPiecesInRow(c, r):
                  rtn[c][r] = True

      return rtn

  # Returns the count of how much gray piece should be decremented based on the pop map
  def getDecrementMap(self, popMap):
      rtn = [[0] * SIZE for i in range(SIZE)]
      for c in range(SIZE):
          for r in range(SIZE):
              for (cOffset, rOffset) in ((1, 0), (0, -1), (0 , 1), (-1, 0)):
                  cNew = c + cOffset
                  rNew = r + rOffset
                  if cNew > 0 and cNew < SIZE and rNew > 0 and rNew < SIZE and popMap[cNew][rNew]:
                      rtn[c][r] += 1
      return rtn

  def getPiecesInCol(self, c, r):
      return self.board[c].index(self.EMPTY) if self.EMPTY in self.board[c] else SIZE

  def getPiecesInRow(self, c, r):
      count = 1

      # Count left
      checkCol = c - 1
      while checkCol >= 0 and self.board[checkCol][r] != self.EMPTY:
          count += 1
          checkCol -= 1

      # Count right
      checkCol = c + 1
      while checkCol < SIZE and self.board[checkCol][r] != self.EMPTY:
          count += 1
          checkCol += 1

      return count
