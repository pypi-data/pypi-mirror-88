from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Utilities import trim_str_response
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Gnss:
	"""Gnss commands group definition. 2177 total commands, 25 Sub-groups, 7 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("gnss", core, parent)

	def clone(self) -> 'Gnss':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Gnss(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def adGeneration(self):
		"""adGeneration commands group. 10 Sub-classes, 1 commands."""
		if not hasattr(self, '_adGeneration'):
			from .Gnss_.AdGeneration import AdGeneration
			self._adGeneration = AdGeneration(self._core, self._base)
		return self._adGeneration

	@property
	def apattern(self):
		"""apattern commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_apattern'):
			from .Gnss_.Apattern import Apattern
			self._apattern = Apattern(self._core, self._base)
		return self._apattern

	@property
	def atmospheric(self):
		"""atmospheric commands group. 7 Sub-classes, 0 commands."""
		if not hasattr(self, '_atmospheric'):
			from .Gnss_.Atmospheric import Atmospheric
			self._atmospheric = Atmospheric(self._core, self._base)
		return self._atmospheric

	@property
	def awgn(self):
		"""awgn commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_awgn'):
			from .Gnss_.Awgn import Awgn
			self._awgn = Awgn(self._core, self._base)
		return self._awgn

	@property
	def body(self):
		"""body commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_body'):
			from .Gnss_.Body import Body
			self._body = Body(self._core, self._base)
		return self._body

	@property
	def clock(self):
		"""clock commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_clock'):
			from .Gnss_.Clock import Clock
			self._clock = Clock(self._core, self._base)
		return self._clock

	@property
	def l1Band(self):
		"""l1Band commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_l1Band'):
			from .Gnss_.L1Band import L1Band
			self._l1Band = L1Band(self._core, self._base)
		return self._l1Band

	@property
	def l2Band(self):
		"""l2Band commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_l2Band'):
			from .Gnss_.L2Band import L2Band
			self._l2Band = L2Band(self._core, self._base)
		return self._l2Band

	@property
	def l5Band(self):
		"""l5Band commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_l5Band'):
			from .Gnss_.L5Band import L5Band
			self._l5Band = L5Band(self._core, self._base)
		return self._l5Band

	@property
	def logging(self):
		"""logging commands group. 4 Sub-classes, 1 commands."""
		if not hasattr(self, '_logging'):
			from .Gnss_.Logging import Logging
			self._logging = Logging(self._core, self._base)
		return self._logging

	@property
	def monitor(self):
		"""monitor commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_monitor'):
			from .Gnss_.Monitor import Monitor
			self._monitor = Monitor(self._core, self._base)
		return self._monitor

	@property
	def obscuration(self):
		"""obscuration commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_obscuration'):
			from .Gnss_.Obscuration import Obscuration
			self._obscuration = Obscuration(self._core, self._base)
		return self._obscuration

	@property
	def ostreams(self):
		"""ostreams commands group. 1 Sub-classes, 3 commands."""
		if not hasattr(self, '_ostreams'):
			from .Gnss_.Ostreams import Ostreams
			self._ostreams = Ostreams(self._core, self._base)
		return self._ostreams

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_power'):
			from .Gnss_.Power import Power
			self._power = Power(self._core, self._base)
		return self._power

	@property
	def receiver(self):
		"""receiver commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_receiver'):
			from .Gnss_.Receiver import Receiver
			self._receiver = Receiver(self._core, self._base)
		return self._receiver

	@property
	def rt(self):
		"""rt commands group. 8 Sub-classes, 2 commands."""
		if not hasattr(self, '_rt'):
			from .Gnss_.Rt import Rt
			self._rt = Rt(self._core, self._base)
		return self._rt

	@property
	def setting(self):
		"""setting commands group. 2 Sub-classes, 3 commands."""
		if not hasattr(self, '_setting'):
			from .Gnss_.Setting import Setting
			self._setting = Setting(self._core, self._base)
		return self._setting

	@property
	def simulation(self):
		"""simulation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_simulation'):
			from .Gnss_.Simulation import Simulation
			self._simulation = Simulation(self._core, self._base)
		return self._simulation

	@property
	def stream(self):
		"""stream commands group. 10 Sub-classes, 0 commands."""
		if not hasattr(self, '_stream'):
			from .Gnss_.Stream import Stream
			self._stream = Stream(self._core, self._base)
		return self._stream

	@property
	def sv(self):
		"""sv commands group. 9 Sub-classes, 0 commands."""
		if not hasattr(self, '_sv'):
			from .Gnss_.Sv import Sv
			self._sv = Sv(self._core, self._base)
		return self._sv

	@property
	def svid(self):
		"""svid commands group. 7 Sub-classes, 0 commands."""
		if not hasattr(self, '_svid'):
			from .Gnss_.Svid import Svid
			self._svid = Svid(self._core, self._base)
		return self._svid

	@property
	def system(self):
		"""system commands group. 7 Sub-classes, 0 commands."""
		if not hasattr(self, '_system'):
			from .Gnss_.System import System
			self._system = System(self._core, self._base)
		return self._system

	@property
	def time(self):
		"""time commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_time'):
			from .Gnss_.Time import Time
			self._time = Time(self._core, self._base)
		return self._time

	@property
	def trigger(self):
		"""trigger commands group. 5 Sub-classes, 4 commands."""
		if not hasattr(self, '_trigger'):
			from .Gnss_.Trigger import Trigger
			self._trigger = Trigger(self._core, self._base)
		return self._trigger

	@property
	def vehicle(self):
		"""vehicle commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_vehicle'):
			from .Gnss_.Vehicle import Vehicle
			self._vehicle = Vehicle(self._core, self._base)
		return self._vehicle

	def get_cfrequency(self) -> int:
		"""[SOURce<HW>]:BB:GNSS:CFRequency \n
		Queries the central RF frequency. The response is a mean value depending on enabled RF bands and GNSS systems. \n
			:return: central_rf_freq: integer Range: 1E9 to 2E9, Unit: Hz
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:CFRequency?')
		return Conversions.str_to_int(response)

	# noinspection PyTypeChecker
	def get_ec_mode(self) -> enums.SbasCorrMode:
		"""[SOURce<HW>]:BB:GNSS:ECMode \n
		Sets how the error corrections are generated. For details, see 'Error Correction Mode'. \n
			:return: corrections_mode: AUTO| SYNC| USER AUTO This mode is not supported in the current R&S SMBV100B firmware. Corrections are generated automatically. SYNC Replays historical data and synchronizes the atmosphere parameters and the SV errors. USER Replays historical data; corrections are user-defined.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:ECMode?')
		return Conversions.str_to_scalar_enum(response, enums.SbasCorrMode)

	def set_ec_mode(self, corrections_mode: enums.SbasCorrMode) -> None:
		"""[SOURce<HW>]:BB:GNSS:ECMode \n
		Sets how the error corrections are generated. For details, see 'Error Correction Mode'. \n
			:param corrections_mode: AUTO| SYNC| USER AUTO This mode is not supported in the current R&S SMBV100B firmware. Corrections are generated automatically. SYNC Replays historical data and synchronizes the atmosphere parameters and the SV errors. USER Replays historical data; corrections are user-defined.
		"""
		param = Conversions.enum_scalar_to_str(corrections_mode, enums.SbasCorrMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:ECMode {param}')

	def preset(self) -> None:
		"""[SOURce<HW>]:BB:GNSS:PRESet \n
		Sets the parameters of the digital standard to their default values (*RST values specified for the commands) .
		Not affected is the state set with the command method RsSmbv.Source.Bb.Gnss.state. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:PRESet')

	def preset_with_opc(self) -> None:
		"""[SOURce<HW>]:BB:GNSS:PRESet \n
		Sets the parameters of the digital standard to their default values (*RST values specified for the commands) .
		Not affected is the state set with the command method RsSmbv.Source.Bb.Gnss.state. \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:GNSS:PRESet')

	def get_scenario(self) -> str:
		"""[SOURce<HW>]:BB:GNSS:SCENario \n
		Queries the current scenario. \n
			:return: scenario: string NONE Indicates the preset configuration or a user-defined configuration. Scenario name Displays the scenario name of a predefined scenario, e.g. '3GPP TS 37.571-2: S7 Signaling ST1'. See 'List of Predefined Test Scenarios'. Filename Displays the filename of a saved, user-defined scenario. The scenario file has the extension *.gnss.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:SCENario?')
		return trim_str_response(response)

	def get_ss_values(self) -> bool:
		"""[SOURce<HW>]:BB:GNSS:SSValues \n
		Defines if the navigation message parameters are set as scaled or unscaled values and thus which subset of remote-control
		commands is used. \n
			:return: show_scaled_value: 0| 1| OFF| ON 0 Used are unscaled values The SOURcehw:BB:GNSS:...:UNSCaled commands apply. 1 Used are scaled values Commands without the mnemonic UNSCaled apply.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:SSValues?')
		return Conversions.str_to_bool(response)

	def set_ss_values(self, show_scaled_value: bool) -> None:
		"""[SOURce<HW>]:BB:GNSS:SSValues \n
		Defines if the navigation message parameters are set as scaled or unscaled values and thus which subset of remote-control
		commands is used. \n
			:param show_scaled_value: 0| 1| OFF| ON 0 Used are unscaled values The SOURcehw:BB:GNSS:...:UNSCaled commands apply. 1 Used are scaled values Commands without the mnemonic UNSCaled apply.
		"""
		param = Conversions.bool_to_str(show_scaled_value)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:SSValues {param}')

	def get_state(self) -> bool:
		"""[SOURce<HW>]:BB:GNSS:STATe \n
		Enables/disables the GNSS signal simulation. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""[SOURce<HW>]:BB:GNSS:STATe \n
		Enables/disables the GNSS signal simulation. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:STATe {param}')

	# noinspection PyTypeChecker
	def get_tmode(self) -> enums.SimMode2:
		"""[SOURce<HW>]:BB:GNSS:TMODe \n
		Sets the test mode. \n
			:return: sm_ode: TRACking| NAVigation| SINGle
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GNSS:TMODe?')
		return Conversions.str_to_scalar_enum(response, enums.SimMode2)

	def set_tmode(self, sm_ode: enums.SimMode2) -> None:
		"""[SOURce<HW>]:BB:GNSS:TMODe \n
		Sets the test mode. \n
			:param sm_ode: TRACking| NAVigation| SINGle
		"""
		param = Conversions.enum_scalar_to_str(sm_ode, enums.SimMode2)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:TMODe {param}')
