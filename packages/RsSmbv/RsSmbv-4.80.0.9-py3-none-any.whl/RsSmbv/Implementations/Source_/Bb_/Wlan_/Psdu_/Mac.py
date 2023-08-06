from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mac:
	"""Mac commands group definition. 22 total commands, 4 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mac", core, parent)

	def clone(self) -> 'Mac':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Mac(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def address(self):
		"""address commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_address'):
			from .Mac_.Address import Address
			self._address = Address(self._core, self._base)
		return self._address

	@property
	def fcontrol(self):
		"""fcontrol commands group. 0 Sub-classes, 12 commands."""
		if not hasattr(self, '_fcontrol'):
			from .Mac_.Fcontrol import Fcontrol
			self._fcontrol = Fcontrol(self._core, self._base)
		return self._fcontrol

	@property
	def fcSequence(self):
		"""fcSequence commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fcSequence'):
			from .Mac_.FcSequence import FcSequence
			self._fcSequence = FcSequence(self._core, self._base)
		return self._fcSequence

	@property
	def scontrol(self):
		"""scontrol commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_scontrol'):
			from .Mac_.Scontrol import Scontrol
			self._scontrol = Scontrol(self._core, self._base)
		return self._scontrol

	def get_did(self) -> List[str]:
		"""[SOURce<HW>]:BB:WLAN:PSDU:MAC:DID \n
		No command help available \n
			:return: did: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAN:PSDU:MAC:DID?')
		return Conversions.str_to_str_list(response)

	def set_did(self, did: List[str]) -> None:
		"""[SOURce<HW>]:BB:WLAN:PSDU:MAC:DID \n
		No command help available \n
			:param did: No help available
		"""
		param = Conversions.list_to_csv_str(did)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAN:PSDU:MAC:DID {param}')

	def get_state(self) -> bool:
		"""[SOURce<HW>]:BB:WLAN:PSDU:MAC:STATe \n
		No command help available \n
			:return: state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAN:PSDU:MAC:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""[SOURce<HW>]:BB:WLAN:PSDU:MAC:STATe \n
		No command help available \n
			:param state: No help available
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAN:PSDU:MAC:STATe {param}')
