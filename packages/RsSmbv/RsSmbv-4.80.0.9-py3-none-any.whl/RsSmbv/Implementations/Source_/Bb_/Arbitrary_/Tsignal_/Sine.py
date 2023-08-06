from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sine:
	"""Sine commands group definition. 5 total commands, 1 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sine", core, parent)

	def clone(self) -> 'Sine':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Sine(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def create(self):
		"""create commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_create'):
			from .Sine_.Create import Create
			self._create = Create(self._core, self._base)
		return self._create

	def get_frequency(self) -> float:
		"""[SOURce<HW>]:BB:ARBitrary:TSIGnal:SINE:FREQuency \n
		Sets the frequency of the simple sinusoidal test signal. \n
			:return: frequency: float Range: 100 to depends on the installed options, Unit: Hz
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:TSIGnal:SINE:FREQuency?')
		return Conversions.str_to_float(response)

	def set_frequency(self, frequency: float) -> None:
		"""[SOURce<HW>]:BB:ARBitrary:TSIGnal:SINE:FREQuency \n
		Sets the frequency of the simple sinusoidal test signal. \n
			:param frequency: float Range: 100 to depends on the installed options, Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(frequency)
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:TSIGnal:SINE:FREQuency {param}')

	def get_phase(self) -> float:
		"""[SOURce<HW>]:BB:ARBitrary:TSIGnal:SINE:PHASe \n
		Sets the phase offset of the sine wave on the Q channel relative to the sine wave on the I channel. \n
			:return: phase: float Range: -180 to 180, Unit: DEG
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:TSIGnal:SINE:PHASe?')
		return Conversions.str_to_float(response)

	def set_phase(self, phase: float) -> None:
		"""[SOURce<HW>]:BB:ARBitrary:TSIGnal:SINE:PHASe \n
		Sets the phase offset of the sine wave on the Q channel relative to the sine wave on the I channel. \n
			:param phase: float Range: -180 to 180, Unit: DEG
		"""
		param = Conversions.decimal_value_to_str(phase)
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:TSIGnal:SINE:PHASe {param}')

	def get_samples(self) -> int:
		"""[SOURce<HW>]:BB:ARBitrary:TSIGnal:SINE:SAMPles \n
		Sets the sample rate for the sine signal in samples per period. The resulting clock rate must not exceed the maximum ARB
		clock rate (see data sheet) . The maximum value is automatically restricted by reference to the set frequency and has to
		fulfill the rule Frequency * Samples <= ARB clock rate. \n
			:return: samples: integer Range: 4 to 1000
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:TSIGnal:SINE:SAMPles?')
		return Conversions.str_to_int(response)

	def set_samples(self, samples: int) -> None:
		"""[SOURce<HW>]:BB:ARBitrary:TSIGnal:SINE:SAMPles \n
		Sets the sample rate for the sine signal in samples per period. The resulting clock rate must not exceed the maximum ARB
		clock rate (see data sheet) . The maximum value is automatically restricted by reference to the set frequency and has to
		fulfill the rule Frequency * Samples <= ARB clock rate. \n
			:param samples: integer Range: 4 to 1000
		"""
		param = Conversions.decimal_value_to_str(samples)
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:TSIGnal:SINE:SAMPles {param}')
