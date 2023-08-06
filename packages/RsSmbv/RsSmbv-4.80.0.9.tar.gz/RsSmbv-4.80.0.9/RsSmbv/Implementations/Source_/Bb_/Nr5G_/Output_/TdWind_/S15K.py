from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class S15K:
	"""S15K commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("s15K", core, parent)

	def get_trtsamples(self) -> int:
		"""[SOURce<HW>]:BB:NR5G:OUTPut:TDWind:S15K:TRTSamples \n
		Queries the number of transition samples.
			INTRO_CMD_HELP: The next to last block in the command syntax indicates the used SCS and CP combination. \n
			- DL: SE<SCS>K, where E indicates the extended CP or for normal CP, the designation is omitted \n
			:return: transition_sampl: integer Range: 0 to 1000
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:OUTPut:TDWind:S15K:TRTSamples?')
		return Conversions.str_to_int(response)

	def get_tr_time(self) -> float:
		"""[SOURce<HW>]:BB:NR5G:OUTPut:TDWind:S15K:TRTime \n
		Sets the transition time when time domain windowing is active.
			INTRO_CMD_HELP: The next to last block in the command syntax indicates the used SCS and CP combination. \n
			- DL: SE<SCS>K, where E indicates the extended CP or for normal CP, the designation is omitted \n
			:return: transition_time: float Range: 0 to 1E-5
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:OUTPut:TDWind:S15K:TRTime?')
		return Conversions.str_to_float(response)

	def set_tr_time(self, transition_time: float) -> None:
		"""[SOURce<HW>]:BB:NR5G:OUTPut:TDWind:S15K:TRTime \n
		Sets the transition time when time domain windowing is active.
			INTRO_CMD_HELP: The next to last block in the command syntax indicates the used SCS and CP combination. \n
			- DL: SE<SCS>K, where E indicates the extended CP or for normal CP, the designation is omitted \n
			:param transition_time: float Range: 0 to 1E-5
		"""
		param = Conversions.decimal_value_to_str(transition_time)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:OUTPut:TDWind:S15K:TRTime {param}')
