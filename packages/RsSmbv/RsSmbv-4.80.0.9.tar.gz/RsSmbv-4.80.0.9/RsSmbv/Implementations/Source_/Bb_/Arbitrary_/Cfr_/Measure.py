from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Measure:
	"""Measure commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("measure", core, parent)

	def get_state(self) -> bool:
		"""[SOURce<HW>]:BB:ARBitrary:CFR:MEASure:[STATe] \n
		Queries the state of the crest factor reduction calculation. \n
			:return: measure_state: 0| 1| OFF| ON ON: the original and resulting crest factors are already calculated.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:CFR:MEASure:STATe?')
		return Conversions.str_to_bool(response)
