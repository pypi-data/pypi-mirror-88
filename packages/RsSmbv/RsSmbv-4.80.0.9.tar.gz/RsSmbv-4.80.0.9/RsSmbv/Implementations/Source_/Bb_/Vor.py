from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Vor:
	"""Vor commands group definition. 42 total commands, 10 Sub-groups, 3 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("vor", core, parent)

	def clone(self) -> 'Vor':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Vor(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def clock(self):
		"""clock commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_clock'):
			from .Vor_.Clock import Clock
			self._clock = Clock(self._core, self._base)
		return self._clock

	@property
	def frequency(self):
		"""frequency commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_frequency'):
			from .Vor_.Frequency import Frequency
			self._frequency = Frequency(self._core, self._base)
		return self._frequency

	@property
	def setting(self):
		"""setting commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_setting'):
			from .Vor_.Setting import Setting
			self._setting = Setting(self._core, self._base)
		return self._setting

	@property
	def trigger(self):
		"""trigger commands group. 3 Sub-classes, 4 commands."""
		if not hasattr(self, '_trigger'):
			from .Vor_.Trigger import Trigger
			self._trigger = Trigger(self._core, self._base)
		return self._trigger

	@property
	def comid(self):
		"""comid commands group. 1 Sub-classes, 10 commands."""
		if not hasattr(self, '_comid'):
			from .Vor_.Comid import Comid
			self._comid = Comid(self._core, self._base)
		return self._comid

	@property
	def icao(self):
		"""icao commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_icao'):
			from .Vor_.Icao import Icao
			self._icao = Icao(self._core, self._base)
		return self._icao

	@property
	def reference(self):
		"""reference commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_reference'):
			from .Vor_.Reference import Reference
			self._reference = Reference(self._core, self._base)
		return self._reference

	@property
	def subcarrier(self):
		"""subcarrier commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_subcarrier'):
			from .Vor_.Subcarrier import Subcarrier
			self._subcarrier = Subcarrier(self._core, self._base)
		return self._subcarrier

	@property
	def var(self):
		"""var commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_var'):
			from .Vor_.Var import Var
			self._var = Var(self._core, self._base)
		return self._var

	@property
	def bangle(self):
		"""bangle commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_bangle'):
			from .Vor_.Bangle import Bangle
			self._bangle = Bangle(self._core, self._base)
		return self._bangle

	def preset(self) -> None:
		"""[SOURce<HW>]:BB:VOR:PRESet \n
		Sets the parameters of the digital standard to their default values (*RST values specified for the commands) .
		Not affected is the state set with the command SOURce<hw>:BB:VOR|ILS|DME:STATe. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:BB:VOR:PRESet')

	def preset_with_opc(self) -> None:
		"""[SOURce<HW>]:BB:VOR:PRESet \n
		Sets the parameters of the digital standard to their default values (*RST values specified for the commands) .
		Not affected is the state set with the command SOURce<hw>:BB:VOR|ILS|DME:STATe. \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:VOR:PRESet')

	def get_state(self) -> bool:
		"""[SOURce<HW>]:BB:VOR:STATe \n
		Activates/deactivates the avionic standard. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:VOR:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""[SOURce<HW>]:BB:VOR:STATe \n
		Activates/deactivates the avionic standard. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:VOR:STATe {param}')

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.AvionicVorMode:
		"""[SOURce<HW>]:[BB]:VOR:MODE \n
		Sets the operating mode for the VOR modulation signal. \n
			:return: mode: NORM| VAR| SUBCarrier| FMSubcarrier NORM VOR modulation is active. VAR Amplitude modulation of the output signal with the variable signal component (30Hz signal content) of the VOR signal. The modulation depth of the 30 Hz signal can be set with method RsSmbv.Source.Bb.Vor.Bangle.value. SUBCarrier Amplitude modulation of the output signal with the unmodulated FM carrier (9960Hz) of the VOR signal. The modulation depth of the 30 Hz signal can be set with method RsSmbv.Source.Bb.Vor.Subcarrier.depth. FMSubcarrier Amplitude modulation of the output signal with the frequency modulated FM carrier (9960Hz) of the VOR signal. The modulation depth of the 30 Hz signal can be set with method RsSmbv.Source.Bb.Vor.Subcarrier.depth. The frequency deviation can be set with method RsSmbv.Source.Bb.Vor.Bangle.value.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:VOR:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.AvionicVorMode)

	def set_mode(self, mode: enums.AvionicVorMode) -> None:
		"""[SOURce<HW>]:[BB]:VOR:MODE \n
		Sets the operating mode for the VOR modulation signal. \n
			:param mode: NORM| VAR| SUBCarrier| FMSubcarrier NORM VOR modulation is active. VAR Amplitude modulation of the output signal with the variable signal component (30Hz signal content) of the VOR signal. The modulation depth of the 30 Hz signal can be set with method RsSmbv.Source.Bb.Vor.Bangle.value. SUBCarrier Amplitude modulation of the output signal with the unmodulated FM carrier (9960Hz) of the VOR signal. The modulation depth of the 30 Hz signal can be set with method RsSmbv.Source.Bb.Vor.Subcarrier.depth. FMSubcarrier Amplitude modulation of the output signal with the frequency modulated FM carrier (9960Hz) of the VOR signal. The modulation depth of the 30 Hz signal can be set with method RsSmbv.Source.Bb.Vor.Subcarrier.depth. The frequency deviation can be set with method RsSmbv.Source.Bb.Vor.Bangle.value.
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.AvionicVorMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:VOR:MODE {param}')
