from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class HwAccess:
	"""HwAccess commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("hwAccess", core, parent)

	def get_description(self) -> str:
		"""SYSTem:PROFiling:HWACcess:DESCription \n
		No command help available \n
			:return: description: No help available
		"""
		response = self._core.io.query_str('SYSTem:PROFiling:HWACcess:DESCription?')
		return trim_str_response(response)

	def get_pduration(self) -> int:
		"""SYSTem:PROFiling:HWACcess:PDURation \n
		No command help available \n
			:return: duration_us: No help available
		"""
		response = self._core.io.query_str('SYSTem:PROFiling:HWACcess:PDURation?')
		return Conversions.str_to_int(response)

	def set_pduration(self, duration_us: int) -> None:
		"""SYSTem:PROFiling:HWACcess:PDURation \n
		No command help available \n
			:param duration_us: No help available
		"""
		param = Conversions.decimal_value_to_str(duration_us)
		self._core.io.write(f'SYSTem:PROFiling:HWACcess:PDURation {param}')

	def get_state(self) -> bool:
		"""SYSTem:PROFiling:HWACcess:STATe \n
		No command help available \n
			:return: state: No help available
		"""
		response = self._core.io.query_str('SYSTem:PROFiling:HWACcess:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""SYSTem:PROFiling:HWACcess:STATe \n
		No command help available \n
			:param state: No help available
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SYSTem:PROFiling:HWACcess:STATe {param}')
