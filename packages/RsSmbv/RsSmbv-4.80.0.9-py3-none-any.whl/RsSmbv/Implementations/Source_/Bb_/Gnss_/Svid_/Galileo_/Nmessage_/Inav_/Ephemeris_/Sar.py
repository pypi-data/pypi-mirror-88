from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sar:
	"""Sar commands group definition. 3 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sar", core, parent)

	def clone(self) -> 'Sar':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Sar(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def mode(self):
		"""mode commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mode'):
			from .Sar_.Mode import Mode
			self._mode = Mode(self._core, self._base)
		return self._mode

	@property
	def rlm(self):
		"""rlm commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rlm'):
			from .Sar_.Rlm import Rlm
			self._rlm = Rlm(self._core, self._base)
		return self._rlm

	@property
	def spare(self):
		"""spare commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_spare'):
			from .Sar_.Spare import Spare
			self._spare = Spare(self._core, self._base)
		return self._spare
