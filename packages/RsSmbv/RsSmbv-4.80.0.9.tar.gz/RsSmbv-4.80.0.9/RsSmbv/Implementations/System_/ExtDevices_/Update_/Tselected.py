from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Utilities import trim_str_response


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tselected:
	"""Tselected commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tselected", core, parent)

	def get_catalog(self) -> str:
		"""SYSTem:EXTDevices:UPDate:TSELected:CATalog \n
		No command help available \n
			:return: catalog: No help available
		"""
		response = self._core.io.query_str('SYSTem:EXTDevices:UPDate:TSELected:CATalog?')
		return trim_str_response(response)

	def get_step(self) -> str:
		"""SYSTem:EXTDevices:UPDate:TSELected:STEP \n
		No command help available \n
			:return: sel_string: No help available
		"""
		response = self._core.io.query_str('SYSTem:EXTDevices:UPDate:TSELected:STEP?')
		return trim_str_response(response)

	def set_step(self, sel_string: str) -> None:
		"""SYSTem:EXTDevices:UPDate:TSELected:STEP \n
		No command help available \n
			:param sel_string: No help available
		"""
		param = Conversions.value_to_quoted_str(sel_string)
		self._core.io.write(f'SYSTem:EXTDevices:UPDate:TSELected:STEP {param}')
