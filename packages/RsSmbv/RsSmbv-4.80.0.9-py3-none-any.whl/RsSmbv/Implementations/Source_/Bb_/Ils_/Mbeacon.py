from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mbeacon:
	"""Mbeacon commands group definition. 16 total commands, 3 Sub-groups, 0 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mbeacon", core, parent)

	def clone(self) -> 'Mbeacon':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Mbeacon(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def comid(self):
		"""comid commands group. 1 Sub-classes, 9 commands."""
		if not hasattr(self, '_comid'):
			from .Mbeacon_.Comid import Comid
			self._comid = Comid(self._core, self._base)
		return self._comid

	@property
	def frequency(self):
		"""frequency commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_frequency'):
			from .Mbeacon_.Frequency import Frequency
			self._frequency = Frequency(self._core, self._base)
		return self._frequency

	@property
	def marker(self):
		"""marker commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_marker'):
			from .Mbeacon_.Marker import Marker
			self._marker = Marker(self._core, self._base)
		return self._marker
