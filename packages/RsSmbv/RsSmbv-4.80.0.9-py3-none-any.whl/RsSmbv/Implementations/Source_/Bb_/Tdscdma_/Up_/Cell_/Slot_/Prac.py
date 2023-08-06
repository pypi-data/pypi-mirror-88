from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Prac:
	"""Prac commands group definition. 19 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("prac", core, parent)

	def clone(self) -> 'Prac':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Prac(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def msg(self):
		"""msg commands group. 10 Sub-classes, 0 commands."""
		if not hasattr(self, '_msg'):
			from .Prac_.Msg import Msg
			self._msg = Msg(self._core, self._base)
		return self._msg

	@property
	def pts(self):
		"""pts commands group. 6 Sub-classes, 0 commands."""
		if not hasattr(self, '_pts'):
			from .Prac_.Pts import Pts
			self._pts = Pts(self._core, self._base)
		return self._pts

	@property
	def slength(self):
		"""slength commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_slength'):
			from .Prac_.Slength import Slength
			self._slength = Slength(self._core, self._base)
		return self._slength
