from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Cfactor:
	"""Cfactor commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("cfactor", core, parent)

	def get_actual(self) -> float:
		"""[SOURce<HW>]:BB:MCCW:CFACtor:ACTual \n
		Queries the actual Crest Factor for optimization mode target crest. \n
			:return: actual: float Range: 0 to 100
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:MCCW:CFACtor:ACTual?')
		return Conversions.str_to_float(response)

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.MccwCrestFactMode:
		"""[SOURce<HW>]:BB:MCCW:CFACtor:MODE \n
		Sets the mode by which automatic settings minimize the crest factor or hold it at a chosen value. \n
			:return: mode: OFF| CHIRp| SLOW SLOW corresponds to the manual control 'Target Crest'
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:MCCW:CFACtor:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.MccwCrestFactMode)

	def set_mode(self, mode: enums.MccwCrestFactMode) -> None:
		"""[SOURce<HW>]:BB:MCCW:CFACtor:MODE \n
		Sets the mode by which automatic settings minimize the crest factor or hold it at a chosen value. \n
			:param mode: OFF| CHIRp| SLOW SLOW corresponds to the manual control 'Target Crest'
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.MccwCrestFactMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:MCCW:CFACtor:MODE {param}')

	def get_value(self) -> float:
		"""[SOURce<HW>]:BB:MCCW:CFACtor \n
		Sets the desired crest factor, if the optimization mode target crest factor is used. \n
			:return: cfactor: float Range: 0 to 30
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:MCCW:CFACtor?')
		return Conversions.str_to_float(response)

	def set_value(self, cfactor: float) -> None:
		"""[SOURce<HW>]:BB:MCCW:CFACtor \n
		Sets the desired crest factor, if the optimization mode target crest factor is used. \n
			:param cfactor: float Range: 0 to 30
		"""
		param = Conversions.decimal_value_to_str(cfactor)
		self._core.io.write(f'SOURce<HwInstance>:BB:MCCW:CFACtor {param}')
