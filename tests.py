import unittest
from life import Cell, World


class CellTests(unittest.TestCase):

    def test_cell_is_dead_by_default(self):
        world = World((1, 1))
        test_cell = Cell(0, 0, world)

        self.assertFalse(test_cell.is_alive)

    def test_can_set_initial_state_of_cell(self):
        world = World((1, 1))

        test_cell = Cell(0, 0, world, initially_alive=True)

        self.assertTrue(test_cell.is_alive)

    def test_creating_a_cell_associates_it_with_world(self):
        world = World((50, 50))
        cell = Cell(0, 0, world)

        self.assertIsNotNone(world.cells[0,0])

    def test_cell_can_find_neighbors(self):
        world = World((50, 50))

        Cell(4, 6, world)
        Cell(4, 5, world)
        Cell(4, 4, world)
        Cell(5, 6, world)
        Cell(5, 4, world)
        Cell(6, 6, world)
        Cell(6, 5, world)
        Cell(6, 4, world)
        Cell(40, 40, world)
        Cell(30, 30, world)

        test_cell = Cell(5, 5, world)

        self.assertEqual(len(test_cell.get_neighbors()), 8)

    def test_live_cell_with_fewer_than_two_live_neighbors_dies(self):
        world = World((50, 50))

        Cell(4, 6, world, initially_alive=True)
        Cell(4, 5, world)
        Cell(4, 4, world)
        Cell(5, 6, world)
        Cell(5, 4, world)
        Cell(6, 6, world)
        Cell(6, 5, world)
        Cell(6, 4, world)

        test_cell = Cell(5, 5, world, True)

        self.assertFalse(test_cell.next())

    def test_live_cell_with_two_live_neighbors_lives(self):
        world = World((50, 50))

        Cell(4, 6, world, initially_alive=True)
        Cell(4, 5, world, initially_alive=True)
        Cell(4, 4, world)
        Cell(5, 6, world)
        Cell(5, 4, world)
        Cell(6, 6, world)
        Cell(6, 5, world)
        Cell(6, 4, world)

        test_cell = Cell(5, 5, world, True)

        self.assertTrue(test_cell.next())

    def test_live_cell_with_three_live_neighbors_lives(self):
        world = World((50, 50))

        Cell(4, 6, world, initially_alive=True)
        Cell(4, 5, world, initially_alive=True)
        Cell(4, 4, world, initially_alive=True)
        Cell(5, 6, world)
        Cell(5, 4, world)
        Cell(6, 6, world)
        Cell(6, 5, world)
        Cell(6, 4, world)

        test_cell = Cell(5, 5, world, True)

        self.assertTrue(test_cell.next())

    def test_live_cell_with_more_than_three_live_neighbors_dies(self):
        world = World((50, 50))

        Cell(4, 6, world, initially_alive=True)
        Cell(4, 5, world, initially_alive=True)
        Cell(4, 4, world, initially_alive=True)
        Cell(5, 6, world, initially_alive=True)
        Cell(5, 4, world)
        Cell(6, 6, world)
        Cell(6, 5, world)
        Cell(6, 4, world)

        test_cell = Cell(5, 5, world, True)

        self.assertFalse(test_cell.next())

    def test_dead_cell_with_exactly_three_live_neighbors_becomes_alive(self):
        world = World((50, 50))

        Cell(4, 6, world, initially_alive=True)
        Cell(4, 5, world, initially_alive=True)
        Cell(4, 4, world, initially_alive=True)
        Cell(5, 6, world)
        Cell(5, 4, world)
        Cell(6, 6, world)
        Cell(6, 5, world)
        Cell(6, 4, world)

        test_cell = Cell(5, 5, world)

        self.assertTrue(test_cell.next())

    def test_can_progress_cell_to_next_generation(self):
        world = World((50, 50))

        Cell(4, 6, world, initially_alive=True)
        Cell(4, 5, world, initially_alive=True)
        Cell(4, 4, world, initially_alive=True)
        Cell(5, 6, world)
        Cell(5, 4, world)
        Cell(6, 6, world)
        Cell(6, 5, world)
        Cell(6, 4, world)

        test_cell = Cell(5, 5, world)

        self.assertTrue(test_cell.next())
        self.assertFalse(test_cell.is_alive)

        test_cell.step()

        self.assertIsNone(test_cell._next)
        self.assertTrue(test_cell.is_alive)


class WorldTests(unittest.TestCase):

    def test_can_init_world_with_cells(self):
        world = World((50, 50), auto_gen_cells=True)

        self.assertEqual(world.cells.size, 2500)

    def test_can_init_world_without_cells(self):
        world = World((50, 50))

        for xy in world.world_coordinates():
            self.assertIsNone(world.cells[xy])