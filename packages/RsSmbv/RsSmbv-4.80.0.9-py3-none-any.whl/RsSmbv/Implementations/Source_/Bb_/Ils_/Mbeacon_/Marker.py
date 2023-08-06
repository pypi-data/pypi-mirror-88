from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Marker:
	"""Marker commands group definition. 3 total commands, 0 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("marker", core, parent)

	# noinspection PyTypeChecker
	def get_frequency(self) -> enums.AvionicMkrBcnMarkFreq:
		"""[SOURce<HW>]:[BB]:[ILS]:MBEacon:MARKer:FREQuency \n
		Sets the modulation frequency of the marker signal for the ILS marker beacon modulation signal. \n
			:return: frequency: 400| 1300| 3000 Unit: Hz
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ILS:MBEacon:MARKer:FREQuency?')
		return Conversions.str_to_scalar_enum(response, enums.AvionicMkrBcnMarkFreq)

	def set_frequency(self, frequency: enums.AvionicMkrBcnMarkFreq) -> None:
		"""[SOURce<HW>]:[BB]:[ILS]:MBEacon:MARKer:FREQuency \n
		Sets the modulation frequency of the marker signal for the ILS marker beacon modulation signal. \n
			:param frequency: 400| 1300| 3000 Unit: Hz
		"""
		param = Conversions.enum_scalar_to_str(frequency, enums.AvionicMkrBcnMarkFreq)
		self._core.io.write(f'SOURce<HwInstance>:BB:ILS:MBEacon:MARKer:FREQuency {param}')

	def get_depth(self) -> float:
		"""[SOURce<HW>]:[BB]:[ILS]:MBEacon:[MARKer]:DEPTh \n
		Sets the modulation depth of the marker signal for the ILS marker beacon signal. \n
			:return: depth: float Range: 0 to 100
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ILS:MBEacon:MARKer:DEPTh?')
		return Conversions.str_to_float(response)

	def set_depth(self, depth: float) -> None:
		"""[SOURce<HW>]:[BB]:[ILS]:MBEacon:[MARKer]:DEPTh \n
		Sets the modulation depth of the marker signal for the ILS marker beacon signal. \n
			:param depth: float Range: 0 to 100
		"""
		param = Conversions.decimal_value_to_str(depth)
		self._core.io.write(f'SOURce<HwInstance>:BB:ILS:MBEacon:MARKer:DEPTh {param}')

	def get_pulsed(self) -> bool:
		"""[SOURce<HW>]:[BB]:[ILS]:MBEacon:[MARKer]:PULSed \n
		Activates the modulation of a pulsed marker signal (morse coding) . \n
			:return: pulsed: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ILS:MBEacon:MARKer:PULSed?')
		return Conversions.str_to_bool(response)

	def set_pulsed(self, pulsed: bool) -> None:
		"""[SOURce<HW>]:[BB]:[ILS]:MBEacon:[MARKer]:PULSed \n
		Activates the modulation of a pulsed marker signal (morse coding) . \n
			:param pulsed: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(pulsed)
		self._core.io.write(f'SOURce<HwInstance>:BB:ILS:MBEacon:MARKer:PULSed {param}')
