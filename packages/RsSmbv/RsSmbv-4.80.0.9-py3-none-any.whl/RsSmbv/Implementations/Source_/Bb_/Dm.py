from typing import List

from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Types import DataType
from ....Internal.StructBase import StructBase
from ....Internal.ArgStruct import ArgStruct
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dm:
	"""Dm commands group definition. 100 total commands, 18 Sub-groups, 7 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dm", core, parent)

	def clone(self) -> 'Dm':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Dm(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def apsk16(self):
		"""apsk16 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_apsk16'):
			from .Dm_.Apsk16 import Apsk16
			self._apsk16 = Apsk16(self._core, self._base)
		return self._apsk16

	@property
	def apsk32(self):
		"""apsk32 commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_apsk32'):
			from .Dm_.Apsk32 import Apsk32
			self._apsk32 = Apsk32(self._core, self._base)
		return self._apsk32

	@property
	def aqPsk(self):
		"""aqPsk commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_aqPsk'):
			from .Dm_.AqPsk import AqPsk
			self._aqPsk = AqPsk(self._core, self._base)
		return self._aqPsk

	@property
	def ask(self):
		"""ask commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ask'):
			from .Dm_.Ask import Ask
			self._ask = Ask(self._core, self._base)
		return self._ask

	@property
	def clist(self):
		"""clist commands group. 0 Sub-classes, 8 commands."""
		if not hasattr(self, '_clist'):
			from .Dm_.Clist import Clist
			self._clist = Clist(self._core, self._base)
		return self._clist

	@property
	def clock(self):
		"""clock commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_clock'):
			from .Dm_.Clock import Clock
			self._clock = Clock(self._core, self._base)
		return self._clock

	@property
	def dlist(self):
		"""dlist commands group. 1 Sub-classes, 7 commands."""
		if not hasattr(self, '_dlist'):
			from .Dm_.Dlist import Dlist
			self._dlist = Dlist(self._core, self._base)
		return self._dlist

	@property
	def filterPy(self):
		"""filterPy commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_filterPy'):
			from .Dm_.FilterPy import FilterPy
			self._filterPy = FilterPy(self._core, self._base)
		return self._filterPy

	@property
	def flist(self):
		"""flist commands group. 0 Sub-classes, 5 commands."""
		if not hasattr(self, '_flist'):
			from .Dm_.Flist import Flist
			self._flist = Flist(self._core, self._base)
		return self._flist

	@property
	def fsk(self):
		"""fsk commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_fsk'):
			from .Dm_.Fsk import Fsk
			self._fsk = Fsk(self._core, self._base)
		return self._fsk

	@property
	def mlist(self):
		"""mlist commands group. 0 Sub-classes, 5 commands."""
		if not hasattr(self, '_mlist'):
			from .Dm_.Mlist import Mlist
			self._mlist = Mlist(self._core, self._base)
		return self._mlist

	@property
	def pramp(self):
		"""pramp commands group. 1 Sub-classes, 7 commands."""
		if not hasattr(self, '_pramp'):
			from .Dm_.Pramp import Pramp
			self._pramp = Pramp(self._core, self._base)
		return self._pramp

	@property
	def prbs(self):
		"""prbs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_prbs'):
			from .Dm_.Prbs import Prbs
			self._prbs = Prbs(self._core, self._base)
		return self._prbs

	@property
	def setting(self):
		"""setting commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_setting'):
			from .Dm_.Setting import Setting
			self._setting = Setting(self._core, self._base)
		return self._setting

	@property
	def smodulation(self):
		"""smodulation commands group. 3 Sub-classes, 2 commands."""
		if not hasattr(self, '_smodulation'):
			from .Dm_.Smodulation import Smodulation
			self._smodulation = Smodulation(self._core, self._base)
		return self._smodulation

	@property
	def standard(self):
		"""standard commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_standard'):
			from .Dm_.Standard import Standard
			self._standard = Standard(self._core, self._base)
		return self._standard

	@property
	def switching(self):
		"""switching commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_switching'):
			from .Dm_.Switching import Switching
			self._switching = Switching(self._core, self._base)
		return self._switching

	@property
	def trigger(self):
		"""trigger commands group. 5 Sub-classes, 4 commands."""
		if not hasattr(self, '_trigger'):
			from .Dm_.Trigger import Trigger
			self._trigger = Trigger(self._core, self._base)
		return self._trigger

	# noinspection PyTypeChecker
	def get_coding(self) -> enums.DmCod:
		"""[SOURce<HW>]:BB:DM:CODing \n
		Selects the modulation coding. \n
			:return: coding: OFF| DIFF| DPHS| DGRay| GRAY| GSM| NADC| PDC| PHS| TETRa| APCO25| PWT| TFTS| INMarsat| VDL| EDGE| APCO25FSK| ICO| CDMA2000| WCDMA| APCO258PSK OFF The coding is automatically disabled if the selected modulation type is not possible with the coding that has been set DPHS Phase Difference DGRay Difference + Gray
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DM:CODing?')
		return Conversions.str_to_scalar_enum(response, enums.DmCod)

	def set_coding(self, coding: enums.DmCod) -> None:
		"""[SOURce<HW>]:BB:DM:CODing \n
		Selects the modulation coding. \n
			:param coding: OFF| DIFF| DPHS| DGRay| GRAY| GSM| NADC| PDC| PHS| TETRa| APCO25| PWT| TFTS| INMarsat| VDL| EDGE| APCO25FSK| ICO| CDMA2000| WCDMA| APCO258PSK OFF The coding is automatically disabled if the selected modulation type is not possible with the coding that has been set DPHS Phase Difference DGRay Difference + Gray
		"""
		param = Conversions.enum_scalar_to_str(coding, enums.DmCod)
		self._core.io.write(f'SOURce<HwInstance>:BB:DM:CODing {param}')

	# noinspection PyTypeChecker
	def get_format_py(self) -> enums.BbDmModType:
		"""[SOURce<HW>]:BB:DM:FORMat \n
		Sets the modulation type. When a standard is selected (method RsSmbv.Source.Bb.Dm.Standard.value) , the modulation type
		is set to the default value. \n
			:return: format_py: ASK| BPSK| P2DBpsk| QPSK| QPSK45| OQPSk| P4QPsk| P4DQpsk| PSK8| P8D8psk| P8EDge| QAM16| QAM32| QAM64| QAM256| QAM1024| MSK| FSK2| FSK4| USER| FSKVar| QAM128| QEDGe| QAM16EDge| QAM32EDge| AQPSk| QAM4096| APSK16| APSK32| FSK32| FSK64| FSK8| FSK16| QAM512| QAM2048
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DM:FORMat?')
		return Conversions.str_to_scalar_enum(response, enums.BbDmModType)

	def set_format_py(self, format_py: enums.BbDmModType) -> None:
		"""[SOURce<HW>]:BB:DM:FORMat \n
		Sets the modulation type. When a standard is selected (method RsSmbv.Source.Bb.Dm.Standard.value) , the modulation type
		is set to the default value. \n
			:param format_py: ASK| BPSK| P2DBpsk| QPSK| QPSK45| OQPSk| P4QPsk| P4DQpsk| PSK8| P8D8psk| P8EDge| QAM16| QAM32| QAM64| QAM256| QAM1024| MSK| FSK2| FSK4| USER| FSKVar| QAM128| QEDGe| QAM16EDge| QAM32EDge| AQPSk| QAM4096| APSK16| APSK32| FSK32| FSK64| FSK8| FSK16| QAM512| QAM2048
		"""
		param = Conversions.enum_scalar_to_str(format_py, enums.BbDmModType)
		self._core.io.write(f'SOURce<HwInstance>:BB:DM:FORMat {param}')

	# noinspection PyTypeChecker
	class PatternStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Pattern: List[str]: numeric
			- Bit_Count: int: integer Range: 1 to 64"""
		__meta_args_list = [
			ArgStruct('Pattern', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Pattern: List[str] = None
			self.Bit_Count: int = None

	def get_pattern(self) -> PatternStruct:
		"""[SOURce<HW>]:BB:DM:PATTern \n
		Selects the data pattern for the internal data source. \n
			:return: structure: for return value, see the help for PatternStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:DM:PATTern?', self.__class__.PatternStruct())

	def set_pattern(self, value: PatternStruct) -> None:
		"""[SOURce<HW>]:BB:DM:PATTern \n
		Selects the data pattern for the internal data source. \n
			:param value: see the help for PatternStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:DM:PATTern', value)

	def preset(self) -> None:
		"""[SOURce<HW>]:BB:DM:PRESet \n
		Sets the default settings for digital modulation (*RST values specified for the commands) . Not affected is the state set
		with the command method RsSmbv.Source.Bb.Dm.state \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:BB:DM:PRESet')

	def preset_with_opc(self) -> None:
		"""[SOURce<HW>]:BB:DM:PRESet \n
		Sets the default settings for digital modulation (*RST values specified for the commands) . Not affected is the state set
		with the command method RsSmbv.Source.Bb.Dm.state \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:DM:PRESet')

	# noinspection PyTypeChecker
	def get_source(self) -> enums.DmDataSourV:
		"""[SOURce<HW>]:BB:DM:SOURce \n
		Selects the data source. \n
			:return: source: ZERO| ONE| PRBS| PATTern| DLISt A sequence of 0 or 1, a pseudo-random sequence with different length, a pattern, or a data list.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DM:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.DmDataSourV)

	def set_source(self, source: enums.DmDataSourV) -> None:
		"""[SOURce<HW>]:BB:DM:SOURce \n
		Selects the data source. \n
			:param source: ZERO| ONE| PRBS| PATTern| DLISt A sequence of 0 or 1, a pseudo-random sequence with different length, a pattern, or a data list.
		"""
		param = Conversions.enum_scalar_to_str(source, enums.DmDataSourV)
		self._core.io.write(f'SOURce<HwInstance>:BB:DM:SOURce {param}')

	def get_symbol_rate(self) -> float:
		"""[SOURce<HW>]:BB:DM:SRATe \n
		Sets the symbol rate in Hz/kHz/MHz or sym/s, ksym/s and Msym/s. \n
			:return: srate: float Range: 400 to depends on the installed options, Unit: Hz or sym/s
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DM:SRATe?')
		return Conversions.str_to_float(response)

	def set_symbol_rate(self, srate: float) -> None:
		"""[SOURce<HW>]:BB:DM:SRATe \n
		Sets the symbol rate in Hz/kHz/MHz or sym/s, ksym/s and Msym/s. \n
			:param srate: float Range: 400 to depends on the installed options, Unit: Hz or sym/s
		"""
		param = Conversions.decimal_value_to_str(srate)
		self._core.io.write(f'SOURce<HwInstance>:BB:DM:SRATe {param}')

	def get_state(self) -> bool:
		"""[SOURce<HW>]:BB:DM:STATe \n
		Enables/disables digital modulation. Switching on digital modulation turns off all the other digital standards in the
		same signal path. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DM:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""[SOURce<HW>]:BB:DM:STATe \n
		Enables/disables digital modulation. Switching on digital modulation turns off all the other digital standards in the
		same signal path. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:DM:STATe {param}')
