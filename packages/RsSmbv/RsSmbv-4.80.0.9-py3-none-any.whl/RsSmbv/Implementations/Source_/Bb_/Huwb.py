from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Huwb:
	"""Huwb commands group definition. 91 total commands, 11 Sub-groups, 11 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("huwb", core, parent)

	def clone(self) -> 'Huwb':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Huwb(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def clipping(self):
		"""clipping commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_clipping'):
			from .Huwb_.Clipping import Clipping
			self._clipping = Clipping(self._core, self._base)
		return self._clipping

	@property
	def clock(self):
		"""clock commands group. 1 Sub-classes, 3 commands."""
		if not hasattr(self, '_clock'):
			from .Huwb_.Clock import Clock
			self._clock = Clock(self._core, self._base)
		return self._clock

	@property
	def fconfig(self):
		"""fconfig commands group. 3 Sub-classes, 9 commands."""
		if not hasattr(self, '_fconfig'):
			from .Huwb_.Fconfig import Fconfig
			self._fconfig = Fconfig(self._core, self._base)
		return self._fconfig

	@property
	def filterPy(self):
		"""filterPy commands group. 1 Sub-classes, 3 commands."""
		if not hasattr(self, '_filterPy'):
			from .Huwb_.FilterPy import FilterPy
			self._filterPy = FilterPy(self._core, self._base)
		return self._filterPy

	@property
	def impairments(self):
		"""impairments commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_impairments'):
			from .Huwb_.Impairments import Impairments
			self._impairments = Impairments(self._core, self._base)
		return self._impairments

	@property
	def phr(self):
		"""phr commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_phr'):
			from .Huwb_.Phr import Phr
			self._phr = Phr(self._core, self._base)
		return self._phr

	@property
	def setting(self):
		"""setting commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_setting'):
			from .Huwb_.Setting import Setting
			self._setting = Setting(self._core, self._base)
		return self._setting

	@property
	def symbolRate(self):
		"""symbolRate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_symbolRate'):
			from .Huwb_.SymbolRate import SymbolRate
			self._symbolRate = SymbolRate(self._core, self._base)
		return self._symbolRate

	@property
	def sts(self):
		"""sts commands group. 0 Sub-classes, 5 commands."""
		if not hasattr(self, '_sts'):
			from .Huwb_.Sts import Sts
			self._sts = Sts(self._core, self._base)
		return self._sts

	@property
	def trigger(self):
		"""trigger commands group. 6 Sub-classes, 5 commands."""
		if not hasattr(self, '_trigger'):
			from .Huwb_.Trigger import Trigger
			self._trigger = Trigger(self._core, self._base)
		return self._trigger

	@property
	def waveform(self):
		"""waveform commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_waveform'):
			from .Huwb_.Waveform import Waveform
			self._waveform = Waveform(self._core, self._base)
		return self._waveform

	# noinspection PyTypeChecker
	def get_asl(self) -> enums.HrpUwbActSegmentLength:
		"""[SOURce<HW>]:BB:HUWB:ASL \n
		Sets the active segment length. \n
			:return: act_seg_length: ASL_32| ASL_64| ASL_128| ASL_256
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:ASL?')
		return Conversions.str_to_scalar_enum(response, enums.HrpUwbActSegmentLength)

	def set_asl(self, act_seg_length: enums.HrpUwbActSegmentLength) -> None:
		"""[SOURce<HW>]:BB:HUWB:ASL \n
		Sets the active segment length. \n
			:param act_seg_length: ASL_32| ASL_64| ASL_128| ASL_256
		"""
		param = Conversions.enum_scalar_to_str(act_seg_length, enums.HrpUwbActSegmentLength)
		self._core.io.write(f'SOURce<HwInstance>:BB:HUWB:ASL {param}')

	# noinspection PyTypeChecker
	def get_asn(self) -> enums.HrpUwbActSegmentNum:
		"""[SOURce<HW>]:BB:HUWB:ASN \n
		Sets the number of active segments. \n
			:return: acg_seg_number: ASN_1| ASN_2| ASN_3| ASN_4
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:ASN?')
		return Conversions.str_to_scalar_enum(response, enums.HrpUwbActSegmentNum)

	def set_asn(self, acg_seg_number: enums.HrpUwbActSegmentNum) -> None:
		"""[SOURce<HW>]:BB:HUWB:ASN \n
		Sets the number of active segments. \n
			:param acg_seg_number: ASN_1| ASN_2| ASN_3| ASN_4
		"""
		param = Conversions.enum_scalar_to_str(acg_seg_number, enums.HrpUwbActSegmentNum)
		self._core.io.write(f'SOURce<HwInstance>:BB:HUWB:ASN {param}')

	def get_bandwidth(self) -> float:
		"""[SOURce<HW>]:BB:HUWB:BWIDth \n
		Queries the channel bandwidth. \n
			:return: hrp_uwb_band_width: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:BWIDth?')
		return Conversions.str_to_float(response)

	# noinspection PyTypeChecker
	def get_cccl(self) -> enums.HrpUwbConvConsLen:
		"""[SOURce<HW>]:BB:HUWB:CCCL \n
		Sets the Viterbi constraint length for convolutional coding. \n
			:return: cccl: CL3| CL7
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:CCCL?')
		return Conversions.str_to_scalar_enum(response, enums.HrpUwbConvConsLen)

	def set_cccl(self, cccl: enums.HrpUwbConvConsLen) -> None:
		"""[SOURce<HW>]:BB:HUWB:CCCL \n
		Sets the Viterbi constraint length for convolutional coding. \n
			:param cccl: CL3| CL7
		"""
		param = Conversions.enum_scalar_to_str(cccl, enums.HrpUwbConvConsLen)
		self._core.io.write(f'SOURce<HwInstance>:BB:HUWB:CCCL {param}')

	def get_cnumber(self) -> int:
		"""[SOURce<HW>]:BB:HUWB:CNUMber \n
		Sets the channel number. \n
			:return: channel_number: integer Range: 0 to 15
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:CNUMber?')
		return Conversions.str_to_int(response)

	def set_cnumber(self, channel_number: int) -> None:
		"""[SOURce<HW>]:BB:HUWB:CNUMber \n
		Sets the channel number. \n
			:param channel_number: integer Range: 0 to 15
		"""
		param = Conversions.decimal_value_to_str(channel_number)
		self._core.io.write(f'SOURce<HwInstance>:BB:HUWB:CNUMber {param}')

	def get_iinterval(self) -> float:
		"""[SOURce<HW>]:BB:HUWB:IINTerval \n
		Sets the time of the interval separating two frames. \n
			:return: iinterval: float Range: 0 to 1000000
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:IINTerval?')
		return Conversions.str_to_float(response)

	def set_iinterval(self, iinterval: float) -> None:
		"""[SOURce<HW>]:BB:HUWB:IINTerval \n
		Sets the time of the interval separating two frames. \n
			:param iinterval: float Range: 0 to 1000000
		"""
		param = Conversions.decimal_value_to_str(iinterval)
		self._core.io.write(f'SOURce<HwInstance>:BB:HUWB:IINTerval {param}')

	def preset(self) -> None:
		"""[SOURce<HW>]:BB:HUWB:PRESet \n
		Sets the parameters of the digital standard to their default values (*RST values specified for the commands) .
		Not affected is the state set with the command method RsSmbv.Source.Bb.Huwb.state. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:BB:HUWB:PRESet')

	def preset_with_opc(self) -> None:
		"""[SOURce<HW>]:BB:HUWB:PRESet \n
		Sets the parameters of the digital standard to their default values (*RST values specified for the commands) .
		Not affected is the state set with the command method RsSmbv.Source.Bb.Huwb.state. \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:HUWB:PRESet')

	# noinspection PyTypeChecker
	def get_sfd(self) -> enums.HrpUwbSfdIndex:
		"""[SOURce<HW>]:BB:HUWB:SFD \n
		Sets the start-of-frame delimiter (SFD) . \n
			:return: sfd_index: SFD_0| SFD_1| SFD_2| SFD_3| SFD_4
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:SFD?')
		return Conversions.str_to_scalar_enum(response, enums.HrpUwbSfdIndex)

	def set_sfd(self, sfd_index: enums.HrpUwbSfdIndex) -> None:
		"""[SOURce<HW>]:BB:HUWB:SFD \n
		Sets the start-of-frame delimiter (SFD) . \n
			:param sfd_index: SFD_0| SFD_1| SFD_2| SFD_3| SFD_4
		"""
		param = Conversions.enum_scalar_to_str(sfd_index, enums.HrpUwbSfdIndex)
		self._core.io.write(f'SOURce<HwInstance>:BB:HUWB:SFD {param}')

	def get_slength(self) -> int:
		"""[SOURce<HW>]:BB:HUWB:SLENgth \n
		Sets the sequence length of the signal in number of frames. The signal is calculated in advance and output in the
		arbitrary waveform generator. The maximum number of frames is calculated as follows: Max. No. of Frames = Arbitrary
		waveform memory size/(sampling rate x 10 ms) . \n
			:return: slength: integer Range: 1 to 1024
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:SLENgth?')
		return Conversions.str_to_int(response)

	def set_slength(self, slength: int) -> None:
		"""[SOURce<HW>]:BB:HUWB:SLENgth \n
		Sets the sequence length of the signal in number of frames. The signal is calculated in advance and output in the
		arbitrary waveform generator. The maximum number of frames is calculated as follows: Max. No. of Frames = Arbitrary
		waveform memory size/(sampling rate x 10 ms) . \n
			:param slength: integer Range: 1 to 1024
		"""
		param = Conversions.decimal_value_to_str(slength)
		self._core.io.write(f'SOURce<HwInstance>:BB:HUWB:SLENgth {param}')

	def get_state(self) -> bool:
		"""[SOURce<HW>]:BB:HUWB:STATe \n
		Activates the standard and deactivates all the other digital standards and digital modulation modes in the same path. \n
			:return: hrp_uwb_state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, hrp_uwb_state: bool) -> None:
		"""[SOURce<HW>]:BB:HUWB:STATe \n
		Activates the standard and deactivates all the other digital standards and digital modulation modes in the same path. \n
			:param hrp_uwb_state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(hrp_uwb_state)
		self._core.io.write(f'SOURce<HwInstance>:BB:HUWB:STATe {param}')

	# noinspection PyTypeChecker
	def get_std(self) -> enums.HrpUwbMode:
		"""[SOURce<HW>]:BB:HUWB:STD \n
		Sets the HRP UWB mode. \n
			:return: mode: NONHRP| BPRF| HPRF NONHRP Enables HRP non-ERDEV mode. BPRF Enables HRP-ERDEV base pulse repetition frequency (BPRF) mode. HPRF Enables HRP-ERDEV higher pulse repetition frequency (HPRF) mode.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:STD?')
		return Conversions.str_to_scalar_enum(response, enums.HrpUwbMode)

	def set_std(self, mode: enums.HrpUwbMode) -> None:
		"""[SOURce<HW>]:BB:HUWB:STD \n
		Sets the HRP UWB mode. \n
			:param mode: NONHRP| BPRF| HPRF NONHRP Enables HRP non-ERDEV mode. BPRF Enables HRP-ERDEV base pulse repetition frequency (BPRF) mode. HPRF Enables HRP-ERDEV higher pulse repetition frequency (HPRF) mode.
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.HrpUwbMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:HUWB:STD {param}')
