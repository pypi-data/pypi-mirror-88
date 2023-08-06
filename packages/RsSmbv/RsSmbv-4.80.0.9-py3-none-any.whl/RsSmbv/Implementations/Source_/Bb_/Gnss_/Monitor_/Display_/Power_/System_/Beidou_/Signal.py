from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Signal:
	"""Signal commands group definition. 5 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("signal", core, parent)

	def clone(self) -> 'Signal':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Signal(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def l1Band(self):
		"""l1Band commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_l1Band'):
			from .Signal_.L1Band import L1Band
			self._l1Band = L1Band(self._core, self._base)
		return self._l1Band

	@property
	def l2Band(self):
		"""l2Band commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_l2Band'):
			from .Signal_.L2Band import L2Band
			self._l2Band = L2Band(self._core, self._base)
		return self._l2Band

	@property
	def l5Band(self):
		"""l5Band commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_l5Band'):
			from .Signal_.L5Band import L5Band
			self._l5Band = L5Band(self._core, self._base)
		return self._l5Band
