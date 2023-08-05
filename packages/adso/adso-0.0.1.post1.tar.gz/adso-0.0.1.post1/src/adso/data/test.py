"""Test Dataset."""

from __future__ import annotations

from .common import DATADIR, load_txt
from .dataset import Dataset, LabelledDataset


def load_test_dataset(lines: bool = False) -> Dataset:
    """Load the very simple test dataset as :class:`Dataset`.

    Args:
        lines (bool, optional): consider each line as a document rather than each
            file. Defaults to False.

    Returns:
        Dataset: the very simple test dataset
    """
    _write_test_dataset()
    return load_txt(DATADIR / "Test", lines=lines)


def load_labelled_test_dataset(lines: bool = False) -> LabelledDataset:
    """Load the very simple test dataset as :class:`LabelledDataset`.

    Args:
        lines (bool, optional): consider each line as a document rather than each
            file. Defaults to False.

    Returns:
        LabelledDataset: the very simple test dataset with labels
    """
    _write_test_dataset()
    return load_txt(DATADIR / "Test", lines=lines, label=True)


def _write_test_dataset(force: bool = False) -> None:
    """Write a simple dataset as collection of text file in the DATA directory.

    Args:
        force (bool, optional): force the rewriting of the dataset even if the dataset
            folder already exists. Defaults to False.
    """
    testdir = DATADIR / "Test"
    if (not testdir.exists()) or force:
        testdir.mkdir(exist_ok=True)

        animals = testdir / "animals"
        animals.mkdir(exist_ok=True)
        (animals / "dinosaur.txt").write_text(
            (
                "Dinosaurs are reptiles.\n"
                "Birds descend from dinosaurs.\n"
                "Even if most of the dinosaurs don't fly, "
                "probably the majority of them was covered by feathers."
            )
        )
        (animals / "bird.txt").write_text(
            (
                "Birds lay eggs, like reptiles and fishes.\n"
                "Most of the birds fly, even if penguins, "
                "ostriches and some others are unable to fly.\n"
                "Birds have two wings, like some dinosaurs and others ancient reptiles."
            )
        )

        maths = testdir / "maths"
        maths.mkdir(exist_ok=True)
        (maths / "geometry.txt").write_text(
            (
                "Geometry studies shapes and entities in the space.\n"
                "A geometrician proves theorem about the relation among two "
                "or more geometrical entities.\n"
                "Continuity is a geometric concept widely used in calculus."
            )
        )
        (maths / "linearalgebra.txt").write_text(
            (
                "Linear algebra studies matrices, vectors and vectorial spaces.\n"
                "Sometimes linear algebra is considered a subfield of geometry.\n"
                "Many theorem regarding matrices exists but one of "
                "the most important is the spectral one."
            )
        )
