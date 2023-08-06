from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Osampling:
	"""Osampling commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("osampling", core, parent)

	def get_auto(self) -> bool:
		"""[SOURce<HW>]:BB:GBAS:FILTer:OSAMpling:AUTO \n
		No command help available \n
			:return: auto: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GBAS:FILTer:OSAMpling:AUTO?')
		return Conversions.str_to_bool(response)

	def set_auto(self, auto: bool) -> None:
		"""[SOURce<HW>]:BB:GBAS:FILTer:OSAMpling:AUTO \n
		No command help available \n
			:param auto: No help available
		"""
		param = Conversions.bool_to_str(auto)
		self._core.io.write(f'SOURce<HwInstance>:BB:GBAS:FILTer:OSAMpling:AUTO {param}')

	def get_value(self) -> float:
		"""[SOURce<HW>]:BB:GBAS:FILTer:OSAMpling \n
		No command help available \n
			:return: osampling: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GBAS:FILTer:OSAMpling?')
		return Conversions.str_to_float(response)

	def set_value(self, osampling: float) -> None:
		"""[SOURce<HW>]:BB:GBAS:FILTer:OSAMpling \n
		No command help available \n
			:param osampling: No help available
		"""
		param = Conversions.decimal_value_to_str(osampling)
		self._core.io.write(f'SOURce<HwInstance>:BB:GBAS:FILTer:OSAMpling {param}')
