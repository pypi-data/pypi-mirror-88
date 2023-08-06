from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Rectangle:
	"""Rectangle commands group definition. 6 total commands, 1 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rectangle", core, parent)

	def clone(self) -> 'Rectangle':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Rectangle(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def create(self):
		"""create commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_create'):
			from .Rectangle_.Create import Create
			self._create = Create(self._core, self._base)
		return self._create

	def get_amplitude(self) -> float:
		"""[SOURce<HW>]:BB:ARBitrary:TSIGnal:RECTangle:AMPLitude \n
		Sets the digital amplitude of the rectangular wave. \n
			:return: amplitude: float Range: 0 to 1, Unit: FS
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:TSIGnal:RECTangle:AMPLitude?')
		return Conversions.str_to_float(response)

	def set_amplitude(self, amplitude: float) -> None:
		"""[SOURce<HW>]:BB:ARBitrary:TSIGnal:RECTangle:AMPLitude \n
		Sets the digital amplitude of the rectangular wave. \n
			:param amplitude: float Range: 0 to 1, Unit: FS
		"""
		param = Conversions.decimal_value_to_str(amplitude)
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:TSIGnal:RECTangle:AMPLitude {param}')

	def get_frequency(self) -> float:
		"""[SOURce<HW>]:BB:ARBitrary:TSIGnal:RECTangle:FREQuency \n
		Sets the frequency of the test signal. \n
			:return: frequency: float Range: 100 to depends on the installed options, Unit: Hz
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:TSIGnal:RECTangle:FREQuency?')
		return Conversions.str_to_float(response)

	def set_frequency(self, frequency: float) -> None:
		"""[SOURce<HW>]:BB:ARBitrary:TSIGnal:RECTangle:FREQuency \n
		Sets the frequency of the test signal. \n
			:param frequency: float Range: 100 to depends on the installed options, Unit: Hz
		"""
		param = Conversions.decimal_value_to_str(frequency)
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:TSIGnal:RECTangle:FREQuency {param}')

	def get_offset(self) -> float:
		"""[SOURce<HW>]:BB:ARBitrary:TSIGnal:RECTangle:OFFSet \n
		Sets the DC component. \n
			:return: offset: float Range: -1 to 1, Unit: FS
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:TSIGnal:RECTangle:OFFSet?')
		return Conversions.str_to_float(response)

	def set_offset(self, offset: float) -> None:
		"""[SOURce<HW>]:BB:ARBitrary:TSIGnal:RECTangle:OFFSet \n
		Sets the DC component. \n
			:param offset: float Range: -1 to 1, Unit: FS
		"""
		param = Conversions.decimal_value_to_str(offset)
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:TSIGnal:RECTangle:OFFSet {param}')

	def get_samples(self) -> int:
		"""[SOURce<HW>]:BB:ARBitrary:TSIGnal:RECTangle:SAMPles \n
		Sets the number of sample values required for the rectangular signal per period. \n
			:return: samples: integer Range: 4 to 1000
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:ARBitrary:TSIGnal:RECTangle:SAMPles?')
		return Conversions.str_to_int(response)

	def set_samples(self, samples: int) -> None:
		"""[SOURce<HW>]:BB:ARBitrary:TSIGnal:RECTangle:SAMPles \n
		Sets the number of sample values required for the rectangular signal per period. \n
			:param samples: integer Range: 4 to 1000
		"""
		param = Conversions.decimal_value_to_str(samples)
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:TSIGnal:RECTangle:SAMPles {param}')
