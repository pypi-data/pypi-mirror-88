from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dpcc:
	"""Dpcc commands group definition. 5 total commands, 0 Sub-groups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dpcc", core, parent)

	def get_burst(self) -> int:
		"""[SOURce<HW>]:BB:W3GPp:MSTation:UDTX:DPCC:BURSt \n
		No command help available \n
			:return: burst: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:W3GPp:MSTation:UDTX:DPCC:BURSt?')
		return Conversions.str_to_int(response)

	def set_burst(self, burst: int) -> None:
		"""[SOURce<HW>]:BB:W3GPp:MSTation:UDTX:DPCC:BURSt \n
		No command help available \n
			:param burst: No help available
		"""
		param = Conversions.decimal_value_to_str(burst)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation:UDTX:DPCC:BURSt {param}')

	def get_cycle(self) -> int:
		"""[SOURce<HW>]:BB:W3GPp:MSTation:UDTX:DPCC:CYCLe \n
		No command help available \n
			:return: cycle: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:W3GPp:MSTation:UDTX:DPCC:CYCLe?')
		return Conversions.str_to_int(response)

	def set_cycle(self, cycle: int) -> None:
		"""[SOURce<HW>]:BB:W3GPp:MSTation:UDTX:DPCC:CYCLe \n
		No command help available \n
			:param cycle: No help available
		"""
		param = Conversions.decimal_value_to_str(cycle)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation:UDTX:DPCC:CYCLe {param}')

	def get_offset(self) -> int:
		"""[SOURce<HW>]:BB:W3GPp:MSTation:UDTX:DPCC:OFFSet \n
		No command help available \n
			:return: offset: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:W3GPp:MSTation:UDTX:DPCC:OFFSet?')
		return Conversions.str_to_int(response)

	def set_offset(self, offset: int) -> None:
		"""[SOURce<HW>]:BB:W3GPp:MSTation:UDTX:DPCC:OFFSet \n
		No command help available \n
			:param offset: No help available
		"""
		param = Conversions.decimal_value_to_str(offset)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation:UDTX:DPCC:OFFSet {param}')

	def get_postamble(self) -> int:
		"""[SOURce<HW>]:BB:W3GPp:MSTation:UDTX:DPCC:POSTamble \n
		No command help available \n
			:return: postamble: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:W3GPp:MSTation:UDTX:DPCC:POSTamble?')
		return Conversions.str_to_int(response)

	def get_preamble(self) -> int:
		"""[SOURce<HW>]:BB:W3GPp:MSTation:UDTX:DPCC:PREamble \n
		No command help available \n
			:return: preamble: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:W3GPp:MSTation:UDTX:DPCC:PREamble?')
		return Conversions.str_to_int(response)
