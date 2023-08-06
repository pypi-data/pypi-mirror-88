from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mbeacon:
	"""Mbeacon commands group definition. 2 total commands, 1 Sub-groups, 1 group commands"""

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
	def marker(self):
		"""marker commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_marker'):
			from .Mbeacon_.Marker import Marker
			self._marker = Marker(self._core, self._base)
		return self._marker

	def preset(self) -> None:
		"""[SOURce<HW>]:[ILS]:MBEacon:PRESet \n
		No command help available \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:ILS:MBEacon:PRESet')

	def preset_with_opc(self) -> None:
		"""[SOURce<HW>]:[ILS]:MBEacon:PRESet \n
		No command help available \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:ILS:MBEacon:PRESet')
