from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Utilities import trim_str_response
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Wlnn:
	"""Wlnn commands group definition. 292 total commands, 10 Sub-groups, 8 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("wlnn", core, parent)

	def clone(self) -> 'Wlnn':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Wlnn(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def antenna(self):
		"""antenna commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_antenna'):
			from .Wlnn_.Antenna import Antenna
			self._antenna = Antenna(self._core, self._base)
		return self._antenna

	@property
	def clipping(self):
		"""clipping commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_clipping'):
			from .Wlnn_.Clipping import Clipping
			self._clipping = Clipping(self._core, self._base)
		return self._clipping

	@property
	def clock(self):
		"""clock commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_clock'):
			from .Wlnn_.Clock import Clock
			self._clock = Clock(self._core, self._base)
		return self._clock

	@property
	def fblock(self):
		"""fblock commands group. 62 Sub-classes, 2 commands."""
		if not hasattr(self, '_fblock'):
			from .Wlnn_.Fblock import Fblock
			self._fblock = Fblock(self._core, self._base)
		return self._fblock

	@property
	def filterPy(self):
		"""filterPy commands group. 4 Sub-classes, 2 commands."""
		if not hasattr(self, '_filterPy'):
			from .Wlnn_.FilterPy import FilterPy
			self._filterPy = FilterPy(self._core, self._base)
		return self._filterPy

	@property
	def path(self):
		"""path commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_path'):
			from .Wlnn_.Path import Path
			self._path = Path(self._core, self._base)
		return self._path

	@property
	def setting(self):
		"""setting commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_setting'):
			from .Wlnn_.Setting import Setting
			self._setting = Setting(self._core, self._base)
		return self._setting

	@property
	def symbolRate(self):
		"""symbolRate commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_symbolRate'):
			from .Wlnn_.SymbolRate import SymbolRate
			self._symbolRate = SymbolRate(self._core, self._base)
		return self._symbolRate

	@property
	def trigger(self):
		"""trigger commands group. 4 Sub-classes, 5 commands."""
		if not hasattr(self, '_trigger'):
			from .Wlnn_.Trigger import Trigger
			self._trigger = Trigger(self._core, self._base)
		return self._trigger

	@property
	def waveform(self):
		"""waveform commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_waveform'):
			from .Wlnn_.Waveform import Waveform
			self._waveform = Waveform(self._core, self._base)
		return self._waveform

	# noinspection PyTypeChecker
	def get_bandwidth(self) -> enums.WlannTxBw:
		"""[SOURce<HW>]:BB:WLNN:BWidth \n
		The command selects the transmission bandwidth. Whenever the bandwidth changes from a higher to a lower one, the frame
		blocks are validated because some of them could be invalid in the lower bandwidth (invalid TX Mode) . \n
			:return: bwidth: BW20| BW40| BW80| BW160| BW320 Unit: MHz
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLNN:BWidth?')
		return Conversions.str_to_scalar_enum(response, enums.WlannTxBw)

	def set_bandwidth(self, bwidth: enums.WlannTxBw) -> None:
		"""[SOURce<HW>]:BB:WLNN:BWidth \n
		The command selects the transmission bandwidth. Whenever the bandwidth changes from a higher to a lower one, the frame
		blocks are validated because some of them could be invalid in the lower bandwidth (invalid TX Mode) . \n
			:param bwidth: BW20| BW40| BW80| BW160| BW320 Unit: MHz
		"""
		param = Conversions.enum_scalar_to_str(bwidth, enums.WlannTxBw)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:BWidth {param}')

	def set_cf_block(self, cf_block: int) -> None:
		"""[SOURce<HW>]:BB:WLNN:CFBLock \n
		Copies the selected frame block. \n
			:param cf_block: integer Range: 1 to 100
		"""
		param = Conversions.decimal_value_to_str(cf_block)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:CFBLock {param}')

	def set_df_block(self, df_block: int) -> None:
		"""[SOURce<HW>]:BB:WLNN:DFBLock \n
		Deletes the selected frame block. \n
			:param df_block: integer Range: 1 to 100
		"""
		param = Conversions.decimal_value_to_str(df_block)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:DFBLock {param}')

	def set_if_block(self, if_block: int) -> None:
		"""[SOURce<HW>]:BB:WLNN:IFBLock \n
		The command adds a default frame block before the selected frame block. \n
			:param if_block: No help available
		"""
		param = Conversions.decimal_value_to_str(if_block)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:IFBLock {param}')

	def set_pf_block(self, pf_block: int) -> None:
		"""[SOURce<HW>]:BB:WLNN:PFBLock \n
		Pastes the selected frame block. \n
			:param pf_block: integer Range: 1 to 99
		"""
		param = Conversions.decimal_value_to_str(pf_block)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:PFBLock {param}')

	def preset(self) -> None:
		"""[SOURce<HW>]:BB:WLNN:PRESet \n
		Sets the parameters of the digital standard to their default values (*RST values specified for the commands) .
		Not affected is the state set with the command method RsSmbv.Source.Bb.Wlnn.state. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:PRESet')

	def preset_with_opc(self) -> None:
		"""[SOURce<HW>]:BB:WLNN:PRESet \n
		Sets the parameters of the digital standard to their default values (*RST values specified for the commands) .
		Not affected is the state set with the command method RsSmbv.Source.Bb.Wlnn.state. \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:WLNN:PRESet')

	def get_state(self) -> bool:
		"""[SOURce<HW>]:BB:WLNN:STATe \n
		Activates the standard and deactivates all the other digital standards and digital modulation modes in the same path. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLNN:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""[SOURce<HW>]:BB:WLNN:STATe \n
		Activates the standard and deactivates all the other digital standards and digital modulation modes in the same path. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:STATe {param}')

	def get_version(self) -> str:
		"""[SOURce<HW>]:BB:WLNN:VERSion \n
		No command help available \n
			:return: version: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:WLNN:VERSion?')
		return trim_str_response(response)
