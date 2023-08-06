from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Utilities import trim_str_response
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Eutra:
	"""Eutra commands group definition. 1245 total commands, 16 Sub-groups, 7 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("eutra", core, parent)

	def clone(self) -> 'Eutra':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Eutra(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def clipping(self):
		"""clipping commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_clipping'):
			from .Eutra_.Clipping import Clipping
			self._clipping = Clipping(self._core, self._base)
		return self._clipping

	@property
	def clock(self):
		"""clock commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_clock'):
			from .Eutra_.Clock import Clock
			self._clock = Clock(self._core, self._base)
		return self._clock

	@property
	def dl(self):
		"""dl commands group. 25 Sub-classes, 14 commands."""
		if not hasattr(self, '_dl'):
			from .Eutra_.Dl import Dl
			self._dl = Dl(self._core, self._base)
		return self._dl

	@property
	def filterPy(self):
		"""filterPy commands group. 1 Sub-classes, 3 commands."""
		if not hasattr(self, '_filterPy'):
			from .Eutra_.FilterPy import FilterPy
			self._filterPy = FilterPy(self._core, self._base)
		return self._filterPy

	@property
	def logGen(self):
		"""logGen commands group. 2 Sub-classes, 4 commands."""
		if not hasattr(self, '_logGen'):
			from .Eutra_.LogGen import LogGen
			self._logGen = LogGen(self._core, self._base)
		return self._logGen

	@property
	def powc(self):
		"""powc commands group. 0 Sub-classes, 5 commands."""
		if not hasattr(self, '_powc'):
			from .Eutra_.Powc import Powc
			self._powc = Powc(self._core, self._base)
		return self._powc

	@property
	def setting(self):
		"""setting commands group. 1 Sub-classes, 4 commands."""
		if not hasattr(self, '_setting'):
			from .Eutra_.Setting import Setting
			self._setting = Setting(self._core, self._base)
		return self._setting

	@property
	def symbolRate(self):
		"""symbolRate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_symbolRate'):
			from .Eutra_.SymbolRate import SymbolRate
			self._symbolRate = SymbolRate(self._core, self._base)
		return self._symbolRate

	@property
	def tcw(self):
		"""tcw commands group. 11 Sub-classes, 1 commands."""
		if not hasattr(self, '_tcw'):
			from .Eutra_.Tcw import Tcw
			self._tcw = Tcw(self._core, self._base)
		return self._tcw

	@property
	def tdd(self):
		"""tdd commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_tdd'):
			from .Eutra_.Tdd import Tdd
			self._tdd = Tdd(self._core, self._base)
		return self._tdd

	@property
	def tdw(self):
		"""tdw commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_tdw'):
			from .Eutra_.Tdw import Tdw
			self._tdw = Tdw(self._core, self._base)
		return self._tdw

	@property
	def timc(self):
		"""timc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_timc'):
			from .Eutra_.Timc import Timc
			self._timc = Timc(self._core, self._base)
		return self._timc

	@property
	def trigger(self):
		"""trigger commands group. 5 Sub-classes, 5 commands."""
		if not hasattr(self, '_trigger'):
			from .Eutra_.Trigger import Trigger
			self._trigger = Trigger(self._core, self._base)
		return self._trigger

	@property
	def udt(self):
		"""udt commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_udt'):
			from .Eutra_.Udt import Udt
			self._udt = Udt(self._core, self._base)
		return self._udt

	@property
	def ul(self):
		"""ul commands group. 15 Sub-classes, 13 commands."""
		if not hasattr(self, '_ul'):
			from .Eutra_.Ul import Ul
			self._ul = Ul(self._core, self._base)
		return self._ul

	@property
	def waveform(self):
		"""waveform commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_waveform'):
			from .Eutra_.Waveform import Waveform
			self._waveform = Waveform(self._core, self._base)
		return self._waveform

	# noinspection PyTypeChecker
	def get_duplexing(self) -> enums.EutraDuplexMode:
		"""[SOURce<HW>]:BB:EUTRa:DUPLexing \n
		Sets the duplexing mode. \n
			:return: duplexing: TDD| FDD
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DUPLexing?')
		return Conversions.str_to_scalar_enum(response, enums.EutraDuplexMode)

	def set_duplexing(self, duplexing: enums.EutraDuplexMode) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DUPLexing \n
		Sets the duplexing mode. \n
			:param duplexing: TDD| FDD
		"""
		param = Conversions.enum_scalar_to_str(duplexing, enums.EutraDuplexMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DUPLexing {param}')

	# noinspection PyTypeChecker
	def get_link(self) -> enums.UpDownDirection:
		"""[SOURce<HW>]:BB:EUTRa:LINK \n
		Sets the transmission direction. \n
			:return: link: UP| DOWN
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:LINK?')
		return Conversions.str_to_scalar_enum(response, enums.UpDownDirection)

	def set_link(self, link: enums.UpDownDirection) -> None:
		"""[SOURce<HW>]:BB:EUTRa:LINK \n
		Sets the transmission direction. \n
			:param link: UP| DOWN
		"""
		param = Conversions.enum_scalar_to_str(link, enums.UpDownDirection)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:LINK {param}')

	def preset(self) -> None:
		"""[SOURce<HW>]:BB:EUTRa:PRESet \n
		Sets the parameters of the digital standard to their default values (*RST values specified for the commands) .
		Not affected is the state set with the command method RsSmbv.Source.Bb.Eutra.state. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:PRESet')

	def preset_with_opc(self) -> None:
		"""[SOURce<HW>]:BB:EUTRa:PRESet \n
		Sets the parameters of the digital standard to their default values (*RST values specified for the commands) .
		Not affected is the state set with the command method RsSmbv.Source.Bb.Eutra.state. \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:EUTRa:PRESet')

	def get_slength(self) -> int:
		"""[SOURce<HW>]:BB:EUTRa:SLENgth \n
		Sets the sequence length of the signal in number of frames. The signal is calculated in advance and output in the
		arbitrary waveform generator. The maximum number of frames is calculated as follows: Max. No. of Frames = Arbitrary
		waveform memory size/(sampling rate x 10 ms) . \n
			:return: slength: integer Range: 1 to dynamic
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:SLENgth?')
		return Conversions.str_to_int(response)

	def set_slength(self, slength: int) -> None:
		"""[SOURce<HW>]:BB:EUTRa:SLENgth \n
		Sets the sequence length of the signal in number of frames. The signal is calculated in advance and output in the
		arbitrary waveform generator. The maximum number of frames is calculated as follows: Max. No. of Frames = Arbitrary
		waveform memory size/(sampling rate x 10 ms) . \n
			:param slength: integer Range: 1 to dynamic
		"""
		param = Conversions.decimal_value_to_str(slength)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:SLENgth {param}')

	def get_state(self) -> bool:
		"""[SOURce<HW>]:BB:EUTRa:STATe \n
		Activates the standard and deactivates all the other digital standards and digital modulation modes in the same path. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""[SOURce<HW>]:BB:EUTRa:STATe \n
		Activates the standard and deactivates all the other digital standards and digital modulation modes in the same path. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:STATe {param}')

	# noinspection PyTypeChecker
	def get_std_mode(self) -> enums.EutraStdMode:
		"""[SOURce<HW>]:BB:EUTRa:STDMode \n
		Sets the supported 3GPP standard. \n
			:return: standard_mode: LTE| IOT| LIOT LTE Standalone LTE mode. IoT-specific commands containing the keywords EMTC or NIOT are discarded. IOT Standalone IoT mode. The commands related to LTE-specific features like carrier aggregation or MBSFN are discarded. LIOT Mixed LTE and IoT configuration, for example for interoperability tests.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:STDMode?')
		return Conversions.str_to_scalar_enum(response, enums.EutraStdMode)

	def set_std_mode(self, standard_mode: enums.EutraStdMode) -> None:
		"""[SOURce<HW>]:BB:EUTRa:STDMode \n
		Sets the supported 3GPP standard. \n
			:param standard_mode: LTE| IOT| LIOT LTE Standalone LTE mode. IoT-specific commands containing the keywords EMTC or NIOT are discarded. IOT Standalone IoT mode. The commands related to LTE-specific features like carrier aggregation or MBSFN are discarded. LIOT Mixed LTE and IoT configuration, for example for interoperability tests.
		"""
		param = Conversions.enum_scalar_to_str(standard_mode, enums.EutraStdMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:STDMode {param}')

	def get_version(self) -> str:
		"""[SOURce]:BB:EUTRa:VERSion \n
		Queries the version of the 3GPP standard underlying the definitions. \n
			:return: version: string
		"""
		response = self._core.io.query_str('SOURce:BB:EUTRa:VERSion?')
		return trim_str_response(response)
