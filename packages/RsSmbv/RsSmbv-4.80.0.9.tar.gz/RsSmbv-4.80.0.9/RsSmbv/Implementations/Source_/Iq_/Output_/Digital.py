from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Utilities import trim_str_response
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Digital:
	"""Digital commands group definition. 25 total commands, 6 Sub-groups, 4 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("digital", core, parent)

	def clone(self) -> 'Digital':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Digital(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def bbmm(self):
		"""bbmm commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_bbmm'):
			from .Digital_.Bbmm import Bbmm
			self._bbmm = Bbmm(self._core, self._base)
		return self._bbmm

	@property
	def channel(self):
		"""channel commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_channel'):
			from .Digital_.Channel import Channel
			self._channel = Channel(self._core, self._base)
		return self._channel

	@property
	def gdelay(self):
		"""gdelay commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_gdelay'):
			from .Digital_.Gdelay import Gdelay
			self._gdelay = Gdelay(self._core, self._base)
		return self._gdelay

	@property
	def oflow(self):
		"""oflow commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_oflow'):
			from .Digital_.Oflow import Oflow
			self._oflow = Oflow(self._core, self._base)
		return self._oflow

	@property
	def power(self):
		"""power commands group. 1 Sub-classes, 4 commands."""
		if not hasattr(self, '_power'):
			from .Digital_.Power import Power
			self._power = Power(self._core, self._base)
		return self._power

	@property
	def symbolRate(self):
		"""symbolRate commands group. 2 Sub-classes, 4 commands."""
		if not hasattr(self, '_symbolRate'):
			from .Digital_.SymbolRate import SymbolRate
			self._symbolRate = SymbolRate(self._core, self._base)
		return self._symbolRate

	def get_cdevice(self) -> str:
		"""[SOURce<HW>]:IQ:OUTPut:DIGital:CDEVice \n
		Queries information on the connected device. \n
			:return: cdevice: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:DIGital:CDEVice?')
		return trim_str_response(response)

	# noinspection PyTypeChecker
	def get_interface(self) -> enums.BbinInterfaceMode:
		"""[SOURce<HW>]:IQ:OUTPut:DIGital:INTerface \n
		Selects the connector at that the signal is output. \n
			:return: bbout_interf_mode: DIGital| HSDin | DIN| HSDin DIN Dig I/Q HSDin HS Dig I/Q
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:DIGital:INTerface?')
		return Conversions.str_to_scalar_enum(response, enums.BbinInterfaceMode)

	def set_interface(self, bbout_interf_mode: enums.BbinInterfaceMode) -> None:
		"""[SOURce<HW>]:IQ:OUTPut:DIGital:INTerface \n
		Selects the connector at that the signal is output. \n
			:param bbout_interf_mode: DIGital| HSDin | DIN| HSDin DIN Dig I/Q HSDin HS Dig I/Q
		"""
		param = Conversions.enum_scalar_to_str(bbout_interf_mode, enums.BbinInterfaceMode)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:DIGital:INTerface {param}')

	# noinspection PyTypeChecker
	def get_pon(self) -> enums.UnchOff:
		"""[SOURce<HW>]:IQ:OUTPut:DIGital:PON \n
		Sets the power-on state of the selected digital I/Q output. \n
			:return: pon: OFF| UNCHanged
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:DIGital:PON?')
		return Conversions.str_to_scalar_enum(response, enums.UnchOff)

	def set_pon(self, pon: enums.UnchOff) -> None:
		"""[SOURce<HW>]:IQ:OUTPut:DIGital:PON \n
		Sets the power-on state of the selected digital I/Q output. \n
			:param pon: OFF| UNCHanged
		"""
		param = Conversions.enum_scalar_to_str(pon, enums.UnchOff)
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:DIGital:PON {param}')

	def get_state(self) -> bool:
		"""[SOURce<HW>]:IQ:OUTPut:DIGital:STATe \n
		Activates the digital I/Q signal output. Note: Interdependencies
			INTRO_CMD_HELP: The following functions cannot be activated simultaneously. They deactivate each other. \n
			- The internal baseband generator ([:SOURce<hw>]:BB:<DigStd>:STATe) and the external digital baseband input ([:SOURce<hw>]:BBIN:STATe)
			- The external digital baseband input ([:SOURce<hw>]:BBIN:STATe) and digital output ([:SOURce<hw>]:IQ:OUTPut:DIGital:STATe) because they share the same physical connectors (Dig I/Q and the HS Dig I/Q) .
			- The digital output ([:SOURce<hw>]:IQ:OUTPut:DIGital:STATe) and the output of analog I/Q signals:
			Table Header:  \n
			- If [:SOURce<hw>]:IQ:SOURce BASeband, [:SOURce<hw>]:IQ:STATe + method RsSmbv.Output.State.value or
			- [:SOURce<hw>]:IQ:OUTPut:ANALog:STATe \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:IQ:OUTPut:DIGital:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""[SOURce<HW>]:IQ:OUTPut:DIGital:STATe \n
		Activates the digital I/Q signal output. Note: Interdependencies
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
		self._core.io.write(f'SOURce<HwInstance>:IQ:OUTPut:DIGital:STATe {param}')
