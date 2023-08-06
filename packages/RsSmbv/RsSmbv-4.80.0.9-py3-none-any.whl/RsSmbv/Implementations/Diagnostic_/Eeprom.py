from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Eeprom:
	"""Eeprom commands group definition. 3 total commands, 2 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("eeprom", core, parent)

	def clone(self) -> 'Eeprom':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Eeprom(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def customize(self):
		"""customize commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_customize'):
			from .Eeprom_.Customize import Customize
			self._customize = Customize(self._core, self._base)
		return self._customize

	@property
	def data(self):
		"""data commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_data'):
			from .Eeprom_.Data import Data
			self._data = Data(self._core, self._base)
		return self._data

	def delete(self) -> None:
		"""DIAGnostic<HW>:EEPRom:DELete \n
		No command help available \n
		"""
		self._core.io.write(f'DIAGnostic<HwInstance>:EEPRom:DELete')

	def delete_with_opc(self) -> None:
		"""DIAGnostic<HW>:EEPRom:DELete \n
		No command help available \n
		Same as delete, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'DIAGnostic<HwInstance>:EEPRom:DELete')
