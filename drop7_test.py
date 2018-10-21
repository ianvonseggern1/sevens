import unittest
from drop7 import SIZE, Game

class TestGame(unittest.TestCase):
    def test_can_move(self):
        g = Game()
        for i in range(SIZE):
            self.assertTrue(g.canMove(i))
        g.board[0] = [2] * SIZE
        self.assertFalse(g.canMove(0))
        for i in range(1, SIZE):
            self.assertTrue(g.canMove(i))

    def test_move_without_pop(self):
        g = Game()
        g.nextPiece = 2
        g.move(4)

        expected = [[Game.EMPTY] * SIZE for x in range(SIZE)]
        expected[4][0] = 2
        self.assertEqual(g.board, expected)

    def test_move_with_pop(self):
        g = Game()
        g.nextPiece = 1
        g.move(4)

        expected = [[Game.EMPTY] * SIZE for x in range(SIZE)]
        self.assertEqual(g.board, expected)

    def test_move_with_chain_pop(self):
        g = Game()
        g.board[0][0] = 2
        g.board[1][0] = 2
        g.board[4][0] = 2
        g.nextPiece = 3
        g.move(2)

        expected = [[Game.EMPTY] * SIZE for x in range(SIZE)]
        expected[4][0] = 2
        self.assertEqual(g.board, expected)

    def test_pop_mask(self):
        g = Game()
        g.board[0][0] = 2
        g.board[0][1] = 2
        g.board[0][2] = 3

        expected = [[False] * SIZE for x in range(SIZE)]
        expected[0][2] = True

        self.assertEqual(g.getPopMask(), expected)

    def test_drop(self):
        g = Game()
        g.board[0][1] = 2
        g.board[4][0] = 1
        g.board[4][1] = 2
        g.board[4][3] = 3
        g.board[4][6] = 4
        g.dropPieces()

        expected = [[Game.EMPTY] * SIZE for x in range(SIZE)]
        expected[0][0] = 2
        expected[4][0] = 1
        expected[4][1] = 2
        expected[4][2] = 3
        expected[4][3] = 4

        self.assertEqual(g.board, expected)

    def test_pop_gray(self):
        g = Game()
        g.board[4][0] = Game.GRAY
        g.nextPiece = 2
        g.move(4)

        self.assertTrue(g.board[4][0] > 0)
        self.assertEqual(g.board[4][1], Game.EMPTY)

    def test_drop(self):
        g = Game()
        g.board[4][0] = 2
        g.nextPiece = 3
        g.move(4)

        expected = [[Game.EMPTY] * SIZE for x in range(SIZE)]
        expected[4][0] = 3
        self.assertEqual(g.board, expected)

if __name__ == '__main__':
    unittest.main()
