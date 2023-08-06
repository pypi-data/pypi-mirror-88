from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Analog:
	"""Analog commands group definition. 62 total commands, 6 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("analog", core, parent)

	def clone(self) -> 'Analog':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Analog(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def bias(self):
		"""bias commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_bias'):
			from .Analog_.Bias import Bias
			self._bias = Bias(self._core, self._base)
		return self._bias

	@property
	def envelope(self):
		"""envelope commands group. 7 Sub-classes, 12 commands."""
		if not hasattr(self, '_envelope'):
			from .Analog_.Envelope import Envelope
			self._envelope = Envelope(self._core, self._base)
		return self._envelope

	@property
	def offset(self):
		"""offset commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_offset'):
			from .Analog_.Offset import Offset
			self._offset = Offset(self._core, self._base)
		return self._offset

	@property
	def power(self):
		"""power commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_power'):
			from .Analog_.Power import Power
			self._power = Power(self._core, self._base)
		return self._power

	@property
	def ppsMarker(self):
		"""ppsMarker commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ppsMarker'):
			from .Analog_.PpsMarker import PpsMarker
			self._ppsMarker = PpsMarker(self._core, self._base)
		return self._ppsMarker

	@property
	def setting(self):
		"""setting commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_setting'):
			from .Analog_.Setting import Setting
			self._setting = Setting(self._core, self._base)
		return self._setting

	def get_state(self) -> bool:
		"""[SOURce<HW>]:IQ:OUTPut:ANALog:STATe \n
		Activates the specified analog I/Q output. Note: Interdependencies
			INTRO_CMD_HELP: The following functions cannot be activated simultaneously. They deactivate each other. \n
			- The internal baseband generator ([:SOURce<hw>]:BB:<DigStd>:STATe) and the external digital baseband input ([:SOURce<hw>]:BBIN:STATe)
			- The external digital baseband input ([:SOURce<hw>]:BBIN:STATe) and digital output ([:SOURce<hw>]:IQ:OUTPut:DIGital:STATe) because they share the same physical connectors (Dig I/Q and the HS Dig I/Q) .
			- The digital output ([:SOURce<hw>]:IQ:OUTPut:DIGital:STATe) and the output of analog I/Q signals:
			Table Header:  \n
			- If [:SOURce<hw>]:IQ:SOURce BASeband, [:SOURce<hw>]:IQ:STATe + method RsSmbv.Output.State.value or
			- [:SOURce<hw>]:IQ:OUTPut:ANALog:STATe \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:ANALog:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""[SOURce<HW>]:IQ:OUTPut:ANALog:STATe \n
		Activates the specified analog I/Q output. Note: Interdependencies
			INTRO_CMD_HELP: The following functions cannot be activated simultaneously. They deactivate each other. \n
			- The internal baseband generator ([:SOURce<hw>]:BB:<DigStd>:STATe) and the external digital baseband input ([:SOURce<hw>]:BBIN:STATe)
			- The external digital baseband input ([:SOURce<hw>]:BBIN:STATe) and digital output ([:SOURce<hw>]:IQ:OUTPut:DIGital:STATe) because they share the same physical connectors (Dig I/Q and the HS Dig I/Q) .
			- The digital output ([:SOURce<hw>]:IQ:OUTPut:DIGital:STATe) and the output of analog I/Q signals:
			Table Header:  \n
			- If [:SOURce<hw>]:IQ:SOURce BASeband, [:SOURce<hw>]:IQ:STATe + method RsSmbv.Output.State.value or
			- [:SOURce<hw>]:IQ:OUTPut:ANALog:STATe \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:STATe {param}')

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.IqOutMode:
		"""[SOURce<HW>]:IQ:OUTPut:[ANALog]:MODE \n
		Determines the mode for setting the output parameters. \n
			:return: mode: FIXed| VARiable | VATTenuated FIXed Locks the I/Q output settings VARiable Unlocks the settings VATTenuated Attenuates the signal with the value set with the command method RsSmbv.Source.Iq.Output.Analog.Power.attDigital.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:ANALog:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.IqOutMode)

	def set_mode(self, mode: enums.IqOutMode) -> None:
		"""[SOURce<HW>]:IQ:OUTPut:[ANALog]:MODE \n
		Determines the mode for setting the output parameters. \n
			:param mode: FIXed| VARiable | VATTenuated FIXed Locks the I/Q output settings VARiable Unlocks the settings VATTenuated Attenuates the signal with the value set with the command method RsSmbv.Source.Iq.Output.Analog.Power.attDigital.
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.IqOutMode)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:MODE {param}')

	def preset(self) -> None:
		"""[SOURce<HW>]:IQ:OUTPut:[ANALog]:PRESet \n
		Sets the default settings (*RST values specified for the commands) .
			INTRO_CMD_HELP: Not affected are: \n
			- The state set with the command method RsSmbv.Source.Iq.Output.Analog.state.
			- If SCONfiguration:EXTernal:PBEHaviour 1, the I/Q ouptput type set with the command IQ:TYPE. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:PRESet')

	def preset_with_opc(self) -> None:
		"""[SOURce<HW>]:IQ:OUTPut:[ANALog]:PRESet \n
		Sets the default settings (*RST values specified for the commands) .
			INTRO_CMD_HELP: Not affected are: \n
			- The state set with the command method RsSmbv.Source.Iq.Output.Analog.state.
			- If SCONfiguration:EXTernal:PBEHaviour 1, the I/Q ouptput type set with the command IQ:TYPE. \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:PRESet')

	# noinspection PyTypeChecker
	def get_type_py(self) -> enums.IqOutType:
		"""[SOURce<HW>]:IQ:OUTPut:[ANALog]:TYPE \n
		Sets the type of the analog signal. \n
			:return: type_py: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:ANALog:TYPE?')
		return Conversions.str_to_scalar_enum(response, enums.IqOutType)

	def set_type_py(self, type_py: enums.IqOutType) -> None:
		"""[SOURce<HW>]:IQ:OUTPut:[ANALog]:TYPE \n
		Sets the type of the analog signal. \n
			:param type_py: No help available
		"""
		param = Conversions.enum_scalar_to_str(type_py, enums.IqOutType)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:ANALog:TYPE {param}')
