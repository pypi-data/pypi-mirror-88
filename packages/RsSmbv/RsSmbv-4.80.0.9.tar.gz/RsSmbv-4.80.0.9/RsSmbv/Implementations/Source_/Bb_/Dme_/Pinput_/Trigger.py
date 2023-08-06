from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Trigger:
	"""Trigger commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("trigger", core, parent)

	def get_level(self) -> float:
		"""[SOURce<HW>]:[BB]:DME:PINPut:TRIGger:LEVel \n
		Queries the measured trigger threshold. \n
			:return: trigger_level: float Range: -200 to 200
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:PINPut:TRIGger:LEVel?')
		return Conversions.str_to_float(response)

	def get_search(self) -> bool:
		"""[SOURce<HW>]:[BB]:DME:PINPut:TRIGger:SEARch \n
		Determines the trigger level = 50% voltage point of first pulse of the external DME interrogation signal. Determination
		of the trigger point requires a connected power sensor. Use the R&S NRP-Z81 power sensor to receive the external DME
		signal. Repeat the trigger search function when changing the level of the external DME signal. \n
			:return: search: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:PINPut:TRIGger:SEARch?')
		return Conversions.str_to_bool(response)
