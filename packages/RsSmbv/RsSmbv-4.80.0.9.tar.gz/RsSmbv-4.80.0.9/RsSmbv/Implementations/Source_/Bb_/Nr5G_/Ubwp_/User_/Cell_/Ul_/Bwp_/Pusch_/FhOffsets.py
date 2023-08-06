from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FhOffsets:
	"""FhOffsets commands group definition. 2 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("fhOffsets", core, parent)

	def clone(self) -> 'FhOffsets':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = FhOffsets(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def noffsets(self):
		"""noffsets commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_noffsets'):
			from .FhOffsets_.Noffsets import Noffsets
			self._noffsets = Noffsets(self._core, self._base)
		return self._noffsets

	@property
	def offset(self):
		"""offset commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_offset'):
			from .FhOffsets_.Offset import Offset
			self._offset = Offset(self._core, self._base)
		return self._offset
