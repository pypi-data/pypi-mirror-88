from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ramp:
	"""Ramp commands group definition. 21 total commands, 5 Sub-groups, 10 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ramp", core, parent)

	def clone(self) -> 'Ramp':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Ramp(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def blank(self):
		"""blank commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_blank'):
			from .Ramp_.Blank import Blank
			self._blank = Blank(self._core, self._base)
		return self._blank

	@property
	def fall(self):
		"""fall commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fall'):
			from .Ramp_.Fall import Fall
			self._fall = Fall(self._core, self._base)
		return self._fall

	@property
	def preSweep(self):
		"""preSweep commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_preSweep'):
			from .Ramp_.PreSweep import PreSweep
			self._preSweep = PreSweep(self._core, self._base)
		return self._preSweep

	@property
	def stair(self):
		"""stair commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_stair'):
			from .Ramp_.Stair import Stair
			self._stair = Stair(self._core, self._base)
		return self._stair

	@property
	def sweep(self):
		"""sweep commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sweep'):
			from .Ramp_.Sweep import Sweep
			self._sweep = Sweep(self._core, self._base)
		return self._sweep

	def get_attenuation(self) -> float:
		"""[SOURce<HW>]:BB:PRAMp:RAMP:ATTenuation \n
		No command help available \n
			:return: const_atten: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:PRAMp:RAMP:ATTenuation?')
		return Conversions.str_to_float(response)

	def set_attenuation(self, const_atten: float) -> None:
		"""[SOURce<HW>]:BB:PRAMp:RAMP:ATTenuation \n
		No command help available \n
			:param const_atten: No help available
		"""
		param = Conversions.decimal_value_to_str(const_atten)
		self._core.io.write(f'SOURce<HwInstance>:BB:PRAMp:RAMP:ATTenuation {param}')

	def get_constmode(self) -> bool:
		"""[SOURce<HW>]:BB:PRAMp:RAMP:CONStmode \n
		No command help available \n
			:return: const_mode: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:PRAMp:RAMP:CONStmode?')
		return Conversions.str_to_bool(response)

	def set_constmode(self, const_mode: bool) -> None:
		"""[SOURce<HW>]:BB:PRAMp:RAMP:CONStmode \n
		No command help available \n
			:param const_mode: No help available
		"""
		param = Conversions.bool_to_str(const_mode)
		self._core.io.write(f'SOURce<HwInstance>:BB:PRAMp:RAMP:CONStmode {param}')

	def get_level(self) -> float:
		"""[SOURce<HW>]:BB:PRAMp:RAMP:LEVel \n
		No command help available \n
			:return: const_level: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:PRAMp:RAMP:LEVel?')
		return Conversions.str_to_float(response)

	def get_range(self) -> float:
		"""[SOURce<HW>]:BB:PRAMp:RAMP:RANGe \n
		No command help available \n
			:return: range_py: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:PRAMp:RAMP:RANGe?')
		return Conversions.str_to_float(response)

	def set_range(self, range_py: float) -> None:
		"""[SOURce<HW>]:BB:PRAMp:RAMP:RANGe \n
		No command help available \n
			:param range_py: No help available
		"""
		param = Conversions.decimal_value_to_str(range_py)
		self._core.io.write(f'SOURce<HwInstance>:BB:PRAMp:RAMP:RANGe {param}')

	def get_resolution(self) -> float:
		"""[SOURce<HW>]:BB:PRAMp:RAMP:RESolution \n
		No command help available \n
			:return: power_resolution: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:PRAMp:RAMP:RESolution?')
		return Conversions.str_to_float(response)

	def get_sample_rate(self) -> float:
		"""[SOURce<HW>]:BB:PRAMp:RAMP:SAMPlerate \n
		No command help available \n
			:return: sample_rate: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:PRAMp:RAMP:SAMPlerate?')
		return Conversions.str_to_float(response)

	# noinspection PyTypeChecker
	def get_shape(self) -> enums.PowerRampShape:
		"""[SOURce<HW>]:BB:PRAMp:RAMP:SHAPe \n
		No command help available \n
			:return: shape: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:PRAMp:RAMP:SHAPe?')
		return Conversions.str_to_scalar_enum(response, enums.PowerRampShape)

	def set_shape(self, shape: enums.PowerRampShape) -> None:
		"""[SOURce<HW>]:BB:PRAMp:RAMP:SHAPe \n
		No command help available \n
			:param shape: No help available
		"""
		param = Conversions.enum_scalar_to_str(shape, enums.PowerRampShape)
		self._core.io.write(f'SOURce<HwInstance>:BB:PRAMp:RAMP:SHAPe {param}')

	# noinspection PyTypeChecker
	def get_slope(self) -> enums.PowerRampSlope:
		"""[SOURce<HW>]:BB:PRAMp:RAMP:SLOPe \n
		No command help available \n
			:return: slope: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:PRAMp:RAMP:SLOPe?')
		return Conversions.str_to_scalar_enum(response, enums.PowerRampSlope)

	def set_slope(self, slope: enums.PowerRampSlope) -> None:
		"""[SOURce<HW>]:BB:PRAMp:RAMP:SLOPe \n
		No command help available \n
			:param slope: No help available
		"""
		param = Conversions.enum_scalar_to_str(slope, enums.PowerRampSlope)
		self._core.io.write(f'SOURce<HwInstance>:BB:PRAMp:RAMP:SLOPe {param}')

	def get_start_level(self) -> float:
		"""[SOURce<HW>]:BB:PRAMp:RAMP:STARtlevel \n
		No command help available \n
			:return: start_level: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:PRAMp:RAMP:STARtlevel?')
		return Conversions.str_to_float(response)

	def get_stop_level(self) -> float:
		"""[SOURce<HW>]:BB:PRAMp:RAMP:STOPlevel \n
		No command help available \n
			:return: stop_level: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:PRAMp:RAMP:STOPlevel?')
		return Conversions.str_to_float(response)
