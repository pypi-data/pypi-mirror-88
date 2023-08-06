from typing import List

from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.Types import DataType
from ......Internal.StructBase import StructBase
from ......Internal.ArgStruct import ArgStruct
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pconfiguration:
	"""Pconfiguration commands group definition. 121 total commands, 13 Sub-groups, 84 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pconfiguration", core, parent)

	def clone(self) -> 'Pconfiguration':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Pconfiguration(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def acad(self):
		"""acad commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_acad'):
			from .Pconfiguration_.Acad import Acad
			self._acad = Acad(self._core, self._base)
		return self._acad

	@property
	def data(self):
		"""data commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_data'):
			from .Pconfiguration_.Data import Data
			self._data = Data(self._core, self._base)
		return self._data

	@property
	def dcmTable(self):
		"""dcmTable commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_dcmTable'):
			from .Pconfiguration_.DcmTable import DcmTable
			self._dcmTable = DcmTable(self._core, self._base)
		return self._dcmTable

	@property
	def eheader(self):
		"""eheader commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_eheader'):
			from .Pconfiguration_.Eheader import Eheader
			self._eheader = Eheader(self._core, self._base)
		return self._eheader

	@property
	def ehFlags(self):
		"""ehFlags commands group. 7 Sub-classes, 0 commands."""
		if not hasattr(self, '_ehFlags'):
			from .Pconfiguration_.EhFlags import EhFlags
			self._ehFlags = EhFlags(self._core, self._base)
		return self._ehFlags

	@property
	def fsbit(self):
		"""fsbit commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_fsbit'):
			from .Pconfiguration_.Fsbit import Fsbit
			self._fsbit = Fsbit(self._core, self._base)
		return self._fsbit

	@property
	def mtsphy(self):
		"""mtsphy commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_mtsphy'):
			from .Pconfiguration_.Mtsphy import Mtsphy
			self._mtsphy = Mtsphy(self._core, self._base)
		return self._mtsphy

	@property
	def offset(self):
		"""offset commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_offset'):
			from .Pconfiguration_.Offset import Offset
			self._offset = Offset(self._core, self._base)
		return self._offset

	@property
	def phy(self):
		"""phy commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_phy'):
			from .Pconfiguration_.Phy import Phy
			self._phy = Phy(self._core, self._base)
		return self._phy

	@property
	def phys(self):
		"""phys commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_phys'):
			from .Pconfiguration_.Phys import Phys
			self._phys = Phys(self._core, self._base)
		return self._phys

	@property
	def rphys(self):
		"""rphys commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_rphys'):
			from .Pconfiguration_.Rphys import Rphys
			self._rphys = Rphys(self._core, self._base)
		return self._rphys

	@property
	def stmPhy(self):
		"""stmPhy commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_stmPhy'):
			from .Pconfiguration_.StmPhy import StmPhy
			self._stmPhy = StmPhy(self._core, self._base)
		return self._stmPhy

	@property
	def tphys(self):
		"""tphys commands group. 3 Sub-classes, 0 commands."""
		if not hasattr(self, '_tphys'):
			from .Pconfiguration_.Tphys import Tphys
			self._tphys = Tphys(self._core, self._base)
		return self._tphys

	# noinspection PyTypeChecker
	class AaddressStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Aaddress: List[str]: numeric
			- Bit_Count: int: integer Range: 32 to 32"""
		__meta_args_list = [
			ArgStruct('Aaddress', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Aaddress: List[str] = None
			self.Bit_Count: int = None

	def get_aaddress(self) -> AaddressStruct:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:AADDress \n
		Sets the access address of the link layer connection (32-bit string) . \n
			:return: structure: for return value, see the help for AaddressStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:AADDress?', self.__class__.AaddressStruct())

	def set_aaddress(self, value: AaddressStruct) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:AADDress \n
		Sets the access address of the link layer connection (32-bit string) . \n
			:param value: see the help for AaddressStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:AADDress', value)

	# noinspection PyTypeChecker
	class AcAssignedStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Ac_Assigned: List[str]: No parameter help available
			- Bit_Count: int: integer Range: 24 to 24"""
		__meta_args_list = [
			ArgStruct('Ac_Assigned', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Ac_Assigned: List[str] = None
			self.Bit_Count: int = None

	def get_ac_assigned(self) -> AcAssignedStruct:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:ACASsigned \n
		Sets the advertiser´s device address. For advertising channel packets, the format of the device address differs,
		depending on the selected address type.
			INTRO_CMD_HELP: Selects the clock source: \n
			- 'Public Address Types' The public address is given from the registration authority IEEE and is composed of:
			Table Header:  \n
			- LSB: 24 bits = company_assigned
			- MSB: 24 bits = company_id
			- 'Random Address Type' is a 48-bits random static device address.
			- 'Private Address Type' A private address is optional and composed of:
			Table Header:  \n
			- LSB: 24 bits = hash
			- MSB: 24 bits = random \n
			:return: structure: for return value, see the help for AcAssignedStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:ACASsigned?', self.__class__.AcAssignedStruct())

	def set_ac_assigned(self, value: AcAssignedStruct) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:ACASsigned \n
		Sets the advertiser´s device address. For advertising channel packets, the format of the device address differs,
		depending on the selected address type.
			INTRO_CMD_HELP: Selects the clock source: \n
			- 'Public Address Types' The public address is given from the registration authority IEEE and is composed of:
			Table Header:  \n
			- LSB: 24 bits = company_assigned
			- MSB: 24 bits = company_id
			- 'Random Address Type' is a 48-bits random static device address.
			- 'Private Address Type' A private address is optional and composed of:
			Table Header:  \n
			- LSB: 24 bits = hash
			- MSB: 24 bits = random \n
			:param value: see the help for AcAssignedStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:ACASsigned', value)

	# noinspection PyTypeChecker
	class AcidStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Acid: List[str]: No parameter help available
			- Bit_Count: int: integer Range: 24 to 24"""
		__meta_args_list = [
			ArgStruct('Acid', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Acid: List[str] = None
			self.Bit_Count: int = None

	def get_acid(self) -> AcidStruct:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:ACID \n
		Sets the advertiser´s device address. For advertising channel packets, the format of the device address differs,
		depending on the selected address type.
			INTRO_CMD_HELP: Selects the clock source: \n
			- 'Public Address Types' The public address is given from the registration authority IEEE and is composed of:
			Table Header:  \n
			- LSB: 24 bits = company_assigned
			- MSB: 24 bits = company_id
			- 'Random Address Type' is a 48-bits random static device address.
			- 'Private Address Type' A private address is optional and composed of:
			Table Header:  \n
			- LSB: 24 bits = hash
			- MSB: 24 bits = random \n
			:return: structure: for return value, see the help for AcidStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:ACID?', self.__class__.AcidStruct())

	def set_acid(self, value: AcidStruct) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:ACID \n
		Sets the advertiser´s device address. For advertising channel packets, the format of the device address differs,
		depending on the selected address type.
			INTRO_CMD_HELP: Selects the clock source: \n
			- 'Public Address Types' The public address is given from the registration authority IEEE and is composed of:
			Table Header:  \n
			- LSB: 24 bits = company_assigned
			- MSB: 24 bits = company_id
			- 'Random Address Type' is a 48-bits random static device address.
			- 'Private Address Type' A private address is optional and composed of:
			Table Header:  \n
			- LSB: 24 bits = hash
			- MSB: 24 bits = random \n
			:param value: see the help for AcidStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:ACID', value)

	# noinspection PyTypeChecker
	class AdidStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Adid: List[str]: numeric
			- Bit_Count: int: integer Range: 12 to 12"""
		__meta_args_list = [
			ArgStruct('Adid', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Adid: List[str] = None
			self.Bit_Count: int = None

	def get_adid(self) -> AdidStruct:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:ADID \n
		Specifies 'Advertising Data ID' in hexadecimal format to be signaled within an extended header. \n
			:return: structure: for return value, see the help for AdidStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:ADID?', self.__class__.AdidStruct())

	def set_adid(self, value: AdidStruct) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:ADID \n
		Specifies 'Advertising Data ID' in hexadecimal format to be signaled within an extended header. \n
			:param value: see the help for AdidStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:ADID', value)

	# noinspection PyTypeChecker
	class AlapStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Lap: List[str]: numeric
			- Bit_Count: int: integer Range: 24 to 24"""
		__meta_args_list = [
			ArgStruct('Lap', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Lap: List[str] = None
			self.Bit_Count: int = None

	def get_alap(self) -> AlapStruct:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:ALAP \n
		Sets the lower address part (LAP) of Bluetooth device address. Commands for the advertising ..:ALAP, initiating ..:ILAP,
		scanning ..:SLAP PDUs of advertising channel type are provided. In addition, a command is provided for scanner’s or
		initiator’s target device address to which the advertisement is directed ..:TLAP. \n
			:return: structure: for return value, see the help for AlapStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:ALAP?', self.__class__.AlapStruct())

	def set_alap(self, value: AlapStruct) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:ALAP \n
		Sets the lower address part (LAP) of Bluetooth device address. Commands for the advertising ..:ALAP, initiating ..:ILAP,
		scanning ..:SLAP PDUs of advertising channel type are provided. In addition, a command is provided for scanner’s or
		initiator’s target device address to which the advertisement is directed ..:TLAP. \n
			:param value: see the help for AlapStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:ALAP', value)

	def get_alength(self) -> int:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:ALENgth \n
		Specifies the length of ACAD data pattern. \n
			:return: length: integer Range: 0 to 62
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:ALENgth?')
		return Conversions.str_to_int(response)

	def set_alength(self, length: int) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:ALENgth \n
		Specifies the length of ACAD data pattern. \n
			:param length: integer Range: 0 to 62
		"""
		param = Conversions.decimal_value_to_str(length)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:ALENgth {param}')

	# noinspection PyTypeChecker
	def get_amode(self) -> enums.BtoAdvMode:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:AMODe \n
		Indicates the mode of the advertisement. \n
			:return: am_ode: NCNS| CNS| NCS NCNS: Non-connectable, non-scannable CNS: Connectable, non-scannable NCS: Non-connectable, non-scannable
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:AMODe?')
		return Conversions.str_to_scalar_enum(response, enums.BtoAdvMode)

	def set_amode(self, am_ode: enums.BtoAdvMode) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:AMODe \n
		Indicates the mode of the advertisement. \n
			:param am_ode: NCNS| CNS| NCS NCNS: Non-connectable, non-scannable CNS: Connectable, non-scannable NCS: Non-connectable, non-scannable
		"""
		param = Conversions.enum_scalar_to_str(am_ode, enums.BtoAdvMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:AMODe {param}')

	# noinspection PyTypeChecker
	class AnuapStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Nap_Uap: List[str]: numeric
			- Bit_Count: int: integer Range: 24 to 24"""
		__meta_args_list = [
			ArgStruct('Nap_Uap', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Nap_Uap: List[str] = None
			self.Bit_Count: int = None

	def get_anuap(self) -> AnuapStruct:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:ANUap \n
		Sets the non-significant address part (NAP) and upper address part (UAP) of Bluetooth device address. Commands for the
		advertising ..:ANUap, initiating ..:INUap, and scanning ..:SNUap PDUs of advertising channel type are provided.
		In addition, a command is provided for scanner’s or initiator’s target device address to which the advertisement is
		directed ..:TNUap. \n
			:return: structure: for return value, see the help for AnuapStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:ANUap?', self.__class__.AnuapStruct())

	def set_anuap(self, value: AnuapStruct) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:ANUap \n
		Sets the non-significant address part (NAP) and upper address part (UAP) of Bluetooth device address. Commands for the
		advertising ..:ANUap, initiating ..:INUap, and scanning ..:SNUap PDUs of advertising channel type are provided.
		In addition, a command is provided for scanner’s or initiator’s target device address to which the advertisement is
		directed ..:TNUap. \n
			:param value: see the help for AnuapStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:ANUap', value)

	def get_aoffset(self) -> float:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:AOFFset \n
		Specifies the time from the start of the packet containing the AuxPtr field to the approximate start of the auxiliary
		packet. The offset is determined by multiplying the value by the unit, see method RsSmbv.Source.Bb.Btooth.Econfiguration.
		Pconfiguration.aoUnits \n
			:return: ao_ffset: float Range: 0 to 245.7 or 246 to 2457 depending on offset unit
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:AOFFset?')
		return Conversions.str_to_float(response)

	def set_aoffset(self, ao_ffset: float) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:AOFFset \n
		Specifies the time from the start of the packet containing the AuxPtr field to the approximate start of the auxiliary
		packet. The offset is determined by multiplying the value by the unit, see method RsSmbv.Source.Bb.Btooth.Econfiguration.
		Pconfiguration.aoUnits \n
			:param ao_ffset: float Range: 0 to 245.7 or 246 to 2457 depending on offset unit
		"""
		param = Conversions.decimal_value_to_str(ao_ffset)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:AOFFset {param}')

	# noinspection PyTypeChecker
	def get_ao_units(self) -> enums.BtoOffsUnit:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:AOUNits \n
		Indicates the units used by the 'Aux Offset' parameter, see method RsSmbv.Source.Bb.Btooth.Econfiguration.Pconfiguration.
		aoffset \n
			:return: unit: U30| U300 U30: 30 µs U300: 300 µs
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:AOUNits?')
		return Conversions.str_to_scalar_enum(response, enums.BtoOffsUnit)

	def set_ao_units(self, unit: enums.BtoOffsUnit) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:AOUNits \n
		Indicates the units used by the 'Aux Offset' parameter, see method RsSmbv.Source.Bb.Btooth.Econfiguration.Pconfiguration.
		aoffset \n
			:param unit: U30| U300 U30: 30 µs U300: 300 µs
		"""
		param = Conversions.enum_scalar_to_str(unit, enums.BtoOffsUnit)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:AOUNits {param}')

	# noinspection PyTypeChecker
	def get_aphy(self) -> enums.PackFormat:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:APHY \n
		Specifies the physical layer used to transmit the auxiliary packet. \n
			:return: aphy: L1M| L2M| LCOD LE 1M, LE 2M, LE coded PHY
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:APHY?')
		return Conversions.str_to_scalar_enum(response, enums.PackFormat)

	def set_aphy(self, aphy: enums.PackFormat) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:APHY \n
		Specifies the physical layer used to transmit the auxiliary packet. \n
			:param aphy: L1M| L2M| LCOD LE 1M, LE 2M, LE coded PHY
		"""
		param = Conversions.enum_scalar_to_str(aphy, enums.PackFormat)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:APHY {param}')

	# noinspection PyTypeChecker
	class AsidStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Asid: List[str]: numeric
			- Bit_Count: int: integer Range: 4 to 4"""
		__meta_args_list = [
			ArgStruct('Asid', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Asid: List[str] = None
			self.Bit_Count: int = None

	def get_asid(self) -> AsidStruct:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:ASID \n
		Specifies the 'Advertising Set ID' in hexadecimal format to be signaled within an extended header. \n
			:return: structure: for return value, see the help for AsidStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:ASID?', self.__class__.AsidStruct())

	def set_asid(self, value: AsidStruct) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:ASID \n
		Specifies the 'Advertising Set ID' in hexadecimal format to be signaled within an extended header. \n
			:param value: see the help for AsidStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:ASID', value)

	# noinspection PyTypeChecker
	def get_atype(self) -> enums.BtoUlpAddrType:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:ATYPe \n
		Sets the address type in the payload of Bluetooth LE LL_PERIODIC_SYNC_IND packets. \n
			:return: atype: PUBLic| RANDom
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:ATYPe?')
		return Conversions.str_to_scalar_enum(response, enums.BtoUlpAddrType)

	def set_atype(self, atype: enums.BtoUlpAddrType) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:ATYPe \n
		Sets the address type in the payload of Bluetooth LE LL_PERIODIC_SYNC_IND packets. \n
			:param atype: PUBLic| RANDom
		"""
		param = Conversions.enum_scalar_to_str(atype, enums.BtoUlpAddrType)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:ATYPe {param}')

	# noinspection PyTypeChecker
	def get_caccuracy(self) -> enums.BtoClkAcc:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:CACCuracy \n
		Specifies the clock accuracy of the advertiser used between the packet containing this data and the auxiliary packet. \n
			:return: caccuracy: T500| T50 T500: 51 ppm to 500 ppm T50: 0 ppm to 50 ppm
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:CACCuracy?')
		return Conversions.str_to_scalar_enum(response, enums.BtoClkAcc)

	def set_caccuracy(self, caccuracy: enums.BtoClkAcc) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:CACCuracy \n
		Specifies the clock accuracy of the advertiser used between the packet containing this data and the auxiliary packet. \n
			:param caccuracy: T500| T50 T500: 51 ppm to 500 ppm T50: 0 ppm to 50 ppm
		"""
		param = Conversions.enum_scalar_to_str(caccuracy, enums.BtoClkAcc)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:CACCuracy {param}')

	def get_cecount(self) -> int:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:CECount \n
		Specifies the connection event count in the CtrData field of the LL_PERIODIC_SYNC_IND control data PDU. \n
			:return: ce_count: integer Range: 0 to 65535
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:CECount?')
		return Conversions.str_to_int(response)

	def set_cecount(self, ce_count: int) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:CECount \n
		Specifies the connection event count in the CtrData field of the LL_PERIODIC_SYNC_IND control data PDU. \n
			:param ce_count: integer Range: 0 to 65535
		"""
		param = Conversions.decimal_value_to_str(ce_count)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:CECount {param}')

	# noinspection PyTypeChecker
	class CidStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Cid: List[str]: numeric
			- Bit_Count: int: integer Range: 16 to 16"""
		__meta_args_list = [
			ArgStruct('Cid', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Cid: List[str] = None
			self.Bit_Count: int = None

	def get_cid(self) -> CidStruct:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:CID \n
		Sets the company identifier of the manufacturer of the Bluetooth Controller. A 16 bit value is set. Note: This parameter
		is relevant for data frame configuration and for the packet type LL_VERSION_IND. \n
			:return: structure: for return value, see the help for CidStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:CID?', self.__class__.CidStruct())

	def set_cid(self, value: CidStruct) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:CID \n
		Sets the company identifier of the manufacturer of the Bluetooth Controller. A 16 bit value is set. Note: This parameter
		is relevant for data frame configuration and for the packet type LL_VERSION_IND. \n
			:param value: see the help for CidStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:CID', value)

	def get_cinstant(self) -> int:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:CINStant \n
		Sets a connection instant for indicating the connection event at which the new connection parameters are taken in use. \n
			:return: cinstant: integer Range: 1 to depends on sequence length
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:CINStant?')
		return Conversions.str_to_int(response)

	def set_cinstant(self, cinstant: int) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:CINStant \n
		Sets a connection instant for indicating the connection event at which the new connection parameters are taken in use. \n
			:param cinstant: integer Range: 1 to depends on sequence length
		"""
		param = Conversions.decimal_value_to_str(cinstant)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:CINStant {param}')

	def get_cinterval(self) -> float:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:CINTerval \n
		Sets the time interval between the start points of two consecutive connection events for the packet type DATA and all
		CONTROL_DATA packet types. Command sets the values in ms. Query returns values in s. \n
			:return: cinterval: float Range: 7.5E-3 s to depends on oversampling , Unit: ms
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:CINTerval?')
		return Conversions.str_to_float(response)

	def set_cinterval(self, cinterval: float) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:CINTerval \n
		Sets the time interval between the start points of two consecutive connection events for the packet type DATA and all
		CONTROL_DATA packet types. Command sets the values in ms. Query returns values in s. \n
			:param cinterval: float Range: 7.5E-3 s to depends on oversampling , Unit: ms
		"""
		param = Conversions.decimal_value_to_str(cinterval)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:CINTerval {param}')

	# noinspection PyTypeChecker
	class CivalueStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Ci_Value: List[str]: numeric
			- Bit_Count: int: integer Range: 24 to 24"""
		__meta_args_list = [
			ArgStruct('Ci_Value', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Ci_Value: List[str] = None
			self.Bit_Count: int = None

	def get_civalue(self) -> CivalueStruct:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:CIValue \n
		Sets the initialization value for the CRC (Cyclic Redundancy Check, 24 bits) calculation. A packet has been received
		correctly, when it has passed the CRC check. \n
			:return: structure: for return value, see the help for CivalueStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:CIValue?', self.__class__.CivalueStruct())

	def set_civalue(self, value: CivalueStruct) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:CIValue \n
		Sets the initialization value for the CRC (Cyclic Redundancy Check, 24 bits) calculation. A packet has been received
		correctly, when it has passed the CRC check. \n
			:param value: see the help for CivalueStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:CIValue', value)

	def get_cpresent(self) -> bool:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:CPResent \n
		Activates the CTEInfo field in the header of Bluetooth LE data packets in the LE uncoded PHY. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:CPResent?')
		return Conversions.str_to_bool(response)

	def set_cpresent(self, state: bool) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:CPResent \n
		Activates the CTEInfo field in the header of Bluetooth LE data packets in the LE uncoded PHY. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:CPResent {param}')

	# noinspection PyTypeChecker
	def get_cselection(self) -> enums.BtoChSel:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:CSELection \n
		Specifies the algorithm of channel selection. \n
			:return: csrlection: CS1| CS2 Algorithm #1 or algorithm #2
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:CSELection?')
		return Conversions.str_to_scalar_enum(response, enums.BtoChSel)

	def set_cselection(self, csrlection: enums.BtoChSel) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:CSELection \n
		Specifies the algorithm of channel selection. \n
			:param csrlection: CS1| CS2 Algorithm #1 or algorithm #2
		"""
		param = Conversions.enum_scalar_to_str(csrlection, enums.BtoChSel)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:CSELection {param}')

	def get_ctime(self) -> float:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:CTIMe \n
		Sets the CTETime comprising the length of constant tone extension field of the Bluetooth LE PDU. \n
			:return: ctime: float Range: 16E-6 to 160E-6
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:CTIMe?')
		return Conversions.str_to_float(response)

	def set_ctime(self, ctime: float) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:CTIMe \n
		Sets the CTETime comprising the length of constant tone extension field of the Bluetooth LE PDU. \n
			:param ctime: float Range: 16E-6 to 160E-6
		"""
		param = Conversions.decimal_value_to_str(ctime)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:CTIMe {param}')

	# noinspection PyTypeChecker
	def get_ct_req(self) -> enums.BtoCteType:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:CTReq \n
		Sets the CTE type in the CTETypeReq field of the CtrData field of the LL_CTE_REQ PDU. \n
			:return: ct_req: AOD1| AOA| AOD2 AOA AoA Constant Tone Extension AOD1 AoD Constant Tone Extension with 1 µs time slots AOD2 AoD Constant Tone Extension with 2 µs time slots
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:CTReq?')
		return Conversions.str_to_scalar_enum(response, enums.BtoCteType)

	def set_ct_req(self, ct_req: enums.BtoCteType) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:CTReq \n
		Sets the CTE type in the CTETypeReq field of the CtrData field of the LL_CTE_REQ PDU. \n
			:param ct_req: AOD1| AOA| AOD2 AOA AoA Constant Tone Extension AOD1 AoD Constant Tone Extension with 1 µs time slots AOD2 AoD Constant Tone Extension with 2 µs time slots
		"""
		param = Conversions.enum_scalar_to_str(ct_req, enums.BtoCteType)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:CTReq {param}')

	# noinspection PyTypeChecker
	def get_ctype(self) -> enums.BtoCteType:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:CTYPe \n
		Sets the type of constant tone extension. The type specifies the CTE AoA/AoD method and for AoD the length of the
		switching and I/Q sampling slots. \n
			:return: ctype: AOD1| AOA| AOD2 AOA AoA Constant Tone Extension AOD1 AoD Constant Tone Extension with 1 µs time slots AOD2 AoD Constant Tone Extension with 2 µs time slots
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:CTYPe?')
		return Conversions.str_to_scalar_enum(response, enums.BtoCteType)

	def set_ctype(self, ctype: enums.BtoCteType) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:CTYPe \n
		Sets the type of constant tone extension. The type specifies the CTE AoA/AoD method and for AoD the length of the
		switching and I/Q sampling slots. \n
			:param ctype: AOD1| AOA| AOD2 AOA AoA Constant Tone Extension AOD1 AoD Constant Tone Extension with 1 µs time slots AOD2 AoD Constant Tone Extension with 2 µs time slots
		"""
		param = Conversions.enum_scalar_to_str(ctype, enums.BtoCteType)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:CTYPe {param}')

	def get_dlength(self) -> int:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:DLENgth \n
		Sets the payload data length in bytes. \n
			:return: dlength: integer Range: 0 to 255 (advertiser) or 251 (data)
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:DLENgth?')
		return Conversions.str_to_int(response)

	def set_dlength(self, dlength: int) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:DLENgth \n
		Sets the payload data length in bytes. \n
			:param dlength: integer Range: 0 to 255 (advertiser) or 251 (data)
		"""
		param = Conversions.decimal_value_to_str(dlength)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:DLENgth {param}')

	def get_dwhitening(self) -> bool:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:DWHitening \n
		Activates or deactivates the Data Whitening. Evenly distributed white noise is ideal for the transmission and real data
		can be forced to look similar to white noise with different methods called Data Whitening. Applied to the PDU and CRC
		fields of all packet types, whitening is used to avoid long equal seqeunces in the data bit stream. \n
			:return: dwhitening: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:DWHitening?')
		return Conversions.str_to_bool(response)

	def set_dwhitening(self, dwhitening: bool) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:DWHitening \n
		Activates or deactivates the Data Whitening. Evenly distributed white noise is ideal for the transmission and real data
		can be forced to look similar to white noise with different methods called Data Whitening. Applied to the PDU and CRC
		fields of all packet types, whitening is used to avoid long equal seqeunces in the data bit stream. \n
			:param dwhitening: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(dwhitening)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:DWHitening {param}')

	# noinspection PyTypeChecker
	class EcodeStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Ecode: List[str]: numeric
			- Bit_Count: int: integer Range: 8 to 8"""
		__meta_args_list = [
			ArgStruct('Ecode', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Ecode: List[str] = None
			self.Bit_Count: int = None

	def get_ecode(self) -> EcodeStruct:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:ECODe \n
		Sets the error code value to inform the remote device why the connection is about to be terminated in case of
		LL_TERMINATE_IND packet. On the other hand, this parameter for LL_REJECT_IND packet is used for the reason a request was
		rejected. A 8 bit value is set. Note: This parameter is relevant for data frame configuration and the packet type:
			INTRO_CMD_HELP: Selects the clock source: \n
			- LL_TERMINATE_IND
			- LL_REJECT_IND \n
			:return: structure: for return value, see the help for EcodeStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:ECODe?', self.__class__.EcodeStruct())

	def set_ecode(self, value: EcodeStruct) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:ECODe \n
		Sets the error code value to inform the remote device why the connection is about to be terminated in case of
		LL_TERMINATE_IND packet. On the other hand, this parameter for LL_REJECT_IND packet is used for the reason a request was
		rejected. A 8 bit value is set. Note: This parameter is relevant for data frame configuration and the packet type:
			INTRO_CMD_HELP: Selects the clock source: \n
			- LL_TERMINATE_IND
			- LL_REJECT_IND \n
			:param value: see the help for EcodeStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:ECODe', value)

	def get_ecounter(self) -> int:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:ECOunter \n
		Counts the AUX_SYNC_IND packets that the SyncInfo field describes. \n
			:return: ecounter: integer Range: 0 to 65535
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:ECOunter?')
		return Conversions.str_to_int(response)

	def set_ecounter(self, ecounter: int) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:ECOunter \n
		Counts the AUX_SYNC_IND packets that the SyncInfo field describes. \n
			:param ecounter: integer Range: 0 to 65535
		"""
		param = Conversions.decimal_value_to_str(ecounter)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:ECOunter {param}')

	# noinspection PyTypeChecker
	class EdiversifierStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Ediversifier: List[str]: numeric
			- Bit_Count: int: integer Range: 16 to 16"""
		__meta_args_list = [
			ArgStruct('Ediversifier', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Ediversifier: List[str] = None
			self.Bit_Count: int = None

	def get_ediversifier(self) -> EdiversifierStruct:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:EDIVersifier \n
		Sets the encrypted diversifier of the master for device identification. The parameter is an initialization vector
		provided by the host in the HCI_ULP_Start_Encryption command. \n
			:return: structure: for return value, see the help for EdiversifierStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:EDIVersifier?', self.__class__.EdiversifierStruct())

	def set_ediversifier(self, value: EdiversifierStruct) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:EDIVersifier \n
		Sets the encrypted diversifier of the master for device identification. The parameter is an initialization vector
		provided by the host in the HCI_ULP_Start_Encryption command. \n
			:param value: see the help for EdiversifierStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:EDIVersifier', value)

	def get_fs_length(self) -> int:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:FSLength \n
		Enables that the feature set length is indicated. \n
			:return: fs_length: integer Range: 1 to 26
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:FSLength?')
		return Conversions.str_to_int(response)

	def set_fs_length(self, fs_length: int) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:FSLength \n
		Enables that the feature set length is indicated. \n
			:param fs_length: integer Range: 1 to 26
		"""
		param = Conversions.decimal_value_to_str(fs_length)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:FSLength {param}')

	def get_hlength(self) -> int:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:HLENgth \n
		(for data event and advertising frame configuration with the packet type CONNECT_IND) Sets the difference from the
		current channel to the next channel. The master and slave devices determine the data channel in use for every connection
		event from the channel map. Hop_length is set for the LL connection and communicated in the CONNECT_IND and
		LL_CHANNEL_MAP_IND packets. \n
			:return: hlength: integer Range: 5 to 16
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:HLENgth?')
		return Conversions.str_to_int(response)

	def set_hlength(self, hlength: int) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:HLENgth \n
		(for data event and advertising frame configuration with the packet type CONNECT_IND) Sets the difference from the
		current channel to the next channel. The master and slave devices determine the data channel in use for every connection
		event from the channel map. Hop_length is set for the LL connection and communicated in the CONNECT_IND and
		LL_CHANNEL_MAP_IND packets. \n
			:param hlength: integer Range: 5 to 16
		"""
		param = Conversions.decimal_value_to_str(hlength)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:HLENgth {param}')

	# noinspection PyTypeChecker
	class IcAssignedStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Ic_Assigned: List[str]: No parameter help available
			- Bit_Count: int: integer Range: 24 to 24"""
		__meta_args_list = [
			ArgStruct('Ic_Assigned', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Ic_Assigned: List[str] = None
			self.Bit_Count: int = None

	def get_ic_assigned(self) -> IcAssignedStruct:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:ICASsigned \n
		Sets the advertiser´s device address. For advertising channel packets, the format of the device address differs,
		depending on the selected address type.
			INTRO_CMD_HELP: Selects the clock source: \n
			- 'Public Address Types' The public address is given from the registration authority IEEE and is composed of:
			Table Header:  \n
			- LSB: 24 bits = company_assigned
			- MSB: 24 bits = company_id
			- 'Random Address Type' is a 48-bits random static device address.
			- 'Private Address Type' A private address is optional and composed of:
			Table Header:  \n
			- LSB: 24 bits = hash
			- MSB: 24 bits = random \n
			:return: structure: for return value, see the help for IcAssignedStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:ICASsigned?', self.__class__.IcAssignedStruct())

	def set_ic_assigned(self, value: IcAssignedStruct) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:ICASsigned \n
		Sets the advertiser´s device address. For advertising channel packets, the format of the device address differs,
		depending on the selected address type.
			INTRO_CMD_HELP: Selects the clock source: \n
			- 'Public Address Types' The public address is given from the registration authority IEEE and is composed of:
			Table Header:  \n
			- LSB: 24 bits = company_assigned
			- MSB: 24 bits = company_id
			- 'Random Address Type' is a 48-bits random static device address.
			- 'Private Address Type' A private address is optional and composed of:
			Table Header:  \n
			- LSB: 24 bits = hash
			- MSB: 24 bits = random \n
			:param value: see the help for IcAssignedStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:ICASsigned', value)

	# noinspection PyTypeChecker
	class IcidStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Icid: List[str]: numeric
			- Bit_Count: int: integer Range: 24 to 24"""
		__meta_args_list = [
			ArgStruct('Icid', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Icid: List[str] = None
			self.Bit_Count: int = None

	def get_icid(self) -> IcidStruct:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:ICID \n
		Sets the advertiser´s device address. For advertising channel packets, the format of the device address differs,
		depending on the selected address type.
			INTRO_CMD_HELP: Selects the clock source: \n
			- 'Public Address Types' The public address is given from the registration authority IEEE and is composed of:
			Table Header:  \n
			- LSB: 24 bits = company_assigned
			- MSB: 24 bits = company_id
			- 'Random Address Type' is a 48-bits random static device address.
			- 'Private Address Type' A private address is optional and composed of:
			Table Header:  \n
			- LSB: 24 bits = hash
			- MSB: 24 bits = random \n
			:return: structure: for return value, see the help for IcidStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:ICID?', self.__class__.IcidStruct())

	def set_icid(self, value: IcidStruct) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:ICID \n
		Sets the advertiser´s device address. For advertising channel packets, the format of the device address differs,
		depending on the selected address type.
			INTRO_CMD_HELP: Selects the clock source: \n
			- 'Public Address Types' The public address is given from the registration authority IEEE and is composed of:
			Table Header:  \n
			- LSB: 24 bits = company_assigned
			- MSB: 24 bits = company_id
			- 'Random Address Type' is a 48-bits random static device address.
			- 'Private Address Type' A private address is optional and composed of:
			Table Header:  \n
			- LSB: 24 bits = hash
			- MSB: 24 bits = random \n
			:param value: see the help for IcidStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:ICID', value)

	# noinspection PyTypeChecker
	class IdStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Idn: List[str]: numeric
			- Bit_Count: int: integer Range: 16 to 16"""
		__meta_args_list = [
			ArgStruct('Idn', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Idn: List[str] = None
			self.Bit_Count: int = None

	def get_id(self) -> IdStruct:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:ID \n
		Specifies the ID in the CtrData field of the LL_PERIODIC_SYNC_IND PDU. \n
			:return: structure: for return value, see the help for IdStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:ID?', self.__class__.IdStruct())

	def set_id(self, value: IdStruct) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:ID \n
		Specifies the ID in the CtrData field of the LL_PERIODIC_SYNC_IND PDU. \n
			:param value: see the help for IdStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:ID', value)

	# noinspection PyTypeChecker
	class IlapStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Lap: List[str]: numeric
			- Bit_Count: int: integer Range: 24 to 24"""
		__meta_args_list = [
			ArgStruct('Lap', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Lap: List[str] = None
			self.Bit_Count: int = None

	def get_ilap(self) -> IlapStruct:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:ILAP \n
		Sets the lower address part (LAP) of Bluetooth device address. Commands for the advertising ..:ALAP, initiating ..:ILAP,
		scanning ..:SLAP PDUs of advertising channel type are provided. In addition, a command is provided for scanner’s or
		initiator’s target device address to which the advertisement is directed ..:TLAP. \n
			:return: structure: for return value, see the help for IlapStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:ILAP?', self.__class__.IlapStruct())

	def set_ilap(self, value: IlapStruct) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:ILAP \n
		Sets the lower address part (LAP) of Bluetooth device address. Commands for the advertising ..:ALAP, initiating ..:ILAP,
		scanning ..:SLAP PDUs of advertising channel type are provided. In addition, a command is provided for scanner’s or
		initiator’s target device address to which the advertisement is directed ..:TLAP. \n
			:param value: see the help for IlapStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:ILAP', value)

	# noinspection PyTypeChecker
	class InuapStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Nap_Uap: List[str]: numeric
			- Bit_Count: int: integer Range: 24 to 24"""
		__meta_args_list = [
			ArgStruct('Nap_Uap', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Nap_Uap: List[str] = None
			self.Bit_Count: int = None

	def get_inuap(self) -> InuapStruct:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:INUap \n
		Sets the non-significant address part (NAP) and upper address part (UAP) of Bluetooth device address. Commands for the
		advertising ..:ANUap, initiating ..:INUap, and scanning ..:SNUap PDUs of advertising channel type are provided.
		In addition, a command is provided for scanner’s or initiator’s target device address to which the advertisement is
		directed ..:TNUap. \n
			:return: structure: for return value, see the help for InuapStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:INUap?', self.__class__.InuapStruct())

	def set_inuap(self, value: InuapStruct) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:INUap \n
		Sets the non-significant address part (NAP) and upper address part (UAP) of Bluetooth device address. Commands for the
		advertising ..:ANUap, initiating ..:INUap, and scanning ..:SNUap PDUs of advertising channel type are provided.
		In addition, a command is provided for scanner’s or initiator’s target device address to which the advertisement is
		directed ..:TNUap. \n
			:param value: see the help for InuapStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:INUap', value)

	def get_lc_timeout(self) -> float:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:LCTimeout \n
		Defines the maximum time between two correctly received Bluetooth LE packets in the LL connection before the connection
		is considered lost for the packet type CONNECT_IND. Command sets the values in ms. Query returns values in s. \n
			:return: lc_timeout: float Range: 100E-3 s to 32000E-3 s , Unit: ms
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:LCTimeout?')
		return Conversions.str_to_float(response)

	def set_lc_timeout(self, lc_timeout: float) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:LCTimeout \n
		Defines the maximum time between two correctly received Bluetooth LE packets in the LL connection before the connection
		is considered lost for the packet type CONNECT_IND. Command sets the values in ms. Query returns values in s. \n
			:param lc_timeout: float Range: 100E-3 s to 32000E-3 s , Unit: ms
		"""
		param = Conversions.decimal_value_to_str(lc_timeout)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:LCTimeout {param}')

	def get_lpe_counter(self) -> int:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:LPECounter \n
		Specifies the lastPaEventCounter field in the CtrData field of the LL_PERIODIC_SYNC_IND PDU. \n
			:return: lpecounter: integer Range: 0 to 65535
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:LPECounter?')
		return Conversions.str_to_int(response)

	def set_lpe_counter(self, lpecounter: int) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:LPECounter \n
		Specifies the lastPaEventCounter field in the CtrData field of the LL_PERIODIC_SYNC_IND PDU. \n
			:param lpecounter: integer Range: 0 to 65535
		"""
		param = Conversions.decimal_value_to_str(lpecounter)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:LPECounter {param}')

	def get_mcl_req(self) -> float:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:MCLReq \n
		Specifies the minimum CTE length in the CtrData field of the LL_CTE_Req PDU. \n
			:return: mcl_req: float Range: 16E-6 to 160E-6
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:MCLReq?')
		return Conversions.str_to_float(response)

	def set_mcl_req(self, mcl_req: float) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:MCLReq \n
		Specifies the minimum CTE length in the CtrData field of the LL_CTE_Req PDU. \n
			:param mcl_req: float Range: 16E-6 to 160E-6
		"""
		param = Conversions.decimal_value_to_str(mcl_req)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:MCLReq {param}')

	# noinspection PyTypeChecker
	class MiVectorStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Mi_Vector: List[str]: No parameter help available
			- Bit_Count: int: integer Range: 32 to 32"""
		__meta_args_list = [
			ArgStruct('Mi_Vector', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Mi_Vector: List[str] = None
			self.Bit_Count: int = None

	def get_mi_vector(self) -> MiVectorStruct:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:MIVector \n
		Sets the master's or the slave's portion of the initialization vector (IVm/IVs) . \n
			:return: structure: for return value, see the help for MiVectorStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:MIVector?', self.__class__.MiVectorStruct())

	def set_mi_vector(self, value: MiVectorStruct) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:MIVector \n
		Sets the master's or the slave's portion of the initialization vector (IVm/IVs) . \n
			:param value: see the help for MiVectorStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:MIVector', value)

	def get_mn_interval(self) -> float:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:MNINterval \n
		Specifies the minimum allowed connection interval. Command sets the values in ms. Query returns values in s. \n
			:return: mn_interval: float Range: 7.5E-3 s to depending on Max. Interval
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:MNINterval?')
		return Conversions.str_to_float(response)

	def set_mn_interval(self, mn_interval: float) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:MNINterval \n
		Specifies the minimum allowed connection interval. Command sets the values in ms. Query returns values in s. \n
			:param mn_interval: float Range: 7.5E-3 s to depending on Max. Interval
		"""
		param = Conversions.decimal_value_to_str(mn_interval)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:MNINterval {param}')

	def get_mr_octets(self) -> int:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:MROCtets \n
		Specifies the maximum allowed payload length of a packet to be received (..:MROCtets) or transmitted (..:MTOCtets) .
		Information is signaled via LL_LENGTH_REQ and LL_LENGTH_RSP. \n
			:return: mr_octets: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:MROCtets?')
		return Conversions.str_to_int(response)

	def set_mr_octets(self, mr_octets: int) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:MROCtets \n
		Specifies the maximum allowed payload length of a packet to be received (..:MROCtets) or transmitted (..:MTOCtets) .
		Information is signaled via LL_LENGTH_REQ and LL_LENGTH_RSP. \n
			:param mr_octets: integer Range: 27 to 251
		"""
		param = Conversions.decimal_value_to_str(mr_octets)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:MROCtets {param}')

	def get_mr_time(self) -> float:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:MRTime \n
		Specifies the maximum allowed time to receive (..:MRTime) or transmit (..:MTTime) a packet. Information is signaled via
		LL_LENGTH_REQ and LL_LENGTH_RSP. \n
			:return: mrtime: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:MRTime?')
		return Conversions.str_to_float(response)

	def set_mr_time(self, mrtime: float) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:MRTime \n
		Specifies the maximum allowed time to receive (..:MRTime) or transmit (..:MTTime) a packet. Information is signaled via
		LL_LENGTH_REQ and LL_LENGTH_RSP. \n
			:param mrtime: float Range: 0.328E-3 to 17.04E-3
		"""
		param = Conversions.decimal_value_to_str(mrtime)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:MRTime {param}')

	# noinspection PyTypeChecker
	class MskdStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Mskd: List[str]: No parameter help available
			- Bit_Count: int: integer Range: 64 to 64"""
		__meta_args_list = [
			ArgStruct('Mskd', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Mskd: List[str] = None
			self.Bit_Count: int = None

	def get_mskd(self) -> MskdStruct:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:MSKD \n
		Sets the master's or the slave's portion of the session key diversifier (SKDm/SKDs) . \n
			:return: structure: for return value, see the help for MskdStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:MSKD?', self.__class__.MskdStruct())

	def set_mskd(self, value: MskdStruct) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:MSKD \n
		Sets the master's or the slave's portion of the session key diversifier (SKDm/SKDs) . \n
			:param value: see the help for MskdStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:MSKD', value)

	def get_mt_octets(self) -> int:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:MTOCtets \n
		Specifies the maximum allowed payload length of a packet to be received (..:MROCtets) or transmitted (..:MTOCtets) .
		Information is signaled via LL_LENGTH_REQ and LL_LENGTH_RSP. \n
			:return: mt_octets: integer Range: 27 to 251
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:MTOCtets?')
		return Conversions.str_to_int(response)

	def set_mt_octets(self, mt_octets: int) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:MTOCtets \n
		Specifies the maximum allowed payload length of a packet to be received (..:MROCtets) or transmitted (..:MTOCtets) .
		Information is signaled via LL_LENGTH_REQ and LL_LENGTH_RSP. \n
			:param mt_octets: integer Range: 27 to 251
		"""
		param = Conversions.decimal_value_to_str(mt_octets)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:MTOCtets {param}')

	def get_mt_time(self) -> float:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:MTTime \n
		Specifies the maximum allowed time to receive (..:MRTime) or transmit (..:MTTime) a packet. Information is signaled via
		LL_LENGTH_REQ and LL_LENGTH_RSP. \n
			:return: mttime: float Range: 0.328E-3 to 17.04E-3
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:MTTime?')
		return Conversions.str_to_float(response)

	def set_mt_time(self, mttime: float) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:MTTime \n
		Specifies the maximum allowed time to receive (..:MRTime) or transmit (..:MTTime) a packet. Information is signaled via
		LL_LENGTH_REQ and LL_LENGTH_RSP. \n
			:param mttime: float Range: 0.328E-3 to 17.04E-3
		"""
		param = Conversions.decimal_value_to_str(mttime)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:MTTime {param}')

	def get_mu_channels(self) -> int:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:MUCHannels \n
		Specifies the minimum number of channels to be used on the specified PHYs, see method RsSmbv.Source.Bb.Btooth.
		Econfiguration.Pconfiguration.Phys.L1M.State.set etc. \n
			:return: muchannels: integer Range: 2 to 37
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:MUCHannels?')
		return Conversions.str_to_int(response)

	def set_mu_channels(self, muchannels: int) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:MUCHannels \n
		Specifies the minimum number of channels to be used on the specified PHYs, see method RsSmbv.Source.Bb.Btooth.
		Econfiguration.Pconfiguration.Phys.L1M.State.set etc. \n
			:param muchannels: integer Range: 2 to 37
		"""
		param = Conversions.decimal_value_to_str(muchannels)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:MUCHannels {param}')

	def get_mx_interval(self) -> float:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:MXINterval \n
		Specifies the maximum allowed connection interval. Command sets the values in ms. Query returns values in s. \n
			:return: minterval: float Range: 7.5E-3 s to 4000E-3 s
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:MXINterval?')
		return Conversions.str_to_float(response)

	def set_mx_interval(self, minterval: float) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:MXINterval \n
		Specifies the maximum allowed connection interval. Command sets the values in ms. Query returns values in s. \n
			:param minterval: float Range: 7.5E-3 s to 4000E-3 s
		"""
		param = Conversions.decimal_value_to_str(minterval)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:MXINterval {param}')

	def get_nc_interval(self) -> float:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:NCINterval \n
		Sets the time interval new connection events for the packet types CONNECT_IND and LL_CONNECTION_UPDATE_IND. Command sets
		the values in ms. Query returns values in s. \n
			:return: nc_interval: float Range: 7.5E-3 s to depends on oversampling , Unit: ms
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:NCINterval?')
		return Conversions.str_to_float(response)

	def set_nc_interval(self, nc_interval: float) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:NCINterval \n
		Sets the time interval new connection events for the packet types CONNECT_IND and LL_CONNECTION_UPDATE_IND. Command sets
		the values in ms. Query returns values in s. \n
			:param nc_interval: float Range: 7.5E-3 s to depends on oversampling , Unit: ms
		"""
		param = Conversions.decimal_value_to_str(nc_interval)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:NCINterval {param}')

	def get_nlc_timeout(self) -> float:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:NLCTimeout \n
		Defines the maximum time between two correctly received Bluetooth LE packets in the LL connection before the connection
		is considered lost only for the packet type LL_CONNECTION_UPDATE_IND. Command sets the values in ms. Query returns values
		in s. \n
			:return: nlc_timeout: float Range: 100E-3 s to 32000E-3 s , Unit: ms
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:NLCTimeout?')
		return Conversions.str_to_float(response)

	def set_nlc_timeout(self, nlc_timeout: float) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:NLCTimeout \n
		Defines the maximum time between two correctly received Bluetooth LE packets in the LL connection before the connection
		is considered lost only for the packet type LL_CONNECTION_UPDATE_IND. Command sets the values in ms. Query returns values
		in s. \n
			:param nlc_timeout: float Range: 100E-3 s to 32000E-3 s , Unit: ms
		"""
		param = Conversions.decimal_value_to_str(nlc_timeout)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:NLCTimeout {param}')

	def get_ns_latency(self) -> int:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:NSLatency \n
		(for data event and advertising frame configuration with the packet type LL_CONNECTION_UPDATE_IND) Sets the number of
		consecutive connection events the slave can ignore for asymmetric link layer connections. \n
			:return: ns_latency: integer Range: 0 to depends on LL connection timeout and connection event interval
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:NSLatency?')
		return Conversions.str_to_int(response)

	def set_ns_latency(self, ns_latency: int) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:NSLatency \n
		(for data event and advertising frame configuration with the packet type LL_CONNECTION_UPDATE_IND) Sets the number of
		consecutive connection events the slave can ignore for asymmetric link layer connections. \n
			:param ns_latency: integer Range: 0 to depends on LL connection timeout and connection event interval
		"""
		param = Conversions.decimal_value_to_str(ns_latency)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:NSLatency {param}')

	def get_nsvalue(self) -> int:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:NSValue \n
		Sets the start value of the next expected packet from the same device in the LL connection ('N'ext'E'xpected
		'S'equence'N'umber) . This parameter can be set in the first event. From the second event this field is not indicated. \n
			:return: ns_value: integer Range: 0 to 1
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:NSValue?')
		return Conversions.str_to_int(response)

	def set_nsvalue(self, ns_value: int) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:NSValue \n
		Sets the start value of the next expected packet from the same device in the LL connection ('N'ext'E'xpected
		'S'equence'N'umber) . This parameter can be set in the first event. From the second event this field is not indicated. \n
			:param ns_value: integer Range: 0 to 1
		"""
		param = Conversions.decimal_value_to_str(ns_value)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:NSValue {param}')

	def get_nw_offset(self) -> float:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:NWOFfset \n
		Sets the start point of the transmit window for data event and advertising frame configuration with the packet type
		LL_CONNECTION_UPDATE_IND. Command sets the values in ms. Query returns values in s. \n
			:return: nw_offset: float Range: 0 s to depends on connection event interval , Unit: ms
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:NWOFfset?')
		return Conversions.str_to_float(response)

	def set_nw_offset(self, nw_offset: float) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:NWOFfset \n
		Sets the start point of the transmit window for data event and advertising frame configuration with the packet type
		LL_CONNECTION_UPDATE_IND. Command sets the values in ms. Query returns values in s. \n
			:param nw_offset: float Range: 0 s to depends on connection event interval , Unit: ms
		"""
		param = Conversions.decimal_value_to_str(nw_offset)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:NWOFfset {param}')

	def get_nw_size(self) -> float:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:NWSize \n
		Sets the size of the transmit window, regarding to the start point for data event and advertising frame configuration
		with the packet type LL_CONNECTION_UPDATE_IND. \n
			:return: nw_size: float Range: 1.25E-3 to depends on connection event interval
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:NWSize?')
		return Conversions.str_to_float(response)

	def set_nw_size(self, nw_size: float) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:NWSize \n
		Sets the size of the transmit window, regarding to the start point for data event and advertising frame configuration
		with the packet type LL_CONNECTION_UPDATE_IND. \n
			:param nw_size: float Range: 1.25E-3 to depends on connection event interval
		"""
		param = Conversions.decimal_value_to_str(nw_size)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:NWSize {param}')

	def get_oadjust(self) -> bool:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:OADJust \n
		Adjusts the 'Sync Packet Offset' automatically to the next value, which is a multiple of the ''Offset Units'. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:OADJust?')
		return Conversions.str_to_bool(response)

	def set_oadjust(self, state: bool) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:OADJust \n
		Adjusts the 'Sync Packet Offset' automatically to the next value, which is a multiple of the ''Offset Units'. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:OADJust {param}')

	def get_pa_interval(self) -> float:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:PAINterval \n
		Sets the time interval between the start of two AUX_SYNC_IND PDUs from the same advertising set. Command sets the values
		in ms. Query returns values in s. \n
			:return: interval: float Range: 7.5E-3 s to depending on oversampling , Unit: ms
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:PAINterval?')
		return Conversions.str_to_float(response)

	def set_pa_interval(self, interval: float) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:PAINterval \n
		Sets the time interval between the start of two AUX_SYNC_IND PDUs from the same advertising set. Command sets the values
		in ms. Query returns values in s. \n
			:param interval: float Range: 7.5E-3 s to depending on oversampling , Unit: ms
		"""
		param = Conversions.decimal_value_to_str(interval)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:PAINterval {param}')

	def get_pperiodicity(self) -> float:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:PPERiodicity \n
		Specifies a value the connection interval is preferred to be a multiple of. \n
			:return: pp_eriodicity: float Range: 0 to depends on Max. Interval
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:PPERiodicity?')
		return Conversions.str_to_float(response)

	def set_pperiodicity(self, pp_eriodicity: float) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:PPERiodicity \n
		Specifies a value the connection interval is preferred to be a multiple of. \n
			:param pp_eriodicity: float Range: 0 to depends on Max. Interval
		"""
		param = Conversions.decimal_value_to_str(pp_eriodicity)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:PPERiodicity {param}')

	# noinspection PyTypeChecker
	def get_ratype(self) -> enums.BtoUlpAddrType:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:RATYpe \n
		Selects the address type of the controller device. Depending on the Bluetooth controller role either Tx or Rx or both
		address types are assigned. Subdivided into private and random, a Bluetooth LE device address consits of 48 bits.
		The format of the device address differs depending on the selected address type. \n
			:return: ra_type: PUBLic| RANDom PUBlic Allocates a unique 48 bit address to each Bluetooth LE device. The public address is given from the registration authority IEEE. RANDom Allocates a 48-bit address to each Bluetooth LE device. A random address is optional.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:RATYpe?')
		return Conversions.str_to_scalar_enum(response, enums.BtoUlpAddrType)

	def set_ratype(self, ra_type: enums.BtoUlpAddrType) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:RATYpe \n
		Selects the address type of the controller device. Depending on the Bluetooth controller role either Tx or Rx or both
		address types are assigned. Subdivided into private and random, a Bluetooth LE device address consits of 48 bits.
		The format of the device address differs depending on the selected address type. \n
			:param ra_type: PUBLic| RANDom PUBlic Allocates a unique 48 bit address to each Bluetooth LE device. The public address is given from the registration authority IEEE. RANDom Allocates a 48-bit address to each Bluetooth LE device. A random address is optional.
		"""
		param = Conversions.enum_scalar_to_str(ra_type, enums.BtoUlpAddrType)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:RATYpe {param}')

	def get_rce_count(self) -> int:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:RCECount \n
		Specifies the ReferenceConnEventCount field of LL_CONNECTION_PARAM_REQ. \n
			:return: rce_count: integer Range: 0 to 65535
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:RCECount?')
		return Conversions.str_to_int(response)

	def set_rce_count(self, rce_count: int) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:RCECount \n
		Specifies the ReferenceConnEventCount field of LL_CONNECTION_PARAM_REQ. \n
			:param rce_count: integer Range: 0 to 65535
		"""
		param = Conversions.decimal_value_to_str(rce_count)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:RCECount {param}')

	# noinspection PyTypeChecker
	class RopcodeStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Rop_Code: List[str]: numeric
			- Bit_Count: int: integer Range: 8 to 8"""
		__meta_args_list = [
			ArgStruct('Rop_Code', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Rop_Code: List[str] = None
			self.Bit_Count: int = None

	def get_ropcode(self) -> RopcodeStruct:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:ROPCode \n
		Specifies the Opcode of rejected LL control PDU. information is signaled via LL_REJECT_EXT_IND. \n
			:return: structure: for return value, see the help for RopcodeStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:ROPCode?', self.__class__.RopcodeStruct())

	def set_ropcode(self, value: RopcodeStruct) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:ROPCode \n
		Specifies the Opcode of rejected LL control PDU. information is signaled via LL_REJECT_EXT_IND. \n
			:param value: see the help for RopcodeStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:ROPCode', value)

	# noinspection PyTypeChecker
	class RvectorStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Rvector: List[str]: numeric
			- Bit_Count: int: integer Range: 64 to 64"""
		__meta_args_list = [
			ArgStruct('Rvector', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Rvector: List[str] = None
			self.Bit_Count: int = None

	def get_rvector(self) -> RvectorStruct:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:RVECtor \n
		Sets the random vector of the master for device identification.The parameter is an initialization vector provided by the
		Host in the HCI_ULP_Start_Encryption command. \n
			:return: structure: for return value, see the help for RvectorStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:RVECtor?', self.__class__.RvectorStruct())

	def set_rvector(self, value: RvectorStruct) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:RVECtor \n
		Sets the random vector of the master for device identification.The parameter is an initialization vector provided by the
		Host in the HCI_ULP_Start_Encryption command. \n
			:param value: see the help for RvectorStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:RVECtor', value)

	# noinspection PyTypeChecker
	def get_sc_accuracy(self) -> enums.BtoSlpClckAccrcy:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:SCACcuracy \n
		Defines the master´s clock accuracy with specified encoding. This parameter is used by the slave to determine required
		listening windows in the LL connection. It is a controller design parameter known by the Controller. \n
			:return: sc_accuracy: SCA0| SCA1| SCA2| SCA3| SCA4| SCA5| SCA6| SCA7
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:SCACcuracy?')
		return Conversions.str_to_scalar_enum(response, enums.BtoSlpClckAccrcy)

	def set_sc_accuracy(self, sc_accuracy: enums.BtoSlpClckAccrcy) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:SCACcuracy \n
		Defines the master´s clock accuracy with specified encoding. This parameter is used by the slave to determine required
		listening windows in the LL connection. It is a controller design parameter known by the Controller. \n
			:param sc_accuracy: SCA0| SCA1| SCA2| SCA3| SCA4| SCA5| SCA6| SCA7
		"""
		param = Conversions.enum_scalar_to_str(sc_accuracy, enums.BtoSlpClckAccrcy)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:SCACcuracy {param}')

	# noinspection PyTypeChecker
	class ScAssignedStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Sc_Assigned: List[str]: No parameter help available
			- Bit_Count: int: integer Range: 24 to 24"""
		__meta_args_list = [
			ArgStruct('Sc_Assigned', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Sc_Assigned: List[str] = None
			self.Bit_Count: int = None

	def get_sc_assigned(self) -> ScAssignedStruct:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:SCASsigned \n
		Sets the advertiser´s device address. For advertising channel packets, the format of the device address differs,
		depending on the selected address type.
			INTRO_CMD_HELP: Selects the clock source: \n
			- 'Public Address Types' The public address is given from the registration authority IEEE and is composed of:
			Table Header:  \n
			- LSB: 24 bits = company_assigned
			- MSB: 24 bits = company_id
			- 'Random Address Type' is a 48-bits random static device address.
			- 'Private Address Type' A private address is optional and composed of:
			Table Header:  \n
			- LSB: 24 bits = hash
			- MSB: 24 bits = random \n
			:return: structure: for return value, see the help for ScAssignedStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:SCASsigned?', self.__class__.ScAssignedStruct())

	def set_sc_assigned(self, value: ScAssignedStruct) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:SCASsigned \n
		Sets the advertiser´s device address. For advertising channel packets, the format of the device address differs,
		depending on the selected address type.
			INTRO_CMD_HELP: Selects the clock source: \n
			- 'Public Address Types' The public address is given from the registration authority IEEE and is composed of:
			Table Header:  \n
			- LSB: 24 bits = company_assigned
			- MSB: 24 bits = company_id
			- 'Random Address Type' is a 48-bits random static device address.
			- 'Private Address Type' A private address is optional and composed of:
			Table Header:  \n
			- LSB: 24 bits = hash
			- MSB: 24 bits = random \n
			:param value: see the help for ScAssignedStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:SCASsigned', value)

	def get_sce_counter(self) -> int:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:SCECounter \n
		No command help available \n
			:return: sce_counter: integer Range: 0 to 65535
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:SCECounter?')
		return Conversions.str_to_int(response)

	def set_sce_counter(self, sce_counter: int) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:SCECounter \n
		No command help available \n
			:param sce_counter: integer Range: 0 to 65535
		"""
		param = Conversions.decimal_value_to_str(sce_counter)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:SCECounter {param}')

	# noinspection PyTypeChecker
	class ScidStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Scid: List[str]: No parameter help available
			- Bit_Count: int: integer Range: 24 to 24"""
		__meta_args_list = [
			ArgStruct('Scid', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Scid: List[str] = None
			self.Bit_Count: int = None

	def get_scid(self) -> ScidStruct:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:SCID \n
		Sets the advertiser´s device address. For advertising channel packets, the format of the device address differs,
		depending on the selected address type.
			INTRO_CMD_HELP: Selects the clock source: \n
			- 'Public Address Types' The public address is given from the registration authority IEEE and is composed of:
			Table Header:  \n
			- LSB: 24 bits = company_assigned
			- MSB: 24 bits = company_id
			- 'Random Address Type' is a 48-bits random static device address.
			- 'Private Address Type' A private address is optional and composed of:
			Table Header:  \n
			- LSB: 24 bits = hash
			- MSB: 24 bits = random \n
			:return: structure: for return value, see the help for ScidStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:SCID?', self.__class__.ScidStruct())

	def set_scid(self, value: ScidStruct) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:SCID \n
		Sets the advertiser´s device address. For advertising channel packets, the format of the device address differs,
		depending on the selected address type.
			INTRO_CMD_HELP: Selects the clock source: \n
			- 'Public Address Types' The public address is given from the registration authority IEEE and is composed of:
			Table Header:  \n
			- LSB: 24 bits = company_assigned
			- MSB: 24 bits = company_id
			- 'Random Address Type' is a 48-bits random static device address.
			- 'Private Address Type' A private address is optional and composed of:
			Table Header:  \n
			- LSB: 24 bits = hash
			- MSB: 24 bits = random \n
			:param value: see the help for ScidStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:SCID', value)

	# noinspection PyTypeChecker
	class SidStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Sid: List[str]: numeric
			- Bit_Count: int: integer Range: 4 to 4"""
		__meta_args_list = [
			ArgStruct('Sid', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Sid: List[str] = None
			self.Bit_Count: int = None

	def get_sid(self) -> SidStruct:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:SID \n
		Specifies the SID in the CtrData field of the LL_PERIODIC_SYNC_IND. \n
			:return: structure: for return value, see the help for SidStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:SID?', self.__class__.SidStruct())

	def set_sid(self, value: SidStruct) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:SID \n
		Specifies the SID in the CtrData field of the LL_PERIODIC_SYNC_IND. \n
			:param value: see the help for SidStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:SID', value)

	# noinspection PyTypeChecker
	class SivectorStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Si_Vector: List[str]: numeric
			- Bit_Count: int: integer Range: 32 to 32"""
		__meta_args_list = [
			ArgStruct('Si_Vector', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Si_Vector: List[str] = None
			self.Bit_Count: int = None

	def get_sivector(self) -> SivectorStruct:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:SIVector \n
		Sets the master's or the slave's portion of the initialization vector (IVm/IVs) . \n
			:return: structure: for return value, see the help for SivectorStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:SIVector?', self.__class__.SivectorStruct())

	def set_sivector(self, value: SivectorStruct) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:SIVector \n
		Sets the master's or the slave's portion of the initialization vector (IVm/IVs) . \n
			:param value: see the help for SivectorStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:SIVector', value)

	# noinspection PyTypeChecker
	class SlapStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Lap: List[str]: numeric
			- Bit_Count: int: integer Range: 24 to 24"""
		__meta_args_list = [
			ArgStruct('Lap', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Lap: List[str] = None
			self.Bit_Count: int = None

	def get_slap(self) -> SlapStruct:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:SLAP \n
		Sets the lower address part (LAP) of Bluetooth device address. Commands for the advertising ..:ALAP, initiating ..:ILAP,
		scanning ..:SLAP PDUs of advertising channel type are provided. In addition, a command is provided for scanner’s or
		initiator’s target device address to which the advertisement is directed ..:TLAP. \n
			:return: structure: for return value, see the help for SlapStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:SLAP?', self.__class__.SlapStruct())

	def set_slap(self, value: SlapStruct) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:SLAP \n
		Sets the lower address part (LAP) of Bluetooth device address. Commands for the advertising ..:ALAP, initiating ..:ILAP,
		scanning ..:SLAP PDUs of advertising channel type are provided. In addition, a command is provided for scanner’s or
		initiator’s target device address to which the advertisement is directed ..:TLAP. \n
			:param value: see the help for SlapStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:SLAP', value)

	def get_slatency(self) -> int:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:SLATency \n
		(For data event and advertising frame configuration with the packet type CONNECT_IND) Sets the number of consecutive
		connection events the slave can ignore for asymmetric link layer connections. \n
			:return: slatency: integer Range: 0 to depends on LL connection timeout and connection event interval
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:SLATency?')
		return Conversions.str_to_int(response)

	def set_slatency(self, slatency: int) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:SLATency \n
		(For data event and advertising frame configuration with the packet type CONNECT_IND) Sets the number of consecutive
		connection events the slave can ignore for asymmetric link layer connections. \n
			:param slatency: integer Range: 0 to depends on LL connection timeout and connection event interval
		"""
		param = Conversions.decimal_value_to_str(slatency)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:SLATency {param}')

	# noinspection PyTypeChecker
	class SnuapStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Nap_Uap: List[str]: numeric
			- Bit_Count: int: integer Range: 24 to 24"""
		__meta_args_list = [
			ArgStruct('Nap_Uap', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Nap_Uap: List[str] = None
			self.Bit_Count: int = None

	def get_snuap(self) -> SnuapStruct:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:SNUap \n
		Sets the non-significant address part (NAP) and upper address part (UAP) of Bluetooth device address. Commands for the
		advertising ..:ANUap, initiating ..:INUap, and scanning ..:SNUap PDUs of advertising channel type are provided.
		In addition, a command is provided for scanner’s or initiator’s target device address to which the advertisement is
		directed ..:TNUap. \n
			:return: structure: for return value, see the help for SnuapStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:SNUap?', self.__class__.SnuapStruct())

	def set_snuap(self, value: SnuapStruct) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:SNUap \n
		Sets the non-significant address part (NAP) and upper address part (UAP) of Bluetooth device address. Commands for the
		advertising ..:ANUap, initiating ..:INUap, and scanning ..:SNUap PDUs of advertising channel type are provided.
		In addition, a command is provided for scanner’s or initiator’s target device address to which the advertisement is
		directed ..:TNUap. \n
			:param value: see the help for SnuapStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:SNUap', value)

	# noinspection PyTypeChecker
	def get_sounits(self) -> enums.BtoOffsUnit:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:SOUNits \n
		Indicates the units used by the 'Sync Packet Offset' parameter, see method RsSmbv.Source.Bb.Btooth.Econfiguration.
		Pconfiguration.spOffset \n
			:return: unit: U30| U300 U30 30 µs U300 300 µs
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:SOUNits?')
		return Conversions.str_to_scalar_enum(response, enums.BtoOffsUnit)

	def set_sounits(self, unit: enums.BtoOffsUnit) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:SOUNits \n
		Indicates the units used by the 'Sync Packet Offset' parameter, see method RsSmbv.Source.Bb.Btooth.Econfiguration.
		Pconfiguration.spOffset \n
			:param unit: U30| U300 U30 30 µs U300 300 µs
		"""
		param = Conversions.enum_scalar_to_str(unit, enums.BtoOffsUnit)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:SOUNits {param}')

	# noinspection PyTypeChecker
	def get_spbit(self) -> enums.BtoSymPerBit:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:SPBit \n
		Specifies a coding for LE coded packets. The specification for Bluetooth wireless technology defines two values S for
		forward error correction: S = 2 symbol/bit and S = 8 symbol/bit. \n
			:return: spb: TWO| EIGHt
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:SPBit?')
		return Conversions.str_to_scalar_enum(response, enums.BtoSymPerBit)

	def set_spbit(self, spb: enums.BtoSymPerBit) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:SPBit \n
		Specifies a coding for LE coded packets. The specification for Bluetooth wireless technology defines two values S for
		forward error correction: S = 2 symbol/bit and S = 8 symbol/bit. \n
			:param spb: TWO| EIGHt
		"""
		param = Conversions.enum_scalar_to_str(spb, enums.BtoSymPerBit)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:SPBit {param}')

	def get_sp_offset(self) -> float:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:SPOFfset \n
		Specifies the time from the start of the AUX_ADV_IND packet containing the SyncInfo field to the start of the
		AUX_SYNC_IND packet. The offset is determined by multiplying the value by the unit, see method RsSmbv.Source.Bb.Btooth.
		Econfiguration.Pconfiguration.sounits \n
			:return: sp_offset: float Range: 0 to 245.7 or 246 to 2457 depending on offset unit
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:SPOFfset?')
		return Conversions.str_to_float(response)

	def set_sp_offset(self, sp_offset: float) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:SPOFfset \n
		Specifies the time from the start of the AUX_ADV_IND packet containing the SyncInfo field to the start of the
		AUX_SYNC_IND packet. The offset is determined by multiplying the value by the unit, see method RsSmbv.Source.Bb.Btooth.
		Econfiguration.Pconfiguration.sounits \n
			:param sp_offset: float Range: 0 to 245.7 or 246 to 2457 depending on offset unit
		"""
		param = Conversions.decimal_value_to_str(sp_offset)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:SPOFfset {param}')

	# noinspection PyTypeChecker
	class SskdStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Sskd: List[str]: numeric
			- Bit_Count: int: integer Range: 64 to 64"""
		__meta_args_list = [
			ArgStruct('Sskd', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Sskd: List[str] = None
			self.Bit_Count: int = None

	def get_sskd(self) -> SskdStruct:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:SSKD \n
		Sets the master's or the slave's portion of the session key diversifier (SKDm/SKDs) . \n
			:return: structure: for return value, see the help for SskdStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:SSKD?', self.__class__.SskdStruct())

	def set_sskd(self, value: SskdStruct) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:SSKD \n
		Sets the master's or the slave's portion of the session key diversifier (SKDm/SKDs) . \n
			:param value: see the help for SskdStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:SSKD', value)

	def get_ss_value(self) -> int:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:SSValue \n
		Sets the sequence number of the packet. This parameter can be set in the first event. From the second event, this field
		is not indicated. \n
			:return: ss_value: integer Range: 0 to 1
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:SSValue?')
		return Conversions.str_to_int(response)

	def set_ss_value(self, ss_value: int) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:SSValue \n
		Sets the sequence number of the packet. This parameter can be set in the first event. From the second event, this field
		is not indicated. \n
			:param ss_value: integer Range: 0 to 1
		"""
		param = Conversions.decimal_value_to_str(ss_value)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:SSValue {param}')

	# noinspection PyTypeChecker
	class SvnumberStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Sv_Number: List[str]: numeric
			- Bit_Count: int: integer Range: 16 to 16"""
		__meta_args_list = [
			ArgStruct('Sv_Number', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Sv_Number: List[str] = None
			self.Bit_Count: int = None

	def get_svnumber(self) -> SvnumberStruct:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:SVNumber \n
		Sets a unique value for each implementation or revision of an implementation of the Bluetooth Controller. A 16 bit value
		is set. Note: This parameter is relevant for data frame configuration and for the packet type: LL_VERSION_IND. \n
			:return: structure: for return value, see the help for SvnumberStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:SVNumber?', self.__class__.SvnumberStruct())

	def set_svnumber(self, value: SvnumberStruct) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:SVNumber \n
		Sets a unique value for each implementation or revision of an implementation of the Bluetooth Controller. A 16 bit value
		is set. Note: This parameter is relevant for data frame configuration and for the packet type: LL_VERSION_IND. \n
			:param value: see the help for SvnumberStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:SVNumber', value)

	# noinspection PyTypeChecker
	def get_ta_type(self) -> enums.BtoUlpAddrType:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:TATYpe \n
		Selects the address type of the controller device. Depending on the Bluetooth controller role either Tx or Rx or both
		address types are assigned. Subdivided into private and random, a Bluetooth LE device address consits of 48 bits.
		The format of the device address differs depending on the selected address type. \n
			:return: ta_type: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:TATYpe?')
		return Conversions.str_to_scalar_enum(response, enums.BtoUlpAddrType)

	def set_ta_type(self, ta_type: enums.BtoUlpAddrType) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:TATYpe \n
		Selects the address type of the controller device. Depending on the Bluetooth controller role either Tx or Rx or both
		address types are assigned. Subdivided into private and random, a Bluetooth LE device address consits of 48 bits.
		The format of the device address differs depending on the selected address type. \n
			:param ta_type: PUBLic| RANDom PUBlic Allocates a unique 48 bit address to each Bluetooth LE device. The public address is given from the registration authority IEEE. RANDom Allocates a 48-bit address to each Bluetooth LE device. A random address is optional.
		"""
		param = Conversions.enum_scalar_to_str(ta_type, enums.BtoUlpAddrType)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:TATYpe {param}')

	# noinspection PyTypeChecker
	class TlapStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Lap: List[str]: numeric
			- Bit_Count: int: integer Range: 24 to 24"""
		__meta_args_list = [
			ArgStruct('Lap', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Lap: List[str] = None
			self.Bit_Count: int = None

	def get_tlap(self) -> TlapStruct:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:TLAP \n
		Sets the lower address part (LAP) of Bluetooth device address. Commands for the advertising ..:ALAP, initiating ..:ILAP,
		scanning ..:SLAP PDUs of advertising channel type are provided. In addition, a command is provided for scanner’s or
		initiator’s target device address to which the advertisement is directed ..:TLAP. \n
			:return: structure: for return value, see the help for TlapStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:TLAP?', self.__class__.TlapStruct())

	def set_tlap(self, value: TlapStruct) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:TLAP \n
		Sets the lower address part (LAP) of Bluetooth device address. Commands for the advertising ..:ALAP, initiating ..:ILAP,
		scanning ..:SLAP PDUs of advertising channel type are provided. In addition, a command is provided for scanner’s or
		initiator’s target device address to which the advertisement is directed ..:TLAP. \n
			:param value: see the help for TlapStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:TLAP', value)

	# noinspection PyTypeChecker
	class TnuapStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Nap_Uap: List[str]: numeric
			- Bit_Count: int: integer Range: 24 to 24"""
		__meta_args_list = [
			ArgStruct('Nap_Uap', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Nap_Uap: List[str] = None
			self.Bit_Count: int = None

	def get_tnuap(self) -> TnuapStruct:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:TNUap \n
		Sets the non-significant address part (NAP) and upper address part (UAP) of Bluetooth device address. Commands for the
		advertising ..:ANUap, initiating ..:INUap, and scanning ..:SNUap PDUs of advertising channel type are provided.
		In addition, a command is provided for scanner’s or initiator’s target device address to which the advertisement is
		directed ..:TNUap. \n
			:return: structure: for return value, see the help for TnuapStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:TNUap?', self.__class__.TnuapStruct())

	def set_tnuap(self, value: TnuapStruct) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:TNUap \n
		Sets the non-significant address part (NAP) and upper address part (UAP) of Bluetooth device address. Commands for the
		advertising ..:ANUap, initiating ..:INUap, and scanning ..:SNUap PDUs of advertising channel type are provided.
		In addition, a command is provided for scanner’s or initiator’s target device address to which the advertisement is
		directed ..:TNUap. \n
			:param value: see the help for TnuapStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:TNUap', value)

	def get_tpower(self) -> int:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:TPOWer \n
		Sets the required transmit power to be signaled within an extended header. \n
			:return: tpower: integer Range: -127 to 126
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:TPOWer?')
		return Conversions.str_to_int(response)

	def set_tpower(self, tpower: int) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:TPOWer \n
		Sets the required transmit power to be signaled within an extended header. \n
			:param tpower: integer Range: -127 to 126
		"""
		param = Conversions.decimal_value_to_str(tpower)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:TPOWer {param}')

	# noinspection PyTypeChecker
	class UtypeStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Utype: List[str]: numeric
			- Bit_Count: int: integer Range: 8 to 8"""
		__meta_args_list = [
			ArgStruct('Utype', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Utype: List[str] = None
			self.Bit_Count: int = None

	def get_utype(self) -> UtypeStruct:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:UTYPe \n
		Enables that an invalid control packet is indicated. The CtrType field indicates the value of the LL control packet that
		caused the transmission of this packet. \n
			:return: structure: for return value, see the help for UtypeStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:UTYPe?', self.__class__.UtypeStruct())

	def set_utype(self, value: UtypeStruct) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:UTYPe \n
		Enables that an invalid control packet is indicated. The CtrType field indicates the value of the LL control packet that
		caused the transmission of this packet. \n
			:param value: see the help for UtypeStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:UTYPe', value)

	# noinspection PyTypeChecker
	class VnumberStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Vnumber: List[str]: numeric
			- Bit_Count: int: integer Range: 8 to 8"""
		__meta_args_list = [
			ArgStruct('Vnumber', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Vnumber: List[str] = None
			self.Bit_Count: int = None

	def get_vnumber(self) -> VnumberStruct:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:VNUMber \n
		Sets the company identifier of the manufacturer of the Bluetooth Controller. A 8 bit value is set. Note: This parameter
		is relevant for data frame configuration and for the packet type LL_VERSION_IND. \n
			:return: structure: for return value, see the help for VnumberStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:VNUMber?', self.__class__.VnumberStruct())

	def set_vnumber(self, value: VnumberStruct) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:VNUMber \n
		Sets the company identifier of the manufacturer of the Bluetooth Controller. A 8 bit value is set. Note: This parameter
		is relevant for data frame configuration and for the packet type LL_VERSION_IND. \n
			:param value: see the help for VnumberStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:VNUMber', value)

	def get_woffset(self) -> float:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:WOFFset \n
		Sets the start point of the window transmit for data event and advertising frame configuration with the packet type
		CONNECT_IND. Command sets the values in ms. Query returns values in s. \n
			:return: wo_ffset: float Range: 0 s to depending on connection event interval , Unit: ms
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:WOFFset?')
		return Conversions.str_to_float(response)

	def set_woffset(self, wo_ffset: float) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:WOFFset \n
		Sets the start point of the window transmit for data event and advertising frame configuration with the packet type
		CONNECT_IND. Command sets the values in ms. Query returns values in s. \n
			:param wo_ffset: float Range: 0 s to depending on connection event interval , Unit: ms
		"""
		param = Conversions.decimal_value_to_str(wo_ffset)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:WOFFset {param}')

	def get_wsize(self) -> float:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:WSIZe \n
		Sets the size of the transmit window, regarding to the start point for data event and advertising frame configuration
		with the packet type CONNECT_IND. \n
			:return: wsize: float Range: 1.25E-3 to depends on connection event interval
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:WSIZe?')
		return Conversions.str_to_float(response)

	def set_wsize(self, wsize: float) -> None:
		"""[SOURce<HW>]:BB:BTOoth:ECONfiguration:PCONfiguration:WSIZe \n
		Sets the size of the transmit window, regarding to the start point for data event and advertising frame configuration
		with the packet type CONNECT_IND. \n
			:param wsize: float Range: 1.25E-3 to depends on connection event interval
		"""
		param = Conversions.decimal_value_to_str(wsize)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:ECONfiguration:PCONfiguration:WSIZe {param}')
