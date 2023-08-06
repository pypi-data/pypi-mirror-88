from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Gsm:
	"""Gsm commands group definition. 101 total commands, 17 Sub-groups, 7 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("gsm", core, parent)

	def clone(self) -> 'Gsm':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Gsm(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def aqPsk(self):
		"""aqPsk commands group. 2 Sub-classes, 1 commands."""
		if not hasattr(self, '_aqPsk'):
			from .Gsm_.AqPsk import AqPsk
			self._aqPsk = AqPsk(self._core, self._base)
		return self._aqPsk

	@property
	def clock(self):
		"""clock commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_clock'):
			from .Gsm_.Clock import Clock
			self._clock = Clock(self._core, self._base)
		return self._clock

	@property
	def edge(self):
		"""edge commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_edge'):
			from .Gsm_.Edge import Edge
			self._edge = Edge(self._core, self._base)
		return self._edge

	@property
	def filterPy(self):
		"""filterPy commands group. 7 Sub-classes, 2 commands."""
		if not hasattr(self, '_filterPy'):
			from .Gsm_.FilterPy import FilterPy
			self._filterPy = FilterPy(self._core, self._base)
		return self._filterPy

	@property
	def frame(self):
		"""frame commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_frame'):
			from .Gsm_.Frame import Frame
			self._frame = Frame(self._core, self._base)
		return self._frame

	@property
	def fsk(self):
		"""fsk commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_fsk'):
			from .Gsm_.Fsk import Fsk
			self._fsk = Fsk(self._core, self._base)
		return self._fsk

	@property
	def h16Qam(self):
		"""h16Qam commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_h16Qam'):
			from .Gsm_.H16Qam import H16Qam
			self._h16Qam = H16Qam(self._core, self._base)
		return self._h16Qam

	@property
	def h32Qam(self):
		"""h32Qam commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_h32Qam'):
			from .Gsm_.H32Qam import H32Qam
			self._h32Qam = H32Qam(self._core, self._base)
		return self._h32Qam

	@property
	def hqpsk(self):
		"""hqpsk commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_hqpsk'):
			from .Gsm_.Hqpsk import Hqpsk
			self._hqpsk = Hqpsk(self._core, self._base)
		return self._hqpsk

	@property
	def mframe(self):
		"""mframe commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_mframe'):
			from .Gsm_.Mframe import Mframe
			self._mframe = Mframe(self._core, self._base)
		return self._mframe

	@property
	def n16Qam(self):
		"""n16Qam commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_n16Qam'):
			from .Gsm_.N16Qam import N16Qam
			self._n16Qam = N16Qam(self._core, self._base)
		return self._n16Qam

	@property
	def n32Qam(self):
		"""n32Qam commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_n32Qam'):
			from .Gsm_.N32Qam import N32Qam
			self._n32Qam = N32Qam(self._core, self._base)
		return self._n32Qam

	@property
	def pramp(self):
		"""pramp commands group. 1 Sub-classes, 4 commands."""
		if not hasattr(self, '_pramp'):
			from .Gsm_.Pramp import Pramp
			self._pramp = Pramp(self._core, self._base)
		return self._pramp

	@property
	def sattenuation(self):
		"""sattenuation commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_sattenuation'):
			from .Gsm_.Sattenuation import Sattenuation
			self._sattenuation = Sattenuation(self._core, self._base)
		return self._sattenuation

	@property
	def setting(self):
		"""setting commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_setting'):
			from .Gsm_.Setting import Setting
			self._setting = Setting(self._core, self._base)
		return self._setting

	@property
	def symbolRate(self):
		"""symbolRate commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_symbolRate'):
			from .Gsm_.SymbolRate import SymbolRate
			self._symbolRate = SymbolRate(self._core, self._base)
		return self._symbolRate

	@property
	def trigger(self):
		"""trigger commands group. 4 Sub-classes, 5 commands."""
		if not hasattr(self, '_trigger'):
			from .Gsm_.Trigger import Trigger
			self._trigger = Trigger(self._core, self._base)
		return self._trigger

	def get_fone(self) -> bool:
		"""[SOURce<HW>]:BB:GSM:FONE \n
		A modulating bit stream consisting of consecutive ones is used for inactive slots (according to GSM 05.04) .
		If this parameter is disabled, the inactive slots are filled in with 0. \n
			:return: fone: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GSM:FONE?')
		return Conversions.str_to_bool(response)

	def set_fone(self, fone: bool) -> None:
		"""[SOURce<HW>]:BB:GSM:FONE \n
		A modulating bit stream consisting of consecutive ones is used for inactive slots (according to GSM 05.04) .
		If this parameter is disabled, the inactive slots are filled in with 0. \n
			:param fone: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(fone)
		self._core.io.write(f'SOURce<HwInstance>:BB:GSM:FONE {param}')

	# noinspection PyTypeChecker
	def get_format_py(self) -> enums.GsmModTypeGsm:
		"""[SOURce<HW>]:BB:GSM:FORMat \n
		The command selects the modulation type. \n
			:return: format_py: MSK| FSK2
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GSM:FORMat?')
		return Conversions.str_to_scalar_enum(response, enums.GsmModTypeGsm)

	def set_format_py(self, format_py: enums.GsmModTypeGsm) -> None:
		"""[SOURce<HW>]:BB:GSM:FORMat \n
		The command selects the modulation type. \n
			:param format_py: MSK| FSK2
		"""
		param = Conversions.enum_scalar_to_str(format_py, enums.GsmModTypeGsm)
		self._core.io.write(f'SOURce<HwInstance>:BB:GSM:FORMat {param}')

	def get_is_length(self) -> bool:
		"""[SOURce<HW>]:BB:GSM:ISLength \n
		Selects constant slot length. \n
			:return: is_length: 0| 1| OFF| ON For normal symbol rate mode: The command selects whether the 1/4 symbol of a GSM slot is ignored or compensated for by an extra symbol every 4th slot. For higher symbol rate mode: The command selects whether the 1/2 symbol of an average slot with a length of 187.5 symbols are ignored or compensated for by an extra symbol every second slot. ON In normal symbol rate mode, all slots are 156 symbols long In higher symbol rate mode, all slots are 187 symbols long OFF In normal symbol rate mode, some slots are 157 symbols long In higher symbol rate mode, some slots are 188 symbols long
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GSM:ISLength?')
		return Conversions.str_to_bool(response)

	def set_is_length(self, is_length: bool) -> None:
		"""[SOURce<HW>]:BB:GSM:ISLength \n
		Selects constant slot length. \n
			:param is_length: 0| 1| OFF| ON For normal symbol rate mode: The command selects whether the 1/4 symbol of a GSM slot is ignored or compensated for by an extra symbol every 4th slot. For higher symbol rate mode: The command selects whether the 1/2 symbol of an average slot with a length of 187.5 symbols are ignored or compensated for by an extra symbol every second slot. ON In normal symbol rate mode, all slots are 156 symbols long In higher symbol rate mode, all slots are 187 symbols long OFF In normal symbol rate mode, some slots are 157 symbols long In higher symbol rate mode, some slots are 188 symbols long
		"""
		param = Conversions.bool_to_str(is_length)
		self._core.io.write(f'SOURce<HwInstance>:BB:GSM:ISLength {param}')

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.GsmMode:
		"""[SOURce<HW>]:BB:GSM:MODE \n
		The command selects GSM mode. \n
			:return: mode: UNFRamed| SINGle| DOUBle| MULTiframe UNFRamed Modulation signal without slot and frame structure. SINGle Modulation signal consisting of one frame. DOUBle Modulation signal in which two frames are defined and then combined by some method into a single multiframe signal. MULTiframe Multiframe signal.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GSM:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.GsmMode)

	def set_mode(self, mode: enums.GsmMode) -> None:
		"""[SOURce<HW>]:BB:GSM:MODE \n
		The command selects GSM mode. \n
			:param mode: UNFRamed| SINGle| DOUBle| MULTiframe UNFRamed Modulation signal without slot and frame structure. SINGle Modulation signal consisting of one frame. DOUBle Modulation signal in which two frames are defined and then combined by some method into a single multiframe signal. MULTiframe Multiframe signal.
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.GsmMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:GSM:MODE {param}')

	def preset(self) -> None:
		"""[SOURce<HW>]:BB:GSM:PRESet \n
		Sets the parameters of the digital standard to their default values (*RST values specified for the commands) .
		Not affected is the state set with the command method RsSmbv.Source.Bb.Gsm.state. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:BB:GSM:PRESet')

	def preset_with_opc(self) -> None:
		"""[SOURce<HW>]:BB:GSM:PRESet \n
		Sets the parameters of the digital standard to their default values (*RST values specified for the commands) .
		Not affected is the state set with the command method RsSmbv.Source.Bb.Gsm.state. \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:GSM:PRESet')

	# noinspection PyTypeChecker
	def get_smode(self) -> enums.GsmSimMode:
		"""[SOURce<HW>]:BB:GSM:SMODe \n
		Selects the modulation signal for the mode Unframed (BB:GSM:MODE UNFR) . The modulation type and filter type are set in
		accordance with the selection.
			INTRO_CMD_HELP: The available simulation modes depend on the selected symbol rate: \n
			- Normal Symbol Rate - GSM, EDGE (8PSK) , AQPSK, 16QAM and 32QAM
			- Higher Symbol Rate - HSR QPSK, HSR 16QAM and HSR 32QAM.
		Note:'Higher Symbol Rate' Mode and 'Simulation Modes' AQPSK, 16QAM, 32QAM, HSR QPSK, HSR 16QAM and HSR 32QAM are
		available for instruments equipped with option R&S SMBVB-K41 only. \n
			:return: sm_ode: GSM| EDGE| N16Qam| N32Qam| HQPSk| H16Qam| H32Qam| AQPSk
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GSM:SMODe?')
		return Conversions.str_to_scalar_enum(response, enums.GsmSimMode)

	def set_smode(self, sm_ode: enums.GsmSimMode) -> None:
		"""[SOURce<HW>]:BB:GSM:SMODe \n
		Selects the modulation signal for the mode Unframed (BB:GSM:MODE UNFR) . The modulation type and filter type are set in
		accordance with the selection.
			INTRO_CMD_HELP: The available simulation modes depend on the selected symbol rate: \n
			- Normal Symbol Rate - GSM, EDGE (8PSK) , AQPSK, 16QAM and 32QAM
			- Higher Symbol Rate - HSR QPSK, HSR 16QAM and HSR 32QAM.
		Note:'Higher Symbol Rate' Mode and 'Simulation Modes' AQPSK, 16QAM, 32QAM, HSR QPSK, HSR 16QAM and HSR 32QAM are
		available for instruments equipped with option R&S SMBVB-K41 only. \n
			:param sm_ode: GSM| EDGE| N16Qam| N32Qam| HQPSk| H16Qam| H32Qam| AQPSk
		"""
		param = Conversions.enum_scalar_to_str(sm_ode, enums.GsmSimMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:GSM:SMODe {param}')

	def get_state(self) -> bool:
		"""[SOURce<HW>]:BB:GSM:STATe \n
		Activates the standard and deactivates all the other digital standards and digital modulation modes in the same path. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:GSM:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""[SOURce<HW>]:BB:GSM:STATe \n
		Activates the standard and deactivates all the other digital standards and digital modulation modes in the same path. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:GSM:STATe {param}')
