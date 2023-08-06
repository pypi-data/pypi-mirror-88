# -*- coding: utf-8 -*-
import unittest
from copy import deepcopy
from random import randint, random, seed
import pickle

import numpy as np

from crystals import (
    Atom,
    Orbital,
    ElectronicStructure,
    Element,
    Lattice,
    distance_cartesian,
    distance_fractional,
    is_element,
)
from crystals.atom_data import chemical_symbols
from crystals.affine import rotation_matrix

seed(23)
np.random.seed(23)

# Madelung rule
MADELUNG = [
    "1s",
    "2s",
    "2p",
    "3s",
    "3p",
    "4s",
    "3d",
    "4p",
    "5s",
    "4d",
    "5p",
    "6s",
    "4f",
    "5d",
    "6p",
    "7s",
    "5f",
    "6d",
    "7p",
]


def random_transform():
    """ Create a rotation matrix, around a random axis, of a random amount """
    return rotation_matrix(random(), axis=np.random.random((3,)))


class TestElement(unittest.TestCase):
    def test_build(self):
        """ Test that all valid chemical symbols can be used to create an Element instance """
        for symbol in chemical_symbols:
            Element(symbol)

    def test_invalid_element(self):
        """ Test that an invalid chemical symbol will raise an error """
        with self.assertRaises(ValueError):
            Element("montreal")

    def test_init_with_atomic_number(self):
        """ Test that constructing an Element from a symbol or atomic number results in the same element """
        for symbol in chemical_symbols:
            from_symbol = Element(symbol)
            from_number = Element(from_symbol.atomic_number)
            self.assertEqual(from_number, from_symbol)

    def test_atomic_number_out_of_range(self):
        """ Test that constructing an Element from an atomic number out-of-range raises a ValueError """
        with self.assertRaises(ValueError):
            Element(256)

    def test_input_equivalence(self):
        """Test that the constructor for `Element` supports atomic numbers,
        strings, and other `Element`s"""
        expected = Element("H")

        self.assertEqual(Element("H"), expected)
        self.assertEqual(Element("Hydrogen"), expected)
        self.assertEqual(Element("hydrogen"), expected)  # not case sensitive
        self.assertEqual(Element(1), expected)
        self.assertEqual(Element(expected), expected)


class TestAtom(unittest.TestCase):
    def setUp(self):
        self.atom = Atom(randint(1, 103), coords=np.random.random((3,)))

    def test_init(self):
        """ Test that Atom can be instantiated with an element str or atomic number """
        by_element = Atom("C", coords=(0, 0, 0))
        by_number = Atom(6, coords=(0, 0, 0))
        self.assertEqual(by_element, by_number)

    def test_equality(self):
        """ Test __eq__ for atoms """
        other = deepcopy(self.atom)
        self.assertEqual(self.atom, self.atom)
        self.assertEqual(self.atom, other)

        other.coords_fractional = self.atom.coords_fractional + 1
        self.assertNotEqual(self.atom, other)

    def test_trivial_transform(self):
        """ Test Atom.transform() with the identity """
        transformed = self.atom.transform(np.eye(3))

        self.assertIsNot(transformed, self.atom)
        self.assertEqual(transformed, self.atom)

    def test_atom_subclasses_transform_preserved(self):
        """ Test transform() preserves subclasses """

        class NewAtom(Atom):
            pass

        atm = NewAtom("He", [0, 0, 0])
        transformed = atm.transform(np.eye(3))

        self.assertIs(type(atm), type(transformed))

    def test_transform_back_and_forth(self):
        """ Test Atom.transform() with a random transformation back and forth """

        transf = random_transform()
        transformed1 = self.atom.transform(transf)
        transformed2 = transformed1.transform(np.linalg.inv(transf))

        self.assertIsNot(transformed2, self.atom)
        self.assertEqual(transformed2, self.atom)

    def test_atom_array(self):
        """ Test that numpy.array(Atom(...)) works as expected """
        arr = np.array(self.atom)
        self.assertTupleEqual(arr.shape, (4,))
        self.assertEqual(arr[0], self.atom.atomic_number)
        self.assertTrue(np.allclose(arr[1::], self.atom.coords_fractional))


