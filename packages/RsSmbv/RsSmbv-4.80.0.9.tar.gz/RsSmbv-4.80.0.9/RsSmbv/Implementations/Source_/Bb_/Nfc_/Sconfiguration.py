from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sconfiguration:
	"""Sconfiguration commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sconfiguration", core, parent)

	def get_tn_samples(self) -> int:
		"""[SOURce<HW>]:BB:NFC:SCONfiguration:TNSamples \n
		Queries the total number of samples allocated to the current frame. \n
			:return: tn_samples: integer
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NFC:SCONfiguration:TNSamples?')
		return Conversions.str_to_int(response)

	def get_ts_duration(self) -> float:
		"""[SOURce<HW>]:BB:NFC:SCONfiguration:TSDuration \n
		Queries the total sequence duration for the current settings. \n
			:return: ts_duration: float
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NFC:SCONfiguration:TSDuration?')
		return Conversions.str_to_float(response)
