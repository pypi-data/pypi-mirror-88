from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Utilities import trim_str_response
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Btooth:
	"""Btooth commands group definition. 251 total commands, 16 Sub-groups, 17 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("btooth", core, parent)

	def clone(self) -> 'Btooth':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Btooth(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def ccrc(self):
		"""ccrc commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_ccrc'):
			from .Btooth_.Ccrc import Ccrc
			self._ccrc = Ccrc(self._core, self._base)
		return self._ccrc

	@property
	def clipping(self):
		"""clipping commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_clipping'):
			from .Btooth_.Clipping import Clipping
			self._clipping = Clipping(self._core, self._base)
		return self._clipping

	@property
	def clock(self):
		"""clock commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_clock'):
			from .Btooth_.Clock import Clock
			self._clock = Clock(self._core, self._base)
		return self._clock

	@property
	def dtTest(self):
		"""dtTest commands group. 3 Sub-classes, 6 commands."""
		if not hasattr(self, '_dtTest'):
			from .Btooth_.DtTest import DtTest
			self._dtTest = DtTest(self._core, self._base)
		return self._dtTest

	@property
	def econfig(self):
		"""econfig commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_econfig'):
			from .Btooth_.Econfig import Econfig
			self._econfig = Econfig(self._core, self._base)
		return self._econfig

	@property
	def econfiguration(self):
		"""econfiguration commands group. 3 Sub-classes, 12 commands."""
		if not hasattr(self, '_econfiguration'):
			from .Btooth_.Econfiguration import Econfiguration
			self._econfiguration = Econfiguration(self._core, self._base)
		return self._econfiguration

	@property
	def filterPy(self):
		"""filterPy commands group. 3 Sub-classes, 3 commands."""
		if not hasattr(self, '_filterPy'):
			from .Btooth_.FilterPy import FilterPy
			self._filterPy = FilterPy(self._core, self._base)
		return self._filterPy

	@property
	def msettings(self):
		"""msettings commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_msettings'):
			from .Btooth_.Msettings import Msettings
			self._msettings = Msettings(self._core, self._base)
		return self._msettings

	@property
	def pconfiguration(self):
		"""pconfiguration commands group. 1 Sub-classes, 18 commands."""
		if not hasattr(self, '_pconfiguration'):
			from .Btooth_.Pconfiguration import Pconfiguration
			self._pconfiguration = Pconfiguration(self._core, self._base)
		return self._pconfiguration

	@property
	def pramping(self):
		"""pramping commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_pramping'):
			from .Btooth_.Pramping import Pramping
			self._pramping = Pramping(self._core, self._base)
		return self._pramping

	@property
	def qhs(self):
		"""qhs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_qhs'):
			from .Btooth_.Qhs import Qhs
			self._qhs = Qhs(self._core, self._base)
		return self._qhs

	@property
	def setting(self):
		"""setting commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_setting'):
			from .Btooth_.Setting import Setting
			self._setting = Setting(self._core, self._base)
		return self._setting

	@property
	def symbolRate(self):
		"""symbolRate commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_symbolRate'):
			from .Btooth_.SymbolRate import SymbolRate
			self._symbolRate = SymbolRate(self._core, self._base)
		return self._symbolRate

	@property
	def trigger(self):
		"""trigger commands group. 4 Sub-classes, 5 commands."""
		if not hasattr(self, '_trigger'):
			from .Btooth_.Trigger import Trigger
			self._trigger = Trigger(self._core, self._base)
		return self._trigger

	@property
	def unit(self):
		"""unit commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_unit'):
			from .Btooth_.Unit import Unit
			self._unit = Unit(self._core, self._base)
		return self._unit

	@property
	def waveform(self):
		"""waveform commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_waveform'):
			from .Btooth_.Waveform import Waveform
			self._waveform = Waveform(self._core, self._base)
		return self._waveform

	# noinspection PyTypeChecker
	def get_bc_role(self) -> enums.BtoCtrlRol:
		"""[SOURce<HW>]:BB:BTOoth:BCRole \n
		Determines the controller role. Depending on the selected channel type different roles are assigned to the controller.
		For channel type 'Data', master or slave can be assigned. If channel type 'Advertising' is selected, the parameter is
		read only and displayed directly above the graph. \n
			:return: bc_role: MASTer| SLAVe| ADVertiser| SCANner| INITiator MASTER Assigns master role to the controller. SLAVE Selects slave as controller role. ADVertiser|SCANner|INITiator Assigned roles depending on the selected packet type of the respective channel type.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:BCRole?')
		return Conversions.str_to_scalar_enum(response, enums.BtoCtrlRol)

	def set_bc_role(self, bc_role: enums.BtoCtrlRol) -> None:
		"""[SOURce<HW>]:BB:BTOoth:BCRole \n
		Determines the controller role. Depending on the selected channel type different roles are assigned to the controller.
		For channel type 'Data', master or slave can be assigned. If channel type 'Advertising' is selected, the parameter is
		read only and displayed directly above the graph. \n
			:param bc_role: MASTer| SLAVe| ADVertiser| SCANner| INITiator MASTER Assigns master role to the controller. SLAVE Selects slave as controller role. ADVertiser|SCANner|INITiator Assigned roles depending on the selected packet type of the respective channel type.
		"""
		param = Conversions.enum_scalar_to_str(bc_role, enums.BtoCtrlRol)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:BCRole {param}')

	def get_bc_text(self) -> str:
		"""[SOURce<HW>]:BB:BTOoth:BCText \n
		Queries the state and controller role. \n
			:return: bc_text: string Connected (only data channel type) Advertiser (only advertising channel type) ADV_IND, ADV_DIRECT_IND, ADV_NONCONN_IND, ADV_SCAN_IND Within R&S SMBVB-K117 also ADV_EXT_IND, AUX_ADV_IND, AUX_SYNC_IND, AUX_CHAIN_IND Scanner (only advertising channel type) SCAN_REQ, SCAN_RSP Within R&S SMBVB-K117 also AUX_SCAN_REQ, AUX_SCAN_RSP Initiator (only advertising channel type) CONNECT_IND Within R&S SMBVB-K117 also AUX_CONNECT_REQ, AUX_CONNECT_RSP
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:BCText?')
		return trim_str_response(response)

	# noinspection PyTypeChecker
	def get_bmode(self) -> enums.BtoMode:
		"""[SOURce<HW>]:BB:BTOoth:BMODe \n
		Determines the Bluetooth mode. \n
			:return: bm_ode: BASic| BLENergy BASic Selects Bluetooth mode BR + EDR. BLENergy Selects Bluetooth LE.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:BMODe?')
		return Conversions.str_to_scalar_enum(response, enums.BtoMode)

	def set_bmode(self, bm_ode: enums.BtoMode) -> None:
		"""[SOURce<HW>]:BB:BTOoth:BMODe \n
		Determines the Bluetooth mode. \n
			:param bm_ode: BASic| BLENergy BASic Selects Bluetooth mode BR + EDR. BLENergy Selects Bluetooth LE.
		"""
		param = Conversions.enum_scalar_to_str(bm_ode, enums.BtoMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:BMODe {param}')

	# noinspection PyTypeChecker
	def get_ctype(self) -> enums.BtoChnnelType:
		"""[SOURce<HW>]:BB:BTOoth:CTYPe \n
		Determines the channel type. Advertising and data are available. \n
			:return: ctype: ADVertising| DATA ADVertising Selects channel type advertising. DATA Selects channel type data. Devices in a connected state transmit data channel packets in connection events with a start point and an interval.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:CTYPe?')
		return Conversions.str_to_scalar_enum(response, enums.BtoChnnelType)

	def set_ctype(self, ctype: enums.BtoChnnelType) -> None:
		"""[SOURce<HW>]:BB:BTOoth:CTYPe \n
		Determines the channel type. Advertising and data are available. \n
			:param ctype: ADVertising| DATA ADVertising Selects channel type advertising. DATA Selects channel type data. Devices in a connected state transmit data channel packets in connection events with a start point and an interval.
		"""
		param = Conversions.enum_scalar_to_str(ctype, enums.BtoChnnelType)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:CTYPe {param}')

	# noinspection PyTypeChecker
	def get_dcycle(self) -> enums.LowHigh:
		"""[SOURce<HW>]:BB:BTOoth:DCYCle \n
		Specifies duty cycle for directed advertising (packet type ADV_DIRECT_IND) . \n
			:return: dcycle: LOW| HIGH
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:DCYCle?')
		return Conversions.str_to_scalar_enum(response, enums.LowHigh)

	def set_dcycle(self, dcycle: enums.LowHigh) -> None:
		"""[SOURce<HW>]:BB:BTOoth:DCYCle \n
		Specifies duty cycle for directed advertising (packet type ADV_DIRECT_IND) . \n
			:param dcycle: LOW| HIGH
		"""
		param = Conversions.enum_scalar_to_str(dcycle, enums.LowHigh)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:DCYCle {param}')

	def get_duration(self) -> float:
		"""[SOURce<HW>]:BB:BTOoth:DURation \n
		Specifies the transmission duration of CONTINUOUS payload transmission. Command sets the values in ms. Query returns
		values in s. \n
			:return: duration: float Range: depending on modulation format, symbols per a bit and payload type , Unit: ms
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:DURation?')
		return Conversions.str_to_float(response)

	def set_duration(self, duration: float) -> None:
		"""[SOURce<HW>]:BB:BTOoth:DURation \n
		Specifies the transmission duration of CONTINUOUS payload transmission. Command sets the values in ms. Query returns
		values in s. \n
			:param duration: float Range: depending on modulation format, symbols per a bit and payload type , Unit: ms
		"""
		param = Conversions.decimal_value_to_str(duration)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:DURation {param}')

	# noinspection PyTypeChecker
	def get_mformat(self) -> enums.PackFormat:
		"""[SOURce<HW>]:BB:BTOoth:MFORmat \n
		Specifies the physical layer used for CONTINUOUS payload transmission. \n
			:return: mod_fmt: L1M| L2M| LCOD | L2M| LCOD L1M: LE 1M L2M: LE 2M LCOD: LE coded
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:MFORmat?')
		return Conversions.str_to_scalar_enum(response, enums.PackFormat)

	def set_mformat(self, mod_fmt: enums.PackFormat) -> None:
		"""[SOURce<HW>]:BB:BTOoth:MFORmat \n
		Specifies the physical layer used for CONTINUOUS payload transmission. \n
			:param mod_fmt: L1M| L2M| LCOD | L2M| LCOD L1M: LE 1M L2M: LE 2M LCOD: LE coded
		"""
		param = Conversions.enum_scalar_to_str(mod_fmt, enums.PackFormat)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:MFORmat {param}')

	# noinspection PyTypeChecker
	def get_pformat(self) -> enums.PackFormat:
		"""[SOURce<HW>]:BB:BTOoth:PFORmat \n
		Specifies the physical layer of LE signal. \n
			:return: pf_ormat: L1M| L2M| LCOD L1M LE 1M L2M LE 2M LCOD LE coded
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:PFORmat?')
		return Conversions.str_to_scalar_enum(response, enums.PackFormat)

	def set_pformat(self, pf_ormat: enums.PackFormat) -> None:
		"""[SOURce<HW>]:BB:BTOoth:PFORmat \n
		Specifies the physical layer of LE signal. \n
			:param pf_ormat: L1M| L2M| LCOD L1M LE 1M L2M LE 2M LCOD LE coded
		"""
		param = Conversions.enum_scalar_to_str(pf_ormat, enums.PackFormat)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:PFORmat {param}')

	def preset(self) -> None:
		"""[SOURce<HW>]:BB:BTOoth:PRESet \n
		Sets the parameters of the digital standard to their default values (*RST values specified for the commands) .
		Not affected is the state set with the command method RsSmbv.Source.Bb.Btooth.state. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:PRESet')

	def preset_with_opc(self) -> None:
		"""[SOURce<HW>]:BB:BTOoth:PRESet \n
		Sets the parameters of the digital standard to their default values (*RST values specified for the commands) .
		Not affected is the state set with the command method RsSmbv.Source.Bb.Btooth.state. \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:BTOoth:PRESet')

	# noinspection PyTypeChecker
	def get_ptype(self) -> enums.BtoPckType:
		"""[SOURce<HW>]:BB:BTOoth:PTYPe \n
		The available packets depend on the selected transport mode. All packet types as defined in the Bluetooth specifications
		are supported. \n
			:return: ptype: ID| NULL| POLL| FHS| DM1| DH1| DM3| DH3| DM5| DH5| AUX1| ADH1| ADH3| ADH5| AEDH1| AEDH3| AEDH5| HV1| HV2| HV3| DV| EV3| EV4| EV5| EEV3| EEV5| EEEV3| EEEV5
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:PTYPe?')
		return Conversions.str_to_scalar_enum(response, enums.BtoPckType)

	def set_ptype(self, ptype: enums.BtoPckType) -> None:
		"""[SOURce<HW>]:BB:BTOoth:PTYPe \n
		The available packets depend on the selected transport mode. All packet types as defined in the Bluetooth specifications
		are supported. \n
			:param ptype: ID| NULL| POLL| FHS| DM1| DH1| DM3| DH3| DM5| DH5| AUX1| ADH1| ADH3| ADH5| AEDH1| AEDH3| AEDH5| HV1| HV2| HV3| DV| EV3| EV4| EV5| EEV3| EEV5| EEEV3| EEEV5
		"""
		param = Conversions.enum_scalar_to_str(ptype, enums.BtoPckType)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:PTYPe {param}')

	def get_slength(self) -> int:
		"""[SOURce<HW>]:BB:BTOoth:SLENgth \n
		Sets the sequence length of the Bluetooth signal in number of frames. This signal is calculated in advance and output in
		the arbitrary waveform generator. \n
			:return: slength: integer Range: depends on the number of states in dirty transmitter test to dynamic
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:SLENgth?')
		return Conversions.str_to_int(response)

	def set_slength(self, slength: int) -> None:
		"""[SOURce<HW>]:BB:BTOoth:SLENgth \n
		Sets the sequence length of the Bluetooth signal in number of frames. This signal is calculated in advance and output in
		the arbitrary waveform generator. \n
			:param slength: integer Range: depends on the number of states in dirty transmitter test to dynamic
		"""
		param = Conversions.decimal_value_to_str(slength)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:SLENgth {param}')

	def get_state(self) -> bool:
		"""[SOURce<HW>]:BB:BTOoth:STATe \n
		Activates the standard and deactivates all the other digital standards and digital modulation modes in the same path. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""[SOURce<HW>]:BB:BTOoth:STATe \n
		Activates the standard and deactivates all the other digital standards and digital modulation modes in the same path. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:STATe {param}')

	# noinspection PyTypeChecker
	def get_stiming(self) -> enums.BtoSlotTiming:
		"""[SOURce<HW>]:BB:BTOoth:STIMing \n
		Selects the Rx slot timing mode. \n
			:return: slot_timing: TX| LOOPback
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:STIMing?')
		return Conversions.str_to_scalar_enum(response, enums.BtoSlotTiming)

	def set_stiming(self, slot_timing: enums.BtoSlotTiming) -> None:
		"""[SOURce<HW>]:BB:BTOoth:STIMing \n
		Selects the Rx slot timing mode. \n
			:param slot_timing: TX| LOOPback
		"""
		param = Conversions.enum_scalar_to_str(slot_timing, enums.BtoSlotTiming)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:STIMing {param}')

	# noinspection PyTypeChecker
	def get_tmode(self) -> enums.BtoTranMode:
		"""[SOURce<HW>]:BB:BTOoth:TMODe \n
		Selects the transport mode. \n
			:return: tm_ode: ACL| SCO| ESCO ACL Asynchronous connection-less mode used for a point-to-point multipoint link between a master and all slaves. SCO Synchronous connection-oriented mode used for a point-to-point link between a master and a specific slave. ESCO Enhanced synchronous connection-oriented mode used for a symmetric or asymmetric point-to point link between a master and a specific slave.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:TMODe?')
		return Conversions.str_to_scalar_enum(response, enums.BtoTranMode)

	def set_tmode(self, tm_ode: enums.BtoTranMode) -> None:
		"""[SOURce<HW>]:BB:BTOoth:TMODe \n
		Selects the transport mode. \n
			:param tm_ode: ACL| SCO| ESCO ACL Asynchronous connection-less mode used for a point-to-point multipoint link between a master and all slaves. SCO Synchronous connection-oriented mode used for a point-to-point link between a master and a specific slave. ESCO Enhanced synchronous connection-oriented mode used for a symmetric or asymmetric point-to point link between a master and a specific slave.
		"""
		param = Conversions.enum_scalar_to_str(tm_ode, enums.BtoTranMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:TMODe {param}')

	# noinspection PyTypeChecker
	def get_up_type(self) -> enums.BtoUlpPckType:
		"""[SOURce<HW>]:BB:BTOoth:UPTYpe \n
		Selects the packet type. The available packets depend on the selected channel type. \n
			:return: up_type: AIND| ADINd| ANINd| SREQ| SRSP| CREQ| ADCind| DATA| CUReq| CMReq| TIND| EREQ| ERSP| SEReq| SERSp| URSP| FREQ| FRSP| TPACket| PEReq| PERSp| VIND| RIND| PREQ| PRSP| PUIN| LREQ| LRSP| SFR| CPR| CPRS| REIN| PIR| PIRS| AEINd| AAINd| ACINd| ASINd| ASReq| ASPSp| ACRSp| ACReq| MUCH| CONT| CTEQ| CTEP| PSINd| CAReq| CARSp AIND: ADV_IND ADINd: ADV_DIRECT_IND ANINd: ADV_NONCONN_IND SREQ: SCAN_REQ SRSP: SCAN_RSP CREQ: CONNECT_IND ADCind: ADV_SCAN_IND DATA: DATA CUReq: LL_CONNECTION_UPDATE_IND CMReq: LL_CHANNEL_MAP_IND TIND: LL_TERMINATE_IND EREQ: LL_ENC_REQ ERSP: LL_ENC_RSP SEReq: LL_START_ENC_REQ SERSp: LL_START_ENC_RSP URSP: LL_UNKNONW_RSP FREQ: LL_FEATURE_REQ FRSP: LL_FEATURE_RSP TPACket: TEST PACKET PEReq: LL_PAUSE_ENC_REQ PERSp: LL_PAUSE_ENC_RSP VIND: LL_VERSION_IND RIND: LL_REJECT_IND PREQ: LL_PHY_REQ PRSP: LL_PHY_RSP PUIN: LL_PHY_UPDATE_IND LREQ: LL_LENGTH_REQ LRSP: LL_LENGTH_RSP SFR: LL_SLAVE_FEATURE_REQ CPR: LL_CONNECTION_PARAM_REQ CPRS: LL_CONNECTION_PARAM_RSP REIN: LL_REJECT_EXT_IND PIR: LL_PING_REQ PIRS: LL_PING_RSP AEINd: ADV_EXT_IND AAINd: AUX_ADV_IND ACINd: AUX_CHAIN_IND ASINd: AUX_SYNC_IND ASReq: AUX_SCAN_REQ ASPSp: AUX_SCAN_RSP ACRSp: AUX_CONNECT_RSP ACReq: AUX_CONNECT_REQ MUCH: LL_MIN_USED_CHANNELS_IND CONT: CONTINUOUS CTEQ: LL_CTE_REQ CTEP: LL_CTE_RSP PSIND: LL_PERIODIC_SYNC CAReq: LL_CLOCK_ACCURACY_REQ CARSp: LL_CLOCK_ACCURACY_RSP
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:UPTYpe?')
		return Conversions.str_to_scalar_enum(response, enums.BtoUlpPckType)

	def set_up_type(self, up_type: enums.BtoUlpPckType) -> None:
		"""[SOURce<HW>]:BB:BTOoth:UPTYpe \n
		Selects the packet type. The available packets depend on the selected channel type. \n
			:param up_type: AIND| ADINd| ANINd| SREQ| SRSP| CREQ| ADCind| DATA| CUReq| CMReq| TIND| EREQ| ERSP| SEReq| SERSp| URSP| FREQ| FRSP| TPACket| PEReq| PERSp| VIND| RIND| PREQ| PRSP| PUIN| LREQ| LRSP| SFR| CPR| CPRS| REIN| PIR| PIRS| AEINd| AAINd| ACINd| ASINd| ASReq| ASPSp| ACRSp| ACReq| MUCH| CONT| CTEQ| CTEP| PSINd| CAReq| CARSp AIND: ADV_IND ADINd: ADV_DIRECT_IND ANINd: ADV_NONCONN_IND SREQ: SCAN_REQ SRSP: SCAN_RSP CREQ: CONNECT_IND ADCind: ADV_SCAN_IND DATA: DATA CUReq: LL_CONNECTION_UPDATE_IND CMReq: LL_CHANNEL_MAP_IND TIND: LL_TERMINATE_IND EREQ: LL_ENC_REQ ERSP: LL_ENC_RSP SEReq: LL_START_ENC_REQ SERSp: LL_START_ENC_RSP URSP: LL_UNKNONW_RSP FREQ: LL_FEATURE_REQ FRSP: LL_FEATURE_RSP TPACket: TEST PACKET PEReq: LL_PAUSE_ENC_REQ PERSp: LL_PAUSE_ENC_RSP VIND: LL_VERSION_IND RIND: LL_REJECT_IND PREQ: LL_PHY_REQ PRSP: LL_PHY_RSP PUIN: LL_PHY_UPDATE_IND LREQ: LL_LENGTH_REQ LRSP: LL_LENGTH_RSP SFR: LL_SLAVE_FEATURE_REQ CPR: LL_CONNECTION_PARAM_REQ CPRS: LL_CONNECTION_PARAM_RSP REIN: LL_REJECT_EXT_IND PIR: LL_PING_REQ PIRS: LL_PING_RSP AEINd: ADV_EXT_IND AAINd: AUX_ADV_IND ACINd: AUX_CHAIN_IND ASINd: AUX_SYNC_IND ASReq: AUX_SCAN_REQ ASPSp: AUX_SCAN_RSP ACRSp: AUX_CONNECT_RSP ACReq: AUX_CONNECT_REQ MUCH: LL_MIN_USED_CHANNELS_IND CONT: CONTINUOUS CTEQ: LL_CTE_REQ CTEP: LL_CTE_RSP PSIND: LL_PERIODIC_SYNC CAReq: LL_CLOCK_ACCURACY_REQ CARSp: LL_CLOCK_ACCURACY_RSP
		"""
		param = Conversions.enum_scalar_to_str(up_type, enums.BtoUlpPckType)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:UPTYpe {param}')

	def get_us_length(self) -> int:
		"""[SOURce<HW>]:BB:BTOoth:USLength \n
		Selects the number of frames or events depending on the packet type. The signal repeats after the specified number of
		frames/events. For SCAN_REQ and CONNECT_IND packet, the sequence length is expressed in 'Frames'. For AUX_SCAN_REQ and
		AUX_CONNECT_REQ packet, the sequence length is expressed in 'Frames'. For LL_TERMINATE_IND packets, a default value
		according to the specification is given: Master: 'SlaveLatency + 6' Slave: '6' For all other packet types the sequence
		length is expressed in 'Events'. \n
			:return: us_length: integer Range: depends on the number of states in dirty transmitter test to dynamic
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:USLength?')
		return Conversions.str_to_int(response)

	def set_us_length(self, us_length: int) -> None:
		"""[SOURce<HW>]:BB:BTOoth:USLength \n
		Selects the number of frames or events depending on the packet type. The signal repeats after the specified number of
		frames/events. For SCAN_REQ and CONNECT_IND packet, the sequence length is expressed in 'Frames'. For AUX_SCAN_REQ and
		AUX_CONNECT_REQ packet, the sequence length is expressed in 'Frames'. For LL_TERMINATE_IND packets, a default value
		according to the specification is given: Master: 'SlaveLatency + 6' Slave: '6' For all other packet types the sequence
		length is expressed in 'Events'. \n
			:param us_length: integer Range: depends on the number of states in dirty transmitter test to dynamic
		"""
		param = Conversions.decimal_value_to_str(us_length)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:USLength {param}')

	def get_version(self) -> str:
		"""[SOURce<HW>]:BB:BTOoth:VERSion \n
		Queries the version of the specification for Bluetooth wireless technology underlying the definitions. \n
			:return: version: string
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:BTOoth:VERSion?')
		return trim_str_response(response)
