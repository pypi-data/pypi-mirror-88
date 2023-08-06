from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dm:
	"""Dm commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dm", core, parent)

	def get_filter_py(self) -> int:
		"""[SOURce<HW>]:BB:PROGress:MCODer:DM:FILTer \n
		No command help available \n
			:return: filter_py: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:PROGress:MCODer:DM:FILTer?')
		return Conversions.str_to_int(response)

	def get_sub(self) -> int:
		"""[SOURce<HW>]:BB:PROGress:MCODer:DM:SUB \n
		No command help available \n
			:return: sub: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:PROGress:MCODer:DM:SUB?')
		return Conversions.str_to_int(response)