class TestAtomicDistances(unittest.TestCase):
    def test_distance_fractional(self):
        """ Test the fractional distance between atoms """
        atm1 = Atom("He", [0, 0, 0])
        atm2 = Atom("He", [1, 0, 0])
        self.assertEqual(distance_fractional(atm1, atm2), 1)
        self.assertEqual(
            distance_fractional(atm1, atm2), distance_fractional(atm2, atm1)
        )

    def test_distance_cartesian(self):
        """ Test the cartesian distance between atom """
        lattice = Lattice(4 * np.eye(3))  # Cubic lattice side length 4 angs

        atm1 = Atom("He", [0, 0, 0], lattice=lattice)
        atm2 = Atom("He", [1, 0, 0], lattice=lattice)

        self.assertEqual(distance_cartesian(atm1, atm2), 4.0)

    def test_distance_different_lattice(self):
        """Test that fractional and cartesian distances
        between atoms in different lattices raises an error."""
        lattice1 = Lattice(np.eye(3))
        lattice2 = Lattice(2 * np.eye(3))

        atm1 = Atom("He", [0, 0, 0], lattice=lattice1)
        atm2 = Atom("He", [1, 0, 0], lattice=lattice2)

        with self.subTest("Fractional distance"):
            with self.assertRaises(RuntimeError):
                distance_fractional(atm1, atm2)

        with self.subTest("Cartesian distance"):
            with self.assertRaises(RuntimeError):
                distance_cartesian(atm1, atm2)


class TestIsElement(unittest.TestCase):
    def test_input_types(self):
        """Test that is_element() works as expected for all
        supported input types"""
        atm = Atom("V", [0, 0, 0])

        self.assertTrue(is_element(atm.element)(atm))
        self.assertTrue(is_element(atm.atomic_number)(atm))
        self.assertTrue(is_element(atm)(atm))


class TestOrbital(unittest.TestCase):
    def test_madelung_rule(self):
        """Test that the orbitals are listed in the Madelung rule order,
        which is the filling order."""

        enumeration = [shell.value for shell in Orbital]
        self.assertEqual(MADELUNG, enumeration)

    def test_maximum_electrons(self):
        """ That that the maximum number of electrons per Orbital is as expected. """
        maxima = {"s": 2, "p": 6, "d": 10, "f": 14}
        for shell in Orbital:
            with self.subTest(str(shell)):
                self.assertEqual(
                    maxima[shell.value[-1]], Orbital.maximum_electrons(shell)
                )


class TestElectronicStructure(unittest.TestCase):
    def test_maximum_electrons(self):
        """ Test that an error is raised for impossible electronic structures. """
        with self.assertRaises(ValueError):
            ElectronicStructure({"1s": 3})

    def test_pickable(self):
        """ Test that ElectronicStructure instances are pickable. """
        structure = ElectronicStructure.ground_state("W")
        self.assertEqual(structure, pickle.loads(pickle.dumps(structure)))

    def test_missing_orbital(self):
        """ Test that 'missing' orbitals will return 0 electrons """
        struct = ElectronicStructure.ground_state("He")
        self.assertEqual(struct["2p"], 0)

    def test_orbital_keys(self):
        """ Test that orbital occupancies can be accessed either with strings or Orbital """
        struct = ElectronicStructure.ground_state("He")
        self.assertEqual(struct["1s"], struct[Orbital.one_s])

    def test_modification_in_place(self):
        """ Test that ElectronicStructure instances can be modified in-place """
        struct = ElectronicStructure({"1s": 2, "2s": 2, "2p": 4})
        expected = ElectronicStructure({"1s": 2, "2s": 2, "2p": 3, "4s": 1})
        struct["2p"] -= 1
        struct["4s"] += 1
        self.assertEqual(struct, expected)

    def test_valence_shell(self):
        """ Test that the outermost shell is as expected """
        struct = ElectronicStructure({"1s": 2})
        self.assertEqual(struct.outer_shell, Orbital("1s"))

        # Intentionally omitting 2s
        struct = ElectronicStructure({"1s": 2, "2p": 4})
        self.assertEqual(struct.outer_shell, Orbital("2p"))


if __name__ == "__main__":
    unittest.main()
