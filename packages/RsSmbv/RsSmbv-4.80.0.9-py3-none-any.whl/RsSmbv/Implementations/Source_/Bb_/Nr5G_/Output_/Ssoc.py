from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ssoc:
	"""Ssoc commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ssoc", core, parent)

	def get_state(self) -> bool:
		"""[SOURce<HW>]:BB:NR5G:OUTPut:SSOC:STATe \n
		If enabled, the subcarriers that use the same frequency as the center frequency of the baseband output are not
		transmitted. \n
			:return: sup_scon_opc_tr: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:OUTPut:SSOC:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, sup_scon_opc_tr: bool) -> None:
		"""[SOURce<HW>]:BB:NR5G:OUTPut:SSOC:STATe \n
		If enabled, the subcarriers that use the same frequency as the center frequency of the baseband output are not
		transmitted. \n
			:param sup_scon_opc_tr: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(sup_scon_opc_tr)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:OUTPut:SSOC:STATe {param}')
