from typing import List

from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from .....Internal.Types import DataType
from .....Internal.StructBase import StructBase
from .....Internal.ArgStruct import ArgStruct
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pconfiguration:
	"""Pconfiguration commands group definition. 23 total commands, 1 Sub-groups, 18 group commands"""

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
	def data(self):
		"""data commands group. 0 Sub-classes, 5 commands."""
		if not hasattr(self, '_data'):
			from .Pconfiguration_.Data import Data
			self._data = Data(self._core, self._base)
		return self._data

	# noinspection PyTypeChecker
	def get_acknowledgement(self) -> enums.BtoAckNldgmt:
		"""[SOURce<HW>]:BB:BTOoth:PCONfiguration:ACKNowledgement \n
		Sets the ARQN bit of the packet header.. \n
			:return: acknowledgement: NAK| ACK NAK Request to retransmit the previous payload. ACK Previous payload has been received successfully.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:PCONfiguration:ACKNowledgement?')
		return Conversions.str_to_scalar_enum(response, enums.BtoAckNldgmt)

	def set_acknowledgement(self, acknowledgement: enums.BtoAckNldgmt) -> None:
		"""[SOURce<HW>]:BB:BTOoth:PCONfiguration:ACKNowledgement \n
		Sets the ARQN bit of the packet header.. \n
			:param acknowledgement: NAK| ACK NAK Request to retransmit the previous payload. ACK Previous payload has been received successfully.
		"""
		param = Conversions.enum_scalar_to_str(acknowledgement, enums.BtoAckNldgmt)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:PCONfiguration:ACKNowledgement {param}')

	# noinspection PyTypeChecker
	class BdalapStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Bda_Lap: List[str]: numeric Range: #H000000 to #HFFFFFF
			- Bit_Count: int: integer Range: 8 to 24"""
		__meta_args_list = [
			ArgStruct('Bda_Lap', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Bda_Lap: List[str] = None
			self.Bit_Count: int = None

	def get_bdalap(self) -> BdalapStruct:
		"""[SOURce<HW>]:BB:BTOoth:PCONfiguration:BDALap \n
		Sets the lower address part of Bluetooth Device Address. The length of LAP is 24 bits or 6 hexadecimal figures. \n
			:return: structure: for return value, see the help for BdalapStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:BTOoth:PCONfiguration:BDALap?', self.__class__.BdalapStruct())

	def set_bdalap(self, value: BdalapStruct) -> None:
		"""[SOURce<HW>]:BB:BTOoth:PCONfiguration:BDALap \n
		Sets the lower address part of Bluetooth Device Address. The length of LAP is 24 bits or 6 hexadecimal figures. \n
			:param value: see the help for BdalapStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:BTOoth:PCONfiguration:BDALap', value)

	# noinspection PyTypeChecker
	class BdanapStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Bda_Nap: List[str]: numeric Range: #H0000 to #HFFFF
			- Bit_Count: int: integer Range: 16 to 16"""
		__meta_args_list = [
			ArgStruct('Bda_Nap', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Bda_Nap: List[str] = None
			self.Bit_Count: int = None

	def get_bdanap(self) -> BdanapStruct:
		"""[SOURce<HW>]:BB:BTOoth:PCONfiguration:BDANap \n
		Enters the non-significant address part of Bluetooth Device Address. The length of NAP is 16 bits or 4 hexadecimal
		figures. \n
			:return: structure: for return value, see the help for BdanapStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:BTOoth:PCONfiguration:BDANap?', self.__class__.BdanapStruct())

	def set_bdanap(self, value: BdanapStruct) -> None:
		"""[SOURce<HW>]:BB:BTOoth:PCONfiguration:BDANap \n
		Enters the non-significant address part of Bluetooth Device Address. The length of NAP is 16 bits or 4 hexadecimal
		figures. \n
			:param value: see the help for BdanapStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:BTOoth:PCONfiguration:BDANap', value)

	# noinspection PyTypeChecker
	class BdauapStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Bda_Uap: List[str]: numeric Range: #H00 to #HFF
			- Bit_Count: int: integer Range: 8 to 8"""
		__meta_args_list = [
			ArgStruct('Bda_Uap', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Bda_Uap: List[str] = None
			self.Bit_Count: int = None

	def get_bdauap(self) -> BdauapStruct:
		"""[SOURce<HW>]:BB:BTOoth:PCONfiguration:BDAUap \n
		Enters the upper address part of Bluetooth Device Address. The length of UAP is 8 bits or 2 hexadecimal figures. \n
			:return: structure: for return value, see the help for BdauapStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:BTOoth:PCONfiguration:BDAUap?', self.__class__.BdauapStruct())

	def set_bdauap(self, value: BdauapStruct) -> None:
		"""[SOURce<HW>]:BB:BTOoth:PCONfiguration:BDAUap \n
		Enters the upper address part of Bluetooth Device Address. The length of UAP is 8 bits or 2 hexadecimal figures. \n
			:param value: see the help for BdauapStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:BTOoth:PCONfiguration:BDAUap', value)

	# noinspection PyTypeChecker
	class CoDeviceStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Co_Device: List[str]: numeric Range: #H000000 to #HFFFFFF
			- Bit_Count: int: integer Range: 24 to 24"""
		__meta_args_list = [
			ArgStruct('Co_Device', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Co_Device: List[str] = None
			self.Bit_Count: int = None

	def get_co_device(self) -> CoDeviceStruct:
		"""[SOURce<HW>]:BB:BTOoth:PCONfiguration:CODevice \n
		A parameter received during the device discovery procedure, indicates the type of device and which types of service that
		are supported. \n
			:return: structure: for return value, see the help for CoDeviceStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:BTOoth:PCONfiguration:CODevice?', self.__class__.CoDeviceStruct())

	def set_co_device(self, value: CoDeviceStruct) -> None:
		"""[SOURce<HW>]:BB:BTOoth:PCONfiguration:CODevice \n
		A parameter received during the device discovery procedure, indicates the type of device and which types of service that
		are supported. \n
			:param value: see the help for CoDeviceStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:BTOoth:PCONfiguration:CODevice', value)

	def get_dlength(self) -> int:
		"""[SOURce<HW>]:BB:BTOoth:PCONfiguration:DLENgth \n
		Sets the payload data length in bytes. \n
			:return: dlength: integer Range: 0 to depends on packet type
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:PCONfiguration:DLENgth?')
		return Conversions.str_to_int(response)

	def set_dlength(self, dlength: int) -> None:
		"""[SOURce<HW>]:BB:BTOoth:PCONfiguration:DLENgth \n
		Sets the payload data length in bytes. \n
			:param dlength: integer Range: 0 to depends on packet type
		"""
		param = Conversions.decimal_value_to_str(dlength)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:PCONfiguration:DLENgth {param}')

	# noinspection PyTypeChecker
	def get_dsf_packet(self) -> enums.BtoDataSourForPck:
		"""[SOURce<HW>]:BB:BTOoth:PCONfiguration:DSFPacket \n
		Selects the data source for the selected packet type. \n
			:return: dsf_packet: PEDit| ADATa PED Enables the 'Packet Editor'. All packet fields can be configured individually. ADAT Fills the generated packets with the selected data source. Useful if predefined data contents are loaded with a data list file or the data contents of the packet are not of interest.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:PCONfiguration:DSFPacket?')
		return Conversions.str_to_scalar_enum(response, enums.BtoDataSourForPck)

	def set_dsf_packet(self, dsf_packet: enums.BtoDataSourForPck) -> None:
		"""[SOURce<HW>]:BB:BTOoth:PCONfiguration:DSFPacket \n
		Selects the data source for the selected packet type. \n
			:param dsf_packet: PEDit| ADATa PED Enables the 'Packet Editor'. All packet fields can be configured individually. ADAT Fills the generated packets with the selected data source. Useful if predefined data contents are loaded with a data list file or the data contents of the packet are not of interest.
		"""
		param = Conversions.enum_scalar_to_str(dsf_packet, enums.BtoDataSourForPck)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:PCONfiguration:DSFPacket {param}')

	def get_dwhitening(self) -> bool:
		"""[SOURce<HW>]:BB:BTOoth:PCONfiguration:DWHitening \n
		Activates the 'Data Whitening'. \n
			:return: dwhitening: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:PCONfiguration:DWHitening?')
		return Conversions.str_to_bool(response)

	def set_dwhitening(self, dwhitening: bool) -> None:
		"""[SOURce<HW>]:BB:BTOoth:PCONfiguration:DWHitening \n
		Activates the 'Data Whitening'. \n
			:param dwhitening: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(dwhitening)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:PCONfiguration:DWHitening {param}')

	# noinspection PyTypeChecker
	def get_eir_packet_follows(self) -> enums.YesNoStatus:
		"""[SOURce<HW>]:BB:BTOoth:PCONfiguration:EIRPacketfollows \n
		Indicates that an extended inquiry response packet can follow. \n
			:return: eir_packet_follow: YES| NO YES Indicates that EIR packet follows. NO Indicates that EIR packet does not follow.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:PCONfiguration:EIRPacketfollows?')
		return Conversions.str_to_scalar_enum(response, enums.YesNoStatus)

	def set_eir_packet_follows(self, eir_packet_follow: enums.YesNoStatus) -> None:
		"""[SOURce<HW>]:BB:BTOoth:PCONfiguration:EIRPacketfollows \n
		Indicates that an extended inquiry response packet can follow. \n
			:param eir_packet_follow: YES| NO YES Indicates that EIR packet follows. NO Indicates that EIR packet does not follow.
		"""
		param = Conversions.enum_scalar_to_str(eir_packet_follow, enums.YesNoStatus)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:PCONfiguration:EIRPacketfollows {param}')

	# noinspection PyTypeChecker
	def get_hf_control(self) -> enums.BtoFlowCtrl:
		"""[SOURce<HW>]:BB:BTOoth:PCONfiguration:HFControl \n
		The command sets the FLOW bit in the header. This bit indicates start or stop of transmission of packets over the ACL
		logical transport. \n
			:return: hf_control: GO| STOP GO Allows the other devices to transmit new data. STOP Stops the other devices from transmitting data temporarily.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:PCONfiguration:HFControl?')
		return Conversions.str_to_scalar_enum(response, enums.BtoFlowCtrl)

	def set_hf_control(self, hf_control: enums.BtoFlowCtrl) -> None:
		"""[SOURce<HW>]:BB:BTOoth:PCONfiguration:HFControl \n
		The command sets the FLOW bit in the header. This bit indicates start or stop of transmission of packets over the ACL
		logical transport. \n
			:param hf_control: GO| STOP GO Allows the other devices to transmit new data. STOP Stops the other devices from transmitting data temporarily.
		"""
		param = Conversions.enum_scalar_to_str(hf_control, enums.BtoFlowCtrl)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:PCONfiguration:HFControl {param}')

	# noinspection PyTypeChecker
	class LfsWordStruct(StructBase):
		"""Structure for reading output parameters. Fields: \n
			- Lap_For_Sw: List[str]: numeric Range: #H000000 to #HFFFFFF
			- Bit_Count: int: integer Range: 8 to 24"""
		__meta_args_list = [
			ArgStruct('Lap_For_Sw', DataType.RawStringList, None, False, True, 1),
			ArgStruct.scalar_int('Bit_Count')]

		def __init__(self):
			StructBase.__init__(self, self)
			self.Lap_For_Sw: List[str] = None
			self.Bit_Count: int = None

	def get_lfs_word(self) -> LfsWordStruct:
		"""[SOURce<HW>]:BB:BTOoth:PCONfiguration:LFSWord \n
		Sets the lower address part (LAP) of the sync word for FHS packets. The length of LAP is 24 bits or 6 hexadecimal figures. \n
			:return: structure: for return value, see the help for LfsWordStruct structure arguments.
		"""
		return self._core.io.query_struct('SOURce<HwInstance>:BB:BTOoth:PCONfiguration:LFSWord?', self.__class__.LfsWordStruct())

	def set_lfs_word(self, value: LfsWordStruct) -> None:
		"""[SOURce<HW>]:BB:BTOoth:PCONfiguration:LFSWord \n
		Sets the lower address part (LAP) of the sync word for FHS packets. The length of LAP is 24 bits or 6 hexadecimal figures. \n
			:param value: see the help for LfsWordStruct structure arguments.
		"""
		self._core.io.write_struct('SOURce<HwInstance>:BB:BTOoth:PCONfiguration:LFSWord', value)

	def get_lt_address(self) -> int:
		"""[SOURce<HW>]:BB:BTOoth:PCONfiguration:LTADdress \n
		The command enters the logical transport address for the header. Each slave active in a piconet is assigned a primary
		logical transport address (LT_ADDR) . The all-zero LT_ADDR is reserved for broadcast messages. \n
			:return: lt_address: integer Range: 0 to 7
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:PCONfiguration:LTADdress?')
		return Conversions.str_to_int(response)

	def set_lt_address(self, lt_address: int) -> None:
		"""[SOURce<HW>]:BB:BTOoth:PCONfiguration:LTADdress \n
		The command enters the logical transport address for the header. Each slave active in a piconet is assigned a primary
		logical transport address (LT_ADDR) . The all-zero LT_ADDR is reserved for broadcast messages. \n
			:param lt_address: integer Range: 0 to 7
		"""
		param = Conversions.decimal_value_to_str(lt_address)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:PCONfiguration:LTADdress {param}')

	# noinspection PyTypeChecker
	def get_pf_control(self) -> enums.BtoFlowCtrl:
		"""[SOURce<HW>]:BB:BTOoth:PCONfiguration:PFControl \n
		The command sets the FLOW bit in the payload (flow control per logical link) . \n
			:return: pf_control: GO| STOP GO Indicates the start of transmission of ACL packets after a new connection has been established. STOP Indicates the stop of transmission of ACL packets before an additional amount of payload data is sent.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:PCONfiguration:PFControl?')
		return Conversions.str_to_scalar_enum(response, enums.BtoFlowCtrl)

	def set_pf_control(self, pf_control: enums.BtoFlowCtrl) -> None:
		"""[SOURce<HW>]:BB:BTOoth:PCONfiguration:PFControl \n
		The command sets the FLOW bit in the payload (flow control per logical link) . \n
			:param pf_control: GO| STOP GO Indicates the start of transmission of ACL packets after a new connection has been established. STOP Indicates the stop of transmission of ACL packets before an additional amount of payload data is sent.
		"""
		param = Conversions.enum_scalar_to_str(pf_control, enums.BtoFlowCtrl)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:PCONfiguration:PFControl {param}')

	def get_plength(self) -> int:
		"""[SOURce<HW>]:BB:BTOoth:PCONfiguration:PLENgth \n
		Sets the packet length in symbols. \n
			:return: plength: integer Range: 1 to depends on packet type
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:PCONfiguration:PLENgth?')
		return Conversions.str_to_int(response)

	def set_plength(self, plength: int) -> None:
		"""[SOURce<HW>]:BB:BTOoth:PCONfiguration:PLENgth \n
		Sets the packet length in symbols. \n
			:param plength: integer Range: 1 to depends on packet type
		"""
		param = Conversions.decimal_value_to_str(plength)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:PCONfiguration:PLENgth {param}')

	def get_slap(self) -> bool:
		"""[SOURce<HW>]:BB:BTOoth:PCONfiguration:SLAP \n
		Activates synchronization of the lower address part (LAP) of the sync word and Bluetooth device address. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:PCONfiguration:SLAP?')
		return Conversions.str_to_bool(response)

	def set_slap(self, state: bool) -> None:
		"""[SOURce<HW>]:BB:BTOoth:PCONfiguration:SLAP \n
		Activates synchronization of the lower address part (LAP) of the sync word and Bluetooth device address. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:PCONfiguration:SLAP {param}')

	def get_sns_value(self) -> int:
		"""[SOURce<HW>]:BB:BTOoth:PCONfiguration:SNSValue \n
		Sets the start value of the header SEQN bit. The SEQN bit is present in the header to filter out retransmissions in the
		destination. The signal generator is altering this bit automatically on consecutive frames, if a sequence length of at
		least 2 frames is set. \n
			:return: sn_svalue: integer Range: 0 to 1
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:PCONfiguration:SNSValue?')
		return Conversions.str_to_int(response)

	def set_sns_value(self, sn_svalue: int) -> None:
		"""[SOURce<HW>]:BB:BTOoth:PCONfiguration:SNSValue \n
		Sets the start value of the header SEQN bit. The SEQN bit is present in the header to filter out retransmissions in the
		destination. The signal generator is altering this bit automatically on consecutive frames, if a sequence length of at
		least 2 frames is set. \n
			:param sn_svalue: integer Range: 0 to 1
		"""
		param = Conversions.decimal_value_to_str(sn_svalue)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:PCONfiguration:SNSValue {param}')

	# noinspection PyTypeChecker
	def get_sr_mode(self) -> enums.BtoScanReMode:
		"""[SOURce<HW>]:BB:BTOoth:PCONfiguration:SRMode \n
		The command indicates the interval between two consecutive page scan windows, determines the behavior of the paging
		device. \n
			:return: sr_mode: R0| R1| R2 R0 The scan interval is equal to the scan window T w page scan (continuous nscan) and maximal 1.28s. R1 The scan interval is maximal 1.28s. R2 The scan interval is maximal 2.56s.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:PCONfiguration:SRMode?')
		return Conversions.str_to_scalar_enum(response, enums.BtoScanReMode)

	def set_sr_mode(self, sr_mode: enums.BtoScanReMode) -> None:
		"""[SOURce<HW>]:BB:BTOoth:PCONfiguration:SRMode \n
		The command indicates the interval between two consecutive page scan windows, determines the behavior of the paging
		device. \n
			:param sr_mode: R0| R1| R2 R0 The scan interval is equal to the scan window T w page scan (continuous nscan) and maximal 1.28s. R1 The scan interval is maximal 1.28s. R2 The scan interval is maximal 2.56s.
		"""
		param = Conversions.enum_scalar_to_str(sr_mode, enums.BtoScanReMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:PCONfiguration:SRMode {param}')

	# noinspection PyTypeChecker
	def get_vdata(self) -> enums.BtoDataSourc:
		"""[SOURce<HW>]:BB:BTOoth:PCONfiguration:VDATa \n
		Selects the data source for the voice field. \n
			:return: vdata: ALL0| ALL1| PATTern| PN09| PN11| PN15| PN16| PN20| PN21| PN23| DLISt
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:PCONfiguration:VDATa?')
		return Conversions.str_to_scalar_enum(response, enums.BtoDataSourc)

	def set_vdata(self, vdata: enums.BtoDataSourc) -> None:
		"""[SOURce<HW>]:BB:BTOoth:PCONfiguration:VDATa \n
		Selects the data source for the voice field. \n
			:param vdata: ALL0| ALL1| PATTern| PN09| PN11| PN15| PN16| PN20| PN21| PN23| DLISt
		"""
		param = Conversions.enum_scalar_to_str(vdata, enums.BtoDataSourc)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:PCONfiguration:VDATa {param}')
