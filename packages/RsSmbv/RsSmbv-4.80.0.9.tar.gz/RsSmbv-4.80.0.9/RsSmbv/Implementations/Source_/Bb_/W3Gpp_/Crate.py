from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Crate:
	"""Crate commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("crate", core, parent)

	def get_variation(self) -> float:
		"""[SOURce<HW>]:BB:W3GPp:CRATe:VARiation \n
		Sets the output chip rate. The chip rate entry changes the output clock and the modulation bandwidth, as well as the
		synchronization signals that are output. It does not affect the calculated chip sequence. \n
			:return: variation: float Range: 400 to 5E6
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:W3GPp:CRATe:VARiation?')
		return Conversions.str_to_float(response)

	def set_variation(self, variation: float) -> None:
		"""[SOURce<HW>]:BB:W3GPp:CRATe:VARiation \n
		Sets the output chip rate. The chip rate entry changes the output clock and the modulation bandwidth, as well as the
		synchronization signals that are output. It does not affect the calculated chip sequence. \n
			:param variation: float Range: 400 to 5E6
		"""
		param = Conversions.decimal_value_to_str(variation)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:CRATe:VARiation {param}')

	# noinspection PyTypeChecker
	def get_value(self) -> enums.ChipRate:
		"""[SOURce<HW>]:BB:W3GPp:CRATe \n
		The command queries the set system chip rate. The output chip rate can be set with the command method RsSmbv.Source.Bb.
		W3Gpp.Crate.variation. \n
			:return: crate: R3M8
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:W3GPp:CRATe?')
		return Conversions.str_to_scalar_enum(response, enums.ChipRate)
