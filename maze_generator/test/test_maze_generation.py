import logging
import unittest

from maze_generator.src.maze import Maze
    

class TestMazeGeneration(unittest.TestCase):
    def test_generated_maze_has_one_start_location_and_one_end_location(self):
        for _ in range(100):
            num_rows = 11
            num_cols = 11
            generated_maze = Maze(num_rows, num_cols)
            print(generated_maze)
            free_spots = []
            for col in range(num_cols):
                for row in range(num_rows):
                    if ((row == 0) or (col == 0) or (row == num_rows -1) or (col == num_cols - 1)):
                        if generated_maze.is_coordinate_free(col, row):
                            free_spots.append((col, row))
            self.assertEqual(2, len(free_spots))
            self.assertIn(generated_maze.get_starting_coordinate(), free_spots)
            self.assertIn(generated_maze.get_ending_coordinate(), free_spots)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    unittest.main()