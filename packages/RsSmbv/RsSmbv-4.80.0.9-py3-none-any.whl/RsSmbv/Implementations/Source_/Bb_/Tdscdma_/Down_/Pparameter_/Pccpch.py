from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pccpch:
	"""Pccpch commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pccpch", core, parent)

	def get_state(self) -> bool:
		"""[SOURce<HW>]:BB:TDSCdma:DOWN:PPARameter:PCCPch:STATe \n
		Defines, if P-CCPCH is used in the scenario or not. If P-CCPCH is used, both P-CCPCHs are activated in slot 0 with
		spreading code 0+1. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:TDSCdma:DOWN:PPARameter:PCCPch:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""[SOURce<HW>]:BB:TDSCdma:DOWN:PPARameter:PCCPch:STATe \n
		Defines, if P-CCPCH is used in the scenario or not. If P-CCPCH is used, both P-CCPCHs are activated in slot 0 with
		spreading code 0+1. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:TDSCdma:DOWN:PPARameter:PCCPch:STATe {param}')
