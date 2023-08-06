from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Modulation:
	"""Modulation commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("modulation", core, parent)

	# noinspection PyTypeChecker
	def get(self, modulation: enums.ModulationC) -> enums.ModulationC:
		"""[SOURce<HW>]:BB:EUTRa:DL:MBSFn:AI:MCCH:MODulation \n
		Queries the values as set with the command method RsSmbv.Source.Bb.Eutra.Dl.Mbsfn.Ai.Mcch.mcs. \n
			:param modulation: QPSK| QAM16| QAM64
			:return: modulation: QPSK| QAM16| QAM64"""
		param = Conversions.enum_scalar_to_str(modulation, enums.ModulationC)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:MBSFn:AI:MCCH:MODulation? {param}')
		return Conversions.str_to_scalar_enum(response, enums.ModulationC)
