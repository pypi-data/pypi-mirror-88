from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Lora:
	"""Lora commands group definition. 55 total commands, 7 Sub-groups, 6 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("lora", core, parent)

	def clone(self) -> 'Lora':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Lora(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def clock(self):
		"""clock commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_clock'):
			from .Lora_.Clock import Clock
			self._clock = Clock(self._core, self._base)
		return self._clock

	@property
	def fconfiguration(self):
		"""fconfiguration commands group. 9 Sub-classes, 5 commands."""
		if not hasattr(self, '_fconfiguration'):
			from .Lora_.Fconfiguration import Fconfiguration
			self._fconfiguration = Fconfiguration(self._core, self._base)
		return self._fconfiguration

	@property
	def impairments(self):
		"""impairments commands group. 1 Sub-classes, 6 commands."""
		if not hasattr(self, '_impairments'):
			from .Lora_.Impairments import Impairments
			self._impairments = Impairments(self._core, self._base)
		return self._impairments

	@property
	def setting(self):
		"""setting commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_setting'):
			from .Lora_.Setting import Setting
			self._setting = Setting(self._core, self._base)
		return self._setting

	@property
	def symbolRate(self):
		"""symbolRate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_symbolRate'):
			from .Lora_.SymbolRate import SymbolRate
			self._symbolRate = SymbolRate(self._core, self._base)
		return self._symbolRate

	@property
	def trigger(self):
		"""trigger commands group. 4 Sub-classes, 5 commands."""
		if not hasattr(self, '_trigger'):
			from .Lora_.Trigger import Trigger
			self._trigger = Trigger(self._core, self._base)
		return self._trigger

	@property
	def waveform(self):
		"""waveform commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_waveform'):
			from .Lora_.Waveform import Waveform
			self._waveform = Waveform(self._core, self._base)
		return self._waveform

	# noinspection PyTypeChecker
	def get_bandwidth(self) -> enums.LoRaBw:
		"""[SOURce<HW>]:BB:LORA:BWIDth \n
		Sets the channel bandwidth. \n
			:return: bw: BW7| BW10| BW15| BW20| BW31| BW41| BW62| BW125| BW250| BW500
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:LORA:BWIDth?')
		return Conversions.str_to_scalar_enum(response, enums.LoRaBw)

	def set_bandwidth(self, bw: enums.LoRaBw) -> None:
		"""[SOURce<HW>]:BB:LORA:BWIDth \n
		Sets the channel bandwidth. \n
			:param bw: BW7| BW10| BW15| BW20| BW31| BW41| BW62| BW125| BW250| BW500
		"""
		param = Conversions.enum_scalar_to_str(bw, enums.LoRaBw)
		self._core.io.write(f'SOURce<HwInstance>:BB:LORA:BWIDth {param}')

	def get_iinterval(self) -> float:
		"""[SOURce<HW>]:BB:LORA:IINTerval \n
		Sets the time of the interval separating two frames. \n
			:return: iinterval: float Range: 0 to 1, Unit: s
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:LORA:IINTerval?')
		return Conversions.str_to_float(response)

	def set_iinterval(self, iinterval: float) -> None:
		"""[SOURce<HW>]:BB:LORA:IINTerval \n
		Sets the time of the interval separating two frames. \n
			:param iinterval: float Range: 0 to 1, Unit: s
		"""
		param = Conversions.decimal_value_to_str(iinterval)
		self._core.io.write(f'SOURce<HwInstance>:BB:LORA:IINTerval {param}')

	def get_osampling(self) -> int:
		"""[SOURce<HW>]:BB:LORA:OSAMpling \n
		Sets the oversampling factor of the generated waveform. A reduced sample rate saves significantly the amount of memory or
		allows an increased signal cycle time, and vice versa. \n
			:return: osampling: integer Range: 1 to 32
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:LORA:OSAMpling?')
		return Conversions.str_to_int(response)

	def set_osampling(self, osampling: int) -> None:
		"""[SOURce<HW>]:BB:LORA:OSAMpling \n
		Sets the oversampling factor of the generated waveform. A reduced sample rate saves significantly the amount of memory or
		allows an increased signal cycle time, and vice versa. \n
			:param osampling: integer Range: 1 to 32
		"""
		param = Conversions.decimal_value_to_str(osampling)
		self._core.io.write(f'SOURce<HwInstance>:BB:LORA:OSAMpling {param}')

	def preset(self) -> None:
		"""[SOURce<HW>]:BB:LORA:PRESet \n
		Sets the parameters of the digital standard to their default values (*RST values specified for the commands) .
		Not affected is the state set with the command method RsSmbv.Source.Bb.Lora.state. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:BB:LORA:PRESet')

	def preset_with_opc(self) -> None:
		"""[SOURce<HW>]:BB:LORA:PRESet \n
		Sets the parameters of the digital standard to their default values (*RST values specified for the commands) .
		Not affected is the state set with the command method RsSmbv.Source.Bb.Lora.state. \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:LORA:PRESet')

	def get_slength(self) -> int:
		"""[SOURce<HW>]:BB:LORA:SLENgth \n
		Sets the sequence length of the signal in number of frames. The signal is calculated in advance and output in the
		arbitrary waveform generator. \n
			:return: slength: integer Range: 1 to dynamic
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:LORA:SLENgth?')
		return Conversions.str_to_int(response)

	def set_slength(self, slength: int) -> None:
		"""[SOURce<HW>]:BB:LORA:SLENgth \n
		Sets the sequence length of the signal in number of frames. The signal is calculated in advance and output in the
		arbitrary waveform generator. \n
			:param slength: integer Range: 1 to dynamic
		"""
		param = Conversions.decimal_value_to_str(slength)
		self._core.io.write(f'SOURce<HwInstance>:BB:LORA:SLENgth {param}')

	def get_state(self) -> bool:
		"""[SOURce<HW>]:BB:LORA:STATe \n
		Activates the standard and deactivates all the other digital standards and digital modulation modes in the same path. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:LORA:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""[SOURce<HW>]:BB:LORA:STATe \n
		Activates the standard and deactivates all the other digital standards and digital modulation modes in the same path. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:LORA:STATe {param}')
