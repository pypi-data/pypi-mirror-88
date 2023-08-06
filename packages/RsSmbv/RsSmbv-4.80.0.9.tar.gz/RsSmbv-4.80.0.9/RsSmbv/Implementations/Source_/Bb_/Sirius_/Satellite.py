from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Satellite:
	"""Satellite commands group definition. 32 total commands, 4 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("satellite", core, parent)

	def clone(self) -> 'Satellite':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Satellite(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def clock(self):
		"""clock commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_clock'):
			from .Satellite_.Clock import Clock
			self._clock = Clock(self._core, self._base)
		return self._clock

	@property
	def filterPy(self):
		"""filterPy commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_filterPy'):
			from .Satellite_.FilterPy import FilterPy
			self._filterPy = FilterPy(self._core, self._base)
		return self._filterPy

	@property
	def symbolRate(self):
		"""symbolRate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_symbolRate'):
			from .Satellite_.SymbolRate import SymbolRate
			self._symbolRate = SymbolRate(self._core, self._base)
		return self._symbolRate

	@property
	def trigger(self):
		"""trigger commands group. 3 Sub-classes, 3 commands."""
		if not hasattr(self, '_trigger'):
			from .Satellite_.Trigger import Trigger
			self._trigger = Trigger(self._core, self._base)
		return self._trigger

	def get_delay(self) -> float:
		"""[SOURce<HW>]:BB:SIRius:SATellite:DELay \n
		No command help available \n
			:return: delay: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:SIRius:SATellite:DELay?')
		return Conversions.str_to_float(response)

	def set_delay(self, delay: float) -> None:
		"""[SOURce<HW>]:BB:SIRius:SATellite:DELay \n
		No command help available \n
			:param delay: No help available
		"""
		param = Conversions.decimal_value_to_str(delay)
		self._core.io.write(f'SOURce<HwInstance>:BB:SIRius:SATellite:DELay {param}')

	# noinspection PyTypeChecker
	def get_modulation(self) -> enums.SiriusSatMod:
		"""[SOURce<HW>]:BB:SIRius:SATellite:MODulation \n
		No command help available \n
			:return: modulation: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:SIRius:SATellite:MODulation?')
		return Conversions.str_to_scalar_enum(response, enums.SiriusSatMod)

	def set_modulation(self, modulation: enums.SiriusSatMod) -> None:
		"""[SOURce<HW>]:BB:SIRius:SATellite:MODulation \n
		No command help available \n
			:param modulation: No help available
		"""
		param = Conversions.enum_scalar_to_str(modulation, enums.SiriusSatMod)
		self._core.io.write(f'SOURce<HwInstance>:BB:SIRius:SATellite:MODulation {param}')

	def get_oa_offset(self) -> int:
		"""[SOURce<HW>]:BB:SIRius:SATellite:OAOFfset \n
		No command help available \n
			:return: oa_offset: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:SIRius:SATellite:OAOFfset?')
		return Conversions.str_to_int(response)

	def set_oa_offset(self, oa_offset: int) -> None:
		"""[SOURce<HW>]:BB:SIRius:SATellite:OAOFfset \n
		No command help available \n
			:param oa_offset: No help available
		"""
		param = Conversions.decimal_value_to_str(oa_offset)
		self._core.io.write(f'SOURce<HwInstance>:BB:SIRius:SATellite:OAOFfset {param}')
