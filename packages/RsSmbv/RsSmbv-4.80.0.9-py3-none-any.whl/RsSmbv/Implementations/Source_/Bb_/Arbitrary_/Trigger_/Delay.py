from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Delay:
	"""Delay commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("delay", core, parent)

	# noinspection PyTypeChecker
	def get_unit(self) -> enums.TrigDelUnit:
		"""[SOURce<HW>]:BB:ARBitrary:TRIGger:DELay:UNIT \n
		Sets the units the trigger delay is expressed in. \n
			:return: trig_del_unit: SAMPle| TIME
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:TRIGger:DELay:UNIT?')
		return Conversions.str_to_scalar_enum(response, enums.TrigDelUnit)

	def set_unit(self, trig_del_unit: enums.TrigDelUnit) -> None:
		"""[SOURce<HW>]:BB:ARBitrary:TRIGger:DELay:UNIT \n
		Sets the units the trigger delay is expressed in. \n
			:param trig_del_unit: SAMPle| TIME
		"""
		param = Conversions.enum_scalar_to_str(trig_del_unit, enums.TrigDelUnit)
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:TRIGger:DELay:UNIT {param}')
