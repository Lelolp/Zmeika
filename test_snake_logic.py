import unittest
from collections import deque
from ZMEIKA import next_position, place_food, step_game, WIDTH, HEIGHT


class SnakeLogicTests(unittest.TestCase):
    def test_next_position(self):
        self.assertEqual(next_position((5, 5), (1, 0)), (6, 5))
        self.assertEqual(next_position((5, 5), (0, -1)), (5, 4))

    def test_place_food_not_on_snake_and_inside(self):
        occupied = {(x, 1) for x in range(1, WIDTH - 1)} | {(1, y) for y in range(1, HEIGHT - 1)}
        food = place_food(occupied)
        self.assertIsNotNone(food)
        self.assertNotIn(food, occupied)
        x, y = food
        self.assertTrue(1 <= x <= WIDTH - 2)
        self.assertTrue(1 <= y <= HEIGHT - 2)

    def test_step_game_growth_and_collision(self):
        body = deque([(5, 5), (4, 5), (3, 5)])
        direction = (1, 0)
        food = (6, 5)
        body2, direction2, food2, ate, dead = step_game(body, direction, food)
        self.assertTrue(ate)
        self.assertFalse(dead)
        self.assertEqual(len(body2), len(body) + 1)

        # self collision
        body3 = deque([(5, 5), (5, 6), (4, 6), (4, 5)])
        direction = (0, 1)  # move down into own body
        body4, _, _, ate2, dead2 = step_game(body3, direction, (10, 10))
        self.assertFalse(ate2)
        self.assertTrue(dead2)

        # wall collision
        body5 = deque([(1, 1)])
        direction = (-1, 0)
        body6, _, _, _, dead3 = step_game(body5, direction, None)
        self.assertTrue(dead3)


if __name__ == '__main__':
    unittest.main()
