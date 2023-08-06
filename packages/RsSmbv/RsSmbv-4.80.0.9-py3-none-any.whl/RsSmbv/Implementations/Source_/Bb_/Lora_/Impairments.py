from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Impairments:
	"""Impairments commands group definition. 7 total commands, 1 Sub-groups, 6 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("impairments", core, parent)

	def clone(self) -> 'Impairments':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Impairments(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def fdrift(self):
		"""fdrift commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fdrift'):
			from .Impairments_.Fdrift import Fdrift
			self._fdrift = Fdrift(self._core, self._base)
		return self._fdrift

	def get_fd_deviation(self) -> int:
		"""[SOURce<HW>]:BB:LORA:IMPairments:FDDeviation \n
		Sets the frequency deviation of the frequency drift. \n
			:return: fd_deviation: integer Range: -200E3 to 200E3
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:LORA:IMPairments:FDDeviation?')
		return Conversions.str_to_int(response)

	def set_fd_deviation(self, fd_deviation: int) -> None:
		"""[SOURce<HW>]:BB:LORA:IMPairments:FDDeviation \n
		Sets the frequency deviation of the frequency drift. \n
			:param fd_deviation: integer Range: -200E3 to 200E3
		"""
		param = Conversions.decimal_value_to_str(fd_deviation)
		self._core.io.write(f'SOURce<HwInstance>:BB:LORA:IMPairments:FDDeviation {param}')

	def get_fd_rate(self) -> int:
		"""[SOURce<HW>]:BB:LORA:IMPairments:FDRate \n
		Sets the rate of the carrier frequency drift. \n
			:return: fd_rate: integer Range: 160 to 1.6E3
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:LORA:IMPairments:FDRate?')
		return Conversions.str_to_int(response)

	def set_fd_rate(self, fd_rate: int) -> None:
		"""[SOURce<HW>]:BB:LORA:IMPairments:FDRate \n
		Sets the rate of the carrier frequency drift. \n
			:param fd_rate: integer Range: 160 to 1.6E3
		"""
		param = Conversions.decimal_value_to_str(fd_rate)
		self._core.io.write(f'SOURce<HwInstance>:BB:LORA:IMPairments:FDRate {param}')

	# noinspection PyTypeChecker
	def get_fd_type(self) -> enums.LoRaFreqDfTp:
		"""[SOURce<HW>]:BB:LORA:IMPairments:FDTYpe \n
		Sets the frequency drift type. \n
			:return: fd_type: LINear| SINE LINear Generation of frequency drift is set linear. SINE Generation of frequency drift is set sinusoid.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:LORA:IMPairments:FDTYpe?')
		return Conversions.str_to_scalar_enum(response, enums.LoRaFreqDfTp)

	def set_fd_type(self, fd_type: enums.LoRaFreqDfTp) -> None:
		"""[SOURce<HW>]:BB:LORA:IMPairments:FDTYpe \n
		Sets the frequency drift type. \n
			:param fd_type: LINear| SINE LINear Generation of frequency drift is set linear. SINE Generation of frequency drift is set sinusoid.
		"""
		param = Conversions.enum_scalar_to_str(fd_type, enums.LoRaFreqDfTp)
		self._core.io.write(f'SOURce<HwInstance>:BB:LORA:IMPairments:FDTYpe {param}')

	def get_foffset(self) -> int:
		"""[SOURce<HW>]:BB:LORA:IMPairments:FOFFset \n
		Sets the frequency offset. \n
			:return: fo_ffset: integer Range: -200E3 to 200E3
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:LORA:IMPairments:FOFFset?')
		return Conversions.str_to_int(response)

	def set_foffset(self, fo_ffset: int) -> None:
		"""[SOURce<HW>]:BB:LORA:IMPairments:FOFFset \n
		Sets the frequency offset. \n
			:param fo_ffset: integer Range: -200E3 to 200E3
		"""
		param = Conversions.decimal_value_to_str(fo_ffset)
		self._core.io.write(f'SOURce<HwInstance>:BB:LORA:IMPairments:FOFFset {param}')

	def get_state(self) -> bool:
		"""[SOURce<HW>]:BB:LORA:IMPairments:STATe \n
		Activates impairments settings in the payload. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:LORA:IMPairments:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""[SOURce<HW>]:BB:LORA:IMPairments:STATe \n
		Activates impairments settings in the payload. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:LORA:IMPairments:STATe {param}')

	def get_st_error(self) -> int:
		"""[SOURce<HW>]:BB:LORA:IMPairments:STERror \n
		Sets symbol timing error. \n
			:return: st_error: integer Range: -300 to 300
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:LORA:IMPairments:STERror?')
		return Conversions.str_to_int(response)

	def set_st_error(self, st_error: int) -> None:
		"""[SOURce<HW>]:BB:LORA:IMPairments:STERror \n
		Sets symbol timing error. \n
			:param st_error: integer Range: -300 to 300
		"""
		param = Conversions.decimal_value_to_str(st_error)
		self._core.io.write(f'SOURce<HwInstance>:BB:LORA:IMPairments:STERror {param}')
