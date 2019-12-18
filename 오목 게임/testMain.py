import unittest
import copy

from Main import Main

class TestMain(unittest.TestCase):

    def setUp(self):
        self.m1 = Main()
        self.m2 = Main()
        self.m2.omok_pan[0][0] = 1
        self.m2.omok_pan[0][1] = 1
        self.m2.omok_pan[0][2] = 1

        self.m3 = Main()
        self.m3.omok_pan[0][0] = 1
        self.m3.omok_pan[1][0] = 1
        self.m3.omok_pan[2][0] = 1

        self.m4 = Main()
        self.m4.omok_pan[0][0] = 1
        self.m4.omok_pan[1][1] = 1
        self.m4.omok_pan[2][2] = 1

        self.m5 = Main()
        self.m5.omok_pan[7][8] = 1
        self.m5.omok_pan[7][9] = 1

        self.m6 = Main()
        self.m6.omok_pan[6][7] = 1
        self.m6.omok_pan[5][7] = 1


    def testVictory(self):
        # victory return : 1 , else : 0
        # black win
        self.m2.omok_pan[0][3] = 1
        self.assertEqual(self.m1.victory_condition(), 0)
        self.m2.omok_pan[0][4] = 2
        self.assertEqual(self.m2.victory_condition(), 0)
        self.m2.omok_pan[0][4] = 1
        self.assertEqual(self.m2.victory_condition(), 1)
        self.m2.omok_pan[0][5] = 1
        self.assertEqual(self.m2.victory_condition(), 1)

        #white win
        self.m1.omok_pan[0][0] = 2
        self.assertEqual(self.m1.victory_condition(), 0)
        self.m1.omok_pan[0][1] = 2
        self.assertEqual(self.m1.victory_condition(), 0)
        self.m1.omok_pan[0][2] = 2
        self.assertEqual(self.m1.victory_condition(), 0)
        self.m1.omok_pan[0][3] = 2
        self.assertEqual(self.m1.victory_condition(), 0)
        self.m1.omok_pan[0][4] = 2
        self.assertEqual(self.m1.victory_condition(), 1)
        self.m1.omok_pan[0][5] = 2
        self.assertEqual(self.m1.victory_condition(), 1)


        #대각선
        self.m4.omok_pan[3][3] = 1
        self.assertEqual(self.m4.victory_condition(), 0)
        self.m4.omok_pan[4][4] = 1
        self.assertEqual(self.m4.victory_condition(), 1)

        #세로
        self.m3.omok_pan[3][0] = 1
        self.assertEqual(self.m3.victory_condition(), 0)
        self.m3.omok_pan[4][0] = 1
        self.assertEqual(self.m3.victory_condition(), 1)



    #
    def testcheck_33(self):
        #검은 돌 두어져 있는 자리 초기화하고 33 검사
        #ㄱ 모양
        self.m5.omok_pan[7][9] = 0
        self.assertEqual(self.m5.check_33(7, 9), False)
        self.m5.omok_pan[8][9] = 1
        self.assertEqual(self.m5.check_33(7, 9), False)
        self.m5.omok_pan[9][9] = 1
        self.assertEqual(self.m5.check_33(7, 9), True)


        #대각선 모양
        self.m1.omok_pan[7][8] = 1
        self.assertEqual(self.m1.check_33(7, 9), False)
        self.m1.omok_pan[8][8] = 1
        self.assertEqual(self.m1.check_33(7, 9), False)
        self.m1.omok_pan[9][7] = 1
        self.assertEqual(self.m1.check_33(7, 9), True)


    def testcheck_44(self):
        #ㄱ 모양
        self.assertEqual(self.m5.check_44(7, 10), False)
        self.m5.omok_pan[8][10] = 1
        self.assertEqual(self.m5.check_44(7, 10), False)
        self.m5.omok_pan[9][10] = 1
        self.assertEqual(self.m5.check_44(7, 10), False)
        self.m5.omok_pan[10][10] = 1
        self.assertEqual(self.m5.check_44(7, 10), True)


        #대각선 모양
        self.m5.omok_pan[10][9] = 1
        self.assertEqual(self.m5.check_44(11, 10), False)
        self.m5.omok_pan[9][8] = 1
        self.assertEqual(self.m5.check_44(11, 10), False)
        self.m5.omok_pan[8][7] = 1
        self.assertEqual(self.m5.check_44(11, 10), True)


    def testcheck_6(self):
        # 검은 돌은 6목을 둘 수 없게 하는지 검사
        self.m2.omok_pan[0][3] = 1
        self.assertEqual(self.m2.check_6(0, 4), False)
        self.m2.omok_pan[0][5] = 1
        self.assertEqual(self.m2.check_6(0, 4), True)
        self.m2.omok_pan[0][5] = 2
        self.assertEqual(self.m2.check_6(0, 4), False)
        self.m2.omok_pan[0][6] = 1
        self.assertEqual(self.m2.check_6(0, 4), False)
        self.m2.omok_pan[0][5] = 1
        self.assertEqual(self.m2.check_6(0, 4), True)

        #흰돌은 6목 둘 수 있는지 검사
        self.m1.omok_pan[1][5] = 2
        self.assertEqual(self.m1.check_6(1, 8), False)
        self.m1.omok_pan[1][6] = 2
        self.assertEqual(self.m1.check_6(1, 8), False)
        self.m1.omok_pan[1][7] = 2
        self.assertEqual(self.m1.check_6(1, 8), False)
        self.m1.omok_pan[1][9] = 2
        self.assertEqual(self.m1.check_6(1, 8), False)
        self.m1.omok_pan[1][10] = 2
        self.assertEqual(self.m1.check_6(1, 8), False)
        self.m1.omok_pan[1][8] = 2

        #대각선 검사
        self.m4.omok_pan[0][0] = 0
        self.assertEqual(self.m4.check_6(3, 3), False)
        self.m4.omok_pan[4][4] = 1
        self.assertEqual(self.m4.check_6(3, 3), False)
        self.m4.omok_pan[5][5] = 1
        self.assertEqual(self.m4.check_6(3, 3), False)
        self.m4.omok_pan[6][6] = 1
        self.assertEqual(self.m4.check_6(3, 3), True)

        #세로 검사
        self.m6.omok_pan[9][7] = 1
        self.assertEqual(self.m6.check_6(8, 7), False)
        self.m6.omok_pan[10][7] = 1
        self.assertEqual(self.m6.check_6(8, 7), True)



if __name__ == '__main__':
    unittest.main()
