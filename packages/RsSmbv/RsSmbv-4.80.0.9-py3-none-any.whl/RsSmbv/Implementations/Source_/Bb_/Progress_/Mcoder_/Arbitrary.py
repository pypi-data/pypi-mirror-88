from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Arbitrary:
	"""Arbitrary commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("arbitrary", core, parent)

	def get_mcarrier(self) -> int:
		"""[SOURce<HW>]:BB:PROGress:MCODer:ARBitrary:MCARrier \n
		Queries the status of an initiated process, like for example the calculation of a signal in accordance to a digital
		standard, or the calculation of a multi-carrier or multi-segment waveform file. \n
			:return: mcarrier: integer Indicates the task progress in percent Range: 0 to 100
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:PROGress:MCODer:ARBitrary:MCARrier?')
		return Conversions.str_to_int(response)

	def get_wsegment(self) -> int:
		"""[SOURce<HW>]:BB:PROGress:MCODer:ARBitrary:WSEGment \n
		Queries the status of an initiated process, like for example the calculation of a signal in accordance to a digital
		standard, or the calculation of a multi-carrier or multi-segment waveform file. \n
			:return: wsegment: integer Indicates the task progress in percent Range: 0 to 100
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:PROGress:MCODer:ARBitrary:WSEGment?')
		return Conversions.str_to_int(response)
