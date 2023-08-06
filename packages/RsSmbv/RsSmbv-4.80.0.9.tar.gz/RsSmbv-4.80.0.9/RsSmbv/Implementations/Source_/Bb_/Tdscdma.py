from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Utilities import trim_str_response
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Tdscdma:
	"""Tdscdma commands group definition. 355 total commands, 12 Sub-groups, 6 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tdscdma", core, parent)

	def clone(self) -> 'Tdscdma':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Tdscdma(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def clipping(self):
		"""clipping commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_clipping'):
			from .Tdscdma_.Clipping import Clipping
			self._clipping = Clipping(self._core, self._base)
		return self._clipping

	@property
	def clock(self):
		"""clock commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_clock'):
			from .Tdscdma_.Clock import Clock
			self._clock = Clock(self._core, self._base)
		return self._clock

	@property
	def copy(self):
		"""copy commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_copy'):
			from .Tdscdma_.Copy import Copy
			self._copy = Copy(self._core, self._base)
		return self._copy

	@property
	def crate(self):
		"""crate commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_crate'):
			from .Tdscdma_.Crate import Crate
			self._crate = Crate(self._core, self._base)
		return self._crate

	@property
	def down(self):
		"""down commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_down'):
			from .Tdscdma_.Down import Down
			self._down = Down(self._core, self._base)
		return self._down

	@property
	def filterPy(self):
		"""filterPy commands group. 3 Sub-classes, 1 commands."""
		if not hasattr(self, '_filterPy'):
			from .Tdscdma_.FilterPy import FilterPy
			self._filterPy = FilterPy(self._core, self._base)
		return self._filterPy

	@property
	def power(self):
		"""power commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_power'):
			from .Tdscdma_.Power import Power
			self._power = Power(self._core, self._base)
		return self._power

	@property
	def pramp(self):
		"""pramp commands group. 0 Sub-classes, 5 commands."""
		if not hasattr(self, '_pramp'):
			from .Tdscdma_.Pramp import Pramp
			self._pramp = Pramp(self._core, self._base)
		return self._pramp

	@property
	def setting(self):
		"""setting commands group. 1 Sub-classes, 3 commands."""
		if not hasattr(self, '_setting'):
			from .Tdscdma_.Setting import Setting
			self._setting = Setting(self._core, self._base)
		return self._setting

	@property
	def trigger(self):
		"""trigger commands group. 4 Sub-classes, 5 commands."""
		if not hasattr(self, '_trigger'):
			from .Tdscdma_.Trigger import Trigger
			self._trigger = Trigger(self._core, self._base)
		return self._trigger

	@property
	def up(self):
		"""up commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_up'):
			from .Tdscdma_.Up import Up
			self._up = Up(self._core, self._base)
		return self._up

	@property
	def waveform(self):
		"""waveform commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_waveform'):
			from .Tdscdma_.Waveform import Waveform
			self._waveform = Waveform(self._core, self._base)
		return self._waveform

	# noinspection PyTypeChecker
	def get_link(self) -> enums.LinkDir:
		"""[SOURce<HW>]:BB:TDSCdma:LINK \n
		Defines the transmission direction. \n
			:return: link: FORWard| DOWN | REVerse| UP
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:TDSCdma:LINK?')
		return Conversions.str_to_scalar_enum(response, enums.LinkDir)

	def set_link(self, link: enums.LinkDir) -> None:
		"""[SOURce<HW>]:BB:TDSCdma:LINK \n
		Defines the transmission direction. \n
			:param link: FORWard| DOWN | REVerse| UP
		"""
		param = Conversions.enum_scalar_to_str(link, enums.LinkDir)
		self._core.io.write(f'SOURce<HwInstance>:BB:TDSCdma:LINK {param}')

	def preset(self) -> None:
		"""[SOURce<HW>]:BB:TDSCdma:PRESet \n
		Sets the parameters of the digital standard to their default values (*RST values specified for the commands) .
		Not affected is the state set with the command method RsSmbv.Source.Bb.Tdscdma.state. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:BB:TDSCdma:PRESet')

	def preset_with_opc(self) -> None:
		"""[SOURce<HW>]:BB:TDSCdma:PRESet \n
		Sets the parameters of the digital standard to their default values (*RST values specified for the commands) .
		Not affected is the state set with the command method RsSmbv.Source.Bb.Tdscdma.state. \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:TDSCdma:PRESet')

	def reset(self) -> None:
		"""[SOURce<HW>]:BB:TDSCdma:RESet \n
		Resets all cells to the predefined settings. The reset applies to the selected link direction. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:BB:TDSCdma:RESet')

	def reset_with_opc(self) -> None:
		"""[SOURce<HW>]:BB:TDSCdma:RESet \n
		Resets all cells to the predefined settings. The reset applies to the selected link direction. \n
		Same as reset, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:TDSCdma:RESet')

	def get_slength(self) -> int:
		"""[SOURce<HW>]:BB:TDSCdma:SLENgth \n
		Sets the sequence length of the arbitrary waveform component of the TD-SCDMA signal in the number of frames.
		This component is calculated in advance and output in the arbitrary waveform generator. It is added to the realtime
		signal components. \n
			:return: slength: integer Range: 1 to 5000
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:TDSCdma:SLENgth?')
		return Conversions.str_to_int(response)

	def set_slength(self, slength: int) -> None:
		"""[SOURce<HW>]:BB:TDSCdma:SLENgth \n
		Sets the sequence length of the arbitrary waveform component of the TD-SCDMA signal in the number of frames.
		This component is calculated in advance and output in the arbitrary waveform generator. It is added to the realtime
		signal components. \n
			:param slength: integer Range: 1 to 5000
		"""
		param = Conversions.decimal_value_to_str(slength)
		self._core.io.write(f'SOURce<HwInstance>:BB:TDSCdma:SLENgth {param}')

	def get_state(self) -> bool:
		"""[SOURce<HW>]:BB:TDSCdma:STATe \n
		Activates the standard and deactivates all the other digital standards and digital modulation modes in the same path. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:TDSCdma:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""[SOURce<HW>]:BB:TDSCdma:STATe \n
		Activates the standard and deactivates all the other digital standards and digital modulation modes in the same path. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:TDSCdma:STATe {param}')

	def get_version(self) -> str:
		"""[SOURce<HW>]:BB:TDSCdma:VERSion \n
		Queries the version of the TD-SCDMA standard underlying the definitions. \n
			:return: version: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:TDSCdma:VERSion?')
		return trim_str_response(response)
