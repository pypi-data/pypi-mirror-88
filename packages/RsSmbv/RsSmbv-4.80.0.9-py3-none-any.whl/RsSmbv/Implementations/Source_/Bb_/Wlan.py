from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Wlan:
	"""Wlan commands group definition. 87 total commands, 13 Sub-groups, 9 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("wlan", core, parent)

	def clone(self) -> 'Wlan':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Wlan(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def clipping(self):
		"""clipping commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_clipping'):
			from .Wlan_.Clipping import Clipping
			self._clipping = Clipping(self._core, self._base)
		return self._clipping

	@property
	def clock(self):
		"""clock commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_clock'):
			from .Wlan_.Clock import Clock
			self._clock = Clock(self._core, self._base)
		return self._clock

	@property
	def crate(self):
		"""crate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_crate'):
			from .Wlan_.Crate import Crate
			self._crate = Crate(self._core, self._base)
		return self._crate

	@property
	def filterPy(self):
		"""filterPy commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_filterPy'):
			from .Wlan_.FilterPy import FilterPy
			self._filterPy = FilterPy(self._core, self._base)
		return self._filterPy

	@property
	def ileaver(self):
		"""ileaver commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ileaver'):
			from .Wlan_.Ileaver import Ileaver
			self._ileaver = Ileaver(self._core, self._base)
		return self._ileaver

	@property
	def plcp(self):
		"""plcp commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_plcp'):
			from .Wlan_.Plcp import Plcp
			self._plcp = Plcp(self._core, self._base)
		return self._plcp

	@property
	def psdu(self):
		"""psdu commands group. 3 Sub-classes, 4 commands."""
		if not hasattr(self, '_psdu'):
			from .Wlan_.Psdu import Psdu
			self._psdu = Psdu(self._core, self._base)
		return self._psdu

	@property
	def scrambler(self):
		"""scrambler commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_scrambler'):
			from .Wlan_.Scrambler import Scrambler
			self._scrambler = Scrambler(self._core, self._base)
		return self._scrambler

	@property
	def service(self):
		"""service commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_service'):
			from .Wlan_.Service import Service
			self._service = Service(self._core, self._base)
		return self._service

	@property
	def setting(self):
		"""setting commands group. 1 Sub-classes, 3 commands."""
		if not hasattr(self, '_setting'):
			from .Wlan_.Setting import Setting
			self._setting = Setting(self._core, self._base)
		return self._setting

	@property
	def tdWindowing(self):
		"""tdWindowing commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tdWindowing'):
			from .Wlan_.TdWindowing import TdWindowing
			self._tdWindowing = TdWindowing(self._core, self._base)
		return self._tdWindowing

	@property
	def trigger(self):
		"""trigger commands group. 5 Sub-classes, 5 commands."""
		if not hasattr(self, '_trigger'):
			from .Wlan_.Trigger import Trigger
			self._trigger = Trigger(self._core, self._base)
		return self._trigger

	@property
	def waveform(self):
		"""waveform commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_waveform'):
			from .Wlan_.Waveform import Waveform
			self._waveform = Waveform(self._core, self._base)
		return self._waveform

	# noinspection PyTypeChecker
	def get_fformat(self) -> enums.WlanFramType:
		"""[SOURce<HW>]:BB:WLAN:FFORmat \n
		No command help available \n
			:return: fformat: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAN:FFORmat?')
		return Conversions.str_to_scalar_enum(response, enums.WlanFramType)

	def set_fformat(self, fformat: enums.WlanFramType) -> None:
		"""[SOURce<HW>]:BB:WLAN:FFORmat \n
		No command help available \n
			:param fformat: No help available
		"""
		param = Conversions.enum_scalar_to_str(fformat, enums.WlanFramType)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAN:FFORmat {param}')

	def get_itime(self) -> float:
		"""[SOURce<HW>]:BB:WLAN:ITIMe \n
		No command help available \n
			:return: itime: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAN:ITIMe?')
		return Conversions.str_to_float(response)

	def set_itime(self, itime: float) -> None:
		"""[SOURce<HW>]:BB:WLAN:ITIMe \n
		No command help available \n
			:param itime: No help available
		"""
		param = Conversions.decimal_value_to_str(itime)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAN:ITIMe {param}')

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.WlanCodMode:
		"""[SOURce<HW>]:BB:WLAN:MODE \n
		No command help available \n
			:return: mode: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAN:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.WlanCodMode)

	def set_mode(self, mode: enums.WlanCodMode) -> None:
		"""[SOURce<HW>]:BB:WLAN:MODE \n
		No command help available \n
			:param mode: No help available
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.WlanCodMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAN:MODE {param}')

	def preset(self) -> None:
		"""[SOURce<HW>]:BB:WLAN:PRESet \n
		No command help available \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAN:PRESet')

	def preset_with_opc(self) -> None:
		"""[SOURce<HW>]:BB:WLAN:PRESet \n
		No command help available \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:WLAN:PRESet')

	def get_slength(self) -> float:
		"""[SOURce<HW>]:BB:WLAN:SLENgth \n
		No command help available \n
			:return: slength: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAN:SLENgth?')
		return Conversions.str_to_float(response)

	def set_slength(self, slength: float) -> None:
		"""[SOURce<HW>]:BB:WLAN:SLENgth \n
		No command help available \n
			:param slength: No help available
		"""
		param = Conversions.decimal_value_to_str(slength)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAN:SLENgth {param}')

	# noinspection PyTypeChecker
	def get_smode(self) -> enums.WlanMode:
		"""[SOURce<HW>]:BB:WLAN:SMODe \n
		No command help available \n
			:return: smode: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAN:SMODe?')
		return Conversions.str_to_scalar_enum(response, enums.WlanMode)

	def set_smode(self, smode: enums.WlanMode) -> None:
		"""[SOURce<HW>]:BB:WLAN:SMODe \n
		No command help available \n
			:param smode: No help available
		"""
		param = Conversions.enum_scalar_to_str(smode, enums.WlanMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAN:SMODe {param}')

	# noinspection PyTypeChecker
	def get_standard(self) -> enums.WlanStan:
		"""[SOURce<HW>]:BB:WLAN:STANdard \n
		No command help available \n
			:return: standard: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAN:STANdard?')
		return Conversions.str_to_scalar_enum(response, enums.WlanStan)

	def set_standard(self, standard: enums.WlanStan) -> None:
		"""[SOURce<HW>]:BB:WLAN:STANdard \n
		No command help available \n
			:param standard: No help available
		"""
		param = Conversions.enum_scalar_to_str(standard, enums.WlanStan)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAN:STANdard {param}')

	def get_state(self) -> bool:
		"""[SOURce<HW>]:BB:WLAN:STATe \n
		No command help available \n
			:return: state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAN:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""[SOURce<HW>]:BB:WLAN:STATe \n
		No command help available \n
			:param state: No help available
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAN:STATe {param}')

	def get_ttime(self) -> float:
		"""[SOURce<HW>]:BB:WLAN:TTIMe \n
		No command help available \n
			:return: ttime: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLAN:TTIMe?')
		return Conversions.str_to_float(response)

	def set_ttime(self, ttime: float) -> None:
		"""[SOURce<HW>]:BB:WLAN:TTIMe \n
		No command help available \n
			:param ttime: No help available
		"""
		param = Conversions.decimal_value_to_str(ttime)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLAN:TTIMe {param}')
