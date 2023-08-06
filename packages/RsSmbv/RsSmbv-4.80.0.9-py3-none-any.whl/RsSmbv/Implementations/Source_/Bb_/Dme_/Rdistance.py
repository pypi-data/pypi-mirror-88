from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Rdistance:
	"""Rdistance commands group definition. 2 total commands, 0 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rdistance", core, parent)

	# noinspection PyTypeChecker
	def get_unit(self) -> enums.UnitNmAvionic:
		"""[SOURce<HW>]:[BB]:DME:RDIStance:UNIT \n
		Sets the unit for the range distance that can be defined with the method RsSmbv.Source.Bb.Dme.Rdistance.value.
		The distance can be given in nautic miles (NM) or µs. 1 nm is 1852.01 meters and corresponds to a run time of 12.359 µs. \n
			:return: unit: US| NM
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:RDIStance:UNIT?')
		return Conversions.str_to_scalar_enum(response, enums.UnitNmAvionic)

	def set_unit(self, unit: enums.UnitNmAvionic) -> None:
		"""[SOURce<HW>]:[BB]:DME:RDIStance:UNIT \n
		Sets the unit for the range distance that can be defined with the method RsSmbv.Source.Bb.Dme.Rdistance.value.
		The distance can be given in nautic miles (NM) or µs. 1 nm is 1852.01 meters and corresponds to a run time of 12.359 µs. \n
			:param unit: US| NM
		"""
		param = Conversions.enum_scalar_to_str(unit, enums.UnitNmAvionic)
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:RDIStance:UNIT {param}')

	def get_value(self) -> float:
		"""[SOURce<HW>]:[BB]:DME:RDIStance \n
		Sets the simulated distance between the interrogator and the transponder for reply mode (BB:DME:MODE:REPLy) .
		The distance can be given in nautic miles (NM) or µs with the command method RsSmbv.Source.Bb.Dme.Rdistance.unit. If the
		unit is not provided next to the value, the value is considered to be in the current unit (last unit set via GUI or the
		SCPI) . The query always provides the value in the unit set with method RsSmbv.Source.Bb.Dme.Rdistance.unit. The range
		distance and the external trigger delay are interdependent according to: Range distance = (trigger delay – X/Y mode
		delay) /12.359 μs/nm (X mode delay = 50 μs, Y mode delay is 56 μs) Changing one value automatically changes the other
		value. \n
			:return: rdistance: float Range: -4.046 (X) , -4.531 (Y) to 400
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:RDIStance?')
		return Conversions.str_to_float(response)

	def set_value(self, rdistance: float) -> None:
		"""[SOURce<HW>]:[BB]:DME:RDIStance \n
		Sets the simulated distance between the interrogator and the transponder for reply mode (BB:DME:MODE:REPLy) .
		The distance can be given in nautic miles (NM) or µs with the command method RsSmbv.Source.Bb.Dme.Rdistance.unit. If the
		unit is not provided next to the value, the value is considered to be in the current unit (last unit set via GUI or the
		SCPI) . The query always provides the value in the unit set with method RsSmbv.Source.Bb.Dme.Rdistance.unit. The range
		distance and the external trigger delay are interdependent according to: Range distance = (trigger delay – X/Y mode
		delay) /12.359 μs/nm (X mode delay = 50 μs, Y mode delay is 56 μs) Changing one value automatically changes the other
		value. \n
			:param rdistance: float Range: -4.046 (X) , -4.531 (Y) to 400
		"""
		param = Conversions.decimal_value_to_str(rdistance)
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:RDIStance {param}')
