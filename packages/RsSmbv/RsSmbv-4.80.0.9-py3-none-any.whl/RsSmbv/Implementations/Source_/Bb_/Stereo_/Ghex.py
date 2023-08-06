from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ghex:
	"""Ghex commands group definition. 6 total commands, 1 Sub-groups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ghex", core, parent)

	def clone(self) -> 'Ghex':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Ghex(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def data(self):
		"""data commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_data'):
			from .Ghex_.Data import Data
			self._data = Data(self._core, self._base)
		return self._data

	def get_catalog(self) -> List[str]:
		"""[SOURce<HW>]:BB:STEReo:GHEX:CATalog \n
		No command help available \n
			:return: catalog: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:STEReo:GHEX:CATalog?')
		return Conversions.str_to_str_list(response)

	def load(self, load: str) -> None:
		"""[SOURce<HW>]:BB:STEReo:GHEX:LOAD \n
		No command help available \n
			:param load: No help available
		"""
		param = Conversions.value_to_quoted_str(load)
		self._core.io.write(f'SOURce<HwInstance>:BB:STEReo:GHEX:LOAD {param}')

	def get_no_entries(self) -> int:
		"""[SOURce<HW>]:BB:STEReo:GHEX:NOENtries \n
		No command help available \n
			:return: no_entries: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:STEReo:GHEX:NOENtries?')
		return Conversions.str_to_int(response)

	def set_no_entries(self, no_entries: int) -> None:
		"""[SOURce<HW>]:BB:STEReo:GHEX:NOENtries \n
		No command help available \n
			:param no_entries: No help available
		"""
		param = Conversions.decimal_value_to_str(no_entries)
		self._core.io.write(f'SOURce<HwInstance>:BB:STEReo:GHEX:NOENtries {param}')

	def preset(self) -> None:
		"""[SOURce<HW>]:BB:STEReo:GHEX:PRESet \n
		No command help available \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:BB:STEReo:GHEX:PRESet')

	def preset_with_opc(self) -> None:
		"""[SOURce<HW>]:BB:STEReo:GHEX:PRESet \n
		No command help available \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:STEReo:GHEX:PRESet')

	def set_store(self, store: str) -> None:
		"""[SOURce<HW>]:BB:STEReo:GHEX:STORe \n
		No command help available \n
			:param store: No help available
		"""
		param = Conversions.value_to_quoted_str(store)
		self._core.io.write(f'SOURce<HwInstance>:BB:STEReo:GHEX:STORe {param}')
