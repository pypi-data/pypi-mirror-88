from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Utilities import trim_str_response
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Evdo:
	"""Evdo commands group definition. 151 total commands, 13 Sub-groups, 8 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("evdo", core, parent)

	def clone(self) -> 'Evdo':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Evdo(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def anetwork(self):
		"""anetwork commands group. 3 Sub-classes, 3 commands."""
		if not hasattr(self, '_anetwork'):
			from .Evdo_.Anetwork import Anetwork
			self._anetwork = Anetwork(self._core, self._base)
		return self._anetwork

	@property
	def clipping(self):
		"""clipping commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_clipping'):
			from .Evdo_.Clipping import Clipping
			self._clipping = Clipping(self._core, self._base)
		return self._clipping

	@property
	def clock(self):
		"""clock commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_clock'):
			from .Evdo_.Clock import Clock
			self._clock = Clock(self._core, self._base)
		return self._clock

	@property
	def crate(self):
		"""crate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_crate'):
			from .Evdo_.Crate import Crate
			self._crate = Crate(self._core, self._base)
		return self._crate

	@property
	def down(self):
		"""down commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_down'):
			from .Evdo_.Down import Down
			self._down = Down(self._core, self._base)
		return self._down

	@property
	def filterPy(self):
		"""filterPy commands group. 3 Sub-classes, 2 commands."""
		if not hasattr(self, '_filterPy'):
			from .Evdo_.FilterPy import FilterPy
			self._filterPy = FilterPy(self._core, self._base)
		return self._filterPy

	@property
	def iqswap(self):
		"""iqswap commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_iqswap'):
			from .Evdo_.Iqswap import Iqswap
			self._iqswap = Iqswap(self._core, self._base)
		return self._iqswap

	@property
	def setting(self):
		"""setting commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_setting'):
			from .Evdo_.Setting import Setting
			self._setting = Setting(self._core, self._base)
		return self._setting

	@property
	def terminal(self):
		"""terminal commands group. 15 Sub-classes, 0 commands."""
		if not hasattr(self, '_terminal'):
			from .Evdo_.Terminal import Terminal
			self._terminal = Terminal(self._core, self._base)
		return self._terminal

	@property
	def trigger(self):
		"""trigger commands group. 4 Sub-classes, 5 commands."""
		if not hasattr(self, '_trigger'):
			from .Evdo_.Trigger import Trigger
			self._trigger = Trigger(self._core, self._base)
		return self._trigger

	@property
	def up(self):
		"""up commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_up'):
			from .Evdo_.Up import Up
			self._up = Up(self._core, self._base)
		return self._up

	@property
	def user(self):
		"""user commands group. 11 Sub-classes, 0 commands."""
		if not hasattr(self, '_user'):
			from .Evdo_.User import User
			self._user = User(self._core, self._base)
		return self._user

	@property
	def waveform(self):
		"""waveform commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_waveform'):
			from .Evdo_.Waveform import Waveform
			self._waveform = Waveform(self._core, self._base)
		return self._waveform

	# noinspection PyTypeChecker
	def get_link(self) -> enums.LinkDir:
		"""[SOURce<HW>]:BB:EVDO:LINK \n
		Defines the transmission direction. \n
			:return: link: FORWard/DOWN | REVerse/UP
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EVDO:LINK?')
		return Conversions.str_to_scalar_enum(response, enums.LinkDir)

	def set_link(self, link: enums.LinkDir) -> None:
		"""[SOURce<HW>]:BB:EVDO:LINK \n
		Defines the transmission direction. \n
			:param link: FORWard/DOWN | REVerse/UP
		"""
		param = Conversions.enum_scalar_to_str(link, enums.LinkDir)
		self._core.io.write(f'SOURce<HwInstance>:BB:EVDO:LINK {param}')

	def get_pn_offset(self) -> int:
		"""[SOURce<HW>]:BB:EVDO:PNOFfset \n
		Sets the PN Offset of the 1xEV-DO signal. \n
			:return: pn_offset: integer Range: 0 to 511
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EVDO:PNOFfset?')
		return Conversions.str_to_int(response)

	def set_pn_offset(self, pn_offset: int) -> None:
		"""[SOURce<HW>]:BB:EVDO:PNOFfset \n
		Sets the PN Offset of the 1xEV-DO signal. \n
			:param pn_offset: integer Range: 0 to 511
		"""
		param = Conversions.decimal_value_to_str(pn_offset)
		self._core.io.write(f'SOURce<HwInstance>:BB:EVDO:PNOFfset {param}')

	# noinspection PyTypeChecker
	def get_predefined(self) -> enums.EvdoPredSett:
		"""[SOURce<HW>]:BB:EVDO:PREDefined \n
		Sets the UL setting of Terminal 1 to one of the predefined configurations. The predefined settings are made according to
		3GPP2 C.S0032-A to allow easy receiver testing.
			Table Header: Parameter / Description \n
			- USER / There are no predefined settings
			- ULS1DR9K6 / UL, Subtype 1, 9.6 kbps.
			- ULS1DR19K2 / UL, Subtype 1, 19.2 kbps.
			- ULS1DR38K4 / UL, Subtype 1, 38.4 kbps.
			- ULS1DR76K8 / UL, Subtype 1, 76.8 kbps.
			- ULS1DR153K6 / UL, Subtype 1, 153.6 kbps.
			- ULS2PS128LL / UL, Subtype 2, 128 bits payload, Low Latency.
			- ULS2PS256HC / UL, Subtype 2, 256 bits payload, High Capacity.
			- ULS2PS256LL / UL, Subtype 2, 256 bits payload, Low Latency.
			- ULS2PS512LL / UL, Subtype 2, 512 bits payload, Low Latency.
			- ULS2PS768LL / UL, Subtype 2, 768 bits payload, Low Latency.
			- ULS2PS1024LL / UL, Subtype 2, 1024 bits payload, Low Latency.
			- ULS2PS1536LL / UL, Subtype 2, 1536 bits payload, Low Latency.
			- ULS2PS2048LL / UL, Subtype 2, 2048 bits payload, Low Latency.
			- ULS2PS3072LL / UL, Subtype 2, 3072 bits payload, Low Latency.
			- ULS2PS4096LL / UL, Subtype 2, 4096 bits payload, Low Latency.
			- ULS2PS6144LL / UL, Subtype 2, 6144 bits payload, Low Latency.
			- ULS2PS8192LL / UL, Subtype 2, 8192 bits payload, Low Latency.
			- ULS2PS12288LL / UL, Subtype 2, 12288 bits payload, Low Latency. \n
			:return: predefined: USER| ULS1DR9K6| ULS1DR19K2| ULS1DR38K4| ULS1DR76K8| ULS1DR153K6| ULS2PS128LL| ULS2PS256HC| ULS2PS256LL| ULS2PS512LL| ULS2PS768LL| ULS2PS1024LL| ULS2PS1536LL| ULS2PS2048LL| ULS2PS3072LL| ULS2PS4096LL| ULS2PS6144LL| ULS2PS8192LL| ULS2PS12288LL
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EVDO:PREDefined?')
		return Conversions.str_to_scalar_enum(response, enums.EvdoPredSett)

	def set_predefined(self, predefined: enums.EvdoPredSett) -> None:
		"""[SOURce<HW>]:BB:EVDO:PREDefined \n
		Sets the UL setting of Terminal 1 to one of the predefined configurations. The predefined settings are made according to
		3GPP2 C.S0032-A to allow easy receiver testing.
			Table Header: Parameter / Description \n
			- USER / There are no predefined settings
			- ULS1DR9K6 / UL, Subtype 1, 9.6 kbps.
			- ULS1DR19K2 / UL, Subtype 1, 19.2 kbps.
			- ULS1DR38K4 / UL, Subtype 1, 38.4 kbps.
			- ULS1DR76K8 / UL, Subtype 1, 76.8 kbps.
			- ULS1DR153K6 / UL, Subtype 1, 153.6 kbps.
			- ULS2PS128LL / UL, Subtype 2, 128 bits payload, Low Latency.
			- ULS2PS256HC / UL, Subtype 2, 256 bits payload, High Capacity.
			- ULS2PS256LL / UL, Subtype 2, 256 bits payload, Low Latency.
			- ULS2PS512LL / UL, Subtype 2, 512 bits payload, Low Latency.
			- ULS2PS768LL / UL, Subtype 2, 768 bits payload, Low Latency.
			- ULS2PS1024LL / UL, Subtype 2, 1024 bits payload, Low Latency.
			- ULS2PS1536LL / UL, Subtype 2, 1536 bits payload, Low Latency.
			- ULS2PS2048LL / UL, Subtype 2, 2048 bits payload, Low Latency.
			- ULS2PS3072LL / UL, Subtype 2, 3072 bits payload, Low Latency.
			- ULS2PS4096LL / UL, Subtype 2, 4096 bits payload, Low Latency.
			- ULS2PS6144LL / UL, Subtype 2, 6144 bits payload, Low Latency.
			- ULS2PS8192LL / UL, Subtype 2, 8192 bits payload, Low Latency.
			- ULS2PS12288LL / UL, Subtype 2, 12288 bits payload, Low Latency. \n
			:param predefined: USER| ULS1DR9K6| ULS1DR19K2| ULS1DR38K4| ULS1DR76K8| ULS1DR153K6| ULS2PS128LL| ULS2PS256HC| ULS2PS256LL| ULS2PS512LL| ULS2PS768LL| ULS2PS1024LL| ULS2PS1536LL| ULS2PS2048LL| ULS2PS3072LL| ULS2PS4096LL| ULS2PS6144LL| ULS2PS8192LL| ULS2PS12288LL
		"""
		param = Conversions.enum_scalar_to_str(predefined, enums.EvdoPredSett)
		self._core.io.write(f'SOURce<HwInstance>:BB:EVDO:PREDefined {param}')

	def preset(self) -> None:
		"""[SOURce<HW>]:BB:EVDO:PRESet \n
		Sets the parameters of the digital standard to their default values (*RST values specified for the commands) .
		Not affected is the state set with the command method RsSmbv.Source.Bb.Evdo.state. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:BB:EVDO:PRESet')

	def preset_with_opc(self) -> None:
		"""[SOURce<HW>]:BB:EVDO:PRESet \n
		Sets the parameters of the digital standard to their default values (*RST values specified for the commands) .
		Not affected is the state set with the command method RsSmbv.Source.Bb.Evdo.state. \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:EVDO:PRESet')

	def get_slength(self) -> int:
		"""[SOURce<HW>]:BB:EVDO:SLENgth \n
		(For reverse link mode only) Sets the sequence length of the arbitrary waveform component of the 1XEV-DO signal in number
		of frames. This component is calculated in advance and output in the arbitrary waveform generator. It is added to the
		real time signal components. The number of chips is determined from this sequence length. One slot of 1.67ms duration
		equals 2048 chips. \n
			:return: slength: integer Range: 4 to dynamic
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EVDO:SLENgth?')
		return Conversions.str_to_int(response)

	def set_slength(self, slength: int) -> None:
		"""[SOURce<HW>]:BB:EVDO:SLENgth \n
		(For reverse link mode only) Sets the sequence length of the arbitrary waveform component of the 1XEV-DO signal in number
		of frames. This component is calculated in advance and output in the arbitrary waveform generator. It is added to the
		real time signal components. The number of chips is determined from this sequence length. One slot of 1.67ms duration
		equals 2048 chips. \n
			:param slength: integer Range: 4 to dynamic
		"""
		param = Conversions.decimal_value_to_str(slength)
		self._core.io.write(f'SOURce<HwInstance>:BB:EVDO:SLENgth {param}')

	def get_state(self) -> bool:
		"""[SOURce<HW>]:BB:EVDO:STATe \n
		Activates the standard and deactivates all the other digital standards and digital modulation modes in the same path. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EVDO:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""[SOURce<HW>]:BB:EVDO:STATe \n
		Activates the standard and deactivates all the other digital standards and digital modulation modes in the same path. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:EVDO:STATe {param}')

	def get_stime(self) -> int:
		"""[SOURce<HW>]:BB:EVDO:STIMe \n
		Sets the System Time value of the 1xEV-DO signal and the base station. The System Time value is expressed in units of 1.
		67 ms intervals (80 ms/ 48) . Note: In uplink, the value selected for system time must be multiple of 16. \n
			:return: stime: integer Range: 0 to 2199023255551
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EVDO:STIMe?')
		return Conversions.str_to_int(response)

	def set_stime(self, stime: int) -> None:
		"""[SOURce<HW>]:BB:EVDO:STIMe \n
		Sets the System Time value of the 1xEV-DO signal and the base station. The System Time value is expressed in units of 1.
		67 ms intervals (80 ms/ 48) . Note: In uplink, the value selected for system time must be multiple of 16. \n
			:param stime: integer Range: 0 to 2199023255551
		"""
		param = Conversions.decimal_value_to_str(stime)
		self._core.io.write(f'SOURce<HwInstance>:BB:EVDO:STIMe {param}')

	def get_version(self) -> str:
		"""[SOURce<HW>]:BB:EVDO:VERSion \n
		Queries the version of the 1xEV-DO standard underlying the definitions \n
			:return: version: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EVDO:VERSion?')
		return trim_str_response(response)
