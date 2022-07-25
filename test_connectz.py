from unittest import TestCase
from connectz import Game



class GameTest(TestCase):

    def testA_player1_wins(self):
        game_object = Game('./test_case/test0.txt')
        self.assertEqual(game_object.run_game(),1)
    def testB_player1_wins(self):
         game_object = Game('./test_case/test1.txt')
         self.assertEqual(game_object.run_game(),1)
    def test_player2_wins(self):
        game_object = Game('./test_case/test2.txt')
        self.assertEqual(game_object.run_game(),2)
    def test_draw(self):
       game_object = Game('./test_case/test3.txt')
       self.assertEqual(game_object.run_game(),0)
    def testC_player1_wins(self):
        """
            Diagonal South West to North East
        """
        game_object = Game('./test_case/test4.txt')
        self.assertEqual(game_object.run_game(),1)
    def testD_player1_wins(self):
        """
            Diagonal South East to North West
        """
        game_object = Game('./test_case/test12.txt')
        self.assertEqual(game_object.run_game(),1)
    def testA_invalid_file(self):
        """
            Files containing non-integers value on top line
        """
        game_object = Game('./test_case/test5.txt')
        self.assertEqual(game_object.run_game(),8)
    def testB_invalid_file(self):
        """
            Files containing non-integers anywhere in the file
        """
        game_object = Game('./test_case/test6.txt')
        self.assertEqual(game_object.run_game(),8)
    def test_invalid_col(self):
        """
            Files containing invalid columns
        """
        game_object = Game('./test_case/test7.txt')
        self.assertEqual(game_object.run_game(),6)
    def test_invalid_row(self):
        """
            Files containing invalid rows
        """
        game_object = Game('./test_case/test8.txt')
        self.assertEqual(game_object.run_game(),5)
    def test_incomplete_game(self):
        """
            Files containing incomplete games
        """
        game_object = Game('./test_case/test9.txt')
        self.assertEqual(game_object.run_game(),3)
    def test_illegal_game(self):
        """
            Files containing illegal games
        """
        game_object = Game('./test_case/test10.txt')
        self.assertEqual(game_object.run_game(),7)
    def test_illegal_continue(self):
        """
            Files containing illegal continue
        """
        game_object = Game('./test_case/test11.txt')
        self.assertEqual(game_object.run_game(),4)

if __name__ == '__main__':
    test_obj = GameTest()
    test_obj.test_player1A_wins()
    test_obj.test_player1B_wins()
    test_obj.test_player1C_wins()
    test_obj.testD_player1_wins()
    test_obj.test_player2_wins()
    test_obj.test_draw()
    test_obj.testA_invalid_file()
    test_obj.testB_invalid_file()
    test_obj.test_invalid_col()
    test_obj.test_invalid_row()
    test_obj.test_incomplete_game()
    test_obj.test_illegal_game()
    test_obj.test_illegal_continue()
