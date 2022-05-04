"""PEtab model abstraction"""
from __future__ import annotations

import abc
from typing import Any, Iterable, Tuple


class Model:
    """Base class for wrappers for any PEtab-supported model type"""

    def __init__(self):
        ...
    # TODO more coherent method names / arguments
    # TODO doc
    # TODO remove unused

    @staticmethod
    @abc.abstractmethod
    def from_file(filepath_or_buffer: Any) -> Model:
        """Load the model from the given path/URL

        :param filepath_or_buffer: URL or path of the model
        :returns: A ``Model`` instance holding the given model
        """
        ...

    @abc.abstractmethod
    def get_parameter_ids(self) -> Iterable[str]:
        """Get all parameter IDs from this model

        :returns: Iterator over model parameter IDs
        """
        ...

    @abc.abstractmethod
    def get_parameter_value(self, id_: str) -> float:
        """Get a parameter value

        :param id_: ID of the parameter whose value is to be returned
        :raises ValueError: If no parameter with the given ID exists
        :returns: The value of the given parameter as specified in the model
        """
        ...

    @abc.abstractmethod
    def get_parameter_ids_with_values(self) -> Iterable[Tuple[str, float]]:
        # TODO yet unused
        ...

    @abc.abstractmethod
    def has_species_with_id(self, entity_id: str) -> bool:
        # TODO yet unused
        ...

    @abc.abstractmethod
    def has_compartment_with_id(self, entity_id: str) -> bool:
        # TODO yet unused
        ...

    @abc.abstractmethod
    def has_entity_with_id(self, entity_id) -> bool:
        """Check if there is a model entity with the given ID

        :param entity_id: ID to check for
        :returns: ``True``, if there is an entity with the given ID,
        ``False`` otherwise
        """
        ...

    @abc.abstractmethod
    def get_valid_parameters_for_parameter_table(self) -> Iterable[str]:
        """Get IDs of all parameters that are allowed to occur in the PEtab
        parameters table

        :returns: Iterator over parameter IDs
        """
        ...

    @abc.abstractmethod
    def get_valid_ids_for_condition_table(self) -> Iterable[str]:
        """Get IDs of all model entities that are allowed to occur as columns
        in the PEtab conditions table.

        :returns: Iterator over model entity IDs
        """
        ...

    @abc.abstractmethod
    def symbol_allowed_in_observable_formula(self, id_: str) -> bool:
        """Check if the given ID is allowed to be used in observable formulas

        # TODO currently also used for noise

        :returns: ``True``, if allowed, ``False`` otherwise
        """

        ...

    @abc.abstractmethod
    def is_valid(self) -> bool:
        """Validate this model

        # TODO optional printing?
        :returns: `True` if the model is valid, `False` if there are errors in
        this model
        """
        ...


def model_factory(filepath_or_buffer: Any, model_language: str) -> Model:
    """Create a PEtab model instance from the given model

    :param filepath_or_buffer: Path/URL of the model
    :param model_language: PEtab model language ID for the given model
    :returns: A :py:class:`Model` instance representing the given model
    """
    if model_language == "sbml":
        from .sbml_model import SbmlModel
        return SbmlModel.from_file(filepath_or_buffer)

    if model_language == "pysb":
        from .pysb_model import PySBModel
        return PySBModel.from_file(filepath_or_buffer)

    raise ValueError(f"Unsupported model format: {model_language}")
