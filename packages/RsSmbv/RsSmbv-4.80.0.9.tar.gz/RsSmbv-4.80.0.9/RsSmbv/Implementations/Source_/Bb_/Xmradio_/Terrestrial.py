from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Terrestrial:
	"""Terrestrial commands group definition. 33 total commands, 5 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("terrestrial", core, parent)

	def clone(self) -> 'Terrestrial':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Terrestrial(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def clock(self):
		"""clock commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_clock'):
			from .Terrestrial_.Clock import Clock
			self._clock = Clock(self._core, self._base)
		return self._clock

	@property
	def filterPy(self):
		"""filterPy commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_filterPy'):
			from .Terrestrial_.FilterPy import FilterPy
			self._filterPy = FilterPy(self._core, self._base)
		return self._filterPy

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_power'):
			from .Terrestrial_.Power import Power
			self._power = Power(self._core, self._base)
		return self._power

	@property
	def symbolRate(self):
		"""symbolRate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_symbolRate'):
			from .Terrestrial_.SymbolRate import SymbolRate
			self._symbolRate = SymbolRate(self._core, self._base)
		return self._symbolRate

	@property
	def trigger(self):
		"""trigger commands group. 3 Sub-classes, 4 commands."""
		if not hasattr(self, '_trigger'):
			from .Terrestrial_.Trigger import Trigger
			self._trigger = Trigger(self._core, self._base)
		return self._trigger

	def get_delay(self) -> float:
		"""[SOURce<HW>]:BB:XMRadio:TERRestrial:DELay \n
		No command help available \n
			:return: delay: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:XMRadio:TERRestrial:DELay?')
		return Conversions.str_to_float(response)

	def set_delay(self, delay: float) -> None:
		"""[SOURce<HW>]:BB:XMRadio:TERRestrial:DELay \n
		No command help available \n
			:param delay: No help available
		"""
		param = Conversions.decimal_value_to_str(delay)
		self._core.io.write(f'SOURce<HwInstance>:BB:XMRadio:TERRestrial:DELay {param}')
