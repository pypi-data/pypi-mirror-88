from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dab:
	"""Dab commands group definition. 52 total commands, 11 Sub-groups, 7 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dab", core, parent)

	def clone(self) -> 'Dab':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Dab(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def clock(self):
		"""clock commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_clock'):
			from .Dab_.Clock import Clock
			self._clock = Clock(self._core, self._base)
		return self._clock

	@property
	def coder(self):
		"""coder commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_coder'):
			from .Dab_.Coder import Coder
			self._coder = Coder(self._core, self._base)
		return self._coder

	@property
	def data(self):
		"""data commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_data'):
			from .Dab_.Data import Data
			self._data = Data(self._core, self._base)
		return self._data

	@property
	def eti(self):
		"""eti commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_eti'):
			from .Dab_.Eti import Eti
			self._eti = Eti(self._core, self._base)
		return self._eti

	@property
	def filterPy(self):
		"""filterPy commands group. 3 Sub-classes, 2 commands."""
		if not hasattr(self, '_filterPy'):
			from .Dab_.FilterPy import FilterPy
			self._filterPy = FilterPy(self._core, self._base)
		return self._filterPy

	@property
	def ileaver(self):
		"""ileaver commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ileaver'):
			from .Dab_.Ileaver import Ileaver
			self._ileaver = Ileaver(self._core, self._base)
		return self._ileaver

	@property
	def pnScrambler(self):
		"""pnScrambler commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pnScrambler'):
			from .Dab_.PnScrambler import PnScrambler
			self._pnScrambler = PnScrambler(self._core, self._base)
		return self._pnScrambler

	@property
	def setting(self):
		"""setting commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_setting'):
			from .Dab_.Setting import Setting
			self._setting = Setting(self._core, self._base)
		return self._setting

	@property
	def symbolRate(self):
		"""symbolRate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_symbolRate'):
			from .Dab_.SymbolRate import SymbolRate
			self._symbolRate = SymbolRate(self._core, self._base)
		return self._symbolRate

	@property
	def tii(self):
		"""tii commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tii'):
			from .Dab_.Tii import Tii
			self._tii = Tii(self._core, self._base)
		return self._tii

	@property
	def trigger(self):
		"""trigger commands group. 4 Sub-classes, 4 commands."""
		if not hasattr(self, '_trigger'):
			from .Dab_.Trigger import Trigger
			self._trigger = Trigger(self._core, self._base)
		return self._trigger

	def get_eframes(self) -> float:
		"""[SOURce<HW>]:BB:DAB:EFRames \n
		No command help available \n
			:return: eframes: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DAB:EFRames?')
		return Conversions.str_to_float(response)

	def set_eframes(self, eframes: float) -> None:
		"""[SOURce<HW>]:BB:DAB:EFRames \n
		No command help available \n
			:param eframes: No help available
		"""
		param = Conversions.decimal_value_to_str(eframes)
		self._core.io.write(f'SOURce<HwInstance>:BB:DAB:EFRames {param}')

	def get_lduration(self) -> float:
		"""[SOURce<HW>]:BB:DAB:LDURation \n
		No command help available \n
			:return: lduration: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DAB:LDURation?')
		return Conversions.str_to_float(response)

	def get_mid(self) -> int:
		"""[SOURce<HW>]:BB:DAB:MID \n
		No command help available \n
			:return: mid: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DAB:MID?')
		return Conversions.str_to_int(response)

	def set_mid(self, mid: int) -> None:
		"""[SOURce<HW>]:BB:DAB:MID \n
		No command help available \n
			:param mid: No help available
		"""
		param = Conversions.decimal_value_to_str(mid)
		self._core.io.write(f'SOURce<HwInstance>:BB:DAB:MID {param}')

	def preset(self) -> None:
		"""[SOURce<HW>]:BB:DAB:PRESet \n
		No command help available \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:BB:DAB:PRESet')

	def preset_with_opc(self) -> None:
		"""[SOURce<HW>]:BB:DAB:PRESet \n
		No command help available \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:DAB:PRESet')

	def get_sid(self) -> int:
		"""[SOURce<HW>]:BB:DAB:SID \n
		No command help available \n
			:return: sid: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DAB:SID?')
		return Conversions.str_to_int(response)

	def set_sid(self, sid: int) -> None:
		"""[SOURce<HW>]:BB:DAB:SID \n
		No command help available \n
			:param sid: No help available
		"""
		param = Conversions.decimal_value_to_str(sid)
		self._core.io.write(f'SOURce<HwInstance>:BB:DAB:SID {param}')

	def get_state(self) -> bool:
		"""[SOURce<HW>]:BB:DAB:STATe \n
		No command help available \n
			:return: state: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DAB:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""[SOURce<HW>]:BB:DAB:STATe \n
		No command help available \n
			:param state: No help available
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:DAB:STATe {param}')

	# noinspection PyTypeChecker
	def get_tmode(self) -> enums.DabTxMode:
		"""[SOURce<HW>]:BB:DAB:TMODe \n
		No command help available \n
			:return: tmode: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DAB:TMODe?')
		return Conversions.str_to_scalar_enum(response, enums.DabTxMode)

	def set_tmode(self, tmode: enums.DabTxMode) -> None:
		"""[SOURce<HW>]:BB:DAB:TMODe \n
		No command help available \n
			:param tmode: No help available
		"""
		param = Conversions.enum_scalar_to_str(tmode, enums.DabTxMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:DAB:TMODe {param}')
