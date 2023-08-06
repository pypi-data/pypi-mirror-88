from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class AdMrs:
	"""AdMrs commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("adMrs", core, parent)

	def get_state(self) -> bool:
		"""[SOURce<HW>]:BB:NR5G:TCW:WS:ADMRs:STATe \n
		Enables or disabled the additional DMRS. Additional DMRS signals increase the probability that the UE receives the
		demodulation reference symbols. It leads to a support of lower SNR conditions. \n
			:return: add_dmrs: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:TCW:WS:ADMRs:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, add_dmrs: bool) -> None:
		"""[SOURce<HW>]:BB:NR5G:TCW:WS:ADMRs:STATe \n
		Enables or disabled the additional DMRS. Additional DMRS signals increase the probability that the UE receives the
		demodulation reference symbols. It leads to a support of lower SNR conditions. \n
			:param add_dmrs: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(add_dmrs)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:TCW:WS:ADMRs:STATe {param}')
