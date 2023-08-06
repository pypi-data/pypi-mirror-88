from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Utilities import trim_str_response
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Nfc:
	"""Nfc commands group definition. 188 total commands, 10 Sub-groups, 12 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("nfc", core, parent)

	def clone(self) -> 'Nfc':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Nfc(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def cblock(self):
		"""cblock commands group. 107 Sub-classes, 2 commands."""
		if not hasattr(self, '_cblock'):
			from .Nfc_.Cblock import Cblock
			self._cblock = Cblock(self._core, self._base)
		return self._cblock

	@property
	def clipping(self):
		"""clipping commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_clipping'):
			from .Nfc_.Clipping import Clipping
			self._clipping = Clipping(self._core, self._base)
		return self._clipping

	@property
	def clock(self):
		"""clock commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_clock'):
			from .Nfc_.Clock import Clock
			self._clock = Clock(self._core, self._base)
		return self._clock

	@property
	def mset(self):
		"""mset commands group. 0 Sub-classes, 13 commands."""
		if not hasattr(self, '_mset'):
			from .Nfc_.Mset import Mset
			self._mset = Mset(self._core, self._base)
		return self._mset

	@property
	def pred(self):
		"""pred commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_pred'):
			from .Nfc_.Pred import Pred
			self._pred = Pred(self._core, self._base)
		return self._pred

	@property
	def sconfiguration(self):
		"""sconfiguration commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_sconfiguration'):
			from .Nfc_.Sconfiguration import Sconfiguration
			self._sconfiguration = Sconfiguration(self._core, self._base)
		return self._sconfiguration

	@property
	def setting(self):
		"""setting commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_setting'):
			from .Nfc_.Setting import Setting
			self._setting = Setting(self._core, self._base)
		return self._setting

	@property
	def trigger(self):
		"""trigger commands group. 4 Sub-classes, 5 commands."""
		if not hasattr(self, '_trigger'):
			from .Nfc_.Trigger import Trigger
			self._trigger = Trigger(self._core, self._base)
		return self._trigger

	@property
	def uaiSetting(self):
		"""uaiSetting commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_uaiSetting'):
			from .Nfc_.UaiSetting import UaiSetting
			self._uaiSetting = UaiSetting(self._core, self._base)
		return self._uaiSetting

	@property
	def waveform(self):
		"""waveform commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_waveform'):
			from .Nfc_.Waveform import Waveform
			self._waveform = Waveform(self._core, self._base)
		return self._waveform

	def set_cc_block(self, cc_block: int) -> None:
		"""[SOURce<HW>]:BB:NFC:CCBLock \n
		Copies a command block for later use. \n
			:param cc_block: integer Range: 1 to 100
		"""
		param = Conversions.decimal_value_to_str(cc_block)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:CCBLock {param}')

	def set_dcblock(self, dc_block: int) -> None:
		"""[SOURce<HW>]:BB:NFC:DCBLock \n
		Removes a command block from the command sequence. \n
			:param dc_block: integer Range: 1 to 100
		"""
		param = Conversions.decimal_value_to_str(dc_block)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:DCBLock {param}')

	# noinspection PyTypeChecker
	def get_divisor(self) -> enums.NfcDivForMod:
		"""[SOURce<HW>]:BB:NFC:DIVisor \n
		Selects the divisor and thus the datarate for technology NFC-F. \n
			:return: div_for_mod: DIV2| DIV4
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NFC:DIVisor?')
		return Conversions.str_to_scalar_enum(response, enums.NfcDivForMod)

	def set_divisor(self, div_for_mod: enums.NfcDivForMod) -> None:
		"""[SOURce<HW>]:BB:NFC:DIVisor \n
		Selects the divisor and thus the datarate for technology NFC-F. \n
			:param div_for_mod: DIV2| DIV4
		"""
		param = Conversions.enum_scalar_to_str(div_for_mod, enums.NfcDivForMod)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:DIVisor {param}')

	def get_dvoltage(self) -> float:
		"""[SOURce<HW>]:BB:NFC:DVOLtage \n
		Sets the desired voltage in unmodulated signal parts. \n
			:return: dvoltage: float Range: 0.020 to 1.5
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NFC:DVOLtage?')
		return Conversions.str_to_float(response)

	def set_dvoltage(self, dvoltage: float) -> None:
		"""[SOURce<HW>]:BB:NFC:DVOLtage \n
		Sets the desired voltage in unmodulated signal parts. \n
			:param dvoltage: float Range: 0.020 to 1.5
		"""
		param = Conversions.decimal_value_to_str(dvoltage)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:DVOLtage {param}')

	def set_ic_block(self, ic_block: int) -> None:
		"""[SOURce<HW>]:BB:NFC:ICBLock \n
		Inserts a default command block before the selected command block. The command block with this position must be existing,
		otherwise an error is returned. \n
			:param ic_block: integer Range: 1 to 99
		"""
		param = Conversions.decimal_value_to_str(ic_block)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:ICBLock {param}')

	def set_pc_block(self, pc_block: int) -> None:
		"""[SOURce<HW>]:BB:NFC:PCBLock \n
		Pastes a command block (which was copied before) at the given position into the command sequence. \n
			:param pc_block: integer Range: 1 to 99
		"""
		param = Conversions.decimal_value_to_str(pc_block)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:PCBLock {param}')

	def preset(self) -> None:
		"""[SOURce<HW>]:BB:NFC:PRESet \n
		Sets the parameters of the digital standard to their default values (*RST values specified for the commands) .
		Not affected is the state set with the command method RsSmbv.Source.Bb.Nfc.state. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:PRESet')

	def preset_with_opc(self) -> None:
		"""[SOURce<HW>]:BB:NFC:PRESet \n
		Sets the parameters of the digital standard to their default values (*RST values specified for the commands) .
		Not affected is the state set with the command method RsSmbv.Source.Bb.Nfc.state. \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:NFC:PRESet')

	def get_state(self) -> bool:
		"""[SOURce<HW>]:BB:NFC:STATe \n
		Activates the standard and deactivates all the other digital standards and digital modulation modes in the same path. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NFC:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""[SOURce<HW>]:BB:NFC:STATe \n
		Activates the standard and deactivates all the other digital standards and digital modulation modes in the same path. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:STATe {param}')

	# noinspection PyTypeChecker
	def get_technology(self) -> enums.NfcProtocolMode:
		"""[SOURce<HW>]:BB:NFC:TECHnology \n
		Selects the NFC/EMV technology. \n
			:return: protocol: NFCA| NFCB| NFCF| EMVA| EMVB
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NFC:TECHnology?')
		return Conversions.str_to_scalar_enum(response, enums.NfcProtocolMode)

	def set_technology(self, protocol: enums.NfcProtocolMode) -> None:
		"""[SOURce<HW>]:BB:NFC:TECHnology \n
		Selects the NFC/EMV technology. \n
			:param protocol: NFCA| NFCB| NFCF| EMVA| EMVB
		"""
		param = Conversions.enum_scalar_to_str(protocol, enums.NfcProtocolMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:TECHnology {param}')

	# noinspection PyTypeChecker
	def get_tmode(self) -> enums.NfcTransMode:
		"""[SOURce<HW>]:BB:NFC:TMODe \n
		Selects the transmission mode. \n
			:return: transmission: POLL| LISTen
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NFC:TMODe?')
		return Conversions.str_to_scalar_enum(response, enums.NfcTransMode)

	def set_tmode(self, transmission: enums.NfcTransMode) -> None:
		"""[SOURce<HW>]:BB:NFC:TMODe \n
		Selects the transmission mode. \n
			:param transmission: POLL| LISTen
		"""
		param = Conversions.enum_scalar_to_str(transmission, enums.NfcTransMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:TMODe {param}')

	def get_up_voltage(self) -> int:
		"""[SOURce<HW>]:BB:NFC:UPVoltage \n
		Displays the ratio of the voltage in the unmodulated parts of the signal to its peak value. \n
			:return: up_voltage: integer Range: 0 to 100
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NFC:UPVoltage?')
		return Conversions.str_to_int(response)

	def get_version(self) -> str:
		"""[SOURce<HW>]:BB:NFC:VERSion \n
		Queries the version of the NFC-Forum and EMVCo specifications used for the signal generation. \n
			:return: version: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NFC:VERSion?')
		return trim_str_response(response)
