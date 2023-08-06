from ...Internal.Core import Core
from ...Internal.CommandsGroup import CommandsGroup
from ...Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class FreqSweep:
	"""FreqSweep commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("freqSweep", core, parent)

	def get_continuous(self) -> bool:
		"""INITiate<HW>:FSWeep:CONTinuous \n
		No command help available \n
			:return: freq_sweep_state: No help available
		"""
		response = self._core.io.query_str('INITiate<HwInstance>:FSWeep:CONTinuous?')
		return Conversions.str_to_bool(response)

	def set_continuous(self, freq_sweep_state: bool) -> None:
		"""INITiate<HW>:FSWeep:CONTinuous \n
		No command help available \n
			:param freq_sweep_state: No help available
		"""
		param = Conversions.bool_to_str(freq_sweep_state)
		self._core.io.write(f'INITiate<HwInstance>:FSWeep:CONTinuous {param}')
