from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Time:
	"""Time commands group definition. 132 total commands, 2 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("time", core, parent)

	def clone(self) -> 'Time':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Time(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def conversion(self):
		"""conversion commands group. 9 Sub-classes, 0 commands."""
		if not hasattr(self, '_conversion'):
			from .Time_.Conversion import Conversion
			self._conversion = Conversion(self._core, self._base)
		return self._conversion

	@property
	def start(self):
		"""start commands group. 9 Sub-classes, 5 commands."""
		if not hasattr(self, '_start'):
			from .Time_.Start import Start
			self._start = Start(self._core, self._base)
		return self._start
