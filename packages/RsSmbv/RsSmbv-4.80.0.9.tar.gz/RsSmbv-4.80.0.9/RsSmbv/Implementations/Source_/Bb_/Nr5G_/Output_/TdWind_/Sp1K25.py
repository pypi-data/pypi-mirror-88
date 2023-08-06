from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sp1K25:
	"""Sp1K25 commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sp1K25", core, parent)

	def get_trtsamples(self) -> int:
		"""[SOURce<HW>]:BB:NR5G:OUTPut:TDWind:SP1K25:TRTSamples \n
		No command help available \n
			:return: transition_sampl: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:OUTPut:TDWind:SP1K25:TRTSamples?')
		return Conversions.str_to_int(response)

	def get_tr_time(self) -> float:
		"""[SOURce<HW>]:BB:NR5G:OUTPut:TDWind:SP1K25:TRTime \n
		No command help available \n
			:return: transition_time: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:OUTPut:TDWind:SP1K25:TRTime?')
		return Conversions.str_to_float(response)

	def set_tr_time(self, transition_time: float) -> None:
		"""[SOURce<HW>]:BB:NR5G:OUTPut:TDWind:SP1K25:TRTime \n
		No command help available \n
			:param transition_time: No help available
		"""
		param = Conversions.decimal_value_to_str(transition_time)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:OUTPut:TDWind:SP1K25:TRTime {param}')
