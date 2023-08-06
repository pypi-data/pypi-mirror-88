from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Rs:
	"""Rs commands group definition. 26 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rs", core, parent)

	def clone(self) -> 'Rs':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Rs(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def nrSets(self):
		"""nrSets commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_nrSets'):
			from .Rs_.NrSets import NrSets
			self._nrSets = NrSets(self._core, self._base)
		return self._nrSets

	@property
	def set(self):
		"""set commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_set'):
			from .Rs_.Set import Set
			self._set = Set(self._core, self._base)
		return self._set
