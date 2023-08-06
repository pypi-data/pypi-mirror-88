from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pilot:
	"""Pilot commands group definition. 2 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pilot", core, parent)

	def clone(self) -> 'Pilot':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Pilot(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def pcode(self):
		"""pcode commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_pcode'):
			from .Pilot_.Pcode import Pcode
			self._pcode = Pcode(self._core, self._base)
		return self._pcode

	@property
	def scode(self):
		"""scode commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_scode'):
			from .Pilot_.Scode import Scode
			self._scode = Scode(self._core, self._base)
		return self._scode
