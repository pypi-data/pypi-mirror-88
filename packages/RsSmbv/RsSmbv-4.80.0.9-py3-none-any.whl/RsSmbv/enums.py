from enum import Enum


# noinspection SpellCheckingInspection
class YesNoStatus(Enum):
	"""2 Members, NO ... YES"""
	NO = 0
	YES = 1


# noinspection SpellCheckingInspection
class XmRadioPhysLayer(Enum):
	"""6 Members, SAT1A ... TERRB"""
	SAT1A = 0
	SAT1B = 1
	SAT2A = 2
	SAT2B = 3
	TERRA = 4
	TERRB = 5


# noinspection SpellCheckingInspection
class XmRadioMarkMode(Enum):
	"""7 Members, MCM ... USER"""
	MCM = 0
	PATTern = 1
	PULSe = 2
	RATio = 3
	TPL = 4
	TRIGger = 5
	USER = 6


# noinspection SpellCheckingInspection
class WlanStan(Enum):
	"""3 Members, STAN80211A ... STAN80211G"""
	STAN80211A = 0
	STAN80211B = 1
	STAN80211G = 2


# noinspection SpellCheckingInspection
class WlanScrMode(Enum):
	"""5 Members, OFF ... USER"""
	OFF = 0
	ON = 1
	PONLy = 2
	RANDom = 3
	USER = 4


# noinspection SpellCheckingInspection
class WlannTxOutpDest(Enum):
	"""10 Members, BB ... OFF"""
	BB = 0
	BB_B = 1
	BB_C = 2
	BB_D = 3
	BB_E = 4
	BB_F = 5
	BB_G = 6
	BB_H = 7
	FILE = 8
	OFF = 9


# noinspection SpellCheckingInspection
class WlannTxBw(Enum):
	"""5 Members, BW160 ... BW80"""
	BW160 = 0
	BW20 = 1
	BW320 = 2
	BW40 = 3
	BW80 = 4


# noinspection SpellCheckingInspection
class WlannTxAnt(Enum):
	"""8 Members, A1 ... A8"""
	A1 = 0
	A2 = 1
	A3 = 2
	A4 = 3
	A5 = 4
	A6 = 5
	A7 = 6
	A8 = 7


# noinspection SpellCheckingInspection
class WlannMarkMode(Enum):
	"""9 Members, FAPart ... TRIGger"""
	FAPart = 0
	FBLock = 1
	FIPart = 2
	FRAMe = 3
	PATTern = 4
	PULSe = 5
	RATio = 6
	RESTart = 7
	TRIGger = 8


# noinspection SpellCheckingInspection
class WlannFbUserIdx(Enum):
	"""4 Members, UIDX0 ... UIDX3"""
	UIDX0 = 0
	UIDX1 = 1
	UIDX2 = 2
	UIDX3 = 3


# noinspection SpellCheckingInspection
class WlannFbType(Enum):
	"""4 Members, BEACon ... TRIGger"""
	BEACon = 0
	DATA = 1
	SOUNding = 2
	TRIGger = 3


# noinspection SpellCheckingInspection
class WlannFbTxMode(Enum):
	"""27 Members, CCK ... V8080"""
	CCK = 0
	EHT320 = 1
	HE160 = 2
	HE20 = 3
	HE40 = 4
	HE80 = 5
	HE8080 = 6
	HT20 = 7
	HT40 = 8
	HTDup = 9
	HTLow = 10
	HTUP = 11
	L10 = 12
	L20 = 13
	LDUP = 14
	LLOW = 15
	LUP = 16
	PBCC = 17
	S1 = 18
	S16 = 19
	S2 = 20
	S4 = 21
	V160 = 22
	V20 = 23
	V40 = 24
	V80 = 25
	V8080 = 26


# noinspection SpellCheckingInspection
class WlannFbStd(Enum):
	"""8 Members, USER ... WPJ"""
	USER = 0
	WAC = 1
	WAG = 2
	WAX = 3
	WBE = 4
	WBG = 5
	WN = 6
	WPJ = 7


# noinspection SpellCheckingInspection
class WlannFbStbcState(Enum):
	"""2 Members, ACTive ... INACtive"""
	ACTive = 0
	INACtive = 1


# noinspection SpellCheckingInspection
class WlannFbSpatMapMode(Enum):
	"""5 Members, BEAMforming ... OFF"""
	BEAMforming = 0
	DIRect = 1
	EXPansion = 2
	INDirect = 3
	OFF = 4


# noinspection SpellCheckingInspection
class WlannFbSegment(Enum):
	"""3 Members, BOTH ... SEG1"""
	BOTH = 0
	SEG0 = 1
	SEG1 = 2


# noinspection SpellCheckingInspection
class WlannFbScrMode(Enum):
	"""5 Members, OFF ... USER"""
	OFF = 0
	ON = 1
	PREamble = 2
	RANDom = 3
	USER = 4


# noinspection SpellCheckingInspection
class WlannFbPpduUserRuType(Enum):
	"""8 Members, _106 ... C26"""
	_106 = 0
	_242 = 1
	_26 = 2
	_2996 = 3
	_484 = 4
	_52 = 5
	_996 = 6
	C26 = 7


# noinspection SpellCheckingInspection
class WlannFbPpduRuSel(Enum):
	"""39 Members, RU0 ... RU9"""
	RU0 = 0
	RU1 = 1
	RU10 = 2
	RU11 = 3
	RU12 = 4
	RU13 = 5
	RU14 = 6
	RU15 = 7
	RU16 = 8
	RU17 = 9
	RU18 = 10
	RU19 = 11
	RU2 = 12
	RU20 = 13
	RU21 = 14
	RU22 = 15
	RU23 = 16
	RU24 = 17
	RU25 = 18
	RU26 = 19
	RU27 = 20
	RU28 = 21
	RU29 = 22
	RU3 = 23
	RU30 = 24
	RU31 = 25
	RU32 = 26
	RU33 = 27
	RU34 = 28
	RU35 = 29
	RU36 = 30
	RU37 = 31
	RU38 = 32
	RU4 = 33
	RU5 = 34
	RU6 = 35
	RU7 = 36
	RU8 = 37
	RU9 = 38


# noinspection SpellCheckingInspection
class WlannFbPpduPreamblePuncturingBw(Enum):
	"""4 Members, _4 ... _7"""
	_4 = 0
	_5 = 1
	_6 = 2
	_7 = 3


# noinspection SpellCheckingInspection
class WlannFbPpduPeDuraion(Enum):
	"""3 Members, PE0 ... PE8"""
	PE0 = 0
	PE16 = 1
	PE8 = 2


# noinspection SpellCheckingInspection
class WlannFbPpduHeLtfSymbDuraion(Enum):
	"""3 Members, SD128 ... SD64"""
	SD128 = 0
	SD32 = 1
	SD64 = 2


# noinspection SpellCheckingInspection
class WlannFbPpduFormat(Enum):
	"""4 Members, MU ... TRIG"""
	MU = 0
	SU = 1
	SUEXt = 2
	TRIG = 3


# noinspection SpellCheckingInspection
class WlannFbPilotType(Enum):
	"""2 Members, FIXed ... TRAVeling"""
	FIXed = 0
	TRAVeling = 1


# noinspection SpellCheckingInspection
class WlannFbPhyMode(Enum):
	"""3 Members, GFIeld ... MIXed"""
	GFIeld = 0
	LEGacy = 1
	MIXed = 2


# noinspection SpellCheckingInspection
class WlannFbMod(Enum):
	"""7 Members, BPSK ... QPSK"""
	BPSK = 0
	QAM1024 = 1
	QAM16 = 2
	QAM256 = 3
	QAM4096 = 4
	QAM64 = 5
	QPSK = 6


# noinspection SpellCheckingInspection
class WlannFbMcs(Enum):
	"""77 Members, MCS0 ... MCS9"""
	MCS0 = 0
	MCS1 = 1
	MCS10 = 2
	MCS11 = 3
	MCS12 = 4
	MCS13 = 5
	MCS14 = 6
	MCS15 = 7
	MCS16 = 8
	MCS17 = 9
	MCS18 = 10
	MCS19 = 11
	MCS2 = 12
	MCS20 = 13
	MCS21 = 14
	MCS22 = 15
	MCS23 = 16
	MCS24 = 17
	MCS25 = 18
	MCS26 = 19
	MCS27 = 20
	MCS28 = 21
	MCS29 = 22
	MCS3 = 23
	MCS30 = 24
	MCS31 = 25
	MCS32 = 26
	MCS33 = 27
	MCS34 = 28
	MCS35 = 29
	MCS36 = 30
	MCS37 = 31
	MCS38 = 32
	MCS39 = 33
	MCS4 = 34
	MCS40 = 35
	MCS41 = 36
	MCS42 = 37
	MCS43 = 38
	MCS44 = 39
	MCS45 = 40
	MCS46 = 41
	MCS47 = 42
	MCS48 = 43
	MCS49 = 44
	MCS5 = 45
	MCS50 = 46
	MCS51 = 47
	MCS52 = 48
	MCS53 = 49
	MCS54 = 50
	MCS55 = 51
	MCS56 = 52
	MCS57 = 53
	MCS58 = 54
	MCS59 = 55
	MCS6 = 56
	MCS60 = 57
	MCS61 = 58
	MCS62 = 59
	MCS63 = 60
	MCS64 = 61
	MCS65 = 62
	MCS66 = 63
	MCS67 = 64
	MCS68 = 65
	MCS69 = 66
	MCS7 = 67
	MCS70 = 68
	MCS71 = 69
	MCS72 = 70
	MCS73 = 71
	MCS74 = 72
	MCS75 = 73
	MCS76 = 74
	MCS8 = 75
	MCS9 = 76


# noinspection SpellCheckingInspection
class WlannFbGuard(Enum):
	"""5 Members, GD08 ... SHORt"""
	GD08 = 0
	GD16 = 1
	GD32 = 2
	LONG = 3
	SHORt = 4


# noinspection SpellCheckingInspection
class WlannFbEncoder(Enum):
	"""12 Members, E1 ... E9"""
	E1 = 0
	E10 = 1
	E11 = 2
	E12 = 3
	E2 = 4
	E3 = 5
	E4 = 6
	E5 = 7
	E6 = 8
	E7 = 9
	E8 = 10
	E9 = 11


# noinspection SpellCheckingInspection
class WlannFbDynBwInNonHt(Enum):
	"""3 Members, DYN ... STAT"""
	DYN = 0
	OFF = 1
	STAT = 2


# noinspection SpellCheckingInspection
class WlannFbCodType(Enum):
	"""3 Members, BCC ... OFF"""
	BCC = 0
	LDPC = 1
	OFF = 2


# noinspection SpellCheckingInspection
class WlannFbCodRate(Enum):
	"""4 Members, CR1D2 ... CR5D6"""
	CR1D2 = 0
	CR2D3 = 1
	CR3D4 = 2
	CR5D6 = 3


# noinspection SpellCheckingInspection
class WlannFbChBwInNonHt(Enum):
	"""5 Members, B160 ... OFF"""
	B160 = 0
	B20 = 1
	B40 = 2
	B80 = 3
	OFF = 4


# noinspection SpellCheckingInspection
class WlannDataSource(Enum):
	"""12 Members, AMPDU ... ZERO"""
	AMPDU = 0
	DLISt = 1
	ONE = 2
	PATTern = 3
	PN11 = 4
	PN15 = 5
	PN16 = 6
	PN20 = 7
	PN21 = 8
	PN23 = 9
	PN9 = 10
	ZERO = 11


# noinspection SpellCheckingInspection
class WlanMode(Enum):
	"""2 Members, FRAMed ... UNFRamed"""
	FRAMed = 0
	UNFRamed = 1


# noinspection SpellCheckingInspection
class WlanMarkMode(Enum):
	"""7 Members, FACTive ... TRIGger"""
	FACTive = 0
	FRAMe = 1
	PATTern = 2
	PULSe = 3
	RATio = 4
	RESTart = 5
	TRIGger = 6


# noinspection SpellCheckingInspection
class WlanFramType(Enum):
	"""5 Members, ACK ... USER"""
	ACK = 0
	CTS = 1
	DATA = 2
	RTS = 3
	USER = 4


# noinspection SpellCheckingInspection
class WlanCodMode(Enum):
	"""3 Members, CCK ... PBCC"""
	CCK = 0
	OFDM = 1
	PBCC = 2


# noinspection SpellCheckingInspection
class WcdmaUlDtxThreshold(Enum):
	"""8 Members, _1 ... _8"""
	_1 = 0
	_128 = 1
	_16 = 2
	_256 = 3
	_32 = 4
	_4 = 5
	_64 = 6
	_8 = 7


# noinspection SpellCheckingInspection
class WcdmaUlDtxMode(Enum):
	"""2 Members, UDTX ... USCH"""
	UDTX = 0
	USCH = 1


# noinspection SpellCheckingInspection
class WcdmaUlDtxLongPreLen(Enum):
	"""3 Members, _15 ... _4"""
	_15 = 0
	_2 = 1
	_4 = 2


# noinspection SpellCheckingInspection
class WcdmaUlDtxCycle(Enum):
	"""13 Members, _1 ... _80"""
	_1 = 0
	_10 = 1
	_128 = 2
	_16 = 3
	_160 = 4
	_20 = 5
	_32 = 6
	_4 = 7
	_40 = 8
	_5 = 9
	_64 = 10
	_8 = 11
	_80 = 12


# noinspection SpellCheckingInspection
class WcdmaUlDtxBurstLen(Enum):
	"""3 Members, _1 ... _5"""
	_1 = 0
	_2 = 1
	_5 = 2


# noinspection SpellCheckingInspection
class WcdmaSymbRateEdPdchOverallSymbRate(Enum):
	"""14 Members, D120k ... D960k"""
	D120k = 0
	D15K = 1
	D1920k = 2
	D240k = 3
	D2880k = 4
	D2X1920K = 5
	D2X960K2X1920K = 6
	D30K = 7
	D3840k = 8
	D4800k = 9
	D480k = 10
	D5760k = 11
	D60K = 12
	D960k = 13


# noinspection SpellCheckingInspection
class WcdmaLevRef(Enum):
	"""7 Members, DPCC ... RMS"""
	DPCC = 0
	EDCH = 1
	HACK = 2
	LPP = 3
	PCQI = 4
	PMP = 5
	RMS = 6


# noinspection SpellCheckingInspection
class VrbToPrbInterleaverAll(Enum):
	"""3 Members, VP2 ... VPN"""
	VP2 = 0
	VP4 = 1
	VPN = 2


# noinspection SpellCheckingInspection
class VimDmeTrigMode(Enum):
	"""4 Members, AUTO ... PSENsor"""
	AUTO = 0
	EGATe = 1
	EXTernal = 2
	PSENsor = 3


# noinspection SpellCheckingInspection
class ViewType(Enum):
	"""2 Members, DISTance ... HEIGht"""
	DISTance = 0
	HEIGht = 1


# noinspection SpellCheckingInspection
class UtraTcwtMcodes(Enum):
	"""5 Members, COD16 ... COD8"""
	COD16 = 0
	COD32 = 1
	COD4 = 2
	COD64 = 3
	COD8 = 4


# noinspection SpellCheckingInspection
class UtraTcwsPec(Enum):
	"""1 Members, TS36141 ... TS36141"""
	TS36141 = 0


# noinspection SpellCheckingInspection
class UtraTcwgssUbtest(Enum):
	"""4 Members, STC1 ... STC4"""
	STC1 = 0
	STC2 = 1
	STC3 = 2
	STC4 = 3


# noinspection SpellCheckingInspection
class UtraTcwgsoPtion(Enum):
	"""2 Members, OPT1 ... OPT2"""
	OPT1 = 0
	OPT2 = 1


# noinspection SpellCheckingInspection
class UtraTcwbSclass(Enum):
	"""4 Members, HOME ... WIDE"""
	HOME = 0
	LOCal = 1
	MEDium = 2
	WIDE = 3


# noinspection SpellCheckingInspection
class UtraTcwaCkNackBits(Enum):
	"""2 Members, ANB16 ... ANB4"""
	ANB16 = 0
	ANB4 = 1


# noinspection SpellCheckingInspection
class UpdPolicyMode(Enum):
	"""3 Members, CONFirm ... STRict"""
	CONFirm = 0
	IGNore = 1
	STRict = 2


# noinspection SpellCheckingInspection
class UpDownDirection(Enum):
	"""2 Members, DOWN ... UP"""
	DOWN = 0
	UP = 1


# noinspection SpellCheckingInspection
class Unknown(Enum):
	"""2 Members, DBM ... V"""
	DBM = 0
	V = 1


# noinspection SpellCheckingInspection
class UnitTimeSecMs(Enum):
	"""2 Members, MS ... S"""
	MS = 0
	S = 1


# noinspection SpellCheckingInspection
class UnitSpeed(Enum):
	"""4 Members, KMH ... NMPH"""
	KMH = 0
	MPH = 1
	MPS = 2
	NMPH = 3


# noinspection SpellCheckingInspection
class UnitSlXmRadio(Enum):
	"""3 Members, MCM ... TPL"""
	MCM = 0
	SAMPle = 1
	TPL = 2


# noinspection SpellCheckingInspection
class UnitSlW3Gpp(Enum):
	"""4 Members, CHIP ... SLOT"""
	CHIP = 0
	FRAMe = 1
	SEQuence = 2
	SLOT = 3


# noinspection SpellCheckingInspection
class UnitSlGsm(Enum):
	"""2 Members, FRAMe ... SYMBol"""
	FRAMe = 0
	SYMBol = 1


# noinspection SpellCheckingInspection
class UnitSlEvdo(Enum):
	"""3 Members, CHIP ... SLOT"""
	CHIP = 0
	SEQuence = 1
	SLOT = 2


# noinspection SpellCheckingInspection
class UnitSlDvb(Enum):
	"""2 Members, FRAMe ... SEQuence"""
	FRAMe = 0
	SEQuence = 1


# noinspection SpellCheckingInspection
class UnitSlBto(Enum):
	"""3 Members, EVENt ... SEQuence"""
	EVENt = 0
	FRAMe = 1
	SEQuence = 2


# noinspection SpellCheckingInspection
class UnitSlB(Enum):
	"""2 Members, SAMPle ... SEQuence"""
	SAMPle = 0
	SEQuence = 1


# noinspection SpellCheckingInspection
class UnitSlA(Enum):
	"""3 Members, CHIP ... SEQuence"""
	CHIP = 0
	FRAMe = 1
	SEQuence = 2


# noinspection SpellCheckingInspection
class UnitPowSens(Enum):
	"""3 Members, DBM ... WATT"""
	DBM = 0
	DBUV = 1
	WATT = 2


# noinspection SpellCheckingInspection
class UnitPower(Enum):
	"""3 Members, DBM ... V"""
	DBM = 0
	DBUV = 1
	V = 2


# noinspection SpellCheckingInspection
class UnitNmAvionic(Enum):
	"""2 Members, NM ... US"""
	NM = 0
	US = 1


# noinspection SpellCheckingInspection
class UnitAngle(Enum):
	"""3 Members, DEGree ... RADian"""
	DEGree = 0
	DEGRee = 1
	RADian = 2


# noinspection SpellCheckingInspection
class UnchOff(Enum):
	"""2 Members, OFF ... UNCHanged"""
	OFF = 0
	UNCHanged = 1


# noinspection SpellCheckingInspection
class UlfReqHopping(Enum):
	"""3 Members, DIS ... INTRA"""
	DIS = 0
	INTER = 1
	INTRA = 2


# noinspection SpellCheckingInspection
class UcibIts(Enum):
	"""2 Members, B_40 ... B_7"""
	B_40 = 0
	B_7 = 1


# noinspection SpellCheckingInspection
class TxDiv(Enum):
	"""4 Members, ANT1 ... SANT"""
	ANT1 = 0
	ANT2 = 1
	OFF = 2
	SANT = 3


# noinspection SpellCheckingInspection
class TxConfigAll(Enum):
	"""2 Members, CB ... NCB"""
	CB = 0
	NCB = 1


# noinspection SpellCheckingInspection
class TxAntennaGnss(Enum):
	"""6 Members, ALL ... NONE"""
	ALL = 0
	ANT1 = 1
	ANT2 = 2
	ANT3 = 3
	ANT4 = 4
	NONE = 5


# noinspection SpellCheckingInspection
class TxAntenna(Enum):
	"""2 Members, ANT1 ... ANT2"""
	ANT1 = 0
	ANT2 = 1


# noinspection SpellCheckingInspection
class TropModel(Enum):
	"""3 Members, MOPS ... STANag"""
	MOPS = 0
	NONE = 1
	STANag = 2


# noinspection SpellCheckingInspection
class Tristate(Enum):
	"""6 Members, _0 ... ON"""
	_0 = 0
	_1 = 1
	_2 = 2
	NOvalue = 3
	OFF = 4
	ON = 5


# noinspection SpellCheckingInspection
class TrigSweepSourNoHopExtAuto(Enum):
	"""5 Members, AUTO ... SINGle"""
	AUTO = 0
	BUS = 1
	EXTernal = 2
	IMMediate = 3
	SINGle = 4


# noinspection SpellCheckingInspection
class TrigSweepImmBusExt(Enum):
	"""3 Members, BUS ... IMMediate"""
	BUS = 0
	EXTernal = 1
	IMMediate = 2


# noinspection SpellCheckingInspection
class TrigSourBerBler(Enum):
	"""2 Members, EGT1 ... INTernal"""
	EGT1 = 0
	INTernal = 1


# noinspection SpellCheckingInspection
class TrigRunMode(Enum):
	"""2 Members, RUN ... STOP"""
	RUN = 0
	STOP = 1


# noinspection SpellCheckingInspection
class TriggerSourceC(Enum):
	"""13 Members, BBSY ... OBASeband"""
	BBSY = 0
	BEXTernal = 1
	EGC1 = 2
	EGC2 = 3
	EGT1 = 4
	EGT2 = 5
	ELCLock = 6
	ELTRigger = 7
	EXTernal = 8
	INTA = 9
	INTB = 10
	INTernal = 11
	OBASeband = 12


# noinspection SpellCheckingInspection
class TriggerSourceB(Enum):
	"""4 Members, BEXTernal ... OBASeband"""
	BEXTernal = 0
	EXTernal = 1
	INTernal = 2
	OBASeband = 3


# noinspection SpellCheckingInspection
class TriggerSourceA(Enum):
	"""5 Members, BBSY ... INTernal"""
	BBSY = 0
	EGC1 = 1
	EGT1 = 2
	EXTernal = 3
	INTernal = 4


# noinspection SpellCheckingInspection
class TriggerMarkModeB(Enum):
	"""5 Members, PATTern ... TRIGger"""
	PATTern = 0
	PULSe = 1
	RATio = 2
	RESTart = 3
	TRIGger = 4


# noinspection SpellCheckingInspection
class TriggerMarkModeA(Enum):
	"""6 Members, PATTern ... UNCHanged"""
	PATTern = 0
	PULSe = 1
	RATio = 2
	RESTart = 3
	TRIGger = 4
	UNCHanged = 5


# noinspection SpellCheckingInspection
class TrigDelUnit(Enum):
	"""2 Members, SAMPle ... TIME"""
	SAMPle = 0
	TIME = 1


# noinspection SpellCheckingInspection
class TrigConf(Enum):
	"""2 Members, AAUT ... UNCH"""
	AAUT = 0
	UNCH = 1


# noinspection SpellCheckingInspection
class TranRecTrigSour(Enum):
	"""2 Members, MARKer ... SOFTware"""
	MARKer = 0
	SOFTware = 1


# noinspection SpellCheckingInspection
class TranRecSour(Enum):
	"""6 Members, BBA ... STRA"""
	BBA = 0
	BBIA = 1
	DO1 = 2
	IQO1 = 3
	RFA = 4
	STRA = 5


# noinspection SpellCheckingInspection
class TranRecSize(Enum):
	"""2 Members, MAXimized ... MINimized"""
	MAXimized = 0
	MINimized = 1


# noinspection SpellCheckingInspection
class TranRecSampFactMode(Enum):
	"""3 Members, AUTO ... USER"""
	AUTO = 0
	FULL = 1
	USER = 2


# noinspection SpellCheckingInspection
class TranRecMode(Enum):
	"""7 Members, CCDF ... VECTor"""
	CCDF = 0
	CONStellation = 1
	EYEI = 2
	EYEQ = 3
	IQ = 4
	PSPectrum = 5
	VECTor = 6


# noinspection SpellCheckingInspection
class TranRecFftLen(Enum):
	"""5 Members, LEN1024 ... LEN512"""
	LEN1024 = 0
	LEN2048 = 1
	LEN256 = 2
	LEN4096 = 3
	LEN512 = 4


# noinspection SpellCheckingInspection
class TpcReadMode(Enum):
	"""5 Members, CONTinuous ... S1A"""
	CONTinuous = 0
	S01A = 1
	S0A = 2
	S10A = 3
	S1A = 4


# noinspection SpellCheckingInspection
class TpcMode(Enum):
	"""2 Members, D2B ... D4B"""
	D2B = 0
	D4B = 1


# noinspection SpellCheckingInspection
class TpcDataSour(Enum):
	"""4 Members, DLISt ... ZERO"""
	DLISt = 0
	ONE = 1
	PATTern = 2
	ZERO = 3


# noinspection SpellCheckingInspection
class TimingAdjustmentOffsetAll(Enum):
	"""4 Members, N0 ... N39936"""
	N0 = 0
	N13792 = 1
	N25600 = 2
	N39936 = 3


# noinspection SpellCheckingInspection
class TimeBasis(Enum):
	"""6 Members, BDT ... UTC"""
	BDT = 0
	GLO = 1
	GPS = 2
	GST = 3
	NAV = 4
	UTC = 5


# noinspection SpellCheckingInspection
class TestSpec(Enum):
	"""2 Members, TS38141_1 ... TS38141_2"""
	TS38141_1 = 0
	TS38141_2 = 1


# noinspection SpellCheckingInspection
class TestSetup(Enum):
	"""2 Members, TS_1 ... TS_2"""
	TS_1 = 0
	TS_2 = 1


# noinspection SpellCheckingInspection
class TestRequire(Enum):
	"""2 Members, BLPE ... COBS"""
	BLPE = 0
	COBS = 1


# noinspection SpellCheckingInspection
class TestModel(Enum):
	"""1 Members, TM1_1 ... TM1_1"""
	TM1_1 = 0


# noinspection SpellCheckingInspection
class TestExtIqMode(Enum):
	"""2 Members, IQIN ... IQOut"""
	IQIN = 0
	IQOut = 1


# noinspection SpellCheckingInspection
class TestCase(Enum):
	"""45 Members, TS381411_TC67 ... TS381412_TC841"""
	TS381411_TC67 = 0
	TS381411_TC72 = 1
	TS381411_TC73 = 2
	TS381411_TC741 = 3
	TS381411_TC742A = 4
	TS381411_TC742B = 5
	TS381411_TC75 = 6
	TS381411_TC77 = 7
	TS381411_TC78 = 8
	TS381411_TC821 = 9
	TS381411_TC822 = 10
	TS381411_TC823 = 11
	TS381411_TC831 = 12
	TS381411_TC8321 = 13
	TS381411_TC8322 = 14
	TS381411_TC8331 = 15
	TS381411_TC8332 = 16
	TS381411_TC834 = 17
	TS381411_TC835 = 18
	TS381411_TC8361A = 19
	TS381411_TC8361B = 20
	TS381411_TC841 = 21
	TS381412_TC68 = 22
	TS381412_TC72 = 23
	TS381412_TC73 = 24
	TS381412_TC74 = 25
	TS381412_TC751 = 26
	TS381412_TC752A = 27
	TS381412_TC752B = 28
	TS381412_TC76 = 29
	TS381412_TC78 = 30
	TS381412_TC79 = 31
	TS381412_TC821 = 32
	TS381412_TC822 = 33
	TS381412_TC823 = 34
	TS381412_TC831 = 35
	TS381412_TC8321 = 36
	TS381412_TC8322 = 37
	TS381412_TC8331 = 38
	TS381412_TC8332 = 39
	TS381412_TC834 = 40
	TS381412_TC835 = 41
	TS381412_TC8361A = 42
	TS381412_TC8361B = 43
	TS381412_TC841 = 44


# noinspection SpellCheckingInspection
class TestBbGenIqSour(Enum):
	"""3 Members, ARB ... SINE"""
	ARB = 0
	CONStant = 1
	SINE = 2


# noinspection SpellCheckingInspection
class TestBbBncConn(Enum):
	"""6 Members, AUTO ... USER5"""
	AUTO = 0
	USER1 = 1
	USER2 = 2
	USER3 = 3
	USER4 = 4
	USER5 = 5


# noinspection SpellCheckingInspection
class Test(Enum):
	"""4 Members, _0 ... STOPped"""
	_0 = 0
	_1 = 1
	RUNning = 2
	STOPped = 3


# noinspection SpellCheckingInspection
class TdscdmaTotalUsers(Enum):
	"""8 Members, _10 ... _8"""
	_10 = 0
	_12 = 1
	_14 = 2
	_16 = 3
	_2 = 4
	_4 = 5
	_6 = 6
	_8 = 7


# noinspection SpellCheckingInspection
class TdscdmaTfciLen(Enum):
	"""9 Members, _0 ... _8"""
	_0 = 0
	_12 = 1
	_16 = 2
	_24 = 3
	_32 = 4
	_4 = 5
	_48 = 6
	_6 = 7
	_8 = 8


# noinspection SpellCheckingInspection
class TdscdmaSyncShiftLen(Enum):
	"""8 Members, _0 ... _8"""
	_0 = 0
	_16 = 1
	_2 = 2
	_3 = 3
	_32 = 4
	_4 = 5
	_48 = 6
	_8 = 7


# noinspection SpellCheckingInspection
class TdscdmaSpreadFactor(Enum):
	"""5 Members, _1 ... _8"""
	_1 = 0
	_16 = 1
	_2 = 2
	_4 = 3
	_8 = 4


# noinspection SpellCheckingInspection
class TdscdmaSlotModeUp(Enum):
	"""2 Members, DEDicated ... PRACh"""
	DEDicated = 0
	PRACh = 1


# noinspection SpellCheckingInspection
class TdscdmaPhasRot(Enum):
	"""3 Members, AUTO ... S2"""
	AUTO = 0
	S1 = 1
	S2 = 2


# noinspection SpellCheckingInspection
class TdscdmaMarkMode(Enum):
	"""7 Members, CSPeriod ... USER"""
	CSPeriod = 0
	FACTive = 1
	RATio = 2
	RFRame = 3
	SFNR = 4
	TRIGger = 5
	USER = 6


# noinspection SpellCheckingInspection
class TdscdmaEnhTchTti(Enum):
	"""5 Members, _10MS ... _80MS"""
	_10MS = 0
	_20MS = 1
	_40MS = 2
	_5MS = 3
	_80MS = 4


# noinspection SpellCheckingInspection
class TdscdmaEnhHsTbsTableUp(Enum):
	"""2 Members, C1TO2 ... C3TO6"""
	C1TO2 = 0
	C3TO6 = 1


# noinspection SpellCheckingInspection
class TdscdmaEnhHsTbsTableDn(Enum):
	"""8 Members, C10TO12 ... C7TO9"""
	C10TO12 = 0
	C13TO15 = 1
	C16TO18 = 2
	C19TO21 = 3
	C1TO3 = 4
	C22TO24 = 5
	C4TO6 = 6
	C7TO9 = 7


# noinspection SpellCheckingInspection
class TdscdmaEnhHsRmcMode(Enum):
	"""13 Members, HRMC_0M5_QPSK ... USER"""
	HRMC_0M5_QPSK = 0
	HRMC_1M1_16QAM = 1
	HRMC_1M1_QPSK = 2
	HRMC_1M6_16QAM = 3
	HRMC_1M6_QPSK = 4
	HRMC_2M2_16QAM = 5
	HRMC_2M2_QPSK = 6
	HRMC_2M8_16QAM = 7
	HRMC_2M8_QPSK = 8
	HRMC_64QAM_16UE = 9
	HRMC_64QAM_19UE = 10
	HRMC_64QAM_22UE = 11
	USER = 12


# noinspection SpellCheckingInspection
class TdscdmaEnhHsFrcMode(Enum):
	"""5 Members, _1 ... USER"""
	_1 = 0
	_2 = 1
	_3 = 2
	_4 = 3
	USER = 4


# noinspection SpellCheckingInspection
class TdscdmaDchCoding(Enum):
	"""16 Members, HRMC526K ... USER"""
	HRMC526K = 0
	HRMC730K = 1
	HS_SICH = 2
	HSDPA = 3
	HSUPA = 4
	PLCCH = 5
	RMC12K2 = 6
	RMC144K = 7
	RMC2048K = 8
	RMC384K = 9
	RMC64K = 10
	UP_RMC12K2 = 11
	UP_RMC144K = 12
	UP_RMC384K = 13
	UP_RMC64K = 14
	USER = 15


# noinspection SpellCheckingInspection
class TdscdmaChipRate(Enum):
	"""1 Members, R1M28 ... R1M28"""
	R1M28 = 0


# noinspection SpellCheckingInspection
class TdscdmaChanType(Enum):
	"""23 Members, DPCH_8PSQ ... UP_DPCH_QPSK"""
	DPCH_8PSQ = 0
	DPCH_QPSQ = 1
	E_PUCH_16QAM = 2
	E_PUCH_QPSK = 3
	E_RUCCH = 4
	EAGCH = 5
	EHICH = 6
	FPACH = 7
	HS_PDS_16QAM = 8
	HS_PDS_64QAM = 9
	HS_PDS_QPSK = 10
	HS_SCCH1 = 11
	HS_SCCH2 = 12
	HS_SICH = 13
	P_CCPCH1 = 14
	P_CCPCH2 = 15
	PDSCH = 16
	PLCCH = 17
	PUSCH = 18
	S_CCPCH1 = 19
	S_CCPCH2 = 20
	UP_DPCH_8PSK = 21
	UP_DPCH_QPSK = 22


# noinspection SpellCheckingInspection
class TcwpRachNum(Enum):
	"""5 Members, N1_25 ... N60"""
	N1_25 = 0
	N120 = 1
	N15 = 2
	N30 = 3
	N60 = 4


# noinspection SpellCheckingInspection
class TcwpRachFormat(Enum):
	"""7 Members, F0 ... FC2"""
	F0 = 0
	FA1 = 1
	FA2 = 2
	FA3 = 3
	FB4 = 4
	FC0 = 5
	FC2 = 6


# noinspection SpellCheckingInspection
class TcwfEedbackMode(Enum):
	"""2 Members, S3X8 ... SERial"""
	S3X8 = 0
	SERial = 1


# noinspection SpellCheckingInspection
class TchTranTimInt(Enum):
	"""4 Members, _10MS ... _80MS"""
	_10MS = 0
	_20MS = 1
	_40MS = 2
	_80MS = 3


# noinspection SpellCheckingInspection
class TchCrc(Enum):
	"""5 Members, _12 ... NONE"""
	_12 = 0
	_16 = 1
	_24 = 2
	_8 = 3
	NONE = 4


# noinspection SpellCheckingInspection
class TbAlign(Enum):
	"""2 Members, EVEN ... ODD"""
	EVEN = 0
	ODD = 1


# noinspection SpellCheckingInspection
class SystConfOutpMode(Enum):
	"""6 Members, ALL ... HSDigital"""
	ALL = 0
	ANALog = 1
	DIGital = 2
	DIGMux = 3
	HSALl = 4
	HSDigital = 5


# noinspection SpellCheckingInspection
class SystConfOutpMapMatMode(Enum):
	"""3 Members, ADD ... SINGle"""
	ADD = 0
	MULTiplex = 1
	SINGle = 2


# noinspection SpellCheckingInspection
class SystConfHsChannels(Enum):
	"""9 Members, CH0 ... CH8"""
	CH0 = 0
	CH1 = 1
	CH2 = 2
	CH3 = 3
	CH4 = 4
	CH5 = 5
	CH6 = 6
	CH7 = 7
	CH8 = 8


# noinspection SpellCheckingInspection
class SystConfBbConf(Enum):
	"""3 Members, COUPled ... SEParate"""
	COUPled = 0
	CPENtity = 1
	SEParate = 2


# noinspection SpellCheckingInspection
class SymbRate(Enum):
	"""15 Members, D120k ... D960k"""
	D120k = 0
	D15K = 1
	D1920k = 2
	D240k = 3
	D2880k = 4
	D2X1920K = 5
	D2X960K2X1920K = 6
	D30K = 7
	D3840k = 8
	D4800k = 9
	D480k = 10
	D5760k = 11
	D60K = 12
	D7K5 = 13
	D960k = 14


# noinspection SpellCheckingInspection
class SweepType(Enum):
	"""2 Members, ADVanced ... STANdard"""
	ADVanced = 0
	STANdard = 1


# noinspection SpellCheckingInspection
class SweCyclMode(Enum):
	"""2 Members, SAWTooth ... TRIangle"""
	SAWTooth = 0
	TRIangle = 1


# noinspection SpellCheckingInspection
class SvId(Enum):
	"""201 Members, _1 ... ALL"""
	_1 = 0
	_10 = 1
	_100 = 2
	_101 = 3
	_102 = 4
	_103 = 5
	_104 = 6
	_105 = 7
	_106 = 8
	_107 = 9
	_108 = 10
	_109 = 11
	_11 = 12
	_110 = 13
	_111 = 14
	_112 = 15
	_113 = 16
	_114 = 17
	_115 = 18
	_116 = 19
	_117 = 20
	_118 = 21
	_119 = 22
	_12 = 23
	_120 = 24
	_121 = 25
	_122 = 26
	_123 = 27
	_124 = 28
	_125 = 29
	_126 = 30
	_127 = 31
	_128 = 32
	_129 = 33
	_13 = 34
	_130 = 35
	_131 = 36
	_132 = 37
	_133 = 38
	_134 = 39
	_135 = 40
	_136 = 41
	_137 = 42
	_138 = 43
	_139 = 44
	_14 = 45
	_140 = 46
	_141 = 47
	_142 = 48
	_143 = 49
	_144 = 50
	_145 = 51
	_146 = 52
	_147 = 53
	_148 = 54
	_149 = 55
	_15 = 56
	_150 = 57
	_151 = 58
	_152 = 59
	_153 = 60
	_154 = 61
	_155 = 62
	_156 = 63
	_157 = 64
	_158 = 65
	_159 = 66
	_16 = 67
	_160 = 68
	_161 = 69
	_162 = 70
	_163 = 71
	_164 = 72
	_165 = 73
	_166 = 74
	_167 = 75
	_168 = 76
	_169 = 77
	_17 = 78
	_170 = 79
	_171 = 80
	_172 = 81
	_173 = 82
	_174 = 83
	_175 = 84
	_176 = 85
	_177 = 86
	_178 = 87
	_179 = 88
	_18 = 89
	_180 = 90
	_181 = 91
	_182 = 92
	_183 = 93
	_184 = 94
	_185 = 95
	_186 = 96
	_187 = 97
	_188 = 98
	_189 = 99
	_19 = 100
	_190 = 101
	_191 = 102
	_192 = 103
	_193 = 104
	_194 = 105
	_195 = 106
	_196 = 107
	_197 = 108
	_198 = 109
	_199 = 110
	_2 = 111
	_20 = 112
	_200 = 113
	_21 = 114
	_22 = 115
	_23 = 116
	_24 = 117
	_25 = 118
	_26 = 119
	_27 = 120
	_28 = 121
	_29 = 122
	_3 = 123
	_30 = 124
	_31 = 125
	_32 = 126
	_33 = 127
	_34 = 128
	_35 = 129
	_36 = 130
	_37 = 131
	_38 = 132
	_39 = 133
	_4 = 134
	_40 = 135
	_41 = 136
	_42 = 137
	_43 = 138
	_44 = 139
	_45 = 140
	_46 = 141
	_47 = 142
	_48 = 143
	_49 = 144
	_5 = 145
	_50 = 146
	_51 = 147
	_52 = 148
	_53 = 149
	_54 = 150
	_55 = 151
	_56 = 152
	_57 = 153
	_58 = 154
	_59 = 155
	_6 = 156
	_60 = 157
	_61 = 158
	_62 = 159
	_63 = 160
	_64 = 161
	_65 = 162
	_66 = 163
	_67 = 164
	_68 = 165
	_69 = 166
	_7 = 167
	_70 = 168
	_71 = 169
	_72 = 170
	_73 = 171
	_74 = 172
	_75 = 173
	_76 = 174
	_77 = 175
	_78 = 176
	_79 = 177
	_8 = 178
	_80 = 179
	_81 = 180
	_82 = 181
	_83 = 182
	_84 = 183
	_85 = 184
	_86 = 185
	_87 = 186
	_88 = 187
	_89 = 188
	_9 = 189
	_90 = 190
	_91 = 191
	_92 = 192
	_93 = 193
	_94 = 194
	_95 = 195
	_96 = 196
	_97 = 197
	_98 = 198
	_99 = 199
	ALL = 200


# noinspection SpellCheckingInspection
class StateExtended(Enum):
	"""6 Members, _0 ... ON"""
	_0 = 0
	_1 = 1
	_2 = 2
	DEFault = 3
	OFF = 4
	ON = 5


# noinspection SpellCheckingInspection
class SspbchBitLengthAll(Enum):
	"""3 Members, L4 ... L8"""
	L4 = 0
	L64 = 1
	L8 = 2


# noinspection SpellCheckingInspection
class SrsRsTransComboAll(Enum):
	"""2 Members, TC2 ... TC4"""
	TC2 = 0
	TC4 = 1


# noinspection SpellCheckingInspection
class SrsRsSetUsageAll(Enum):
	"""4 Members, ASW ... NCB"""
	ASW = 0
	BM = 1
	CB = 2
	NCB = 3


# noinspection SpellCheckingInspection
class SrsRsSetRsTypeAll(Enum):
	"""3 Members, APER ... SP"""
	APER = 0
	PER = 1
	SP = 2


# noinspection SpellCheckingInspection
class SrsRsRepFactorAll(Enum):
	"""3 Members, REP1 ... REP4"""
	REP1 = 0
	REP2 = 1
	REP4 = 2


# noinspection SpellCheckingInspection
class SrsRsPeriodicityAll(Enum):
	"""17 Members, SL1 ... SL80"""
	SL1 = 0
	SL10 = 1
	SL1280 = 2
	SL16 = 3
	SL160 = 4
	SL2 = 5
	SL20 = 6
	SL2560 = 7
	SL32 = 8
	SL320 = 9
	SL4 = 10
	SL40 = 11
	SL5 = 12
	SL64 = 13
	SL640 = 14
	SL8 = 15
	SL80 = 16


# noinspection SpellCheckingInspection
class SrsRsNumSymbolsAll(Enum):
	"""3 Members, SYM1 ... SYM4"""
	SYM1 = 0
	SYM2 = 1
	SYM4 = 2


# noinspection SpellCheckingInspection
class SrsPtrsPortIdx(Enum):
	"""2 Members, P0 ... P1"""
	P0 = 0
	P1 = 1


# noinspection SpellCheckingInspection
class Spacing(Enum):
	"""3 Members, LINear ... RAMP"""
	LINear = 0
	LOGarithmic = 1
	RAMP = 2


# noinspection SpellCheckingInspection
class SourceInt(Enum):
	"""2 Members, EXTernal ... INTernal"""
	EXTernal = 0
	INTernal = 1


# noinspection SpellCheckingInspection
class SlopeType(Enum):
	"""2 Members, NEGative ... POSitive"""
	NEGative = 0
	POSitive = 1


# noinspection SpellCheckingInspection
class SiriusTerrMod(Enum):
	"""1 Members, COFDM ... COFDM"""
	COFDM = 0


# noinspection SpellCheckingInspection
class SiriusTerrMarkMode(Enum):
	"""6 Members, FRAMe ... USER"""
	FRAMe = 0
	RATio = 1
	SFRame = 2
	SYMBol = 3
	TRIGger = 4
	USER = 5


# noinspection SpellCheckingInspection
class SiriusSatMod(Enum):
	"""3 Members, P8INV ... QPSK"""
	P8INV = 0
	PSK8 = 1
	QPSK = 2


# noinspection SpellCheckingInspection
class SiriusSatMarkMode(Enum):
	"""6 Members, FRAMe ... USER"""
	FRAMe = 0
	PATTern = 1
	PULSe = 2
	RATio = 3
	TRIGger = 4
	USER = 5


# noinspection SpellCheckingInspection
class SiriusPhysLayer(Enum):
	"""3 Members, SAT1 ... TERR"""
	SAT1 = 0
	SAT2 = 1
	TERR = 2


# noinspection SpellCheckingInspection
class SiriusLayer(Enum):
	"""2 Members, LEGacy ... OVERlay"""
	LEGacy = 0
	OVERlay = 1


# noinspection SpellCheckingInspection
class SingExtAuto(Enum):
	"""8 Members, AUTO ... SINGle"""
	AUTO = 0
	BUS = 1
	DHOP = 2
	EAUTo = 3
	EXTernal = 4
	HOP = 5
	IMMediate = 6
	SINGle = 7


# noinspection SpellCheckingInspection
class SimMode2(Enum):
	"""2 Members, NAVigation ... TRACking"""
	NAVigation = 0
	TRACking = 1


# noinspection SpellCheckingInspection
class SeqGrpHoppingAll(Enum):
	"""3 Members, GRP ... SEQ"""
	GRP = 0
	N = 1
	SEQ = 2


# noinspection SpellCheckingInspection
class SelftLevWrite(Enum):
	"""4 Members, CUSTomer ... SERVice"""
	CUSTomer = 0
	NONE = 1
	PRODuction = 2
	SERVice = 3


# noinspection SpellCheckingInspection
class SelftLev(Enum):
	"""3 Members, CUSTomer ... SERVice"""
	CUSTomer = 0
	PRODuction = 1
	SERVice = 2


# noinspection SpellCheckingInspection
class SelCriteria(Enum):
	"""3 Members, ELEVation ... VISibility"""
	ELEVation = 0
	MANual = 1
	VISibility = 2


# noinspection SpellCheckingInspection
class ScscOmmon(Enum):
	"""2 Members, N15_60 ... N30_120"""
	N15_60 = 0
	N30_120 = 1


# noinspection SpellCheckingInspection
class ScrCodeMode(Enum):
	"""3 Members, LONG ... SHORt"""
	LONG = 0
	OFF = 1
	SHORt = 2


# noinspection SpellCheckingInspection
class SbasCorrMode(Enum):
	"""3 Members, AUTO ... USER"""
	AUTO = 0
	SYNC = 1
	USER = 2


# noinspection SpellCheckingInspection
class SatNavClockMode(Enum):
	"""2 Members, MSYMbol ... SYMBol"""
	MSYMbol = 0
	SYMBol = 1


# noinspection SpellCheckingInspection
class SarMode(Enum):
	"""3 Members, LRLM ... SRLM"""
	LRLM = 0
	SPARe = 1
	SRLM = 2


# noinspection SpellCheckingInspection
class SampRateModeRange(Enum):
	"""2 Members, FFT ... MIN"""
	FFT = 0
	MIN = 1


# noinspection SpellCheckingInspection
class SampRateFifoStatus(Enum):
	"""3 Members, OFLow ... URUN"""
	OFLow = 0
	OK = 1
	URUN = 2


# noinspection SpellCheckingInspection
class SamplesPerPtrsGrpAll(Enum):
	"""2 Members, S2 ... S4"""
	S2 = 0
	S4 = 1


# noinspection SpellCheckingInspection
class RxaNt(Enum):
	"""4 Members, ANT1 ... ANT8"""
	ANT1 = 0
	ANT2 = 1
	ANT4 = 2
	ANT8 = 3


# noinspection SpellCheckingInspection
class RsrcBlockSize(Enum):
	"""2 Members, C1 ... C2"""
	C1 = 0
	C2 = 1


# noinspection SpellCheckingInspection
class Rs232BdRate(Enum):
	"""7 Members, _115200 ... _9600"""
	_115200 = 0
	_19200 = 1
	_2400 = 2
	_38400 = 3
	_4800 = 4
	_57600 = 5
	_9600 = 6


# noinspection SpellCheckingInspection
class RoscOutpFreqMode(Enum):
	"""3 Members, DER10M ... OFF"""
	DER10M = 0
	LOOPthrough = 1
	OFF = 2


# noinspection SpellCheckingInspection
class RoscFreqExt(Enum):
	"""4 Members, _100MHZ ... VARiable"""
	_100MHZ = 0
	_10MHZ = 1
	_1GHZ = 2
	VARiable = 3


# noinspection SpellCheckingInspection
class Rosc1GoUtpFreqMode(Enum):
	"""3 Members, DER1G ... OFF"""
	DER1G = 0
	LOOPthrough = 1
	OFF = 2


# noinspection SpellCheckingInspection
class RfBand(Enum):
	"""3 Members, L1 ... L5"""
	L1 = 0
	L2 = 1
	L5 = 2


# noinspection SpellCheckingInspection
class RestartDataAll(Enum):
	"""3 Members, COAL ... OFF"""
	COAL = 0
	FRAMe = 1
	OFF = 2


# noinspection SpellCheckingInspection
class ResourceAllocAll(Enum):
	"""3 Members, DS ... T1"""
	DS = 0
	T0 = 1
	T1 = 2


# noinspection SpellCheckingInspection
class RepTypeAll(Enum):
	"""5 Members, CUSTom ... SUBFrame"""
	CUSTom = 0
	FRAMe = 1
	OFF = 2
	SLOT = 3
	SUBFrame = 4


# noinspection SpellCheckingInspection
class Release(Enum):
	"""1 Members, REL15 ... REL15"""
	REL15 = 0


# noinspection SpellCheckingInspection
class RefVehicle(Enum):
	"""2 Members, V1 ... V2"""
	V1 = 0
	V2 = 1


# noinspection SpellCheckingInspection
class RefStream(Enum):
	"""4 Members, S1 ... S4"""
	S1 = 0
	S2 = 1
	S3 = 2
	S4 = 3


# noinspection SpellCheckingInspection
class RefScale(Enum):
	"""2 Members, DISTance ... TIME"""
	DISTance = 0
	TIME = 1


# noinspection SpellCheckingInspection
class ReflMaterial(Enum):
	"""6 Members, DRY ... WET"""
	DRY = 0
	MDRY = 1
	SEA = 2
	USER = 3
	WATER = 4
	WET = 5


# noinspection SpellCheckingInspection
class RefFrame(Enum):
	"""2 Members, PZ90 ... WGS84"""
	PZ90 = 0
	WGS84 = 1


# noinspection SpellCheckingInspection
class RefAntenna(Enum):
	"""4 Members, A1 ... A4"""
	A1 = 0
	A2 = 1
	A3 = 2
	A4 = 3


# noinspection SpellCheckingInspection
class RecScpiCmdMode(Enum):
	"""4 Members, AUTO ... OFF"""
	AUTO = 0
	DAUTo = 1
	MANual = 2
	OFF = 3


# noinspection SpellCheckingInspection
class ReadOutMode(Enum):
	"""3 Members, CYCLic ... RTRip"""
	CYCLic = 0
	OWAY = 1
	RTRip = 2


# noinspection SpellCheckingInspection
class RateMatchPeriodictyAll(Enum):
	"""8 Members, _1 ... _8"""
	_1 = 0
	_10 = 1
	_2 = 2
	_20 = 3
	_4 = 4
	_40 = 5
	_5 = 6
	_8 = 7


# noinspection SpellCheckingInspection
class RateMatchGrpIdAll(Enum):
	"""3 Members, G1 ... N"""
	G1 = 0
	G2 = 1
	N = 2


# noinspection SpellCheckingInspection
class RampFunc(Enum):
	"""2 Members, COSine ... LINear"""
	COSine = 0
	LINear = 1


# noinspection SpellCheckingInspection
class QuickSetStateAll(Enum):
	"""3 Members, DIS ... EN"""
	DIS = 0
	DRSK = 1
	EN = 2


# noinspection SpellCheckingInspection
class QuickSetSlotLenAll(Enum):
	"""2 Members, S10 ... S5"""
	S10 = 0
	S5 = 1


# noinspection SpellCheckingInspection
class QucjSettingsScsAll(Enum):
	"""10 Members, N120 ... SCS60"""
	N120 = 0
	N15 = 1
	N240 = 2
	N30 = 3
	N60 = 4
	SCS120 = 5
	SCS15 = 6
	SCS240 = 7
	SCS30 = 8
	SCS60 = 9


# noinspection SpellCheckingInspection
class PuschUciModeAll(Enum):
	"""2 Members, UCIonly ... UCLSch"""
	UCIonly = 0
	UCLSch = 1


# noinspection SpellCheckingInspection
class PuschUciAlphaAll(Enum):
	"""4 Members, A0_5 ... A1_0"""
	A0_5 = 0
	A0_65 = 1
	A0_8 = 2
	A1_0 = 3


# noinspection SpellCheckingInspection
class PuschGrpSeqAll(Enum):
	"""3 Members, GRP ... SEQuence"""
	GRP = 0
	NEITher = 1
	SEQuence = 2


# noinspection SpellCheckingInspection
class PulsTrigModeWithSingle(Enum):
	"""5 Members, AUTO ... SINGle"""
	AUTO = 0
	EGATe = 1
	ESINgle = 2
	EXTernal = 3
	SINGle = 4


# noinspection SpellCheckingInspection
class PulsTransType(Enum):
	"""2 Members, FAST ... SMOothed"""
	FAST = 0
	SMOothed = 1


# noinspection SpellCheckingInspection
class PulsMode(Enum):
	"""4 Members, DOUBle ... SINGle"""
	DOUBle = 0
	PHOPptrain = 1
	PTRain = 2
	SINGle = 3


# noinspection SpellCheckingInspection
class PucchGrpHoppingAll(Enum):
	"""3 Members, DIS ... N"""
	DIS = 0
	ENA = 1
	N = 2


# noinspection SpellCheckingInspection
class PucchFormatAll(Enum):
	"""5 Members, F0 ... F4"""
	F0 = 0
	F1 = 1
	F2 = 2
	F3 = 3
	F4 = 4


# noinspection SpellCheckingInspection
class PucchFmt4OccLength(Enum):
	"""2 Members, L2 ... L4"""
	L2 = 0
	L4 = 1


# noinspection SpellCheckingInspection
class PtrsTpTimeDensityAll(Enum):
	"""2 Members, TD1 ... TD2"""
	TD1 = 0
	TD2 = 1


# noinspection SpellCheckingInspection
class PtrsTpNumberOfPtrsGrpsAll(Enum):
	"""3 Members, G2 ... G8"""
	G2 = 0
	G4 = 1
	G8 = 2


# noinspection SpellCheckingInspection
class PtrsTmeDensity(Enum):
	"""3 Members, TD1 ... TD4"""
	TD1 = 0
	TD2 = 1
	TD4 = 2


# noinspection SpellCheckingInspection
class PtrsReOffset(Enum):
	"""4 Members, RE00 ... RE11"""
	RE00 = 0
	RE01 = 1
	RE10 = 2
	RE11 = 3


# noinspection SpellCheckingInspection
class PtrsPower(Enum):
	"""2 Members, P00 ... P01"""
	P00 = 0
	P01 = 1


# noinspection SpellCheckingInspection
class PtrsFreqDensity(Enum):
	"""2 Members, FD2 ... FD4"""
	FD2 = 0
	FD4 = 1


# noinspection SpellCheckingInspection
class PtrsEpreRatio(Enum):
	"""2 Members, RAT0 ... RAT1"""
	RAT0 = 0
	RAT1 = 1


# noinspection SpellCheckingInspection
class PseudorangeMode(Enum):
	"""3 Members, CONStant ... PROFile"""
	CONStant = 0
	FSBas = 1
	PROFile = 2


# noinspection SpellCheckingInspection
class PrsTimeGap(Enum):
	"""6 Members, TG1 ... TG8"""
	TG1 = 0
	TG16 = 1
	TG2 = 2
	TG32 = 3
	TG4 = 4
	TG8 = 5


# noinspection SpellCheckingInspection
class PrsRepFactor(Enum):
	"""6 Members, REP1 ... REP8"""
	REP1 = 0
	REP16 = 1
	REP2 = 2
	REP32 = 3
	REP4 = 4
	REP8 = 5


# noinspection SpellCheckingInspection
class PrsPeriodicity(Enum):
	"""16 Members, SL10 ... SL8"""
	SL10 = 0
	SL10240 = 1
	SL1280 = 2
	SL16 = 3
	SL160 = 4
	SL20 = 5
	SL2560 = 6
	SL32 = 7
	SL320 = 8
	SL4 = 9
	SL40 = 10
	SL5 = 11
	SL5120 = 12
	SL64 = 13
	SL640 = 14
	SL8 = 15


# noinspection SpellCheckingInspection
class PrsNumSymbols(Enum):
	"""4 Members, S12 ... S6"""
	S12 = 0
	S2 = 1
	S4 = 2
	S6 = 3


# noinspection SpellCheckingInspection
class PrsCombSize(Enum):
	"""4 Members, C12 ... C6"""
	C12 = 0
	C2 = 1
	C4 = 2
	C6 = 3


# noinspection SpellCheckingInspection
class PropagCond(Enum):
	"""6 Members, AWGN ... TDLC300D100"""
	AWGN = 0
	TDLA30D10 = 1
	TDLA30D300 = 2
	TDLA30D75 = 3
	TDLB100D400 = 4
	TDLC300D100 = 5


# noinspection SpellCheckingInspection
class PriorityRole(Enum):
	"""2 Members, MASTer ... SLAVe"""
	MASTer = 0
	SLAVe = 1


# noinspection SpellCheckingInspection
class PrecoderGranularityAll(Enum):
	"""2 Members, ACRB ... REG"""
	ACRB = 0
	REG = 1


# noinspection SpellCheckingInspection
class PrbBundlingType(Enum):
	"""3 Members, DYNamic ... STATic"""
	DYNamic = 0
	NOTC = 1
	STATic = 2


# noinspection SpellCheckingInspection
class PrbBundleSizeSet2(Enum):
	"""2 Members, N4 ... WIDeband"""
	N4 = 0
	WIDeband = 1


# noinspection SpellCheckingInspection
class PrbBundleSizeSet1(Enum):
	"""4 Members, N2WB ... WIDeband"""
	N2WB = 0
	N4 = 1
	N4WB = 2
	WIDeband = 3


# noinspection SpellCheckingInspection
class PrachRestrictedSetAll(Enum):
	"""3 Members, ARES ... URES"""
	ARES = 0
	BRES = 1
	URES = 2


# noinspection SpellCheckingInspection
class PrachNumAll(Enum):
	"""6 Members, N1_25 ... N60"""
	N1_25 = 0
	N120 = 1
	N15 = 2
	N30 = 3
	N5 = 4
	N60 = 5


# noinspection SpellCheckingInspection
class PrachFormatAll(Enum):
	"""13 Members, F0 ... FC2"""
	F0 = 0
	F1 = 1
	F2 = 2
	F3 = 3
	FA1 = 4
	FA2 = 5
	FA3 = 6
	FB1 = 7
	FB2 = 8
	FB3 = 9
	FB4 = 10
	FC0 = 11
	FC2 = 12


# noinspection SpellCheckingInspection
class PowSensSource(Enum):
	"""4 Members, A ... USER"""
	A = 0
	B = 1
	RF = 2
	USER = 3


# noinspection SpellCheckingInspection
class PowSensFiltType(Enum):
	"""3 Members, AUTO ... USER"""
	AUTO = 0
	NSRatio = 1
	USER = 2


# noinspection SpellCheckingInspection
class PowSensDisplayPriority(Enum):
	"""2 Members, AVERage ... PEAK"""
	AVERage = 0
	PEAK = 1


# noinspection SpellCheckingInspection
class PowPreContLen(Enum):
	"""2 Members, S0 ... S8"""
	S0 = 0
	S8 = 1


# noinspection SpellCheckingInspection
class PowLevMode(Enum):
	"""3 Members, LOWDistortion ... NORMal"""
	LOWDistortion = 0
	LOWNoise = 1
	NORMal = 2


# noinspection SpellCheckingInspection
class PowLevBehaviour(Enum):
	"""6 Members, AUTO ... USER"""
	AUTO = 0
	CPHase = 1
	CVSWr = 2
	MONotone = 3
	UNINterrupted = 4
	USER = 5


# noinspection SpellCheckingInspection
class PowerRampSlope(Enum):
	"""2 Members, ASCending ... DESCending"""
	ASCending = 0
	DESCending = 1


# noinspection SpellCheckingInspection
class PowerRampShape(Enum):
	"""3 Members, LINear ... TRIangle"""
	LINear = 0
	STAir = 1
	TRIangle = 2


# noinspection SpellCheckingInspection
class PowerRampMarkMode(Enum):
	"""5 Members, PRESweep ... UNCHanged"""
	PRESweep = 0
	RFBLanking = 1
	STARt = 2
	STOP = 3
	UNCHanged = 4


# noinspection SpellCheckingInspection
class PowerRampClocMode(Enum):
	"""2 Members, MULTisample ... SAMPle"""
	MULTisample = 0
	SAMPle = 1


# noinspection SpellCheckingInspection
class PowerModeAll(Enum):
	"""4 Members, ACTvsf ... PSDConst"""
	ACTvsf = 0
	AVG = 1
	BURSt = 2
	PSDConst = 3


# noinspection SpellCheckingInspection
class PowerAttMode(Enum):
	"""5 Members, AUTO ... NORMal"""
	AUTO = 0
	FIXed = 1
	HPOWer = 2
	MANual = 3
	NORMal = 4


# noinspection SpellCheckingInspection
class PowContStepMan(Enum):
	"""2 Members, MAN0 ... MAN1"""
	MAN0 = 0
	MAN1 = 1


# noinspection SpellCheckingInspection
class PowContMode(Enum):
	"""3 Members, EXTernal ... TPC"""
	EXTernal = 0
	MANual = 1
	TPC = 2


# noinspection SpellCheckingInspection
class PowContAssMode(Enum):
	"""2 Members, FDPCh ... NORMal"""
	FDPCh = 0
	NORMal = 1


# noinspection SpellCheckingInspection
class PowCntrlSelect(Enum):
	"""8 Members, SENS1 ... SENSor4"""
	SENS1 = 0
	SENS2 = 1
	SENS3 = 2
	SENS4 = 3
	SENSor1 = 4
	SENSor2 = 5
	SENSor3 = 6
	SENSor4 = 7


# noinspection SpellCheckingInspection
class PowAttRfOffMode(Enum):
	"""2 Members, FATTenuation ... UNCHanged"""
	FATTenuation = 0
	UNCHanged = 1


# noinspection SpellCheckingInspection
class PowAttMode(Enum):
	"""2 Members, AUTO ... FIXed"""
	AUTO = 0
	FIXed = 1


# noinspection SpellCheckingInspection
class PowAlcSampleLev(Enum):
	"""3 Members, ATTenuated ... MINimum"""
	ATTenuated = 0
	FULL = 1
	MINimum = 2


# noinspection SpellCheckingInspection
class PowAlcDetSensitivity(Enum):
	"""5 Members, AUTO ... MEDium"""
	AUTO = 0
	FIXed = 1
	HIGH = 2
	LOW = 3
	MEDium = 4


# noinspection SpellCheckingInspection
class PositionFormat(Enum):
	"""2 Members, DECimal ... DMS"""
	DECimal = 0
	DMS = 1


# noinspection SpellCheckingInspection
class PmMode(Enum):
	"""3 Members, HBANdwidth ... LNOise"""
	HBANdwidth = 0
	HDEViation = 1
	LNOise = 2


# noinspection SpellCheckingInspection
class PilLen(Enum):
	"""5 Members, BIT0 ... BIT8"""
	BIT0 = 0
	BIT16 = 1
	BIT2 = 2
	BIT4 = 3
	BIT8 = 4


# noinspection SpellCheckingInspection
class PcmOdeAll(Enum):
	"""5 Members, _0 ... OFF"""
	_0 = 0
	_1 = 1
	AUTO = 2
	MANual = 3
	OFF = 4


# noinspection SpellCheckingInspection
class PathUniCodBbin(Enum):
	"""1 Members, A ... A"""
	A = 0


# noinspection SpellCheckingInspection
class Parity(Enum):
	"""3 Members, EVEN ... ODD"""
	EVEN = 0
	NONE = 1
	ODD = 2


# noinspection SpellCheckingInspection
class ParameterSetMode(Enum):
	"""2 Members, GLOBal ... LIST"""
	GLOBal = 0
	LIST = 1


# noinspection SpellCheckingInspection
class PageInd(Enum):
	"""4 Members, D144 ... D72"""
	D144 = 0
	D18 = 1
	D36 = 2
	D72 = 3


# noinspection SpellCheckingInspection
class PackFormat(Enum):
	"""8 Members, L1M ... QHSP6"""
	L1M = 0
	L2M = 1
	LCOD = 2
	QHSP2 = 3
	QHSP3 = 4
	QHSP4 = 5
	QHSP5 = 6
	QHSP6 = 7


# noinspection SpellCheckingInspection
class Output(Enum):
	"""3 Members, NONE ... RFB"""
	NONE = 0
	RFA = 1
	RFB = 2


# noinspection SpellCheckingInspection
class OutpConnGlbSignal(Enum):
	"""18 Members, BERCLKOUT ... TRIGgered"""
	BERCLKOUT = 0
	BERDATENOUT = 1
	BERDATOUT = 2
	BERRESTOUT = 3
	BGATe = 4
	CWMODulation = 5
	HIGH = 6
	HOP = 7
	LATTenuation = 8
	LOW = 9
	MARKA1 = 10
	MARKA2 = 11
	MARKA3 = 12
	MTRigger = 13
	NONE = 14
	SCLock = 15
	SYNCOUT = 16
	TRIGgered = 17


# noinspection SpellCheckingInspection
class OptimizationMode(Enum):
	"""2 Members, FAST ... QHIGh"""
	FAST = 0
	QHIGh = 1


# noinspection SpellCheckingInspection
class OffsetRelativeAll(Enum):
	"""2 Members, POINta ... TXBW"""
	POINta = 0
	TXBW = 1


# noinspection SpellCheckingInspection
class OffsetFactorN(Enum):
	"""3 Members, OFN_1 ... OFN_3"""
	OFN_1 = 0
	OFN_2 = 1
	OFN_3 = 2


# noinspection SpellCheckingInspection
class OcnsMode(Enum):
	"""4 Members, HSDP2 ... STANdard"""
	HSDP2 = 0
	HSDPa = 1
	M3I = 2
	STANdard = 3


# noinspection SpellCheckingInspection
class ObscPhysModel(Enum):
	"""2 Members, OBSCuration ... OMPath"""
	OBSCuration = 0
	OMPath = 1


# noinspection SpellCheckingInspection
class ObscModelVertObst(Enum):
	"""3 Members, URB1 ... USER"""
	URB1 = 0
	URB2 = 1
	USER = 2


# noinspection SpellCheckingInspection
class ObscModelSideBuil(Enum):
	"""4 Members, CUTTing ... USER"""
	CUTTing = 0
	HIGHway = 1
	SUB1 = 2
	USER = 3


# noinspection SpellCheckingInspection
class ObscModelFullObsc(Enum):
	"""8 Members, BR1 ... USER"""
	BR1 = 0
	BR2 = 1
	LTUNnel = 2
	MTUNnel = 3
	P10M = 4
	P1H = 5
	P1M = 6
	USER = 7


# noinspection SpellCheckingInspection
class ObscEnvModel(Enum):
	"""7 Members, FULL ... VOBS"""
	FULL = 0
	GSR = 1
	LMM = 2
	LOS = 3
	MPATh = 4
	RPL = 5
	VOBS = 6


# noinspection SpellCheckingInspection
class NumerologyPrs(Enum):
	"""5 Members, N120 ... X60"""
	N120 = 0
	N15 = 1
	N30 = 2
	N60 = 3
	X60 = 4


# noinspection SpellCheckingInspection
class Numerology(Enum):
	"""6 Members, N120 ... X60"""
	N120 = 0
	N15 = 1
	N240 = 2
	N30 = 3
	N60 = 4
	X60 = 5


# noinspection SpellCheckingInspection
class NumbOfBasebands(Enum):
	"""5 Members, _0 ... _4"""
	_0 = 0
	_1 = 1
	_2 = 2
	_3 = 3
	_4 = 4


# noinspection SpellCheckingInspection
class NumbersH(Enum):
	"""13 Members, _10 ... _9"""
	_10 = 0
	_11 = 1
	_12 = 2
	_13 = 3
	_14 = 4
	_2 = 5
	_3 = 6
	_4 = 7
	_5 = 8
	_6 = 9
	_7 = 10
	_8 = 11
	_9 = 12


# noinspection SpellCheckingInspection
class NumbersG(Enum):
	"""4 Members, _0 ... _3"""
	_0 = 0
	_1 = 1
	_2 = 2
	_3 = 3


# noinspection SpellCheckingInspection
class NumbersE(Enum):
	"""32 Members, _0 ... _9"""
	_0 = 0
	_1 = 1
	_10 = 2
	_11 = 3
	_12 = 4
	_13 = 5
	_14 = 6
	_15 = 7
	_16 = 8
	_17 = 9
	_18 = 10
	_19 = 11
	_2 = 12
	_20 = 13
	_21 = 14
	_22 = 15
	_23 = 16
	_24 = 17
	_25 = 18
	_26 = 19
	_27 = 20
	_28 = 21
	_29 = 22
	_3 = 23
	_30 = 24
	_31 = 25
	_4 = 26
	_5 = 27
	_6 = 28
	_7 = 29
	_8 = 30
	_9 = 31


# noinspection SpellCheckingInspection
class NumbersD(Enum):
	"""2 Members, _2 ... _4"""
	_2 = 0
	_4 = 1


# noinspection SpellCheckingInspection
class NumbersC(Enum):
	"""7 Members, _1 ... _8"""
	_1 = 0
	_2 = 1
	_3 = 2
	_4 = 3
	_5 = 4
	_6 = 5
	_8 = 6


# noinspection SpellCheckingInspection
class NumbersB(Enum):
	"""3 Members, _1 ... _4"""
	_1 = 0
	_2 = 1
	_4 = 2


# noinspection SpellCheckingInspection
class NumberOfPorts(Enum):
	"""3 Members, AP1 ... AP4"""
	AP1 = 0
	AP2 = 1
	AP4 = 2


# noinspection SpellCheckingInspection
class NumberA(Enum):
	"""4 Members, _1 ... _4"""
	_1 = 0
	_2 = 1
	_3 = 2
	_4 = 3


# noinspection SpellCheckingInspection
class NrsIdAll(Enum):
	"""2 Members, CID ... PUID"""
	CID = 0
	PUID = 1


# noinspection SpellCheckingInspection
class Nr5GpuschAp(Enum):
	"""12 Members, AP0 ... AP9"""
	AP0 = 0
	AP1 = 1
	AP10 = 2
	AP11 = 3
	AP2 = 4
	AP3 = 5
	AP4 = 6
	AP5 = 7
	AP6 = 8
	AP7 = 9
	AP8 = 10
	AP9 = 11


# noinspection SpellCheckingInspection
class Nr5GpdschConfigType(Enum):
	"""2 Members, T1 ... T2"""
	T1 = 0
	T2 = 1


# noinspection SpellCheckingInspection
class Nr5GpdschAp(Enum):
	"""12 Members, AP1000 ... AP1011"""
	AP1000 = 0
	AP1001 = 1
	AP1002 = 2
	AP1003 = 3
	AP1004 = 4
	AP1005 = 5
	AP1006 = 6
	AP1007 = 7
	AP1008 = 8
	AP1009 = 9
	AP1010 = 10
	AP1011 = 11


# noinspection SpellCheckingInspection
class Nr5GpbschCase(Enum):
	"""5 Members, A ... E"""
	A = 0
	B = 1
	C = 2
	D = 3
	E = 4


# noinspection SpellCheckingInspection
class Nr5GmarkMode(Enum):
	"""7 Members, FRAM ... ULDL"""
	FRAM = 0
	PERiod = 1
	RATio = 2
	RESTart = 3
	SFNRestart = 4
	SUBFram = 5
	ULDL = 6


# noinspection SpellCheckingInspection
class Nr5gContent(Enum):
	"""11 Members, COReset ... SRS"""
	COReset = 0
	CSIRs = 1
	DUMRe = 2
	LTECrs = 3
	PDSCh = 4
	PRACh = 5
	PRS = 6
	PUCCh = 7
	PUSCh = 8
	SPBCh = 9
	SRS = 10


# noinspection SpellCheckingInspection
class Nr5GclocMode(Enum):
	"""1 Members, SAMPle ... SAMPle"""
	SAMPle = 0


# noinspection SpellCheckingInspection
class Nr5Gcbw(Enum):
	"""15 Members, BW10 ... BW90"""
	BW10 = 0
	BW100 = 1
	BW15 = 2
	BW20 = 3
	BW200 = 4
	BW25 = 5
	BW30 = 6
	BW40 = 7
	BW400 = 8
	BW5 = 9
	BW50 = 10
	BW60 = 11
	BW70 = 12
	BW80 = 13
	BW90 = 14


# noinspection SpellCheckingInspection
class Nr5GcarDep(Enum):
	"""8 Members, BT36 ... LT3"""
	BT36 = 0
	BT37125 = 1
	FR1GT3 = 2
	FR1LT3 = 3
	FR2 = 4
	GT6 = 5
	GT7125 = 6
	LT3 = 7


# noinspection SpellCheckingInspection
class Nr5Gbsp(Enum):
	"""6 Members, BS10 ... BS80"""
	BS10 = 0
	BS160 = 1
	BS20 = 2
	BS40 = 3
	BS5 = 4
	BS80 = 5


# noinspection SpellCheckingInspection
class NormInv(Enum):
	"""2 Members, INVerted ... NORMal"""
	INVerted = 0
	NORMal = 1


# noinspection SpellCheckingInspection
class NoisDistrib(Enum):
	"""4 Members, EQUal ... UNIForm"""
	EQUal = 0
	GAUSs = 1
	NORMal = 2
	UNIForm = 3


# noinspection SpellCheckingInspection
class NoisAwgnPowRefMode(Enum):
	"""2 Members, CARRier ... NOISe"""
	CARRier = 0
	NOISe = 1


# noinspection SpellCheckingInspection
class NoisAwgnPowMode(Enum):
	"""3 Members, CN ... SN"""
	CN = 0
	EN = 1
	SN = 2


# noinspection SpellCheckingInspection
class NoisAwgnMode(Enum):
	"""3 Members, ADD ... ONLY"""
	ADD = 0
	CW = 1
	ONLY = 2


# noinspection SpellCheckingInspection
class NoisAwgnDispOutpMode(Enum):
	"""2 Members, ANALog ... DIGital"""
	ANALog = 0
	DIGital = 1


# noinspection SpellCheckingInspection
class NoisAwgnDispMode(Enum):
	"""2 Members, IQOUT1 ... RFA"""
	IQOUT1 = 0
	RFA = 1


# noinspection SpellCheckingInspection
class NfcTsn(Enum):
	"""5 Members, TSN1 ... TSN8"""
	TSN1 = 0
	TSN16 = 1
	TSN2 = 2
	TSN4 = 3
	TSN8 = 4


# noinspection SpellCheckingInspection
class NfcTransMode(Enum):
	"""2 Members, LISTen ... POLL"""
	LISTen = 0
	POLL = 1


# noinspection SpellCheckingInspection
class NfcSlotNumber(Enum):
	"""15 Members, SN10 ... SN9"""
	SN10 = 0
	SN11 = 1
	SN12 = 2
	SN13 = 3
	SN14 = 4
	SN15 = 5
	SN16 = 6
	SN2 = 7
	SN3 = 8
	SN4 = 9
	SN5 = 10
	SN6 = 11
	SN7 = 12
	SN8 = 13
	SN9 = 14


# noinspection SpellCheckingInspection
class NfcSelCmd(Enum):
	"""3 Members, CL1 ... CL3"""
	CL1 = 0
	CL2 = 1
	CL3 = 2


# noinspection SpellCheckingInspection
class NfcRc(Enum):
	"""3 Members, APFS ... SCIR"""
	APFS = 0
	NSCI = 1
	SCIR = 2


# noinspection SpellCheckingInspection
class NfcProtocolMode(Enum):
	"""5 Members, EMVA ... NFCF"""
	EMVA = 0
	EMVB = 1
	NFCA = 2
	NFCB = 3
	NFCF = 4


# noinspection SpellCheckingInspection
class NfcPredef(Enum):
	"""5 Members, APA ... FPS"""
	APA = 0
	APS = 1
	BPA = 2
	BPS = 3
	FPS = 4


# noinspection SpellCheckingInspection
class NfcPfbType(Enum):
	"""3 Members, ANACk ... SUPer"""
	ANACk = 0
	INFO = 1
	SUPer = 2


# noinspection SpellCheckingInspection
class NfcPcktSelect(Enum):
	"""2 Members, PCK1 ... PCK2"""
	PCK1 = 0
	PCK2 = 1


# noinspection SpellCheckingInspection
class NfcNumOfSlots(Enum):
	"""5 Members, S1 ... S8"""
	S1 = 0
	S16 = 1
	S2 = 2
	S4 = 3
	S8 = 4


# noinspection SpellCheckingInspection
class NfcNfcid2FmtTp(Enum):
	"""2 Members, NDEP ... TT3"""
	NDEP = 0
	TT3 = 1


# noinspection SpellCheckingInspection
class NfcNfcid1Sz(Enum):
	"""3 Members, DOUBle ... TRIPle"""
	DOUBle = 0
	SINGle = 1
	TRIPle = 2


# noinspection SpellCheckingInspection
class NfcNack(Enum):
	"""4 Members, NCK0 ... NCK5"""
	NCK0 = 0
	NCK1 = 1
	NCK4 = 2
	NCK5 = 3


# noinspection SpellCheckingInspection
class NfcMinTr2(Enum):
	"""4 Members, TR20 ... TR23"""
	TR20 = 0
	TR21 = 1
	TR22 = 2
	TR23 = 3


# noinspection SpellCheckingInspection
class NfcMinTr1(Enum):
	"""3 Members, TR10 ... TR12"""
	TR10 = 0
	TR11 = 1
	TR12 = 2


# noinspection SpellCheckingInspection
class NfcMinTr0(Enum):
	"""3 Members, TR00 ... TR02"""
	TR00 = 0
	TR01 = 1
	TR02 = 2


# noinspection SpellCheckingInspection
class NfcLenReduct(Enum):
	"""4 Members, LR128 ... LR64"""
	LR128 = 0
	LR192 = 1
	LR254 = 2
	LR64 = 3


# noinspection SpellCheckingInspection
class NfcLength(Enum):
	"""2 Members, LEN2 ... LEN3"""
	LEN2 = 0
	LEN3 = 1


# noinspection SpellCheckingInspection
class NfcFsc(Enum):
	"""9 Members, F128 ... F96"""
	F128 = 0
	F16 = 1
	F24 = 2
	F256 = 3
	F32 = 4
	F40 = 5
	F48 = 6
	F64 = 7
	F96 = 8


# noinspection SpellCheckingInspection
class NfcDsiDri(Enum):
	"""7 Members, D1 ... D8"""
	D1 = 0
	D16 = 1
	D2 = 2
	D32 = 3
	D4 = 4
	D64 = 5
	D8 = 6


# noinspection SpellCheckingInspection
class NfcDivisor(Enum):
	"""4 Members, DIV1 ... DIV8"""
	DIV1 = 0
	DIV2 = 1
	DIV4 = 2
	DIV8 = 3


# noinspection SpellCheckingInspection
class NfcDivForMod(Enum):
	"""2 Members, DIV2 ... DIV4"""
	DIV2 = 0
	DIV4 = 1


# noinspection SpellCheckingInspection
class NfcDeselWtx(Enum):
	"""2 Members, DSEL ... WTX"""
	DSEL = 0
	WTX = 1


# noinspection SpellCheckingInspection
class NfcConfigType(Enum):
	"""8 Members, _0 ... T4A"""
	_0 = 0
	_1 = 1
	DT4A = 2
	NDEP = 3
	OFF = 4
	ON = 5
	T2 = 6
	T4A = 7


# noinspection SpellCheckingInspection
class NfcCmdType(Enum):
	"""63 Members, ACK ... WRES"""
	ACK = 0
	ALAQ = 1
	ALBQ = 2
	ATBQ = 3
	ATBS = 4
	ATRQ = 5
	ATRS = 6
	ATSS = 7
	BLNK = 8
	CHKQ = 9
	CHKS = 10
	DEPQ = 11
	DEPS = 12
	DSLQ = 13
	DSLS = 14
	GENE = 15
	IDLE = 16
	NACK = 17
	PSLQ = 18
	PSLS = 19
	RATQ = 20
	RD8Q = 21
	RD8S = 22
	RDAQ = 23
	RDAS = 24
	RLAQ = 25
	RLAS = 26
	RLSQ = 27
	RLSS = 28
	RSGQ = 29
	RSGS = 30
	SDAQ = 31
	SDAS = 32
	SLAQ = 33
	SLAS = 34
	SMAR = 35
	SNAQ = 36
	SNAS = 37
	SNBQ = 38
	SNBS = 39
	SNFQ = 40
	SNFS = 41
	SPAQ = 42
	SPBQ = 43
	SPBS = 44
	SSLQ = 45
	T1RQ = 46
	T1RS = 47
	T2RQ = 48
	T2RS = 49
	T2WQ = 50
	T4AD = 51
	T4BD = 52
	UPDQ = 53
	UPDS = 54
	WE8Q = 55
	WE8S = 56
	WN8Q = 57
	WN8S = 58
	WNEQ = 59
	WNES = 60
	WREQ = 61
	WRES = 62


# noinspection SpellCheckingInspection
class NfcBlockType(Enum):
	"""3 Members, TPI ... TPS"""
	TPI = 0
	TPR = 1
	TPS = 2


# noinspection SpellCheckingInspection
class NfcBitFrmSdd(Enum):
	"""6 Members, SDD0 ... SDD8"""
	SDD0 = 0
	SDD1 = 1
	SDD16 = 2
	SDD2 = 3
	SDD4 = 4
	SDD8 = 5


# noinspection SpellCheckingInspection
class NfcAtnTmot(Enum):
	"""2 Members, ATN ... TOUT"""
	ATN = 0
	TOUT = 1


# noinspection SpellCheckingInspection
class NfcAppDataCod(Enum):
	"""2 Members, CRCB ... PROP"""
	CRCB = 0
	PROP = 1


# noinspection SpellCheckingInspection
class NfcApgEnericFrameType(Enum):
	"""3 Members, BOSDd ... STANdard"""
	BOSDd = 0
	SHORt = 1
	STANdard = 2


# noinspection SpellCheckingInspection
class NfcAcssAttrib(Enum):
	"""2 Members, AARO ... AARW"""
	AARO = 0
	AARW = 1


# noinspection SpellCheckingInspection
class NfcAckNack(Enum):
	"""2 Members, ACK ... NACK"""
	ACK = 0
	NACK = 1


# noinspection SpellCheckingInspection
class NetMode(Enum):
	"""2 Members, AUTO ... STATic"""
	AUTO = 0
	STATic = 1


# noinspection SpellCheckingInspection
class NavMsgCtrl(Enum):
	"""3 Members, AUTO ... OFF"""
	AUTO = 0
	EDIT = 1
	OFF = 2


# noinspection SpellCheckingInspection
class NavDataFormat(Enum):
	"""2 Members, CNAV ... LNAV"""
	CNAV = 0
	LNAV = 1


# noinspection SpellCheckingInspection
class MultInstSyncState(Enum):
	"""2 Members, NOSYnc ... SYNC"""
	NOSYnc = 0
	SYNC = 1


# noinspection SpellCheckingInspection
class MsMode(Enum):
	"""5 Members, DPCDch ... PRACh"""
	DPCDch = 0
	PCPCh = 1
	PPCPch = 2
	PPRach = 3
	PRACh = 4


# noinspection SpellCheckingInspection
class MonitorDisplayType(Enum):
	"""7 Members, ATTitude ... TRAJectory"""
	ATTitude = 0
	CHANnels = 1
	MAP = 2
	POWer = 3
	SKY = 4
	TRACks = 5
	TRAJectory = 6


# noinspection SpellCheckingInspection
class ModulationF(Enum):
	"""6 Members, BPSK ... QPSK"""
	BPSK = 0
	CCK = 1
	DBPSK = 2
	DQPSK = 3
	PBCC = 4
	QPSK = 5


# noinspection SpellCheckingInspection
class ModulationE(Enum):
	"""8 Members, BPSK ... QPSK"""
	BPSK = 0
	CCK = 1
	DBPSk = 2
	DQPSk = 3
	PBCC = 4
	QAM16 = 5
	QAM64 = 6
	QPSK = 7


# noinspection SpellCheckingInspection
class ModulationDevMode(Enum):
	"""3 Members, RATio ... UNCoupled"""
	RATio = 0
	TOTal = 1
	UNCoupled = 2


# noinspection SpellCheckingInspection
class ModulationD(Enum):
	"""5 Members, QAM1024 ... QPSK"""
	QAM1024 = 0
	QAM16 = 1
	QAM256 = 2
	QAM64 = 3
	QPSK = 4


# noinspection SpellCheckingInspection
class ModulationC(Enum):
	"""3 Members, QAM16 ... QPSK"""
	QAM16 = 0
	QAM64 = 1
	QPSK = 2


# noinspection SpellCheckingInspection
class ModulationB(Enum):
	"""4 Members, QAM16 ... QPSK"""
	QAM16 = 0
	QAM256 = 1
	QAM64 = 2
	QPSK = 3


# noinspection SpellCheckingInspection
class ModulationA(Enum):
	"""2 Members, QAM16 ... QPSK"""
	QAM16 = 0
	QPSK = 1


# noinspection SpellCheckingInspection
class ModType(Enum):
	"""10 Members, BPSK ... QPSK"""
	BPSK = 0
	BPSK2 = 1
	NSQAM1024 = 2
	NSQAM2048 = 3
	NSQAM4096 = 4
	PSK8 = 5
	QAM16 = 6
	QAM256 = 7
	QAM64 = 8
	QPSK = 9


# noinspection SpellCheckingInspection
class Mode(Enum):
	"""2 Members, DRAT ... FDR"""
	DRAT = 0
	FDR = 1


# noinspection SpellCheckingInspection
class MinPrEv(Enum):
	"""2 Members, _2 ... _8"""
	_2 = 0
	_8 = 1


# noinspection SpellCheckingInspection
class McsTable(Enum):
	"""3 Members, QAM256 ... QAM64LSE"""
	QAM256 = 0
	QAM64 = 1
	QAM64LSE = 2


# noinspection SpellCheckingInspection
class MccwCrestFactMode(Enum):
	"""3 Members, CHIRp ... SLOW"""
	CHIRp = 0
	OFF = 1
	SLOW = 2


# noinspection SpellCheckingInspection
class MaxNrofPorts(Enum):
	"""2 Members, P1 ... P2"""
	P1 = 0
	P2 = 1


# noinspection SpellCheckingInspection
class MaxCbgaLl(Enum):
	"""5 Members, DISabled ... G8"""
	DISabled = 0
	G2 = 1
	G4 = 2
	G6 = 3
	G8 = 4


# noinspection SpellCheckingInspection
class MatProp(Enum):
	"""2 Members, PERM ... PLOSS"""
	PERM = 0
	PLOSS = 1


# noinspection SpellCheckingInspection
class MarkModeGnss(Enum):
	"""6 Members, PATTern ... RATio"""
	PATTern = 0
	PP2S = 1
	PPS = 2
	PPS10 = 3
	PULSe = 4
	RATio = 5


# noinspection SpellCheckingInspection
class MarkModeB(Enum):
	"""15 Members, CSPeriod ... USER"""
	CSPeriod = 0
	DPC = 1
	DPCC = 2
	EDCH = 3
	HACK = 4
	HFE = 5
	LPP = 6
	PCQI = 7
	PMP = 8
	RATio = 9
	RFRame = 10
	SFNR = 11
	SLOT = 12
	TRIGger = 13
	USER = 14


# noinspection SpellCheckingInspection
class MarkModeA(Enum):
	"""6 Members, FRAMe ... TRIGger"""
	FRAMe = 0
	PATTern = 1
	PULSe = 2
	RATio = 3
	RESTart = 4
	TRIGger = 5


# noinspection SpellCheckingInspection
class MarkConf(Enum):
	"""2 Members, FRAM ... UNCH"""
	FRAM = 0
	UNCH = 1


# noinspection SpellCheckingInspection
class MappingType(Enum):
	"""2 Members, A ... B"""
	A = 0
	B = 1


# noinspection SpellCheckingInspection
class LteCrsCarrierBwAll(Enum):
	"""6 Members, N100 ... N75"""
	N100 = 0
	N15 = 1
	N25 = 2
	N50 = 3
	N6 = 4
	N75 = 5


# noinspection SpellCheckingInspection
class LowHigh(Enum):
	"""2 Members, HIGH ... LOW"""
	HIGH = 0
	LOW = 1


# noinspection SpellCheckingInspection
class LoRaSyncMode(Enum):
	"""2 Members, PRIVate ... PUBLic"""
	PRIVate = 0
	PUBLic = 1


# noinspection SpellCheckingInspection
class LoRaSf(Enum):
	"""7 Members, SF10 ... SF9"""
	SF10 = 0
	SF11 = 1
	SF12 = 2
	SF6 = 3
	SF7 = 4
	SF8 = 5
	SF9 = 6


# noinspection SpellCheckingInspection
class LoRaFreqDfTp(Enum):
	"""2 Members, LINear ... SINE"""
	LINear = 0
	SINE = 1


# noinspection SpellCheckingInspection
class LoRaCodRate(Enum):
	"""5 Members, CR0 ... CR4"""
	CR0 = 0
	CR1 = 1
	CR2 = 2
	CR3 = 3
	CR4 = 4


# noinspection SpellCheckingInspection
class LoRaBw(Enum):
	"""10 Members, BW10 ... BW7"""
	BW10 = 0
	BW125 = 1
	BW15 = 2
	BW20 = 3
	BW250 = 4
	BW31 = 5
	BW41 = 6
	BW500 = 7
	BW62 = 8
	BW7 = 9


# noinspection SpellCheckingInspection
class LogRes(Enum):
	"""7 Members, R02S ... R5S"""
	R02S = 0
	R04S = 1
	R08S = 2
	R10S = 3
	R1S = 4
	R2S = 5
	R5S = 6


# noinspection SpellCheckingInspection
class LogMode(Enum):
	"""2 Members, OFFLine ... RT"""
	OFFLine = 0
	RT = 1


# noinspection SpellCheckingInspection
class LogFmtSat(Enum):
	"""1 Members, CSV ... CSV"""
	CSV = 0


# noinspection SpellCheckingInspection
class LocationModel(Enum):
	"""3 Members, HIL ... STATic"""
	HIL = 0
	MOVing = 1
	STATic = 2


# noinspection SpellCheckingInspection
class LmodRunMode(Enum):
	"""2 Members, LEARned ... LIVE"""
	LEARned = 0
	LIVE = 1


# noinspection SpellCheckingInspection
class LinkDir(Enum):
	"""4 Members, DOWN ... UP"""
	DOWN = 0
	FORWard = 1
	REVerse = 2
	UP = 3


# noinspection SpellCheckingInspection
class LfSweepSource(Enum):
	"""2 Members, LF1 ... LF2"""
	LF1 = 0
	LF2 = 1


# noinspection SpellCheckingInspection
class LfSourceImp(Enum):
	"""2 Members, G50 ... G600"""
	G50 = 0
	G600 = 1


# noinspection SpellCheckingInspection
class LfSource(Enum):
	"""17 Members, AM ... NOISe"""
	AM = 0
	AMA = 1
	AMB = 2
	EXT1 = 3
	EXT2 = 4
	FMPM = 5
	FMPMA = 6
	FMPMB = 7
	LF1 = 8
	LF1A = 9
	LF1B = 10
	LF2 = 11
	LF2A = 12
	LF2B = 13
	NOISA = 14
	NOISB = 15
	NOISe = 16


# noinspection SpellCheckingInspection
class LfShapeBfAmily(Enum):
	"""5 Members, PULSe ... TRIangle"""
	PULSe = 0
	SINE = 1
	SQUare = 2
	TRAPeze = 3
	TRIangle = 4


# noinspection SpellCheckingInspection
class LfFreqMode(Enum):
	"""3 Members, CW ... SWEep"""
	CW = 0
	FIXed = 1
	SWEep = 2


# noinspection SpellCheckingInspection
class LfBwidth(Enum):
	"""2 Members, BW0M2 ... BW10m"""
	BW0M2 = 0
	BW10m = 1


# noinspection SpellCheckingInspection
class LeftRightDirection(Enum):
	"""2 Members, LEFT ... RIGHt"""
	LEFT = 0
	RIGHt = 1


# noinspection SpellCheckingInspection
class KbLayout(Enum):
	"""20 Members, CHINese ... SWEDish"""
	CHINese = 0
	DANish = 1
	DUTBe = 2
	DUTCh = 3
	ENGLish = 4
	ENGUK = 5
	ENGUS = 6
	FINNish = 7
	FREBe = 8
	FRECa = 9
	FRENch = 10
	GERMan = 11
	ITALian = 12
	JAPanese = 13
	KORean = 14
	NORWegian = 15
	PORTuguese = 16
	RUSSian = 17
	SPANish = 18
	SWEDish = 19


# noinspection SpellCheckingInspection
class IqOutType(Enum):
	"""2 Members, DIFFerential ... SINGle"""
	DIFFerential = 0
	SINGle = 1


# noinspection SpellCheckingInspection
class IqOutMode(Enum):
	"""3 Members, FIXed ... VATTenuated"""
	FIXed = 0
	VARiable = 1
	VATTenuated = 2


# noinspection SpellCheckingInspection
class IqOutEnvVrEf(Enum):
	"""2 Members, VCC ... VOUT"""
	VCC = 0
	VOUT = 1


# noinspection SpellCheckingInspection
class IqOutEnvTerm(Enum):
	"""2 Members, GROund ... WIRE"""
	GROund = 0
	WIRE = 1


# noinspection SpellCheckingInspection
class IqOutEnvShapeMode(Enum):
	"""6 Members, DETRoughing ... TABLe"""
	DETRoughing = 0
	LINear = 1
	OFF = 2
	POLYnomial = 3
	POWer = 4
	TABLe = 5


# noinspection SpellCheckingInspection
class IqOutEnvScale(Enum):
	"""2 Members, POWer ... VOLTage"""
	POWer = 0
	VOLTage = 1


# noinspection SpellCheckingInspection
class IqOutEnvEtRak(Enum):
	"""4 Members, ET1V2 ... USER"""
	ET1V2 = 0
	ET1V5 = 1
	ET2V0 = 2
	USER = 3


# noinspection SpellCheckingInspection
class IqOutEnvDetrFunc(Enum):
	"""3 Members, F1 ... F3"""
	F1 = 0
	F2 = 1
	F3 = 2


# noinspection SpellCheckingInspection
class IqOutEnvAdaption(Enum):
	"""3 Members, AUTO ... POWer"""
	AUTO = 0
	MANual = 1
	POWer = 2


# noinspection SpellCheckingInspection
class IqOutDispViaType(Enum):
	"""2 Members, LEVel ... PEP"""
	LEVel = 0
	PEP = 1


# noinspection SpellCheckingInspection
class IqMode(Enum):
	"""2 Members, ANALog ... BASeband"""
	ANALog = 0
	BASeband = 1


# noinspection SpellCheckingInspection
class IqGain(Enum):
	"""7 Members, DB0 ... DBM4"""
	DB0 = 0
	DB2 = 1
	DB4 = 2
	DB6 = 3
	DB8 = 4
	DBM2 = 5
	DBM4 = 6


# noinspection SpellCheckingInspection
class IonoGridView(Enum):
	"""2 Members, GIVei ... VDELay"""
	GIVei = 0
	VDELay = 1


# noinspection SpellCheckingInspection
class IonModel(Enum):
	"""4 Members, KLOBuchar ... NONE"""
	KLOBuchar = 0
	MOPS = 1
	NEQuick = 2
	NONE = 3


# noinspection SpellCheckingInspection
class Interpolation(Enum):
	"""3 Members, LINear ... POWer"""
	LINear = 0
	OFF = 1
	POWer = 2


# noinspection SpellCheckingInspection
class InterfererTypeNr(Enum):
	"""3 Members, CW ... NR"""
	CW = 0
	NNR = 1
	NR = 2


# noinspection SpellCheckingInspection
class InterfererTypeCw(Enum):
	"""1 Members, CW ... CW"""
	CW = 0


# noinspection SpellCheckingInspection
class IntelSizeAll(Enum):
	"""3 Members, IS2 ... IS6"""
	IS2 = 0
	IS3 = 1
	IS6 = 2


# noinspection SpellCheckingInspection
class InputImpRf(Enum):
	"""3 Members, G10K ... G50"""
	G10K = 0
	G1K = 1
	G50 = 2


# noinspection SpellCheckingInspection
class InpOutpConnGlbMapSign(Enum):
	"""27 Members, BERCLKIN ... TRIGgered"""
	BERCLKIN = 0
	BERCLKOUT = 1
	BERDATENIN = 2
	BERDATENOUT = 3
	BERDATIN = 4
	BERDATOUT = 5
	BERRESTIN = 6
	BERRESTOUT = 7
	BGATe = 8
	CLOCK1 = 9
	CWMODulation = 10
	DATA = 11
	HIGH = 12
	HOP = 13
	LATTenuation = 14
	LOW = 15
	MARKA1 = 16
	MARKA2 = 17
	MARKA3 = 18
	MTRigger = 19
	NONE = 20
	NSEGM1 = 21
	SCLock = 22
	SYNCIN = 23
	SYNCOUT = 24
	TRIG1 = 25
	TRIGgered = 26


# noinspection SpellCheckingInspection
class InclExcl(Enum):
	"""2 Members, EXCLude ... INCLude"""
	EXCLude = 0
	INCLude = 1


# noinspection SpellCheckingInspection
class ImpG50G1KcoerceG10K(Enum):
	"""2 Members, G1K ... G50"""
	G1K = 0
	G50 = 1


# noinspection SpellCheckingInspection
class Imp(Enum):
	"""3 Members, G50 ... HIGH"""
	G50 = 0
	G600 = 1
	HIGH = 2


# noinspection SpellCheckingInspection
class IlbUndleSize(Enum):
	"""3 Members, BS2 ... BS6"""
	BS2 = 0
	BS3 = 1
	BS6 = 2


# noinspection SpellCheckingInspection
class IecTermMode(Enum):
	"""2 Members, EOI ... STANdard"""
	EOI = 0
	STANdard = 1


# noinspection SpellCheckingInspection
class IdEutraNbiotMode(Enum):
	"""3 Members, ALON ... INBD"""
	ALON = 0
	GBD = 1
	INBD = 2


# noinspection SpellCheckingInspection
class IdEutraEmtcPrachStartingSfPeriod(Enum):
	"""9 Members, _128 ... NONE"""
	_128 = 0
	_16 = 1
	_2 = 2
	_256 = 3
	_32 = 4
	_4 = 5
	_64 = 6
	_8 = 7
	NONE = 8


# noinspection SpellCheckingInspection
class IdEutraDataSourceDlEmtc(Enum):
	"""19 Members, DLISt ... ZERO"""
	DLISt = 0
	MIB = 1
	ONE = 2
	PATTern = 3
	PN11 = 4
	PN15 = 5
	PN16 = 6
	PN20 = 7
	PN21 = 8
	PN23 = 9
	PN9 = 10
	PRNTi = 11
	RARNti = 12
	SIBBr = 13
	USER1 = 14
	USER2 = 15
	USER3 = 16
	USER4 = 17
	ZERO = 18


# noinspection SpellCheckingInspection
class Hybrid(Enum):
	"""7 Members, BEIDou ... SBAS"""
	BEIDou = 0
	GALileo = 1
	GLONass = 2
	GPS = 3
	NAVic = 4
	QZSS = 5
	SBAS = 6


# noinspection SpellCheckingInspection
class HsUpaMod(Enum):
	"""2 Members, BPSK ... PAM4"""
	BPSK = 0
	PAM4 = 1


# noinspection SpellCheckingInspection
class HsUpaHsimMode(Enum):
	"""2 Members, HFEedback ... VHARq"""
	HFEedback = 0
	VHARq = 1


# noinspection SpellCheckingInspection
class HsUpaFrcTable(Enum):
	"""6 Members, TAB0TTI10 ... TAB3TTI2"""
	TAB0TTI10 = 0
	TAB0TTI2 = 1
	TAB1TTI10 = 2
	TAB1TTI2 = 3
	TAB2TTI2 = 4
	TAB3TTI2 = 5


# noinspection SpellCheckingInspection
class HsUpaFrcMode(Enum):
	"""9 Members, _1 ... USER"""
	_1 = 0
	_2 = 1
	_3 = 2
	_4 = 3
	_5 = 4
	_6 = 5
	_7 = 6
	_8 = 7
	USER = 8


# noinspection SpellCheckingInspection
class HsUpaDchTti(Enum):
	"""2 Members, _10ms ... _2ms"""
	_10ms = 0
	_2ms = 1


# noinspection SpellCheckingInspection
class HsUpaCellType(Enum):
	"""2 Members, NOSERVing ... SERVing"""
	NOSERVing = 0
	SERVing = 1


# noinspection SpellCheckingInspection
class HsUpaAgchScope(Enum):
	"""2 Members, ALL ... PER"""
	ALL = 0
	PER = 1


# noinspection SpellCheckingInspection
class HsRel8HarqMode(Enum):
	"""94 Members, A ... S2_N_N_N"""
	A = 0
	D_DTX = 1
	DTX = 2
	M_A = 3
	M_AA = 4
	M_AN = 5
	M_N = 6
	M_NA = 7
	M_NN = 8
	MS_A_A = 9
	MS_A_AA = 10
	MS_A_AN = 11
	MS_A_D = 12
	MS_A_N = 13
	MS_A_NA = 14
	MS_A_NN = 15
	MS_AA_A = 16
	MS_AA_AA = 17
	MS_AA_AN = 18
	MS_AA_D = 19
	MS_AA_N = 20
	MS_AA_NA = 21
	MS_AA_NN = 22
	MS_AN_A = 23
	MS_AN_AA = 24
	MS_AN_AN = 25
	MS_AN_D = 26
	MS_AN_N = 27
	MS_AN_NA = 28
	MS_AN_NN = 29
	MS_D_A = 30
	MS_D_AA = 31
	MS_D_AN = 32
	MS_D_N = 33
	MS_D_NA = 34
	MS_D_NN = 35
	MS_N_A = 36
	MS_N_AA = 37
	MS_N_AN = 38
	MS_N_D = 39
	MS_N_N = 40
	MS_N_NA = 41
	MS_N_NN = 42
	MS_NA_A = 43
	MS_NA_AA = 44
	MS_NA_AN = 45
	MS_NA_D = 46
	MS_NA_N = 47
	MS_NA_NA = 48
	MS_NA_NN = 49
	MS_NN_A = 50
	MS_NN_AA = 51
	MS_NN_AN = 52
	MS_NN_D = 53
	MS_NN_N = 54
	MS_NN_NA = 55
	MS_NN_NN = 56
	N = 57
	POST = 58
	PRE = 59
	S_A_A = 60
	S_A_D = 61
	S_A_N = 62
	S_D_A = 63
	S_D_N = 64
	S_N_A = 65
	S_N_D = 66
	S_N_N = 67
	S2_A_A_A = 68
	S2_A_A_D = 69
	S2_A_A_N = 70
	S2_A_D_A = 71
	S2_A_D_D = 72
	S2_A_D_N = 73
	S2_A_N_A = 74
	S2_A_N_D = 75
	S2_A_N_N = 76
	S2_D_A_A = 77
	S2_D_A_D = 78
	S2_D_A_N = 79
	S2_D_D_A = 80
	S2_D_D_N = 81
	S2_D_N_A = 82
	S2_D_N_D = 83
	S2_D_N_N = 84
	S2_N_A_A = 85
	S2_N_A_D = 86
	S2_N_A_N = 87
	S2_N_D_A = 88
	S2_N_D_D = 89
	S2_N_D_N = 90
	S2_N_N_A = 91
	S2_N_N_D = 92
	S2_N_N_N = 93


# noinspection SpellCheckingInspection
class HsRel8CqiType(Enum):
	"""6 Members, CCQI ... TB"""
	CCQI = 0
	CQI = 1
	DTX = 2
	TADT = 3
	TAST = 4
	TB = 5


# noinspection SpellCheckingInspection
class HsMode(Enum):
	"""7 Members, CONTinuous ... PSF4"""
	CONTinuous = 0
	HSET = 1
	PSF0 = 2
	PSF1 = 3
	PSF2 = 4
	PSF3 = 5
	PSF4 = 6


# noinspection SpellCheckingInspection
class HsMimoHarqMode(Enum):
	"""7 Members, AACK ... SNACk"""
	AACK = 0
	ANACk = 1
	DTX = 2
	NACK = 3
	NNACk = 4
	SACK = 5
	SNACk = 6


# noinspection SpellCheckingInspection
class HsMimoCqiType(Enum):
	"""3 Members, TADT ... TB"""
	TADT = 0
	TAST = 1
	TB = 2


# noinspection SpellCheckingInspection
class HsHsetType(Enum):
	"""18 Members, P10QAM16 ... USER"""
	P10QAM16 = 0
	P10QPSK = 1
	P11QAM64QAM16 = 2
	P12QPSK = 3
	P1QAM16 = 4
	P1QPSK = 5
	P2QAM16 = 6
	P2QPSK = 7
	P3QAM16 = 8
	P3QPSK = 9
	P4QPSK = 10
	P5QPSK = 11
	P6QAM16 = 12
	P6QPSK = 13
	P7QPSK = 14
	P8QAM64 = 15
	P9QAM16QPSK = 16
	USER = 17


# noinspection SpellCheckingInspection
class HsHsetTable(Enum):
	"""2 Members, TAB0 ... TAB1"""
	TAB0 = 0
	TAB1 = 1


# noinspection SpellCheckingInspection
class HsHsetScchType(Enum):
	"""3 Members, LOPeration ... NORMal"""
	LOPeration = 0
	MIMO = 1
	NORMal = 2


# noinspection SpellCheckingInspection
class HsHsetPdscSlotForm(Enum):
	"""4 Members, _0 ... QPSK"""
	_0 = 0
	_1 = 1
	QAM16 = 2
	QPSK = 3


# noinspection SpellCheckingInspection
class HsCompatMode(Enum):
	"""3 Members, REL7 ... REL8RT"""
	REL7 = 0
	REL8 = 1
	REL8RT = 2


# noinspection SpellCheckingInspection
class HrpUwbViterbiRate(Enum):
	"""2 Members, HALF ... ONE"""
	HALF = 0
	ONE = 1


# noinspection SpellCheckingInspection
class HrpUwbUnit(Enum):
	"""2 Members, SAMP ... SEQ"""
	SAMP = 0
	SEQ = 1


# noinspection SpellCheckingInspection
class HrpUwbSyncLength(Enum):
	"""4 Members, SL_1024 ... SL_64"""
	SL_1024 = 0
	SL_16 = 1
	SL_4096 = 2
	SL_64 = 3


# noinspection SpellCheckingInspection
class HrpUwbStspAcketConfig(Enum):
	"""4 Members, SPC_0 ... SPC_3"""
	SPC_0 = 0
	SPC_1 = 1
	SPC_2 = 2
	SPC_3 = 3


# noinspection SpellCheckingInspection
class HrpUwbStsDeltaLen(Enum):
	"""2 Members, DL_4 ... DL_8"""
	DL_4 = 0
	DL_8 = 1


# noinspection SpellCheckingInspection
class HrpUwbSfdlEngth(Enum):
	"""2 Members, SFDL_64 ... SFDL_8"""
	SFDL_64 = 0
	SFDL_8 = 1


# noinspection SpellCheckingInspection
class HrpUwbSfdIndex(Enum):
	"""5 Members, SFD_0 ... SFD_4"""
	SFD_0 = 0
	SFD_1 = 1
	SFD_2 = 2
	SFD_3 = 3
	SFD_4 = 4


# noinspection SpellCheckingInspection
class HrpUwbPhrdAtaRateMode(Enum):
	"""4 Members, BMHP ... HMLR"""
	BMHP = 0
	BMLP = 1
	HMHR = 2
	HMLR = 3


# noinspection SpellCheckingInspection
class HrpUwbOverSampling(Enum):
	"""2 Members, OS_1 ... OS_2"""
	OS_1 = 0
	OS_2 = 1


# noinspection SpellCheckingInspection
class HrpUwbMode(Enum):
	"""2 Members, HPRF ... NONHRP"""
	HPRF = 0
	NONHRP = 1


# noinspection SpellCheckingInspection
class HrpUwbMarkMode(Enum):
	"""2 Members, MAX ... RESTart"""
	MAX = 0
	RESTart = 1


# noinspection SpellCheckingInspection
class HrpUwbHopBurst(Enum):
	"""3 Members, HB_2 ... HB_8"""
	HB_2 = 0
	HB_32 = 1
	HB_8 = 2


# noinspection SpellCheckingInspection
class HrpUwbDeltaLength(Enum):
	"""3 Members, DL_16 ... DL_64"""
	DL_16 = 0
	DL_4 = 1
	DL_64 = 2


# noinspection SpellCheckingInspection
class HrpUwbDataSource(Enum):
	"""9 Members, ONE ... ZERO"""
	ONE = 0
	PN11 = 1
	PN15 = 2
	PN16 = 3
	PN20 = 4
	PN21 = 5
	PN23 = 6
	PN9 = 7
	ZERO = 8


# noinspection SpellCheckingInspection
class HrpUwbConvConsLen(Enum):
	"""2 Members, CL3 ... CL7"""
	CL3 = 0
	CL7 = 1


# noinspection SpellCheckingInspection
class HrpUwbCodeIndex(Enum):
	"""24 Members, CI_1 ... CI_9"""
	CI_1 = 0
	CI_10 = 1
	CI_11 = 2
	CI_12 = 3
	CI_13 = 4
	CI_14 = 5
	CI_15 = 6
	CI_16 = 7
	CI_17 = 8
	CI_18 = 9
	CI_19 = 10
	CI_2 = 11
	CI_20 = 12
	CI_21 = 13
	CI_22 = 14
	CI_23 = 15
	CI_24 = 16
	CI_3 = 17
	CI_4 = 18
	CI_5 = 19
	CI_6 = 20
	CI_7 = 21
	CI_8 = 22
	CI_9 = 23


# noinspection SpellCheckingInspection
class HrpUwbClocMode(Enum):
	"""3 Members, CSAMple ... SAMPle"""
	CSAMple = 0
	MSAMple = 1
	SAMPle = 2


# noinspection SpellCheckingInspection
class HrpUwbChipsPerBurst(Enum):
	"""9 Members, CPB_1 ... CPB_8"""
	CPB_1 = 0
	CPB_128 = 1
	CPB_16 = 2
	CPB_2 = 3
	CPB_32 = 4
	CPB_4 = 5
	CPB_512 = 6
	CPB_64 = 7
	CPB_8 = 8


# noinspection SpellCheckingInspection
class HrpUwbActSegmentNum(Enum):
	"""4 Members, ASN_1 ... ASN_4"""
	ASN_1 = 0
	ASN_2 = 1
	ASN_3 = 2
	ASN_4 = 3


# noinspection SpellCheckingInspection
class HrpUwbActSegmentLength(Enum):
	"""4 Members, ASL_128 ... ASL_64"""
	ASL_128 = 0
	ASL_256 = 1
	ASL_32 = 2
	ASL_64 = 3


# noinspection SpellCheckingInspection
class HilIfc(Enum):
	"""2 Members, SCPI ... UDP"""
	SCPI = 0
	UDP = 1


# noinspection SpellCheckingInspection
class HcOpyRegion(Enum):
	"""2 Members, ALL ... DIALog"""
	ALL = 0
	DIALog = 1


# noinspection SpellCheckingInspection
class HcOpImgFormat(Enum):
	"""4 Members, BMP ... XPM"""
	BMP = 0
	JPG = 1
	PNG = 2
	XPM = 3


# noinspection SpellCheckingInspection
class GsmSymbRateMode(Enum):
	"""2 Members, HSRate ... NSRate"""
	HSRate = 0
	NSRate = 1


# noinspection SpellCheckingInspection
class GsmSimMode(Enum):
	"""8 Members, AQPSk ... N32Qam"""
	AQPSk = 0
	EDGE = 1
	GSM = 2
	H16Qam = 3
	H32Qam = 4
	HQPSk = 5
	N16Qam = 6
	N32Qam = 7


# noinspection SpellCheckingInspection
class GsmModTypeQpsk(Enum):
	"""1 Members, QEDGe ... QEDGe"""
	QEDGe = 0


# noinspection SpellCheckingInspection
class GsmModTypeGsm(Enum):
	"""2 Members, FSK2 ... MSK"""
	FSK2 = 0
	MSK = 1


# noinspection SpellCheckingInspection
class GsmModTypeEdge(Enum):
	"""1 Members, P8EDge ... P8EDge"""
	P8EDge = 0


# noinspection SpellCheckingInspection
class GsmModTypeAqpsk(Enum):
	"""1 Members, AQPSk ... AQPSk"""
	AQPSk = 0


# noinspection SpellCheckingInspection
class GsmModType32Qam(Enum):
	"""1 Members, QAM32EDge ... QAM32EDge"""
	QAM32EDge = 0


# noinspection SpellCheckingInspection
class GsmModType16Qam(Enum):
	"""1 Members, QAM16EDge ... QAM16EDge"""
	QAM16EDge = 0


# noinspection SpellCheckingInspection
class GsmMode(Enum):
	"""4 Members, DOUBle ... UNFRamed"""
	DOUBle = 0
	MULTiframe = 1
	SINGle = 2
	UNFRamed = 3


# noinspection SpellCheckingInspection
class GsmMarkMode(Enum):
	"""7 Members, FRAMe ... TRIGger"""
	FRAMe = 0
	PATTern = 1
	PULSe = 2
	RATio = 3
	SDEF = 4
	SLOT = 5
	TRIGger = 6


# noinspection SpellCheckingInspection
class GsmBursType(Enum):
	"""23 Members, A16Qam ... SYNC"""
	A16Qam = 0
	A32Qam = 1
	AAQPsk = 2
	ACCess = 3
	ADATa = 4
	AEDGe = 5
	DUMMy = 6
	EDGE = 7
	FCORrection = 8
	H16Qam = 9
	H32Qam = 10
	HA16Qam = 11
	HA32Qam = 12
	HALF = 13
	HAQPsk = 14
	HQPSk = 15
	N16Qam = 16
	N32Qam = 17
	NAFF = 18
	NAFH = 19
	NAHH = 20
	NORMal = 21
	SYNC = 22


# noinspection SpellCheckingInspection
class GsmBursTscSet(Enum):
	"""2 Members, SET1 ... SET2"""
	SET1 = 0
	SET2 = 1


# noinspection SpellCheckingInspection
class GsmBursTscExt(Enum):
	"""4 Members, COMPact ... USER"""
	COMPact = 0
	CTS = 1
	STANdard = 2
	USER = 3


# noinspection SpellCheckingInspection
class GsmBursTsc(Enum):
	"""9 Members, T0 ... USER"""
	T0 = 0
	T1 = 1
	T2 = 2
	T3 = 3
	T4 = 4
	T5 = 5
	T6 = 6
	T7 = 7
	USER = 8


# noinspection SpellCheckingInspection
class GsmBursSync(Enum):
	"""4 Members, T0 ... USER"""
	T0 = 0
	T1 = 1
	T2 = 2
	USER = 3


# noinspection SpellCheckingInspection
class GsmBursSlotAtt(Enum):
	"""7 Members, A1 ... A7"""
	A1 = 0
	A2 = 1
	A3 = 2
	A4 = 3
	A5 = 4
	A6 = 5
	A7 = 6


# noinspection SpellCheckingInspection
class GsmBursPowMode(Enum):
	"""3 Members, ATT ... OFF"""
	ATT = 0
	FULL = 1
	OFF = 2


# noinspection SpellCheckingInspection
class GsmBursPowerRatio(Enum):
	"""8 Members, SCPIR0 ... SCPIR7"""
	SCPIR0 = 0
	SCPIR1 = 1
	SCPIR2 = 2
	SCPIR3 = 3
	SCPIR4 = 4
	SCPIR5 = 5
	SCPIR6 = 6
	SCPIR7 = 7


# noinspection SpellCheckingInspection
class GsmBursFix(Enum):
	"""3 Members, COMPact ... USER"""
	COMPact = 0
	STANdard = 1
	USER = 2


# noinspection SpellCheckingInspection
class GsmBursDataSour(Enum):
	"""11 Members, ALL0 ... PN9"""
	ALL0 = 0
	ALL1 = 1
	DLISt = 2
	PATTern = 3
	PN11 = 4
	PN15 = 5
	PN16 = 6
	PN20 = 7
	PN21 = 8
	PN23 = 9
	PN9 = 10


# noinspection SpellCheckingInspection
class GilterHigh(Enum):
	"""2 Members, ENPShape ... EWPShape"""
	ENPShape = 0
	EWPShape = 1


# noinspection SpellCheckingInspection
class GilterEdge(Enum):
	"""1 Members, LGAuss ... LGAuss"""
	LGAuss = 0


# noinspection SpellCheckingInspection
class Gilter(Enum):
	"""1 Members, GAUSs ... GAUSs"""
	GAUSs = 0


# noinspection SpellCheckingInspection
class GbasSsid(Enum):
	"""8 Members, A ... H"""
	A = 0
	B = 1
	C = 2
	D = 3
	E = 4
	F = 5
	G = 6
	H = 7


# noinspection SpellCheckingInspection
class GbasRunLet(Enum):
	"""4 Members, LETC ... NLETter"""
	LETC = 0
	LETL = 1
	LETR = 2
	NLETter = 3


# noinspection SpellCheckingInspection
class GbasMode(Enum):
	"""2 Members, GBAS ... SCAT"""
	GBAS = 0
	SCAT = 1


# noinspection SpellCheckingInspection
class GbasMarkMode(Enum):
	"""6 Members, PATTern ... TRIGger"""
	PATTern = 0
	PPS = 1
	PULSe = 2
	RATio = 3
	RESTart = 4
	TRIGger = 5


# noinspection SpellCheckingInspection
class GbasGrdStRefRec(Enum):
	"""3 Members, GW2R ... GW4R"""
	GW2R = 0
	GW3R = 1
	GW4R = 2


# noinspection SpellCheckingInspection
class GbasGrdStAcDes(Enum):
	"""3 Members, GADA ... GADC"""
	GADA = 0
	GADB = 1
	GADC = 2


# noinspection SpellCheckingInspection
class GbasGcid(Enum):
	"""2 Members, FC ... FD"""
	FC = 0
	FD = 1


# noinspection SpellCheckingInspection
class GbasDataSource(Enum):
	"""12 Members, DLISt ... ZERO"""
	DLISt = 0
	ONE = 1
	PATTern = 2
	PN11 = 3
	PN15 = 4
	PN16 = 5
	PN20 = 6
	PN21 = 7
	PN23 = 8
	PN9 = 9
	RGData = 10
	ZERO = 11


# noinspection SpellCheckingInspection
class GbasAppTchUnitSel(Enum):
	"""2 Members, FEET ... MET"""
	FEET = 0
	MET = 1


# noinspection SpellCheckingInspection
class GbasAppPerDes(Enum):
	"""3 Members, GAB ... GCD"""
	GAB = 0
	GC = 1
	GCD = 2


# noinspection SpellCheckingInspection
class FreqStepMode(Enum):
	"""2 Members, DECimal ... USER"""
	DECimal = 0
	USER = 1


# noinspection SpellCheckingInspection
class FreqShift(Enum):
	"""13 Members, FS0 ... FS99"""
	FS0 = 0
	FS1 = 1
	FS14 = 2
	FS19 = 3
	FS2 = 4
	FS24 = 5
	FS29 = 6
	FS3 = 7
	FS4 = 8
	FS54 = 9
	FS79 = 10
	FS9 = 11
	FS99 = 12


# noinspection SpellCheckingInspection
class FreqSel(Enum):
	"""2 Members, ALWD ... NALW"""
	ALWD = 0
	NALW = 1


# noinspection SpellCheckingInspection
class FreqRange(Enum):
	"""2 Members, FR2GT37 ... FR2LT334"""
	FR2GT37 = 0
	FR2LT334 = 1


# noinspection SpellCheckingInspection
class FreqOffset(Enum):
	"""2 Members, FO_0 ... FO_400"""
	FO_0 = 0
	FO_400 = 1


# noinspection SpellCheckingInspection
class FreqMode(Enum):
	"""5 Members, COMBined ... SWEep"""
	COMBined = 0
	CW = 1
	FIXed = 2
	LIST = 3
	SWEep = 4


# noinspection SpellCheckingInspection
class FrcType(Enum):
	"""112 Members, FR1A11 ... NA"""
	FR1A11 = 0
	FR1A12 = 1
	FR1A13 = 2
	FR1A14 = 3
	FR1A15 = 4
	FR1A16 = 5
	FR1A17 = 6
	FR1A18 = 7
	FR1A19 = 8
	FR1A21 = 9
	FR1A22 = 10
	FR1A23 = 11
	FR1A24 = 12
	FR1A25 = 13
	FR1A26 = 14
	FR1A310 = 15
	FR1A311 = 16
	FR1A312 = 17
	FR1A313 = 18
	FR1A314 = 19
	FR1A322 = 20
	FR1A323 = 21
	FR1A324 = 22
	FR1A325 = 23
	FR1A326 = 24
	FR1A327 = 25
	FR1A328 = 26
	FR1A331 = 27
	FR1A332 = 28
	FR1A38 = 29
	FR1A39 = 30
	FR1A410 = 31
	FR1A411 = 32
	FR1A412 = 33
	FR1A413 = 34
	FR1A414 = 35
	FR1A422 = 36
	FR1A423 = 37
	FR1A424 = 38
	FR1A425 = 39
	FR1A426 = 40
	FR1A427 = 41
	FR1A428 = 42
	FR1A48 = 43
	FR1A49 = 44
	FR1A510 = 45
	FR1A511 = 46
	FR1A512 = 47
	FR1A513 = 48
	FR1A514 = 49
	FR1A58 = 50
	FR1A59 = 51
	FR2A11 = 52
	FR2A12 = 53
	FR2A13 = 54
	FR2A14 = 55
	FR2A15 = 56
	FR2A31 = 57
	FR2A310 = 58
	FR2A311 = 59
	FR2A312 = 60
	FR2A313 = 61
	FR2A314 = 62
	FR2A315 = 63
	FR2A316 = 64
	FR2A317 = 65
	FR2A318 = 66
	FR2A319 = 67
	FR2A32 = 68
	FR2A320 = 69
	FR2A321 = 70
	FR2A322 = 71
	FR2A323 = 72
	FR2A324 = 73
	FR2A33 = 74
	FR2A34 = 75
	FR2A35 = 76
	FR2A36 = 77
	FR2A37 = 78
	FR2A38 = 79
	FR2A39 = 80
	FR2A41 = 81
	FR2A410 = 82
	FR2A411 = 83
	FR2A412 = 84
	FR2A413 = 85
	FR2A414 = 86
	FR2A415 = 87
	FR2A416 = 88
	FR2A417 = 89
	FR2A418 = 90
	FR2A419 = 91
	FR2A42 = 92
	FR2A420 = 93
	FR2A43 = 94
	FR2A44 = 95
	FR2A45 = 96
	FR2A46 = 97
	FR2A47 = 98
	FR2A48 = 99
	FR2A49 = 100
	FR2A51 = 101
	FR2A510 = 102
	FR2A52 = 103
	FR2A53 = 104
	FR2A54 = 105
	FR2A55 = 106
	FR2A56 = 107
	FR2A57 = 108
	FR2A58 = 109
	FR2A59 = 110
	NA = 111


# noinspection SpellCheckingInspection
class FormStatReg(Enum):
	"""4 Members, ASCii ... OCTal"""
	ASCii = 0
	BINary = 1
	HEXadecimal = 2
	OCTal = 3


# noinspection SpellCheckingInspection
class FormData(Enum):
	"""2 Members, ASCii ... PACKed"""
	ASCii = 0
	PACKed = 1


# noinspection SpellCheckingInspection
class Fmt(Enum):
	"""1 Members, FMT70 ... FMT70"""
	FMT70 = 0


# noinspection SpellCheckingInspection
class FmStereoTrigMode(Enum):
	"""1 Members, AUTO ... AUTO"""
	AUTO = 0


# noinspection SpellCheckingInspection
class FmStereoTimeCfgSel(Enum):
	"""2 Members, SYSTime ... USRTime"""
	SYSTime = 0
	USRTime = 1


# noinspection SpellCheckingInspection
class FmStereoRdsRbdsCfgUsrGrpBeh(Enum):
	"""2 Members, HEXFormat ... MSGFormat"""
	HEXFormat = 0
	MSGFormat = 1


# noinspection SpellCheckingInspection
class FmStereoRdsRbdsCfgDataSource(Enum):
	"""2 Members, GRPList ... UDGRoups"""
	GRPList = 0
	UDGRoups = 1


# noinspection SpellCheckingInspection
class FmStereoPreEmph(Enum):
	"""3 Members, _50 ... OFF"""
	_50 = 0
	_75 = 1
	OFF = 2


# noinspection SpellCheckingInspection
class FmStereoMscVce(Enum):
	"""2 Members, MUSic ... VOICe"""
	MUSic = 0
	VOICe = 1


# noinspection SpellCheckingInspection
class FmStereoMode(Enum):
	"""5 Members, LEFT ... RNELeft"""
	LEFT = 0
	RELeft = 1
	REMLeft = 2
	RIGHt = 3
	RNELeft = 4


# noinspection SpellCheckingInspection
class FmStereoInpMeth(Enum):
	"""2 Members, PARameters ... UDMessage"""
	PARameters = 0
	UDMessage = 1


# noinspection SpellCheckingInspection
class FmStereoDateCfgSel(Enum):
	"""2 Members, SYSDate ... USRDate"""
	SYSDate = 0
	USRDate = 1


# noinspection SpellCheckingInspection
class FmStereoCfgMode(Enum):
	"""2 Members, RBDS ... RDS"""
	RBDS = 0
	RDS = 1


# noinspection SpellCheckingInspection
class FmStereoAudSrc(Enum):
	"""4 Members, FILE ... SPEXt"""
	FILE = 0
	LFGen = 1
	OFF = 2
	SPEXt = 3


# noinspection SpellCheckingInspection
class FmStereoAudExtClk(Enum):
	"""2 Members, _44100 ... _48000"""
	_44100 = 0
	_48000 = 1


# noinspection SpellCheckingInspection
class FmMode(Enum):
	"""2 Members, HBANdwidth ... LNOise"""
	HBANdwidth = 0
	LNOise = 1


# noinspection SpellCheckingInspection
class FiltOptType(Enum):
	"""5 Members, ACP ... STD"""
	ACP = 0
	ACPN = 1
	BENU = 2
	EVM = 3
	STD = 4


# noinspection SpellCheckingInspection
class FilterWidth(Enum):
	"""2 Members, NARRow ... WIDE"""
	NARRow = 0
	WIDE = 1


# noinspection SpellCheckingInspection
class FilterTestModels(Enum):
	"""9 Members, ALL ... TM3_3"""
	ALL = 0
	TM1_1 = 1
	TM1_2 = 2
	TM2 = 3
	TM2a = 4
	TM3_1 = 5
	TM3_1A = 6
	TM3_2 = 7
	TM3_3 = 8


# noinspection SpellCheckingInspection
class FilterSubcarrierSpacing(Enum):
	"""5 Members, ALL ... F60"""
	ALL = 0
	F120 = 1
	F15 = 2
	F30 = 3
	F60 = 4


# noinspection SpellCheckingInspection
class FilterMode(Enum):
	"""8 Members, _0 ... USER"""
	_0 = 0
	_1 = 1
	_2 = 2
	BWP = 3
	CBW = 4
	FAST = 5
	OFF = 6
	USER = 7


# noinspection SpellCheckingInspection
class FilterFreqRange(Enum):
	"""3 Members, ALL ... FR2"""
	ALL = 0
	FR1 = 1
	FR2 = 2


# noinspection SpellCheckingInspection
class FilterDuplexing(Enum):
	"""3 Members, ALL ... TDD"""
	ALL = 0
	FDD = 1
	TDD = 2


# noinspection SpellCheckingInspection
class FilterBandwidth(Enum):
	"""16 Members, ALL ... F90"""
	ALL = 0
	F10 = 1
	F100 = 2
	F15 = 3
	F20 = 4
	F200 = 5
	F25 = 6
	F30 = 7
	F40 = 8
	F400 = 9
	F5 = 10
	F50 = 11
	F60 = 12
	F70 = 13
	F80 = 14
	F90 = 15


# noinspection SpellCheckingInspection
class FeedbackRateAll(Enum):
	"""3 Members, R115 ... R1M9"""
	R115 = 0
	R1M6 = 1
	R1M9 = 2


# noinspection SpellCheckingInspection
class FeedbackModeAll(Enum):
	"""3 Members, OFF ... SERial"""
	OFF = 0
	S3X8 = 1
	SERial = 2


# noinspection SpellCheckingInspection
class FeedbackConnectorAll(Enum):
	"""2 Members, GLOBal ... LOCal"""
	GLOBal = 0
	LOCal = 1


# noinspection SpellCheckingInspection
class FeedbackConnector(Enum):
	"""2 Members, LEVatt ... USER1"""
	LEVatt = 0
	USER1 = 1


# noinspection SpellCheckingInspection
class FbiMode(Enum):
	"""3 Members, D1B ... OFF"""
	D1B = 0
	D2B = 1
	OFF = 2


# noinspection SpellCheckingInspection
class EvdoTermMode(Enum):
	"""2 Members, ACCess ... TRAFfic"""
	ACCess = 0
	TRAFfic = 1


# noinspection SpellCheckingInspection
class EvdoRpcMode(Enum):
	"""5 Members, DOWN ... UP"""
	DOWN = 0
	HOLD = 1
	PATTern = 2
	RANGe = 3
	UP = 4


# noinspection SpellCheckingInspection
class EvdoRabLen(Enum):
	"""4 Members, RL16 ... RL8"""
	RL16 = 0
	RL32 = 1
	RL64 = 2
	RL8 = 3


# noinspection SpellCheckingInspection
class EvdoPredSett(Enum):
	"""19 Members, ULS1DR153K6 ... USER"""
	ULS1DR153K6 = 0
	ULS1DR19K2 = 1
	ULS1DR38K4 = 2
	ULS1DR76K8 = 3
	ULS1DR9K6 = 4
	ULS2PS1024LL = 5
	ULS2PS12288LL = 6
	ULS2PS128LL = 7
	ULS2PS1536LL = 8
	ULS2PS2048LL = 9
	ULS2PS256HC = 10
	ULS2PS256LL = 11
	ULS2PS3072LL = 12
	ULS2PS4096LL = 13
	ULS2PS512LL = 14
	ULS2PS6144LL = 15
	ULS2PS768LL = 16
	ULS2PS8192LL = 17
	USER = 18


# noinspection SpellCheckingInspection
class EvdoPayload(Enum):
	"""12 Members, PS1024 ... PS8192"""
	PS1024 = 0
	PS12288 = 1
	PS128 = 2
	PS1536 = 3
	PS2048 = 4
	PS256 = 5
	PS3072 = 6
	PS4096 = 7
	PS512 = 8
	PS6144 = 9
	PS768 = 10
	PS8192 = 11


# noinspection SpellCheckingInspection
class EvdoPacketSize(Enum):
	"""14 Members, PS1024 ... PS8192"""
	PS1024 = 0
	PS12288 = 1
	PS128 = 2
	PS1536 = 3
	PS2048 = 4
	PS256 = 5
	PS3072 = 6
	PS4096 = 7
	PS512 = 8
	PS5120 = 9
	PS6144 = 10
	PS7168 = 11
	PS768 = 12
	PS8192 = 13


# noinspection SpellCheckingInspection
class EvdoModulation(Enum):
	"""5 Members, B4 ... Q4Q2"""
	B4 = 0
	E4E2 = 1
	Q2 = 2
	Q4 = 3
	Q4Q2 = 4


# noinspection SpellCheckingInspection
class EvdoMarkMode(Enum):
	"""7 Members, CSPeriod ... USER"""
	CSPeriod = 0
	ESM = 1
	PNSPeriod = 2
	RATio = 3
	SLOT = 4
	TRIGger = 5
	USER = 6


# noinspection SpellCheckingInspection
class EvdoLayerDn(Enum):
	"""3 Members, S1 ... S3"""
	S1 = 0
	S2 = 1
	S3 = 2


# noinspection SpellCheckingInspection
class EvdoLayer(Enum):
	"""2 Members, S1 ... S2"""
	S1 = 0
	S2 = 1


# noinspection SpellCheckingInspection
class EvdoHarqMode(Enum):
	"""3 Members, ACK ... OFF"""
	ACK = 0
	NAK = 1
	OFF = 2


# noinspection SpellCheckingInspection
class EvdoDrcPer(Enum):
	"""4 Members, DP0 ... DP8"""
	DP0 = 0
	DP16 = 1
	DP4 = 2
	DP8 = 3


# noinspection SpellCheckingInspection
class EvdoDrcLenUp(Enum):
	"""4 Members, DL1 ... DL8"""
	DL1 = 0
	DL2 = 1
	DL4 = 2
	DL8 = 3


# noinspection SpellCheckingInspection
class EvdoDrcLenDn(Enum):
	"""6 Members, DL1 ... DL8"""
	DL1 = 0
	DL16 = 1
	DL32 = 2
	DL4 = 3
	DL64 = 4
	DL8 = 5


# noinspection SpellCheckingInspection
class EvdoDataRate(Enum):
	"""21 Members, DR1075K2 ... DR9K6"""
	DR1075K2 = 0
	DR1228K8 = 1
	DR1536K = 2
	DR153K6 = 3
	DR1843K2 = 4
	DR19K2 = 5
	DR2150K4 = 6
	DR2457K6 = 7
	DR3072K = 8
	DR307K2 = 9
	DR3686K4 = 10
	DR38K4 = 11
	DR4300K8 = 12
	DR460K8 = 13
	DR4915K2 = 14
	DR4K8 = 15
	DR614K4 = 16
	DR768K = 17
	DR76K8 = 18
	DR921K6 = 19
	DR9K6 = 20


# noinspection SpellCheckingInspection
class EvdoBandClass(Enum):
	"""22 Members, BC0 ... BC9"""
	BC0 = 0
	BC1 = 1
	BC10 = 2
	BC11 = 3
	BC12 = 4
	BC13 = 5
	BC14 = 6
	BC15 = 7
	BC16 = 8
	BC17 = 9
	BC18 = 10
	BC19 = 11
	BC2 = 12
	BC20 = 13
	BC21 = 14
	BC3 = 15
	BC4 = 16
	BC5 = 17
	BC6 = 18
	BC7 = 19
	BC8 = 20
	BC9 = 21


# noinspection SpellCheckingInspection
class EvdoAckMode(Enum):
	"""2 Members, BPSK ... OOK"""
	BPSK = 0
	OOK = 1


# noinspection SpellCheckingInspection
class EutraViewMode(Enum):
	"""2 Members, PRB ... VRB"""
	PRB = 0
	VRB = 1


# noinspection SpellCheckingInspection
class EutraUnit(Enum):
	"""5 Members, FRAMe ... SUBFrame"""
	FRAMe = 0
	SAMPle = 1
	SEQuence = 2
	SLOT = 3
	SUBFrame = 4


# noinspection SpellCheckingInspection
class EutraUlueNbiotModulation(Enum):
	"""3 Members, PI2Bpsk ... QPSK"""
	PI2Bpsk = 0
	PI4Qpsk = 1
	QPSK = 2


# noinspection SpellCheckingInspection
class EutraUlSidelinkContentType(Enum):
	"""4 Members, PSBCh ... PSSCh"""
	PSBCh = 0
	PSCCh = 1
	PSDCh = 2
	PSSCh = 3


# noinspection SpellCheckingInspection
class EutraUlNoNpuschrEpNbIoTaLl(Enum):
	"""4 Members, _1 ... _64"""
	_1 = 0
	_16 = 1
	_2 = 2
	_64 = 3


# noinspection SpellCheckingInspection
class EutraUlModulation(Enum):
	"""5 Members, PSK8 ... QPSK"""
	PSK8 = 0
	QAM16 = 1
	QAM256 = 2
	QAM64 = 3
	QPSK = 4


# noinspection SpellCheckingInspection
class EutraUlFreqHopType(Enum):
	"""3 Members, NONE ... TP2"""
	NONE = 0
	TP1 = 1
	TP2 = 2


# noinspection SpellCheckingInspection
class EutraUlFreqHopMode(Enum):
	"""2 Members, INTer ... INTRa"""
	INTer = 0
	INTRa = 1


# noinspection SpellCheckingInspection
class EutraUlFrc(Enum):
	"""79 Members, A11 ... UE3"""
	A11 = 0
	A12 = 1
	A121 = 2
	A122 = 3
	A123 = 4
	A124 = 5
	A125 = 6
	A126 = 7
	A13 = 8
	A131 = 9
	A132 = 10
	A133 = 11
	A134 = 12
	A135 = 13
	A136 = 14
	A14 = 15
	A15 = 16
	A16 = 17
	A17 = 18
	A171 = 19
	A172 = 20
	A173 = 21
	A174 = 22
	A175 = 23
	A176 = 24
	A181 = 25
	A182 = 26
	A183 = 27
	A184 = 28
	A185 = 29
	A186 = 30
	A191 = 31
	A192 = 32
	A193 = 33
	A194 = 34
	A195 = 35
	A196 = 36
	A21 = 37
	A22 = 38
	A23 = 39
	A31 = 40
	A32 = 41
	A33 = 42
	A34 = 43
	A35 = 44
	A36 = 45
	A37 = 46
	A41 = 47
	A42 = 48
	A43 = 49
	A44 = 50
	A45 = 51
	A46 = 52
	A47 = 53
	A48 = 54
	A51 = 55
	A52 = 56
	A53 = 57
	A54 = 58
	A55 = 59
	A56 = 60
	A57 = 61
	A71 = 62
	A72 = 63
	A73 = 64
	A74 = 65
	A75 = 66
	A76 = 67
	A81 = 68
	A82 = 69
	A83 = 70
	A84 = 71
	A85 = 72
	A86 = 73
	UE11 = 74
	UE12 = 75
	UE21 = 76
	UE22 = 77
	UE3 = 78


# noinspection SpellCheckingInspection
class EutraUlFormatEmtc(Enum):
	"""6 Members, F1 ... F2B"""
	F1 = 0
	F1A = 1
	F1B = 2
	F2 = 3
	F2A = 4
	F2B = 5


# noinspection SpellCheckingInspection
class EutraUlFormat(Enum):
	"""9 Members, F1 ... F5"""
	F1 = 0
	F1A = 1
	F1B = 2
	F2 = 3
	F2A = 4
	F2B = 5
	F3 = 6
	F4 = 7
	F5 = 8


# noinspection SpellCheckingInspection
class EutraUlContentTypeWithIot(Enum):
	"""4 Members, EMTC ... PUSCh"""
	EMTC = 0
	NIOT = 1
	PUCCh = 2
	PUSCh = 3


# noinspection SpellCheckingInspection
class EutraUlContentType(Enum):
	"""2 Members, PUCCh ... PUSCh"""
	PUCCh = 0
	PUSCh = 1


# noinspection SpellCheckingInspection
class EutraUeReleaseDl(Enum):
	"""5 Members, EM_A ... R89"""
	EM_A = 0
	EM_B = 1
	LADV = 2
	NIOT = 3
	R89 = 4


# noinspection SpellCheckingInspection
class EutraUeRelease(Enum):
	"""4 Members, EMTC ... R89"""
	EMTC = 0
	LADV = 1
	NIOT = 2
	R89 = 3


# noinspection SpellCheckingInspection
class EutraUeMode(Enum):
	"""2 Members, PRACh ... STD"""
	PRACh = 0
	STD = 1


# noinspection SpellCheckingInspection
class EutraUeCat(Enum):
	"""25 Members, C1 ... USER"""
	C1 = 0
	C10 = 1
	C11 = 2
	C12 = 3
	C13 = 4
	C14 = 5
	C15 = 6
	C16 = 7
	C17 = 8
	C18 = 9
	C19 = 10
	C2 = 11
	C20 = 12
	C3 = 13
	C4 = 14
	C5 = 15
	C6 = 16
	C7 = 17
	C8 = 18
	C9 = 19
	M1 = 20
	M2 = 21
	NB1 = 22
	NB2 = 23
	USER = 24


# noinspection SpellCheckingInspection
class EutraTxMode(Enum):
	"""11 Members, M1 ... USER"""
	M1 = 0
	M10 = 1
	M2 = 2
	M3 = 3
	M4 = 4
	M5 = 5
	M6 = 6
	M7 = 7
	M8 = 8
	M9 = 9
	USER = 10


# noinspection SpellCheckingInspection
class EutraTranSource(Enum):
	"""2 Members, DATA ... DTX"""
	DATA = 0
	DTX = 1


# noinspection SpellCheckingInspection
class EutraTimcNtAoffs(Enum):
	"""4 Members, _0 ... NTA624"""
	_0 = 0
	_624 = 1
	NTA0 = 2
	NTA624 = 3


# noinspection SpellCheckingInspection
class EutraTestCaseTs36141(Enum):
	"""26 Members, TS36141_TC626 ... TS36141_TC841"""
	TS36141_TC626 = 0
	TS36141_TC627 = 1
	TS36141_TC628 = 2
	TS36141_TC67 = 3
	TS36141_TC72 = 4
	TS36141_TC73 = 5
	TS36141_TC74 = 6
	TS36141_TC75A = 7
	TS36141_TC75B = 8
	TS36141_TC76 = 9
	TS36141_TC78 = 10
	TS36141_TC821 = 11
	TS36141_TC821A = 12
	TS36141_TC822 = 13
	TS36141_TC823 = 14
	TS36141_TC824 = 15
	TS36141_TC831 = 16
	TS36141_TC832 = 17
	TS36141_TC833 = 18
	TS36141_TC834 = 19
	TS36141_TC835 = 20
	TS36141_TC836 = 21
	TS36141_TC837 = 22
	TS36141_TC838 = 23
	TS36141_TC839 = 24
	TS36141_TC841 = 25


# noinspection SpellCheckingInspection
class EutraTcwtRigConf(Enum):
	"""2 Members, AAUTo ... UNCHanged"""
	AAUTo = 0
	UNCHanged = 1


# noinspection SpellCheckingInspection
class EutraTcwSignalRout(Enum):
	"""2 Members, PORTA ... PORTB"""
	PORTA = 0
	PORTB = 1


# noinspection SpellCheckingInspection
class EutraTcwsIgAdvNtaOffs(Enum):
	"""2 Members, NTA0 ... NTA624"""
	NTA0 = 0
	NTA624 = 1


# noinspection SpellCheckingInspection
class EutraTcwrtfMode(Enum):
	"""3 Members, BIN ... SER3X8"""
	BIN = 0
	SER = 1
	SER3X8 = 2


# noinspection SpellCheckingInspection
class EutraTcwRelease(Enum):
	"""5 Members, REL10 ... REL9"""
	REL10 = 0
	REL11 = 1
	REL12 = 2
	REL8 = 3
	REL9 = 4


# noinspection SpellCheckingInspection
class EutraTcwPropagCond(Enum):
	"""10 Members, AWGNonly ... PDMov"""
	AWGNonly = 0
	EPA5 = 1
	ETU200Mov = 2
	ETU300 = 3
	ETU70 = 4
	EVA5 = 5
	EVA70 = 6
	HST1 = 7
	HST3 = 8
	PDMov = 9


# noinspection SpellCheckingInspection
class EutraTcwoFfsChanEdge(Enum):
	"""3 Members, OCE12_5 ... OCE7_5"""
	OCE12_5 = 0
	OCE2_5 = 1
	OCE7_5 = 2


# noinspection SpellCheckingInspection
class EutraTcwNumOfRxAnt(Enum):
	"""3 Members, ANT1 ... ANT4"""
	ANT1 = 0
	ANT2 = 1
	ANT4 = 2


# noinspection SpellCheckingInspection
class EutraTcwMarkConf(Enum):
	"""2 Members, FRAMe ... UNCHanged"""
	FRAMe = 0
	UNCHanged = 1


# noinspection SpellCheckingInspection
class EutraTcwInterfType(Enum):
	"""4 Members, CW ... UTRA"""
	CW = 0
	EUTra = 1
	NEUTra = 2
	UTRA = 3


# noinspection SpellCheckingInspection
class EutraTcwiNstSetup(Enum):
	"""2 Members, U1PATH ... U2PATH"""
	U1PATH = 0
	U2PATH = 1


# noinspection SpellCheckingInspection
class EutraTcwGsModeDefaultRange(Enum):
	"""3 Members, ADRate ... FDRate"""
	ADRate = 0
	DRATe = 1
	FDRate = 2


# noinspection SpellCheckingInspection
class EutraTcwGeneratedSig(Enum):
	"""2 Members, IF23 ... WSIF1AWGN"""
	IF23 = 0
	WSIF1AWGN = 1


# noinspection SpellCheckingInspection
class EutraTcwfReqShift(Enum):
	"""13 Members, FS0 ... FS9"""
	FS0 = 0
	FS1 = 1
	FS10 = 2
	FS13 = 3
	FS14 = 4
	FS19 = 5
	FS2 = 6
	FS24 = 7
	FS3 = 8
	FS4 = 9
	FS5 = 10
	FS7 = 11
	FS9 = 12


# noinspection SpellCheckingInspection
class EutraTcwfReqOffset(Enum):
	"""4 Members, FO_0 ... FO_625"""
	FO_0 = 0
	FO_1340 = 1
	FO_270 = 2
	FO_625 = 3


# noinspection SpellCheckingInspection
class EutraTcwfReqAlloc(Enum):
	"""2 Members, HIGHer ... LOWer"""
	HIGHer = 0
	LOWer = 1


# noinspection SpellCheckingInspection
class EutraTcwfRactMaxThroughput(Enum):
	"""2 Members, FMT30 ... FMT70"""
	FMT30 = 0
	FMT70 = 1


# noinspection SpellCheckingInspection
class EutraTcwConnector(Enum):
	"""3 Members, LEVatt ... USER1"""
	LEVatt = 0
	NOFB = 1
	USER1 = 2


# noinspection SpellCheckingInspection
class EutraTcwBurstFormat(Enum):
	"""5 Members, BF0 ... BF4"""
	BF0 = 0
	BF1 = 1
	BF2 = 2
	BF3 = 3
	BF4 = 4


# noinspection SpellCheckingInspection
class EutraTcwaNtSubset(Enum):
	"""3 Members, ALL ... AS34"""
	ALL = 0
	AS12 = 1
	AS34 = 2


# noinspection SpellCheckingInspection
class EutraSubCarrierSpacing(Enum):
	"""2 Members, S15 ... S375"""
	S15 = 0
	S375 = 1


# noinspection SpellCheckingInspection
class EutraStdMode(Enum):
	"""3 Members, IOT ... LTE"""
	IOT = 0
	LIOT = 1
	LTE = 2


# noinspection SpellCheckingInspection
class EutraSpsInt(Enum):
	"""10 Members, S10 ... S80"""
	S10 = 0
	S128 = 1
	S160 = 2
	S20 = 3
	S32 = 4
	S320 = 5
	S40 = 6
	S64 = 7
	S640 = 8
	S80 = 9


# noinspection SpellCheckingInspection
class EutraSlV2XSubchannelSize(Enum):
	"""20 Members, _10 ... _96"""
	_10 = 0
	_100 = 1
	_12 = 2
	_15 = 3
	_16 = 4
	_18 = 5
	_20 = 6
	_25 = 7
	_30 = 8
	_32 = 9
	_4 = 10
	_48 = 11
	_5 = 12
	_50 = 13
	_6 = 14
	_72 = 15
	_75 = 16
	_8 = 17
	_9 = 18
	_96 = 19


# noinspection SpellCheckingInspection
class EutraSlV2XrMc(Enum):
	"""3 Members, R821 ... R823"""
	R821 = 0
	R822 = 1
	R823 = 2


# noinspection SpellCheckingInspection
class EutraSlV2XnUmSubchannels(Enum):
	"""7 Members, _1 ... _8"""
	_1 = 0
	_10 = 1
	_15 = 2
	_20 = 3
	_3 = 4
	_5 = 5
	_8 = 6


# noinspection SpellCheckingInspection
class EutraSlV2XbMpLength(Enum):
	"""8 Members, _10 ... _60"""
	_10 = 0
	_100 = 1
	_16 = 2
	_20 = 3
	_30 = 4
	_40 = 5
	_50 = 6
	_60 = 7


# noinspection SpellCheckingInspection
class EutraSlN3Pdsch(Enum):
	"""2 Members, _1 ... _5"""
	_1 = 0
	_5 = 1


# noinspection SpellCheckingInspection
class EutraSlMode(Enum):
	"""3 Members, COMM ... V2X"""
	COMM = 0
	DISC = 1
	V2X = 2


# noinspection SpellCheckingInspection
class EutraSlDiscType(Enum):
	"""2 Members, D1 ... D2B"""
	D1 = 0
	D2B = 1


# noinspection SpellCheckingInspection
class EutraSlDiscControlPeriod(Enum):
	"""6 Members, _1024 ... _64"""
	_1024 = 0
	_128 = 1
	_256 = 2
	_32 = 3
	_512 = 4
	_64 = 5


# noinspection SpellCheckingInspection
class EutraSlCommControlPeriod(Enum):
	"""10 Members, _120 ... _80"""
	_120 = 0
	_140 = 1
	_160 = 2
	_240 = 3
	_280 = 4
	_320 = 5
	_40 = 6
	_60 = 7
	_70 = 8
	_80 = 9


# noinspection SpellCheckingInspection
class EutraSimAnt(Enum):
	"""4 Members, ANT1 ... ANT4"""
	ANT1 = 0
	ANT2 = 1
	ANT3 = 2
	ANT4 = 3


# noinspection SpellCheckingInspection
class EutraSerialRate(Enum):
	"""3 Members, SR1_6M ... SR115_2K"""
	SR1_6M = 0
	SR1_92M = 1
	SR115_2K = 2


# noinspection SpellCheckingInspection
class EutraSearchSpaceNbIoT(Enum):
	"""3 Members, T1CM ... UE"""
	T1CM = 0
	T2CM = 1
	UE = 2


# noinspection SpellCheckingInspection
class EutraSearchSpaceEmtc(Enum):
	"""4 Members, T0CM ... UE"""
	T0CM = 0
	T1CM = 1
	T2CM = 2
	UE = 3


# noinspection SpellCheckingInspection
class EutraSearchSpace(Enum):
	"""7 Members, _0 ... UE"""
	_0 = 0
	_1 = 1
	AUTO = 2
	COMMon = 3
	OFF = 4
	ON = 5
	UE = 6


# noinspection SpellCheckingInspection
class EutraSciFormat(Enum):
	"""1 Members, _0 ... _0"""
	_0 = 0


# noinspection SpellCheckingInspection
class EutraRepetitionsNbiot(Enum):
	"""8 Members, R1 ... R8"""
	R1 = 0
	R128 = 1
	R16 = 2
	R2 = 3
	R32 = 4
	R4 = 5
	R64 = 6
	R8 = 7


# noinspection SpellCheckingInspection
class EutraPwrUpdMode(Enum):
	"""2 Members, CONTinuous ... MANual"""
	CONTinuous = 0
	MANual = 1


# noinspection SpellCheckingInspection
class EutraPuschTxMode(Enum):
	"""2 Members, M1 ... M2"""
	M1 = 0
	M2 = 1


# noinspection SpellCheckingInspection
class EutraPuschPrecScheme(Enum):
	"""2 Members, NONE ... SPM"""
	NONE = 0
	SPM = 1


# noinspection SpellCheckingInspection
class EutraPuccN1Dmrs(Enum):
	"""8 Members, _0 ... _9"""
	_0 = 0
	_10 = 1
	_2 = 2
	_3 = 3
	_4 = 4
	_6 = 5
	_8 = 6
	_9 = 7


# noinspection SpellCheckingInspection
class EutraPucchNumAp(Enum):
	"""2 Members, AP1 ... AP2"""
	AP1 = 0
	AP2 = 1


# noinspection SpellCheckingInspection
class EutraPracNbiotSubcarriers(Enum):
	"""4 Members, _12 ... _48"""
	_12 = 0
	_24 = 1
	_36 = 2
	_48 = 3


# noinspection SpellCheckingInspection
class EutraPracNbiotSubcarrierOffset(Enum):
	"""18 Members, _0 ... _90"""
	_0 = 0
	_102 = 1
	_108 = 2
	_12 = 3
	_18 = 4
	_2 = 5
	_24 = 6
	_34 = 7
	_36 = 8
	_42 = 9
	_48 = 10
	_54 = 11
	_6 = 12
	_60 = 13
	_72 = 14
	_78 = 15
	_84 = 16
	_90 = 17


# noinspection SpellCheckingInspection
class EutraPracNbiotStartTimeMs(Enum):
	"""18 Members, _10 ... _80"""
	_10 = 0
	_1024 = 1
	_128 = 2
	_1280 = 3
	_16 = 4
	_160 = 5
	_20 = 6
	_256 = 7
	_2560 = 8
	_32 = 9
	_320 = 10
	_40 = 11
	_512 = 12
	_5120 = 13
	_64 = 14
	_640 = 15
	_8 = 16
	_80 = 17


# noinspection SpellCheckingInspection
class EutraPracNbiotPreambleFormat(Enum):
	"""7 Members, _0 ... F2"""
	_0 = 0
	_1 = 1
	F0 = 2
	F0A = 3
	F1 = 4
	F1A = 5
	F2 = 6


# noinspection SpellCheckingInspection
class EutraPracNbiotPeriodicity(Enum):
	"""10 Members, _10240 ... _80"""
	_10240 = 0
	_1280 = 1
	_160 = 2
	_240 = 3
	_2560 = 4
	_320 = 5
	_40 = 6
	_5120 = 7
	_640 = 8
	_80 = 9


# noinspection SpellCheckingInspection
class EutraPrachPreambleSet(Enum):
	"""5 Members, ARES ... URES"""
	ARES = 0
	BRES = 1
	OFF = 2
	ON = 3
	URES = 4


# noinspection SpellCheckingInspection
class EutraPowcRefChan(Enum):
	"""7 Members, NF ... SRS"""
	NF = 0
	PRACH = 1
	PUCCH = 2
	PUCPUS = 3
	PUSCH = 4
	SL = 5
	SRS = 6


# noinspection SpellCheckingInspection
class EutraPowcLevRef(Enum):
	"""5 Members, DRMS ... URMS"""
	DRMS = 0
	FRMS = 1
	NPBCH = 2
	UEBurst = 3
	URMS = 4


# noinspection SpellCheckingInspection
class EutraPhichPwrMode(Enum):
	"""2 Members, CONSt ... IND"""
	CONSt = 0
	IND = 1


# noinspection SpellCheckingInspection
class EutraPhichNg(Enum):
	"""5 Members, NG1 ... NGCustom"""
	NG1 = 0
	NG1_2 = 1
	NG1_6 = 2
	NG2 = 3
	NGCustom = 4


# noinspection SpellCheckingInspection
class EutraPdscPowA(Enum):
	"""8 Members, _0 ... _minus6_dot_02"""
	_0 = 0
	_0_dot_97 = 1
	_minus1_dot_77 = 2
	_2_dot_04 = 3
	_3_dot_01 = 4
	_minus3_dot_01 = 5
	_minus4_dot_77 = 6
	_minus6_dot_02 = 7


# noinspection SpellCheckingInspection
class EutraPdschSchedMode(Enum):
	"""3 Members, ASEQuence ... MANual"""
	ASEQuence = 0
	AUTO = 1
	MANual = 2


# noinspection SpellCheckingInspection
class EutraPdcchTypeEmtc(Enum):
	"""2 Members, MPD1 ... MPD2"""
	MPD1 = 0
	MPD2 = 1


# noinspection SpellCheckingInspection
class EutraPdcchType(Enum):
	"""3 Members, EPD1 ... PDCCh"""
	EPD1 = 0
	EPD2 = 1
	PDCCh = 2


# noinspection SpellCheckingInspection
class EutraPdcchCfg(Enum):
	"""17 Members, CCRNti ... USER4"""
	CCRNti = 0
	NONE = 1
	PRNTi = 2
	RARNti = 3
	SIRNti = 4
	U1Eimta = 5
	U1SPs = 6
	U2Eimta = 7
	U2SPs = 8
	U3Eimta = 9
	U3SPs = 10
	U4Eimta = 11
	U4SPs = 12
	USER1 = 13
	USER2 = 14
	USER3 = 15
	USER4 = 16


# noinspection SpellCheckingInspection
class EutraPdccFmtLaa(Enum):
	"""2 Members, F2 ... F3"""
	F2 = 0
	F3 = 1


# noinspection SpellCheckingInspection
class EutraPdccFmt2(Enum):
	"""6 Members, _0 ... VAR"""
	_0 = 0
	_1 = 1
	_minus1 = 2
	_2 = 3
	_3 = 4
	VAR = 5


# noinspection SpellCheckingInspection
class EutraPbchSfnRestPeriod(Enum):
	"""2 Members, PER3gpp ... PERSlength"""
	PER3gpp = 0
	PERSlength = 1


# noinspection SpellCheckingInspection
class EutraNumUpPts(Enum):
	"""3 Members, _0 ... _4"""
	_0 = 0
	_2 = 1
	_4 = 2


# noinspection SpellCheckingInspection
class EutraNumPrbs(Enum):
	"""3 Members, PRB2 ... PRB8"""
	PRB2 = 0
	PRB4 = 1
	PRB8 = 2


# noinspection SpellCheckingInspection
class EutraNprs(Enum):
	"""4 Members, _1 ... _6"""
	_1 = 0
	_2 = 1
	_4 = 2
	_6 = 3


# noinspection SpellCheckingInspection
class EutraNbMimoConf(Enum):
	"""2 Members, TX1 ... TX2"""
	TX1 = 0
	TX2 = 1


# noinspection SpellCheckingInspection
class EutraNbiotWusTimeOffsetFormat(Enum):
	"""4 Members, TO_40 ... TO240"""
	TO_40 = 0
	TO_80 = 1
	TO160 = 2
	TO240 = 3


# noinspection SpellCheckingInspection
class EutraNbiotWusDurationFormat(Enum):
	"""11 Members, DN_1 ... DN_8"""
	DN_1 = 0
	DN_1024 = 1
	DN_128 = 2
	DN_16 = 3
	DN_2 = 4
	DN_256 = 5
	DN_32 = 6
	DN_4 = 7
	DN_512 = 8
	DN_64 = 9
	DN_8 = 10


# noinspection SpellCheckingInspection
class EutraNbiotSimAnt(Enum):
	"""4 Members, ALL ... NONE"""
	ALL = 0
	ANT1 = 1
	ANT2 = 2
	NONE = 3


# noinspection SpellCheckingInspection
class EutraNbiotSearchSpaceStSubframe(Enum):
	"""8 Members, S1_5 ... S8"""
	S1_5 = 0
	S16 = 1
	S2 = 2
	S32 = 3
	S4 = 4
	S48 = 5
	S64 = 6
	S8 = 7


# noinspection SpellCheckingInspection
class EutraNbiotSearchSpaceOffset(Enum):
	"""4 Members, O0 ... O3_8"""
	O0 = 0
	O1_4 = 1
	O1_8 = 2
	O3_8 = 3


# noinspection SpellCheckingInspection
class EutraNbiotRmAx(Enum):
	"""12 Members, R1 ... R8"""
	R1 = 0
	R1024 = 1
	R128 = 2
	R16 = 3
	R2 = 4
	R2048 = 5
	R256 = 6
	R32 = 7
	R4 = 8
	R512 = 9
	R64 = 10
	R8 = 11


# noinspection SpellCheckingInspection
class EutraNbiotNpuschFormat(Enum):
	"""2 Members, F1 ... F2"""
	F1 = 0
	F2 = 1


# noinspection SpellCheckingInspection
class EutraNbiotNprsConfigType(Enum):
	"""3 Members, PA_A ... PA_B"""
	PA_A = 0
	PA_AB = 1
	PA_B = 2


# noinspection SpellCheckingInspection
class EutraNbiotNprsConfigbStartsf(Enum):
	"""8 Members, STSF0_8 ... STSF7_8"""
	STSF0_8 = 0
	STSF1_8 = 1
	STSF2_8 = 2
	STSF3_8 = 3
	STSF4_8 = 4
	STSF5_8 = 5
	STSF6_8 = 6
	STSF7_8 = 7


# noinspection SpellCheckingInspection
class EutraNbiotNprsConfigbSfnumb(Enum):
	"""8 Members, SFNM_10 ... SFNM_80"""
	SFNM_10 = 0
	SFNM_1280 = 1
	SFNM_160 = 2
	SFNM_20 = 3
	SFNM_320 = 4
	SFNM_40 = 5
	SFNM_640 = 6
	SFNM_80 = 7


# noinspection SpellCheckingInspection
class EutraNbiotNprsConfigbPeriod(Enum):
	"""4 Members, PD_1280 ... PD_640"""
	PD_1280 = 0
	PD_160 = 1
	PD_320 = 2
	PD_640 = 3


# noinspection SpellCheckingInspection
class EutraNbiotInbandBitmapSfAll(Enum):
	"""2 Members, N10 ... N40"""
	N10 = 0
	N40 = 1


# noinspection SpellCheckingInspection
class EutraNbiotGapThreshold(Enum):
	"""4 Members, _128 ... _64"""
	_128 = 0
	_256 = 1
	_32 = 2
	_64 = 3


# noinspection SpellCheckingInspection
class EutraNbiotGapPeriodicity(Enum):
	"""4 Members, _128 ... _64"""
	_128 = 0
	_256 = 1
	_512 = 2
	_64 = 3


# noinspection SpellCheckingInspection
class EutraNbiotGapDurationCoefficent(Enum):
	"""4 Members, _1_2 ... _3_8"""
	_1_2 = 0
	_1_4 = 1
	_1_8 = 2
	_3_8 = 3


# noinspection SpellCheckingInspection
class EutraNbiotEdtTranBlckSize(Enum):
	"""13 Members, _1000 ... _936"""
	_1000 = 0
	_328 = 1
	_408 = 2
	_456 = 3
	_504 = 4
	_536 = 5
	_584 = 6
	_680 = 7
	_712 = 8
	_776 = 9
	_808 = 10
	_88 = 11
	_936 = 12


# noinspection SpellCheckingInspection
class EutraNbiotEdtTbs(Enum):
	"""9 Members, _1000 ... _936"""
	_1000 = 0
	_328 = 1
	_408 = 2
	_504 = 3
	_584 = 4
	_680 = 5
	_808 = 6
	_88 = 7
	_936 = 8


# noinspection SpellCheckingInspection
class EutraNbIoTdCiFormat(Enum):
	"""3 Members, N0 ... N2"""
	N0 = 0
	N1 = 1
	N2 = 2


# noinspection SpellCheckingInspection
class EutraNbIoTdCiDistNpdcchNpdsch(Enum):
	"""3 Members, MIN ... ZERO"""
	MIN = 0
	STD = 1
	ZERO = 2


# noinspection SpellCheckingInspection
class EutraMtchSfAllPer(Enum):
	"""7 Members, AP128 ... AP8"""
	AP128 = 0
	AP16 = 1
	AP256 = 2
	AP32 = 3
	AP4 = 4
	AP64 = 5
	AP8 = 6


# noinspection SpellCheckingInspection
class EutraMpdcchFormat(Enum):
	"""6 Members, _0 ... _5"""
	_0 = 0
	_1 = 1
	_2 = 2
	_3 = 3
	_4 = 4
	_5 = 5


# noinspection SpellCheckingInspection
class EutraModulationDlNbiot(Enum):
	"""1 Members, QPSK ... QPSK"""
	QPSK = 0


# noinspection SpellCheckingInspection
class EutraMobStatType(Enum):
	"""4 Members, UE1 ... UE4"""
	UE1 = 0
	UE2 = 1
	UE3 = 2
	UE4 = 3


# noinspection SpellCheckingInspection
class EutraMcsTable(Enum):
	"""8 Members, _0 ... T4"""
	_0 = 0
	_1 = 1
	OFF = 2
	ON = 3
	T1 = 4
	T2 = 5
	T3 = 6
	T4 = 7


# noinspection SpellCheckingInspection
class EutraMchSchedPer(Enum):
	"""9 Members, SPM ... SPRF8"""
	SPM = 0
	SPRF1024 = 1
	SPRF128 = 2
	SPRF16 = 3
	SPRF256 = 4
	SPRF32 = 5
	SPRF512 = 6
	SPRF64 = 7
	SPRF8 = 8


# noinspection SpellCheckingInspection
class EutraMcchRepPer(Enum):
	"""4 Members, RP128 ... RP64"""
	RP128 = 0
	RP256 = 1
	RP32 = 2
	RP64 = 3


# noinspection SpellCheckingInspection
class EutraMcchModPer(Enum):
	"""2 Members, MP1024 ... MP512"""
	MP1024 = 0
	MP512 = 1


# noinspection SpellCheckingInspection
class EutraMcchMcs(Enum):
	"""4 Members, MCS13 ... MCS7"""
	MCS13 = 0
	MCS19 = 1
	MCS2 = 2
	MCS7 = 3


# noinspection SpellCheckingInspection
class EutraMbsfnUeCat(Enum):
	"""5 Members, C1 ... C5"""
	C1 = 0
	C2 = 1
	C3 = 2
	C4 = 3
	C5 = 4


# noinspection SpellCheckingInspection
class EutraMbsfnType(Enum):
	"""2 Members, MIXed ... OFF"""
	MIXed = 0
	OFF = 1


# noinspection SpellCheckingInspection
class EutraMbsfnSfAllMode(Enum):
	"""2 Members, F1 ... F4"""
	F1 = 0
	F4 = 1


# noinspection SpellCheckingInspection
class EutraMbsfnRfAllPer(Enum):
	"""6 Members, AP1 ... AP8"""
	AP1 = 0
	AP16 = 1
	AP2 = 2
	AP32 = 3
	AP4 = 4
	AP8 = 5


# noinspection SpellCheckingInspection
class EutraMbsfnNotRepCoef(Enum):
	"""2 Members, NRC2 ... NRC4"""
	NRC2 = 0
	NRC4 = 1


# noinspection SpellCheckingInspection
class EutraMarkMode(Enum):
	"""8 Members, FAP ... TRIGger"""
	FAP = 0
	FRAM = 1
	PERiod = 2
	RATio = 3
	RESTart = 4
	SFNRestart = 5
	SUBFram = 6
	TRIGger = 7


# noinspection SpellCheckingInspection
class EutraLaaStartingSlots(Enum):
	"""2 Members, FIRSt ... SECond"""
	FIRSt = 0
	SECond = 1


# noinspection SpellCheckingInspection
class EutraLaalAstSf(Enum):
	"""7 Members, SY10 ... SY9"""
	SY10 = 0
	SY11 = 1
	SY12 = 2
	SY14 = 3
	SY3 = 4
	SY6 = 5
	SY9 = 6


# noinspection SpellCheckingInspection
class EutraLaadci1CMode(Enum):
	"""4 Members, MANual ... N1N"""
	MANual = 0
	N = 1
	N1 = 2
	N1N = 3


# noinspection SpellCheckingInspection
class EutraIotRu(Enum):
	"""8 Members, RU1 ... RU8"""
	RU1 = 0
	RU10 = 1
	RU2 = 2
	RU3 = 3
	RU4 = 4
	RU5 = 5
	RU6 = 6
	RU8 = 7


# noinspection SpellCheckingInspection
class EutraIotRepetitions(Enum):
	"""18 Members, R1 ... R8"""
	R1 = 0
	R1024 = 1
	R12 = 2
	R128 = 3
	R1536 = 4
	R16 = 5
	R192 = 6
	R2 = 7
	R2048 = 8
	R24 = 9
	R256 = 10
	R32 = 11
	R384 = 12
	R4 = 13
	R512 = 14
	R64 = 15
	R768 = 16
	R8 = 17


# noinspection SpellCheckingInspection
class EutraIotHoppingIvl(Enum):
	"""9 Members, H1 ... H8"""
	H1 = 0
	H10 = 1
	H16 = 2
	H2 = 3
	H20 = 4
	H4 = 5
	H40 = 6
	H5 = 7
	H8 = 8


# noinspection SpellCheckingInspection
class EutraGlobMimoConf(Enum):
	"""4 Members, SIBF ... TX4"""
	SIBF = 0
	TX1 = 1
	TX2 = 2
	TX4 = 3


# noinspection SpellCheckingInspection
class EutraFiltOptMode(Enum):
	"""2 Members, OFFLine ... RTime"""
	OFFLine = 0
	RTime = 1


# noinspection SpellCheckingInspection
class EutraFeedbackMode(Enum):
	"""4 Members, BAN ... SERial"""
	BAN = 0
	OFF = 1
	S3X8 = 2
	SERial = 3


# noinspection SpellCheckingInspection
class EutraFeedbackDistMode(Enum):
	"""2 Members, DIRect ... STD"""
	DIRect = 0
	STD = 1


# noinspection SpellCheckingInspection
class EutraFeedbackBlerMode(Enum):
	"""3 Members, APRocesses ... OFF"""
	APRocesses = 0
	FPRocess = 1
	OFF = 2


# noinspection SpellCheckingInspection
class EutraF1AContentType(Enum):
	"""2 Members, PDSCh ... PRACh"""
	PDSCh = 0
	PRACh = 1


# noinspection SpellCheckingInspection
class EutraEpdcchTransType(Enum):
	"""2 Members, DISTributed ... LOCalized"""
	DISTributed = 0
	LOCalized = 1


# noinspection SpellCheckingInspection
class EutraEmtcVrbOffs(Enum):
	"""8 Members, OS0 ... OS9"""
	OS0 = 0
	OS12 = 1
	OS15 = 2
	OS18 = 3
	OS21 = 4
	OS3 = 5
	OS6 = 6
	OS9 = 7


# noinspection SpellCheckingInspection
class EutraEmtcRbCnt(Enum):
	"""8 Members, CN12 ... CN9"""
	CN12 = 0
	CN15 = 1
	CN18 = 2
	CN21 = 3
	CN24 = 4
	CN3 = 5
	CN6 = 6
	CN9 = 7


# noinspection SpellCheckingInspection
class EutraEmtcPdschWideBand(Enum):
	"""3 Members, BW20_00 ... OFF"""
	BW20_00 = 0
	BW5_00 = 1
	OFF = 2


# noinspection SpellCheckingInspection
class EutraEmtcPdschNumRepetitions(Enum):
	"""12 Members, _1024 ... NON"""
	_1024 = 0
	_1536 = 1
	_16 = 2
	_192 = 3
	_2048 = 4
	_256 = 5
	_32 = 6
	_384 = 7
	_512 = 8
	_64 = 9
	_786 = 10
	NON = 11


# noinspection SpellCheckingInspection
class EutraEmtcPdcchCfg(Enum):
	"""6 Members, PRNTi ... USER4"""
	PRNTi = 0
	RARNti = 1
	USER1 = 2
	USER2 = 3
	USER3 = 4
	USER4 = 5


# noinspection SpellCheckingInspection
class EutraEmtcMpdcchStartSf(Enum):
	"""9 Members, S1 ... S8"""
	S1 = 0
	S1_5 = 1
	S10 = 2
	S2 = 3
	S2_5 = 4
	S20 = 5
	S4 = 6
	S5 = 7
	S8 = 8


# noinspection SpellCheckingInspection
class EutraEmtcMpdcchNumRepetitions(Enum):
	"""9 Members, _1 ... _8"""
	_1 = 0
	_128 = 1
	_16 = 2
	_2 = 3
	_256 = 4
	_32 = 5
	_4 = 6
	_64 = 7
	_8 = 8


# noinspection SpellCheckingInspection
class EuTraDuration(Enum):
	"""2 Members, EXTended ... NORMal"""
	EXTended = 0
	NORMal = 1


# noinspection SpellCheckingInspection
class EutraDuplexModeExtRange(Enum):
	"""3 Members, FDD ... TDD"""
	FDD = 0
	LAA = 1
	TDD = 2


# noinspection SpellCheckingInspection
class EutraDuplexMode(Enum):
	"""2 Members, FDD ... TDD"""
	FDD = 0
	TDD = 1


# noinspection SpellCheckingInspection
class EutraDsPeriod(Enum):
	"""3 Members, P160 ... P80"""
	P160 = 0
	P40 = 1
	P80 = 2


# noinspection SpellCheckingInspection
class EutraDrsDuration(Enum):
	"""5 Members, DUR1 ... DUR5"""
	DUR1 = 0
	DUR2 = 1
	DUR3 = 2
	DUR4 = 3
	DUR5 = 4


# noinspection SpellCheckingInspection
class EutraDlpRecMultAntScheme(Enum):
	"""4 Members, BF ... TXD"""
	BF = 0
	NONE = 1
	SPM = 2
	TXD = 3


# noinspection SpellCheckingInspection
class EutraDlpRecCycDelDiv(Enum):
	"""3 Members, LADelay ... SMDelay"""
	LADelay = 0
	NOCDd = 1
	SMDelay = 2


# noinspection SpellCheckingInspection
class EutraDlNbiotStartSymbols(Enum):
	"""4 Members, SYM0 ... SYM3"""
	SYM0 = 0
	SYM1 = 1
	SYM2 = 2
	SYM3 = 3


# noinspection SpellCheckingInspection
class EutraDlNbiotRbIndex(Enum):
	"""37 Members, _12 ... USER"""
	_12 = 0
	_14 = 1
	_17 = 2
	_19 = 3
	_2 = 4
	_22 = 5
	_24 = 6
	_27 = 7
	_29 = 8
	_30 = 9
	_32 = 10
	_34 = 11
	_35 = 12
	_39 = 13
	_4 = 14
	_40 = 15
	_42 = 16
	_44 = 17
	_45 = 18
	_47 = 19
	_52 = 20
	_55 = 21
	_57 = 22
	_60 = 23
	_62 = 24
	_65 = 25
	_67 = 26
	_7 = 27
	_70 = 28
	_72 = 29
	_75 = 30
	_80 = 31
	_85 = 32
	_9 = 33
	_90 = 34
	_95 = 35
	USER = 36


# noinspection SpellCheckingInspection
class EutraDlNbiotContentType(Enum):
	"""4 Members, NPBCh ... NSIB"""
	NPBCh = 0
	NPDCch = 1
	NPDSch = 2
	NSIB = 3


# noinspection SpellCheckingInspection
class EutraDleMtcContentType(Enum):
	"""5 Members, MPD1 ... PSIB"""
	MPD1 = 0
	MPD2 = 1
	PBCH = 2
	PDSCh = 3
	PSIB = 4


# noinspection SpellCheckingInspection
class EutraDlecpRecScheme(Enum):
	"""2 Members, NONE ... TXD"""
	NONE = 0
	TXD = 1


# noinspection SpellCheckingInspection
class EutraDlDataSourceUser(Enum):
	"""18 Members, DLISt ... ZERO"""
	DLISt = 0
	MCCH = 1
	MIB = 2
	MTCH = 3
	ONE = 4
	PATTern = 5
	PN11 = 6
	PN15 = 7
	PN16 = 8
	PN20 = 9
	PN21 = 10
	PN23 = 11
	PN9 = 12
	USER1 = 13
	USER2 = 14
	USER3 = 15
	USER4 = 16
	ZERO = 17


# noinspection SpellCheckingInspection
class EutraDlContentType(Enum):
	"""5 Members, EPD1 ... PDSCh"""
	EPD1 = 0
	EPD2 = 1
	PBCH = 2
	PDCCh = 3
	PDSCh = 4


# noinspection SpellCheckingInspection
class EutraDciFormatEmtc(Enum):
	"""7 Members, F3 ... F62"""
	F3 = 0
	F3A = 1
	F60A = 2
	F60B = 3
	F61A = 4
	F61B = 5
	F62 = 6


# noinspection SpellCheckingInspection
class EutraDciFormat(Enum):
	"""13 Members, F0 ... F3A"""
	F0 = 0
	F1 = 1
	F1A = 2
	F1B = 3
	F1C = 4
	F1D = 5
	F2 = 6
	F2A = 7
	F2B = 8
	F2C = 9
	F2D = 10
	F3 = 11
	F3A = 12


# noinspection SpellCheckingInspection
class EutraDataSourceDlNbiot(Enum):
	"""19 Members, DLISt ... ZERO"""
	DLISt = 0
	MIB = 1
	ONE = 2
	PATTern = 3
	PN11 = 4
	PN15 = 5
	PN16 = 6
	PN20 = 7
	PN21 = 8
	PN23 = 9
	PN9 = 10
	PRNTi = 11
	RARNti = 12
	SIB1nb = 13
	USER1 = 14
	USER2 = 15
	USER3 = 16
	USER4 = 17
	ZERO = 18


# noinspection SpellCheckingInspection
class EutraCyclicPrefixGs(Enum):
	"""3 Members, EXTended ... USER"""
	EXTended = 0
	NORMal = 1
	USER = 2


# noinspection SpellCheckingInspection
class EutraCw1CodeWord(Enum):
	"""2 Members, CW11 ... CW12"""
	CW11 = 0
	CW12 = 1


# noinspection SpellCheckingInspection
class EutraCsiRsTransComb(Enum):
	"""3 Members, _0 ... _2"""
	_0 = 0
	_1 = 1
	_2 = 2


# noinspection SpellCheckingInspection
class EutraCsiRsNumCfg(Enum):
	"""6 Members, _1 ... _7"""
	_1 = 0
	_2 = 1
	_3 = 2
	_4 = 3
	_5 = 4
	_7 = 5


# noinspection SpellCheckingInspection
class EutraCsiRsNumAp(Enum):
	"""4 Members, AP1 ... AP8"""
	AP1 = 0
	AP2 = 1
	AP4 = 2
	AP8 = 3


# noinspection SpellCheckingInspection
class EutraCsiRsFreqDensity(Enum):
	"""3 Members, D1 ... D13"""
	D1 = 0
	D12 = 1
	D13 = 2


# noinspection SpellCheckingInspection
class EutraCsiRsCdmType(Enum):
	"""3 Members, _2 ... _8"""
	_2 = 0
	_4 = 1
	_8 = 2


# noinspection SpellCheckingInspection
class EutraCodeWordIdx(Enum):
	"""2 Members, CW1 ... CW2"""
	CW1 = 0
	CW2 = 1


# noinspection SpellCheckingInspection
class EuTraClockMode(Enum):
	"""3 Members, CUSTom ... SAMPle"""
	CUSTom = 0
	MSAMp = 1
	SAMPle = 2


# noinspection SpellCheckingInspection
class EutraChannelBandwidth(Enum):
	"""10 Members, BW0_20 ... USER"""
	BW0_20 = 0
	BW1_25 = 1
	BW1_40 = 2
	BW10_00 = 3
	BW15_00 = 4
	BW2_50 = 5
	BW20_00 = 6
	BW3_00 = 7
	BW5_00 = 8
	USER = 9


# noinspection SpellCheckingInspection
class EutraChanCodMode(Enum):
	"""3 Members, COMBined ... ULSChonly"""
	COMBined = 0
	UCIonly = 1
	ULSChonly = 2


# noinspection SpellCheckingInspection
class EutraCeLevel(Enum):
	"""2 Members, CE01 ... CE23"""
	CE01 = 0
	CE23 = 1


# noinspection SpellCheckingInspection
class EutraCcIndexS(Enum):
	"""5 Members, NONE ... SC4"""
	NONE = 0
	SC1 = 1
	SC2 = 2
	SC3 = 3
	SC4 = 4


# noinspection SpellCheckingInspection
class EutraCcIndex(Enum):
	"""5 Members, PC ... SC4"""
	PC = 0
	SC1 = 1
	SC2 = 2
	SC3 = 3
	SC4 = 4


# noinspection SpellCheckingInspection
class EutraCaChannelBandwidth(Enum):
	"""6 Members, BW1_40 ... BW5_00"""
	BW1_40 = 0
	BW10_00 = 1
	BW15_00 = 2
	BW20_00 = 3
	BW3_00 = 4
	BW5_00 = 5


# noinspection SpellCheckingInspection
class EutraBlockOutput(Enum):
	"""8 Members, OUT0 ... OUT7"""
	OUT0 = 0
	OUT1 = 1
	OUT2 = 2
	OUT3 = 3
	OUT4 = 4
	OUT5 = 5
	OUT6 = 6
	OUT7 = 7


# noinspection SpellCheckingInspection
class EutraBitmap(Enum):
	"""2 Members, _10 ... _40"""
	_10 = 0
	_40 = 1


# noinspection SpellCheckingInspection
class EutraBfTransScheme(Enum):
	"""4 Members, TM10 ... TM9"""
	TM10 = 0
	TM7 = 1
	TM8 = 2
	TM9 = 3


# noinspection SpellCheckingInspection
class EutraBfapMapMode(Enum):
	"""3 Members, CB ... RCB"""
	CB = 0
	FW = 1
	RCB = 2


# noinspection SpellCheckingInspection
class EutraBfaNtSetEmtc(Enum):
	"""16 Members, AP107 ... AP8"""
	AP107 = 0
	AP107108 = 1
	AP107109 = 2
	AP108 = 3
	AP109 = 4
	AP110 = 5
	AP5 = 6
	AP7 = 7
	AP710 = 8
	AP711 = 9
	AP712 = 10
	AP713 = 11
	AP714 = 12
	AP78 = 13
	AP79 = 14
	AP8 = 15


# noinspection SpellCheckingInspection
class EutraBfaNtSet(Enum):
	"""19 Members, AP107 ... AP8"""
	AP107 = 0
	AP107108 = 1
	AP107109 = 2
	AP108 = 3
	AP109 = 4
	AP11 = 5
	AP110 = 6
	AP1113 = 7
	AP13 = 8
	AP5 = 9
	AP7 = 10
	AP710 = 11
	AP711 = 12
	AP712 = 13
	AP713 = 14
	AP714 = 15
	AP78 = 16
	AP79 = 17
	AP8 = 18


# noinspection SpellCheckingInspection
class EutraBehUnsSubframes(Enum):
	"""2 Members, DTX ... DUData"""
	DTX = 0
	DUData = 1


# noinspection SpellCheckingInspection
class EutraAsEqMcsMode(Enum):
	"""3 Members, FIXed ... TCR"""
	FIXed = 0
	MANual = 1
	TCR = 2


# noinspection SpellCheckingInspection
class EutraAckNackMode(Enum):
	"""2 Members, BUNDling ... MUX"""
	BUNDling = 0
	MUX = 1


# noinspection SpellCheckingInspection
class ErFpowSensMapping(Enum):
	"""9 Members, SENS1 ... UNMapped"""
	SENS1 = 0
	SENS2 = 1
	SENS3 = 2
	SENS4 = 3
	SENSor1 = 4
	SENSor2 = 5
	SENSor3 = 6
	SENSor4 = 7
	UNMapped = 8


# noinspection SpellCheckingInspection
class EphSatType(Enum):
	"""2 Members, GLO ... GLOM"""
	GLO = 0
	GLOM = 1


# noinspection SpellCheckingInspection
class EphAge(Enum):
	"""3 Members, A30M ... A60M"""
	A30M = 0
	A45M = 1
	A60M = 2


# noinspection SpellCheckingInspection
class EnhTchErr(Enum):
	"""4 Members, CON2 ... TURBo3"""
	CON2 = 0
	CON3 = 1
	NONE = 2
	TURBo3 = 3


# noinspection SpellCheckingInspection
class EnhHsHarqMode(Enum):
	"""2 Members, CACK ... CNACk"""
	CACK = 0
	CNACk = 1


# noinspection SpellCheckingInspection
class EnhBitErr(Enum):
	"""2 Members, PHYSical ... TRANsport"""
	PHYSical = 0
	TRANsport = 1


# noinspection SpellCheckingInspection
class ElevMaskType(Enum):
	"""2 Members, ETANgent ... LHORizon"""
	ETANgent = 0
	LHORizon = 1


# noinspection SpellCheckingInspection
class EidNr5GscsGeneral(Enum):
	"""5 Members, SCS120 ... SCS60"""
	SCS120 = 0
	SCS15 = 1
	SCS240 = 2
	SCS30 = 3
	SCS60 = 4


# noinspection SpellCheckingInspection
class EidNr5GresAllocUserAlloc(Enum):
	"""2 Members, T0 ... T1"""
	T0 = 0
	T1 = 1


# noinspection SpellCheckingInspection
class DpdShapeMode(Enum):
	"""3 Members, NORMalized ... TABLe"""
	NORMalized = 0
	POLYnomial = 1
	TABLe = 2


# noinspection SpellCheckingInspection
class DpdPowRef(Enum):
	"""3 Members, ADPD ... SDPD"""
	ADPD = 0
	BDPD = 1
	SDPD = 2


# noinspection SpellCheckingInspection
class DopplerConfig(Enum):
	"""3 Members, USER ... VEL2"""
	USER = 0
	VEL1 = 1
	VEL2 = 2


# noinspection SpellCheckingInspection
class Doppler(Enum):
	"""2 Members, CONStant ... HIGH"""
	CONStant = 0
	HIGH = 1


# noinspection SpellCheckingInspection
class DmTrigMode(Enum):
	"""5 Members, AAUTo ... SINGle"""
	AAUTo = 0
	ARETrigger = 1
	AUTO = 2
	RETRigger = 3
	SINGle = 4


# noinspection SpellCheckingInspection
class DmStan(Enum):
	"""25 Members, APCOPH1C4fm ... WORLdspace"""
	APCOPH1C4fm = 0
	APCOPH1CQpsk = 1
	APCOPH1Lsm = 2
	APCOPH1Wcqpsk = 3
	APCOPH2HCpm = 4
	APCOPH2HD8PSKN = 5
	APCOPH2HD8PSKW = 6
	APCOPH2HDQpsk = 7
	BLUetooth = 8
	CFORward = 9
	CREVerse = 10
	CWBPsk = 11
	DECT = 12
	ETC = 13
	GSM = 14
	GSMEdge = 15
	NADC = 16
	PDC = 17
	PHS = 18
	TDSCdma = 19
	TETRa = 20
	TFTS = 21
	USER = 22
	W3GPp = 23
	WORLdspace = 24


# noinspection SpellCheckingInspection
class DmMarkMode(Enum):
	"""5 Members, CLISt ... TRIGger"""
	CLISt = 0
	PATTern = 1
	PULSe = 2
	RATio = 3
	TRIGger = 4


# noinspection SpellCheckingInspection
class DmFskModType(Enum):
	"""3 Members, FSK16 ... FSK8"""
	FSK16 = 0
	FSK4 = 1
	FSK8 = 2


# noinspection SpellCheckingInspection
class DmFilterEutra(Enum):
	"""20 Members, APCO25 ... USER"""
	APCO25 = 0
	C2K3x = 1
	COEQualizer = 2
	COF705 = 3
	COFequalizer = 4
	CONE = 5
	COSine = 6
	DIRac = 7
	ENPShape = 8
	EWPShape = 9
	GAUSs = 10
	LGAuss = 11
	LPASs = 12
	LPASSEVM = 13
	LTEFilter = 14
	PGAuss = 15
	RCOSine = 16
	RECTangle = 17
	SPHase = 18
	USER = 19


# noinspection SpellCheckingInspection
class DmFilterBto(Enum):
	"""17 Members, APCO25 ... SPHase"""
	APCO25 = 0
	C2K3x = 1
	COEQualizer = 2
	COF705 = 3
	COFequalizer = 4
	CONE = 5
	COSine = 6
	DIRac = 7
	ENPShape = 8
	EWPShape = 9
	GAUSs = 10
	LGAuss = 11
	LPASs = 12
	PGAuss = 13
	RCOSine = 14
	RECTangle = 15
	SPHase = 16


# noinspection SpellCheckingInspection
class DmFilterB(Enum):
	"""22 Members, APCO25 ... USER"""
	APCO25 = 0
	APCO25Hcpm = 1
	APCO25Lsm = 2
	C2K3x = 3
	COEQualizer = 4
	COF705 = 5
	COFequalizer = 6
	CONE = 7
	COSine = 8
	DIRac = 9
	ENPShape = 10
	EWPShape = 11
	GAUSs = 12
	LGAuss = 13
	LPASs = 14
	LPASSEVM = 15
	LTEFilter = 16
	PGAuss = 17
	RCOSine = 18
	RECTangle = 19
	SPHase = 20
	USER = 21


# noinspection SpellCheckingInspection
class DmFilterA(Enum):
	"""18 Members, APCO25 ... SPHase"""
	APCO25 = 0
	C2K3x = 1
	COEQualizer = 2
	COF705 = 3
	COFequalizer = 4
	CONE = 5
	COSine = 6
	DIRac = 7
	ENPShape = 8
	EWPShape = 9
	GAUSs = 10
	LGAuss = 11
	LPASs = 12
	LPASSEVM = 13
	PGAuss = 14
	RCOSine = 15
	RECTangle = 16
	SPHase = 17


# noinspection SpellCheckingInspection
class DmExtRcvStateType(Enum):
	"""5 Members, INValid ... UFLow"""
	INValid = 0
	OFF = 1
	OFLow = 2
	OPERational = 3
	UFLow = 4


# noinspection SpellCheckingInspection
class DmDataSourV(Enum):
	"""5 Members, DLISt ... ZERO"""
	DLISt = 0
	ONE = 1
	PATTern = 2
	PRBS = 3
	ZERO = 4


# noinspection SpellCheckingInspection
class DmDataPrbs(Enum):
	"""14 Members, _11 ... PN9"""
	_11 = 0
	_15 = 1
	_16 = 2
	_20 = 3
	_21 = 4
	_23 = 5
	_9 = 6
	PN11 = 7
	PN15 = 8
	PN16 = 9
	PN20 = 10
	PN21 = 11
	PN23 = 12
	PN9 = 13


# noinspection SpellCheckingInspection
class DmCod(Enum):
	"""21 Members, APCO25 ... WCDMA"""
	APCO25 = 0
	APCO258PSK = 1
	APCO25FSK = 2
	CDMA2000 = 3
	DGRay = 4
	DIFF = 5
	DPHS = 6
	EDGE = 7
	GRAY = 8
	GSM = 9
	ICO = 10
	INMarsat = 11
	NADC = 12
	OFF = 13
	PDC = 14
	PHS = 15
	PWT = 16
	TETRa = 17
	TFTS = 18
	VDL = 19
	WCDMA = 20


# noinspection SpellCheckingInspection
class DmClocMode(Enum):
	"""3 Members, BIT ... SYMBol"""
	BIT = 0
	MSYMbol = 1
	SYMBol = 2


# noinspection SpellCheckingInspection
class DmApskGamma1(Enum):
	"""5 Members, G3D4 ... G9D10"""
	G3D4 = 0
	G4D5 = 1
	G5D6 = 2
	G8D9 = 3
	G9D10 = 4


# noinspection SpellCheckingInspection
class DmApskGamma(Enum):
	"""6 Members, G2D3 ... G9D10"""
	G2D3 = 0
	G3D4 = 1
	G4D5 = 2
	G5D6 = 3
	G8D9 = 4
	G9D10 = 5


# noinspection SpellCheckingInspection
class DlpRbBundlingGranularity(Enum):
	"""3 Members, N2 ... WIDeband"""
	N2 = 0
	N4 = 1
	WIDeband = 2


# noinspection SpellCheckingInspection
class DispKeybLockMode(Enum):
	"""5 Members, DISabled ... VNConly"""
	DISabled = 0
	DONLy = 1
	ENABled = 2
	TOFF = 3
	VNConly = 4


# noinspection SpellCheckingInspection
class DexchSepDec(Enum):
	"""2 Members, COMMa ... DOT"""
	COMMa = 0
	DOT = 1


# noinspection SpellCheckingInspection
class DexchSepCol(Enum):
	"""4 Members, COMMa ... TABulator"""
	COMMa = 0
	SEMicolon = 1
	SPACe = 2
	TABulator = 3


# noinspection SpellCheckingInspection
class DexchMode(Enum):
	"""2 Members, EXPort ... IMPort"""
	EXPort = 0
	IMPort = 1


# noinspection SpellCheckingInspection
class DexchExtension(Enum):
	"""2 Members, CSV ... TXT"""
	CSV = 0
	TXT = 1


# noinspection SpellCheckingInspection
class DevExpFormat(Enum):
	"""4 Members, CGPRedefined ... XML"""
	CGPRedefined = 0
	CGUSer = 1
	SCPI = 2
	XML = 3


# noinspection SpellCheckingInspection
class DeclaredDir(Enum):
	"""3 Members, MREFD ... OTHD"""
	MREFD = 0
	OREFD = 1
	OTHD = 2


# noinspection SpellCheckingInspection
class DataSourGnss(Enum):
	"""13 Members, DLISt ... ZNData"""
	DLISt = 0
	ONE = 1
	PATTern = 2
	PN11 = 3
	PN15 = 4
	PN16 = 5
	PN20 = 6
	PN21 = 7
	PN23 = 8
	PN9 = 9
	RNData = 10
	ZERO = 11
	ZNData = 12


# noinspection SpellCheckingInspection
class DataSour(Enum):
	"""11 Members, DLISt ... ZERO"""
	DLISt = 0
	ONE = 1
	PATTern = 2
	PN11 = 3
	PN15 = 4
	PN16 = 5
	PN20 = 6
	PN21 = 7
	PN23 = 8
	PN9 = 9
	ZERO = 10


# noinspection SpellCheckingInspection
class DabTxMode(Enum):
	"""4 Members, I ... IV"""
	I = 0
	II = 1
	III = 2
	IV = 3


# noinspection SpellCheckingInspection
class DabDataSour(Enum):
	"""5 Members, ALL0 ... PN23"""
	ALL0 = 0
	ALL1 = 1
	ETI = 2
	PN15 = 3
	PN23 = 4


# noinspection SpellCheckingInspection
class CsipArt(Enum):
	"""2 Members, CSIP_1 ... CSIP_2"""
	CSIP_1 = 0
	CSIP_2 = 1


# noinspection SpellCheckingInspection
class CrestFactoralgorithm(Enum):
	"""1 Members, CLF ... CLF"""
	CLF = 0


# noinspection SpellCheckingInspection
class CresFactMode(Enum):
	"""3 Members, AVERage ... WORSt"""
	AVERage = 0
	MINimum = 1
	WORSt = 2


# noinspection SpellCheckingInspection
class Count(Enum):
	"""2 Members, _1 ... _2"""
	_1 = 0
	_2 = 1


# noinspection SpellCheckingInspection
class CoresetUnusedRes(Enum):
	"""3 Members, _0 ... ALLowpdsch"""
	_0 = 0
	_1 = 1
	ALLowpdsch = 2


# noinspection SpellCheckingInspection
class CoordMapMode(Enum):
	"""2 Members, CARTesian ... CYLindrical"""
	CARTesian = 0
	CYLindrical = 1


# noinspection SpellCheckingInspection
class ConnDirection(Enum):
	"""3 Members, INPut ... UNUSed"""
	INPut = 0
	OUTPut = 1
	UNUSed = 2


# noinspection SpellCheckingInspection
class Config(Enum):
	"""9 Members, E1RL ... OUTF"""
	E1RL = 0
	E1RR = 1
	EFL = 2
	EFR = 3
	I1RL = 4
	I1RR = 5
	INNF = 6
	MAN = 7
	OUTF = 8


# noinspection SpellCheckingInspection
class Colour(Enum):
	"""4 Members, GREen ... YELLow"""
	GREen = 0
	NONE = 1
	RED = 2
	YELLow = 3


# noinspection SpellCheckingInspection
class CodeType(Enum):
	"""1 Members, BCHSfn ... BCHSfn"""
	BCHSfn = 0


# noinspection SpellCheckingInspection
class CodeOnL2(Enum):
	"""3 Members, CACode ... REServed"""
	CACode = 0
	PCODe = 1
	REServed = 2


# noinspection SpellCheckingInspection
class CodebookSubsetAll(Enum):
	"""3 Members, FPNC ... PNC"""
	FPNC = 0
	NC = 1
	PNC = 2


# noinspection SpellCheckingInspection
class CmMethUp(Enum):
	"""2 Members, HLSCheduling ... SF2"""
	HLSCheduling = 0
	SF2 = 1


# noinspection SpellCheckingInspection
class CmMethDn(Enum):
	"""3 Members, HLSCheduling ... SF2"""
	HLSCheduling = 0
	PUNCturing = 1
	SF2 = 2


# noinspection SpellCheckingInspection
class ClocSyncMode(Enum):
	"""3 Members, MASTer ... SLAVe"""
	MASTer = 0
	NONE = 1
	SLAVe = 2


# noinspection SpellCheckingInspection
class ClocOutpMode(Enum):
	"""2 Members, BIT ... SYMBol"""
	BIT = 0
	SYMBol = 1


# noinspection SpellCheckingInspection
class ClocModeB(Enum):
	"""2 Members, MSAMple ... SAMPle"""
	MSAMple = 0
	SAMPle = 1


# noinspection SpellCheckingInspection
class ClocMode(Enum):
	"""4 Members, BIT ... SYMBol"""
	BIT = 0
	FSYMbol = 1
	MSYMbol = 2
	SYMBol = 3


# noinspection SpellCheckingInspection
class ClockSourceC(Enum):
	"""3 Members, ELCLock ... INTernal"""
	ELCLock = 0
	EXTernal = 1
	INTernal = 2


# noinspection SpellCheckingInspection
class ClockSourceB(Enum):
	"""3 Members, AINTernal ... INTernal"""
	AINTernal = 0
	EXTernal = 1
	INTernal = 2


# noinspection SpellCheckingInspection
class ClockSourceA(Enum):
	"""1 Members, INTernal ... INTernal"""
	INTernal = 0


# noinspection SpellCheckingInspection
class ClockModeA(Enum):
	"""2 Members, CHIP ... MCHip"""
	CHIP = 0
	MCHip = 1


# noinspection SpellCheckingInspection
class ClipMode(Enum):
	"""2 Members, SCALar ... VECTor"""
	SCALar = 0
	VECTor = 1


# noinspection SpellCheckingInspection
class CifAll(Enum):
	"""8 Members, _0 ... _7"""
	_0 = 0
	_1 = 1
	_2 = 2
	_3 = 3
	_4 = 4
	_5 = 5
	_6 = 6
	_7 = 7


# noinspection SpellCheckingInspection
class ChipRate(Enum):
	"""1 Members, R3M8 ... R3M8"""
	R3M8 = 0


# noinspection SpellCheckingInspection
class ChanTypeDn(Enum):
	"""22 Members, AICH ... SSCH"""
	AICH = 0
	APAich = 1
	DPCCh = 2
	DPCH = 3
	EAGCh = 4
	EHICh = 5
	ERGCh = 6
	FDPCh = 7
	HS16Qam = 8
	HS64Qam = 9
	HSMimo = 10
	HSQam = 11
	HSQPsk = 12
	HSSCch = 13
	PCCPch = 14
	PCPich = 15
	PDSCh = 16
	PICH = 17
	PSCH = 18
	SCCPch = 19
	SCPich = 20
	SSCH = 21


# noinspection SpellCheckingInspection
class ChanCodTypeEnhPrac(Enum):
	"""4 Members, TB168 ... TU360"""
	TB168 = 0
	TB360 = 1
	TU168 = 2
	TU360 = 3


# noinspection SpellCheckingInspection
class ChanCodTypeEnhPcpc(Enum):
	"""2 Members, TB168 ... TB360"""
	TB168 = 0
	TB360 = 1


# noinspection SpellCheckingInspection
class ChanCodType(Enum):
	"""8 Members, AMR ... M64K"""
	AMR = 0
	BTFD1 = 1
	BTFD2 = 2
	BTFD3 = 3
	M12K2 = 4
	M144k = 5
	M384k = 6
	M64K = 7


# noinspection SpellCheckingInspection
class CfrFiltMode(Enum):
	"""2 Members, ENHanced ... SIMPle"""
	ENHanced = 0
	SIMPle = 1


# noinspection SpellCheckingInspection
class CfrAlgo(Enum):
	"""1 Members, CLFiltering ... CLFiltering"""
	CLFiltering = 0


# noinspection SpellCheckingInspection
class CellBarring(Enum):
	"""2 Members, BARR ... NBAR"""
	BARR = 0
	NBAR = 1


# noinspection SpellCheckingInspection
class CellAll(Enum):
	"""16 Members, _0 ... _9"""
	_0 = 0
	_1 = 1
	_10 = 2
	_11 = 3
	_12 = 4
	_13 = 5
	_14 = 6
	_15 = 7
	_2 = 8
	_3 = 9
	_4 = 10
	_5 = 11
	_6 = 12
	_7 = 13
	_8 = 14
	_9 = 15


# noinspection SpellCheckingInspection
class Cdma2KtxDivMode(Enum):
	"""2 Members, OTD ... STS"""
	OTD = 0
	STS = 1


# noinspection SpellCheckingInspection
class Cdma2KtxDiv(Enum):
	"""3 Members, ANT1 ... OFF"""
	ANT1 = 0
	ANT2 = 1
	OFF = 2


# noinspection SpellCheckingInspection
class Cdma2KradioConf(Enum):
	"""5 Members, _1 ... _5"""
	_1 = 0
	_2 = 1
	_3 = 2
	_4 = 3
	_5 = 4


# noinspection SpellCheckingInspection
class Cdma2KpredFramLen(Enum):
	"""3 Members, _20 ... _80"""
	_20 = 0
	_40 = 1
	_80 = 2


# noinspection SpellCheckingInspection
class Cdma2KmsMode(Enum):
	"""4 Members, ACCess ... TRAFfic"""
	ACCess = 0
	CCONtrol = 1
	EACCess = 2
	TRAFfic = 3


# noinspection SpellCheckingInspection
class Cdma2KmpPdchFiveColDn(Enum):
	"""127 Members, _1 ... _99"""
	_1 = 0
	_10 = 1
	_100 = 2
	_101 = 3
	_102 = 4
	_103 = 5
	_104 = 6
	_105 = 7
	_106 = 8
	_107 = 9
	_108 = 10
	_109 = 11
	_11 = 12
	_110 = 13
	_111 = 14
	_112 = 15
	_113 = 16
	_114 = 17
	_115 = 18
	_116 = 19
	_117 = 20
	_118 = 21
	_119 = 22
	_12 = 23
	_120 = 24
	_121 = 25
	_122 = 26
	_123 = 27
	_124 = 28
	_125 = 29
	_126 = 30
	_127 = 31
	_13 = 32
	_14 = 33
	_15 = 34
	_16 = 35
	_17 = 36
	_18 = 37
	_19 = 38
	_2 = 39
	_20 = 40
	_21 = 41
	_22 = 42
	_23 = 43
	_24 = 44
	_25 = 45
	_26 = 46
	_27 = 47
	_28 = 48
	_29 = 49
	_3 = 50
	_30 = 51
	_31 = 52
	_32 = 53
	_33 = 54
	_34 = 55
	_35 = 56
	_36 = 57
	_37 = 58
	_38 = 59
	_39 = 60
	_4 = 61
	_40 = 62
	_41 = 63
	_42 = 64
	_43 = 65
	_44 = 66
	_45 = 67
	_46 = 68
	_47 = 69
	_48 = 70
	_49 = 71
	_5 = 72
	_50 = 73
	_51 = 74
	_52 = 75
	_53 = 76
	_54 = 77
	_55 = 78
	_56 = 79
	_57 = 80
	_58 = 81
	_59 = 82
	_6 = 83
	_60 = 84
	_61 = 85
	_62 = 86
	_63 = 87
	_64 = 88
	_65 = 89
	_66 = 90
	_67 = 91
	_68 = 92
	_69 = 93
	_7 = 94
	_70 = 95
	_71 = 96
	_72 = 97
	_73 = 98
	_74 = 99
	_75 = 100
	_76 = 101
	_77 = 102
	_78 = 103
	_79 = 104
	_8 = 105
	_80 = 106
	_81 = 107
	_82 = 108
	_83 = 109
	_84 = 110
	_85 = 111
	_86 = 112
	_87 = 113
	_88 = 114
	_89 = 115
	_9 = 116
	_90 = 117
	_91 = 118
	_92 = 119
	_93 = 120
	_94 = 121
	_95 = 122
	_96 = 123
	_97 = 124
	_98 = 125
	_99 = 126


# noinspection SpellCheckingInspection
class Cdma2KmarkMode(Enum):
	"""9 Members, CSPeriod ... USER"""
	CSPeriod = 0
	ESECond = 1
	PCGRoup = 2
	RATio = 3
	RFRame = 4
	SCFRame = 5
	SFRame = 6
	TRIGger = 7
	USER = 8


# noinspection SpellCheckingInspection
class Cdma2KframLenUp(Enum):
	"""6 Members, _10 ... _80"""
	_10 = 0
	_20 = 1
	_26_dot_6 = 2
	_40 = 3
	_5 = 4
	_80 = 5


# noinspection SpellCheckingInspection
class Cdma2KframLen(Enum):
	"""8 Members, _10 ... NUSed"""
	_10 = 0
	_160 = 1
	_20 = 2
	_26_dot_6 = 3
	_40 = 4
	_5 = 5
	_80 = 6
	NUSed = 7


# noinspection SpellCheckingInspection
class Cdma2KdomConfModeDn(Enum):
	"""2 Members, BREV ... HAD"""
	BREV = 0
	HAD = 1


# noinspection SpellCheckingInspection
class Cdma2KdataRate(Enum):
	"""26 Members, DR1036K8 ... NUSed"""
	DR1036K8 = 0
	DR115K2 = 1
	DR14K4 = 2
	DR153K6 = 3
	DR19K2 = 4
	DR1K2 = 5
	DR1K3 = 6
	DR1K5 = 7
	DR1K8 = 8
	DR230K4 = 9
	DR259K2 = 10
	DR28K8 = 11
	DR2K4 = 12
	DR2K7 = 13
	DR307K2 = 14
	DR38K4 = 15
	DR3K6 = 16
	DR460K8 = 17
	DR4K8 = 18
	DR518K4 = 19
	DR57K6 = 20
	DR614K4 = 21
	DR76K8 = 22
	DR7K2 = 23
	DR9K6 = 24
	NUSed = 25


# noinspection SpellCheckingInspection
class Cdma2KcodMode(Enum):
	"""4 Members, COMPlete ... OINTerleaving"""
	COMPlete = 0
	NOINterleaving = 1
	OFF = 2
	OINTerleaving = 3


# noinspection SpellCheckingInspection
class Cdma2KchipRate(Enum):
	"""1 Members, R1M2 ... R1M2"""
	R1M2 = 0


# noinspection SpellCheckingInspection
class Cdma2KchanTypeUp(Enum):
	"""9 Members, R_dash_ACH ... R_dash_SCH2"""
	R_dash_ACH = 0
	R_dash_CCCH = 1
	R_dash_DCCH = 2
	R_dash_EACH = 3
	R_dash_FCH = 4
	R_dash_PICH = 5
	R_dash_SCCH = 6
	R_dash_SCH1 = 7
	R_dash_SCH2 = 8


# noinspection SpellCheckingInspection
class Cdma2KchanTypeDn(Enum):
	"""16 Members, F_dash_APICH ... F_dash_TDPICH"""
	F_dash_APICH = 0
	F_dash_ATDPICH = 1
	F_dash_BCH = 2
	F_dash_CACH = 3
	F_dash_CCCH = 4
	F_dash_CPCCH = 5
	F_dash_DCCH = 6
	F_dash_FCH = 7
	F_dash_PCH = 8
	F_dash_PDCCH = 9
	F_dash_PDCH = 10
	F_dash_PICH = 11
	F_dash_QPCH = 12
	F_dash_SCH = 13
	F_dash_SYNC = 14
	F_dash_TDPICH = 15


# noinspection SpellCheckingInspection
class Cdma2KchanCodSymbPunc(Enum):
	"""9 Members, _1OF5 ... T4OF12"""
	_1OF5 = 0
	_1OF9 = 1
	_2OF18 = 2
	_2OF6 = 3
	_4OF12 = 4
	_8OF24 = 5
	NONE = 6
	T2OF18 = 7
	T4OF12 = 8


# noinspection SpellCheckingInspection
class Cdma2KchanCoderType(Enum):
	"""10 Members, CON2 ... TUR5"""
	CON2 = 0
	CON3 = 1
	CON4 = 2
	CON6 = 3
	DEFault = 4
	OFF = 5
	TUR2 = 6
	TUR3 = 7
	TUR4 = 8
	TUR5 = 9


# noinspection SpellCheckingInspection
class Cdma2KchanCodBlkIlea(Enum):
	"""20 Members, _1152 ... NONE"""
	_1152 = 0
	_12288 = 1
	_128 = 2
	_144 = 3
	_1536 = 4
	_18432 = 5
	_192 = 6
	_2304 = 7
	_288 = 8
	_3072 = 9
	_36864 = 10
	_384 = 11
	_4608 = 12
	_48 = 13
	_576 = 14
	_6144 = 15
	_768 = 16
	_9216 = 17
	_96 = 18
	NONE = 19


# noinspection SpellCheckingInspection
class CckFormat(Enum):
	"""2 Members, LONG ... SHORt"""
	LONG = 0
	SHORt = 1


# noinspection SpellCheckingInspection
class CalPowBandwidth(Enum):
	"""3 Members, AUTO ... LOW"""
	AUTO = 0
	HIGH = 1
	LOW = 2


# noinspection SpellCheckingInspection
class CalPowAttMode(Enum):
	"""2 Members, NEW ... OLD"""
	NEW = 0
	OLD = 1


# noinspection SpellCheckingInspection
class CalPowAmpStagMode(Enum):
	"""3 Members, AUTO ... USER"""
	AUTO = 0
	FIXed = 1
	USER = 2


# noinspection SpellCheckingInspection
class CalPowAmpDetMode(Enum):
	"""13 Members, AMP ... OPU"""
	AMP = 0
	AT20 = 1
	AT40 = 2
	AT6 = 3
	ATT = 4
	AUTO = 5
	FIXed = 6
	HP = 7
	HP6 = 8
	OP20 = 9
	OP40 = 10
	OP6 = 11
	OPU = 12


# noinspection SpellCheckingInspection
class CalDataUpdate(Enum):
	"""5 Members, BBFRC ... RFFRC"""
	BBFRC = 0
	FREQuency = 1
	LEVel = 2
	LEVForced = 3
	RFFRC = 4


# noinspection SpellCheckingInspection
class CalDataMode(Enum):
	"""2 Members, CUSTomer ... FACTory"""
	CUSTomer = 0
	FACTory = 1


# noinspection SpellCheckingInspection
class C5GscmaUser(Enum):
	"""6 Members, USER0 ... USER5"""
	USER0 = 0
	USER1 = 1
	USER2 = 2
	USER3 = 3
	USER4 = 4
	USER5 = 5


# noinspection SpellCheckingInspection
class C5Gmod(Enum):
	"""5 Members, FBMC ... UFMC"""
	FBMC = 0
	FOFDm = 1
	GFDM = 2
	OFDM = 3
	UFMC = 4


# noinspection SpellCheckingInspection
class C5GmarkMode(Enum):
	"""1 Members, RESTart ... RESTart"""
	RESTart = 0


# noinspection SpellCheckingInspection
class C5GfiltT(Enum):
	"""9 Members, DCH ... USER"""
	DCH = 0
	DIRichlet = 1
	NONE = 2
	PHYDyas = 3
	RC = 4
	RECT = 5
	RRC = 6
	STRunc = 7
	USER = 8


# noinspection SpellCheckingInspection
class C5GfilterWind(Enum):
	"""3 Members, HAMMing ... NONE"""
	HAMMing = 0
	HANNing = 1
	NONE = 2


# noinspection SpellCheckingInspection
class C5Gds(Enum):
	"""17 Members, DLISt ... ZERO"""
	DLISt = 0
	ONE = 1
	PATTern = 2
	PN11 = 3
	PN15 = 4
	PN16 = 5
	PN20 = 6
	PN21 = 7
	PN23 = 8
	PN9 = 9
	USER0 = 10
	USER1 = 11
	USER2 = 12
	USER3 = 13
	USER4 = 14
	USER5 = 15
	ZERO = 16


# noinspection SpellCheckingInspection
class C5GcontentType(Enum):
	"""4 Members, DATA ... REServed"""
	DATA = 0
	PILot = 1
	PREamble = 2
	REServed = 3


# noinspection SpellCheckingInspection
class C5GbaseMod(Enum):
	"""7 Members, BPSK ... SCMA"""
	BPSK = 0
	CIQ = 1
	QAM16 = 2
	QAM256 = 3
	QAM64 = 4
	QPSK = 5
	SCMA = 6


# noinspection SpellCheckingInspection
class ByteOrder(Enum):
	"""2 Members, NORMal ... SWAPped"""
	NORMal = 0
	SWAPped = 1


# noinspection SpellCheckingInspection
class BtoUlpPckType(Enum):
	"""49 Members, AAINd ... VIND"""
	AAINd = 0
	ACINd = 1
	ACReq = 2
	ACRSp = 3
	ADCind = 4
	ADINd = 5
	AEINd = 6
	AIND = 7
	ANINd = 8
	ASINd = 9
	ASPSp = 10
	ASReq = 11
	CAReq = 12
	CARSp = 13
	CMReq = 14
	CONT = 15
	CPR = 16
	CPRS = 17
	CREQ = 18
	CTEP = 19
	CTEQ = 20
	CUReq = 21
	DATA = 22
	EREQ = 23
	ERSP = 24
	FREQ = 25
	FRSP = 26
	LREQ = 27
	LRSP = 28
	MUCH = 29
	PEReq = 30
	PERSp = 31
	PIR = 32
	PIRS = 33
	PREQ = 34
	PRSP = 35
	PSINd = 36
	PUIN = 37
	REIN = 38
	RIND = 39
	SEReq = 40
	SERSp = 41
	SFR = 42
	SREQ = 43
	SRSP = 44
	TIND = 45
	TPACket = 46
	URSP = 47
	VIND = 48


# noinspection SpellCheckingInspection
class BtoUlpAddrType(Enum):
	"""2 Members, PUBLic ... RANDom"""
	PUBLic = 0
	RANDom = 1


# noinspection SpellCheckingInspection
class BtoTranMode(Enum):
	"""3 Members, ACL ... SCO"""
	ACL = 0
	ESCO = 1
	SCO = 2


# noinspection SpellCheckingInspection
class BtoSymPerBit(Enum):
	"""2 Members, EIGHt ... TWO"""
	EIGHt = 0
	TWO = 1


# noinspection SpellCheckingInspection
class BtoSlpClckAccrcy(Enum):
	"""8 Members, SCA0 ... SCA7"""
	SCA0 = 0
	SCA1 = 1
	SCA2 = 2
	SCA3 = 3
	SCA4 = 4
	SCA5 = 5
	SCA6 = 6
	SCA7 = 7


# noinspection SpellCheckingInspection
class BtoSlotTiming(Enum):
	"""2 Members, LOOPback ... TX"""
	LOOPback = 0
	TX = 1


# noinspection SpellCheckingInspection
class BtoScanReMode(Enum):
	"""3 Members, R0 ... R2"""
	R0 = 0
	R1 = 1
	R2 = 2


# noinspection SpellCheckingInspection
class BtoPyLdSour(Enum):
	"""8 Members, PAT1 ... PN15"""
	PAT1 = 0
	PAT2 = 1
	PAT3 = 2
	PAT4 = 3
	PAT5 = 4
	PAT6 = 5
	PN09 = 6
	PN15 = 7


# noinspection SpellCheckingInspection
class BtoPckType(Enum):
	"""28 Members, ADH1 ... POLL"""
	ADH1 = 0
	ADH3 = 1
	ADH5 = 2
	AEDH1 = 3
	AEDH3 = 4
	AEDH5 = 5
	AUX1 = 6
	DH1 = 7
	DH3 = 8
	DH5 = 9
	DM1 = 10
	DM3 = 11
	DM5 = 12
	DV = 13
	EEEV3 = 14
	EEEV5 = 15
	EEV3 = 16
	EEV5 = 17
	EV3 = 18
	EV4 = 19
	EV5 = 20
	FHS = 21
	HV1 = 22
	HV2 = 23
	HV3 = 24
	ID = 25
	NULL = 26
	POLL = 27


# noinspection SpellCheckingInspection
class BtoOffsUnit(Enum):
	"""2 Members, U30 ... U300"""
	U30 = 0
	U300 = 1


# noinspection SpellCheckingInspection
class BtoNumOfPackPerSet(Enum):
	"""3 Members, NP1 ... NP50"""
	NP1 = 0
	NP2 = 1
	NP50 = 2


# noinspection SpellCheckingInspection
class BtoModIdxMode(Enum):
	"""2 Members, STABle ... STANdard"""
	STABle = 0
	STANdard = 1


# noinspection SpellCheckingInspection
class BtoMode(Enum):
	"""3 Members, BASic ... QHS"""
	BASic = 0
	BLENergy = 1
	QHS = 2


# noinspection SpellCheckingInspection
class BtoMarkMode(Enum):
	"""8 Members, ACTive ... TRIGger"""
	ACTive = 0
	IACTive = 1
	PATTern = 2
	PULSe = 3
	RATio = 4
	RESTart = 5
	STARt = 6
	TRIGger = 7


# noinspection SpellCheckingInspection
class BtoLlCnctMod(Enum):
	"""2 Members, ENC ... UENC"""
	ENC = 0
	UENC = 1


# noinspection SpellCheckingInspection
class BtoFlowCtrl(Enum):
	"""2 Members, GO ... STOP"""
	GO = 0
	STOP = 1


# noinspection SpellCheckingInspection
class BtoDataSourForPck(Enum):
	"""2 Members, ADATa ... PEDit"""
	ADATa = 0
	PEDit = 1


# noinspection SpellCheckingInspection
class BtoDataSourc(Enum):
	"""11 Members, ALL0 ... PN23"""
	ALL0 = 0
	ALL1 = 1
	DLISt = 2
	PATTern = 3
	PN09 = 4
	PN11 = 5
	PN15 = 6
	PN16 = 7
	PN20 = 8
	PN21 = 9
	PN23 = 10


# noinspection SpellCheckingInspection
class BtoCtrlRol(Enum):
	"""5 Members, ADVertiser ... SLAVe"""
	ADVertiser = 0
	INITiator = 1
	MASTer = 2
	SCANner = 3
	SLAVe = 4


# noinspection SpellCheckingInspection
class BtoCteType(Enum):
	"""3 Members, AOA ... AOD2"""
	AOA = 0
	AOD1 = 1
	AOD2 = 2


# noinspection SpellCheckingInspection
class BtoClkAcc(Enum):
	"""2 Members, T50 ... T500"""
	T50 = 0
	T500 = 1


# noinspection SpellCheckingInspection
class BtoChSel(Enum):
	"""2 Members, CS1 ... CS2"""
	CS1 = 0
	CS2 = 1


# noinspection SpellCheckingInspection
class BtoChnnelType(Enum):
	"""2 Members, ADVertising ... DATA"""
	ADVertising = 0
	DATA = 1


# noinspection SpellCheckingInspection
class BtoAdvMode(Enum):
	"""3 Members, CNS ... NCS"""
	CNS = 0
	NCNS = 1
	NCS = 2


# noinspection SpellCheckingInspection
class BtoAckNldgmt(Enum):
	"""2 Members, ACK ... NAK"""
	ACK = 0
	NAK = 1


# noinspection SpellCheckingInspection
class BsType(Enum):
	"""3 Members, BT1H ... BT2O"""
	BT1H = 0
	BT1O = 1
	BT2O = 2


# noinspection SpellCheckingInspection
class BsClass(Enum):
	"""3 Members, LOC ... WIDE"""
	LOC = 0
	MED = 1
	WIDE = 2


# noinspection SpellCheckingInspection
class BitOrder(Enum):
	"""2 Members, LSBit ... MSBit"""
	LSBit = 0
	MSBit = 1


# noinspection SpellCheckingInspection
class BertUnit(Enum):
	"""3 Members, ENGineering ... PPM"""
	ENGineering = 0
	PCT = 1
	PPM = 2


# noinspection SpellCheckingInspection
class BertType(Enum):
	"""1 Members, CRC16 ... CRC16"""
	CRC16 = 0


# noinspection SpellCheckingInspection
class BertTgEnTrigMode(Enum):
	"""2 Members, DENable ... RESTart"""
	DENable = 0
	RESTart = 1


# noinspection SpellCheckingInspection
class BertTestMode(Enum):
	"""2 Members, BER ... BLER"""
	BER = 0
	BLER = 1


# noinspection SpellCheckingInspection
class BertRestState(Enum):
	"""2 Members, _0 ... _1"""
	_0 = 0
	_1 = 1


# noinspection SpellCheckingInspection
class BertPrbs(Enum):
	"""14 Members, PN11 ... PRBS9"""
	PN11 = 0
	PN15 = 1
	PN16 = 2
	PN20 = 3
	PN21 = 4
	PN23 = 5
	PN9 = 6
	PRBS11 = 7
	PRBS15 = 8
	PRBS16 = 9
	PRBS20 = 10
	PRBS21 = 11
	PRBS23 = 12
	PRBS9 = 13


# noinspection SpellCheckingInspection
class BertPattIgn(Enum):
	"""3 Members, OFF ... ZERO"""
	OFF = 0
	ONE = 1
	ZERO = 2


# noinspection SpellCheckingInspection
class BertMask(Enum):
	"""3 Members, HIGH ... OFF"""
	HIGH = 0
	LOW = 1
	OFF = 2


# noinspection SpellCheckingInspection
class BertCrcOrder(Enum):
	"""2 Members, LSB ... MSB"""
	LSB = 0
	MSB = 1


# noinspection SpellCheckingInspection
class BerBlerTrigMode(Enum):
	"""2 Members, AUTO ... SINGle"""
	AUTO = 0
	SINGle = 1


# noinspection SpellCheckingInspection
class BboutClocSour(Enum):
	"""2 Members, DOUT ... USER"""
	DOUT = 0
	USER = 1


# noinspection SpellCheckingInspection
class BbinSampRateMode(Enum):
	"""3 Members, DIN ... USER"""
	DIN = 0
	HSDin = 1
	USER = 2


# noinspection SpellCheckingInspection
class BbinModeDigital(Enum):
	"""1 Members, DIGital ... DIGital"""
	DIGital = 0


# noinspection SpellCheckingInspection
class BbinInterfaceMode(Enum):
	"""2 Members, DIGital ... HSDin"""
	DIGital = 0
	HSDin = 1


# noinspection SpellCheckingInspection
class BbDmModType(Enum):
	"""35 Members, APSK16 ... USER"""
	APSK16 = 0
	APSK32 = 1
	AQPSk = 2
	ASK = 3
	BPSK = 4
	FSK16 = 5
	FSK2 = 6
	FSK32 = 7
	FSK4 = 8
	FSK64 = 9
	FSK8 = 10
	FSKVar = 11
	MSK = 12
	OQPSk = 13
	P2DBpsk = 14
	P4DQpsk = 15
	P4QPsk = 16
	P8D8psk = 17
	P8EDge = 18
	PSK8 = 19
	QAM1024 = 20
	QAM128 = 21
	QAM16 = 22
	QAM16EDge = 23
	QAM2048 = 24
	QAM256 = 25
	QAM32 = 26
	QAM32EDge = 27
	QAM4096 = 28
	QAM512 = 29
	QAM64 = 30
	QEDGe = 31
	QPSK = 32
	QPSK45 = 33
	USER = 34


# noinspection SpellCheckingInspection
class BbDigInpBb(Enum):
	"""9 Members, A ... NONE"""
	A = 0
	B = 1
	C = 2
	D = 3
	E = 4
	F = 5
	G = 6
	H = 7
	NONE = 8


# noinspection SpellCheckingInspection
class BbCodMode(Enum):
	"""2 Members, BBIN ... CODer"""
	BBIN = 0
	CODer = 1


# noinspection SpellCheckingInspection
class Band(Enum):
	"""32 Members, N1 ... N86"""
	N1 = 0
	N12 = 1
	N2 = 2
	N20 = 3
	N25 = 4
	N28 = 5
	N3 = 6
	N34 = 7
	N38 = 8
	N39 = 9
	N40 = 10
	N41 = 11
	N5 = 12
	N50 = 13
	N51 = 14
	N66 = 15
	N7 = 16
	N70 = 17
	N71 = 18
	N74 = 19
	N75 = 20
	N76 = 21
	N77 = 22
	N78 = 23
	N79 = 24
	N8 = 25
	N80 = 26
	N81 = 27
	N82 = 28
	N83 = 29
	N84 = 30
	N86 = 31


# noinspection SpellCheckingInspection
class AxisType(Enum):
	"""2 Members, CIRCles ... GRID"""
	CIRCles = 0
	GRID = 1


# noinspection SpellCheckingInspection
class AvionicVorMode(Enum):
	"""4 Members, FMSubcarrier ... VAR"""
	FMSubcarrier = 0
	NORM = 1
	SUBCarrier = 2
	VAR = 3


# noinspection SpellCheckingInspection
class AvionicVorIcaoChan(Enum):
	"""160 Members, CH100X ... CH99Y"""
	CH100X = 0
	CH100Y = 1
	CH101X = 2
	CH101Y = 3
	CH102X = 4
	CH102Y = 5
	CH103X = 6
	CH103Y = 7
	CH104X = 8
	CH104Y = 9
	CH105X = 10
	CH105Y = 11
	CH106X = 12
	CH106Y = 13
	CH107X = 14
	CH107Y = 15
	CH108X = 16
	CH108Y = 17
	CH109X = 18
	CH109Y = 19
	CH110X = 20
	CH110Y = 21
	CH111X = 22
	CH111Y = 23
	CH112X = 24
	CH112Y = 25
	CH113X = 26
	CH113Y = 27
	CH114X = 28
	CH114Y = 29
	CH115X = 30
	CH115Y = 31
	CH116X = 32
	CH116Y = 33
	CH117X = 34
	CH117Y = 35
	CH118X = 36
	CH118Y = 37
	CH119X = 38
	CH119Y = 39
	CH120X = 40
	CH120Y = 41
	CH121X = 42
	CH121Y = 43
	CH122X = 44
	CH122Y = 45
	CH123X = 46
	CH123Y = 47
	CH124X = 48
	CH124Y = 49
	CH125X = 50
	CH125Y = 51
	CH126X = 52
	CH126Y = 53
	CH17X = 54
	CH17Y = 55
	CH19X = 56
	CH19Y = 57
	CH21X = 58
	CH21Y = 59
	CH23X = 60
	CH23Y = 61
	CH25X = 62
	CH25Y = 63
	CH27X = 64
	CH27Y = 65
	CH29X = 66
	CH29Y = 67
	CH31X = 68
	CH31Y = 69
	CH33X = 70
	CH33Y = 71
	CH35X = 72
	CH35Y = 73
	CH37X = 74
	CH37Y = 75
	CH39X = 76
	CH39Y = 77
	CH41X = 78
	CH41Y = 79
	CH43X = 80
	CH43Y = 81
	CH45X = 82
	CH45Y = 83
	CH47X = 84
	CH47Y = 85
	CH49X = 86
	CH49Y = 87
	CH51X = 88
	CH51Y = 89
	CH53X = 90
	CH53Y = 91
	CH55X = 92
	CH55Y = 93
	CH57X = 94
	CH57Y = 95
	CH58X = 96
	CH58Y = 97
	CH59X = 98
	CH59Y = 99
	CH70X = 100
	CH70Y = 101
	CH71X = 102
	CH71Y = 103
	CH72X = 104
	CH72Y = 105
	CH73X = 106
	CH73Y = 107
	CH74X = 108
	CH74Y = 109
	CH75X = 110
	CH75Y = 111
	CH76X = 112
	CH76Y = 113
	CH77X = 114
	CH77Y = 115
	CH78X = 116
	CH78Y = 117
	CH79X = 118
	CH79Y = 119
	CH80X = 120
	CH80Y = 121
	CH81X = 122
	CH81Y = 123
	CH82X = 124
	CH82Y = 125
	CH83X = 126
	CH83Y = 127
	CH84X = 128
	CH84Y = 129
	CH85X = 130
	CH85Y = 131
	CH86X = 132
	CH86Y = 133
	CH87X = 134
	CH87Y = 135
	CH88X = 136
	CH88Y = 137
	CH89X = 138
	CH89Y = 139
	CH90X = 140
	CH90Y = 141
	CH91X = 142
	CH91Y = 143
	CH92X = 144
	CH92Y = 145
	CH93X = 146
	CH93Y = 147
	CH94X = 148
	CH94Y = 149
	CH95X = 150
	CH95Y = 151
	CH96X = 152
	CH96Y = 153
	CH97X = 154
	CH97Y = 155
	CH98X = 156
	CH98Y = 157
	CH99X = 158
	CH99Y = 159


# noinspection SpellCheckingInspection
class AvionicVorDir(Enum):
	"""2 Members, FROM ... TO"""
	FROM = 0
	TO = 1


# noinspection SpellCheckingInspection
class AvionicMkrBcnMarkFreq(Enum):
	"""3 Members, _1300 ... _400"""
	_1300 = 0
	_3000 = 1
	_400 = 2


# noinspection SpellCheckingInspection
class AvionicMarkMode(Enum):
	"""5 Members, FP50P ... PSTart"""
	FP50P = 0
	FPSTart = 1
	P50P = 2
	PRECeived = 3
	PSTart = 4


# noinspection SpellCheckingInspection
class AvionicKnobStep(Enum):
	"""2 Members, DECimal ... ICAO"""
	DECimal = 0
	ICAO = 1


# noinspection SpellCheckingInspection
class AvionicIlsType(Enum):
	"""4 Members, GS ... MBEacon"""
	GS = 0
	GSLope = 1
	LOCalize = 2
	MBEacon = 3


# noinspection SpellCheckingInspection
class AvionicIlsLocMode(Enum):
	"""3 Members, LLOBe ... RLOBe"""
	LLOBe = 0
	NORM = 1
	RLOBe = 2


# noinspection SpellCheckingInspection
class AvionicIlsIcaoChan(Enum):
	"""40 Members, CH18X ... CH56Y"""
	CH18X = 0
	CH18Y = 1
	CH20X = 2
	CH20Y = 3
	CH22X = 4
	CH22Y = 5
	CH24X = 6
	CH24Y = 7
	CH26X = 8
	CH26Y = 9
	CH28X = 10
	CH28Y = 11
	CH30X = 12
	CH30Y = 13
	CH32X = 14
	CH32Y = 15
	CH34X = 16
	CH34Y = 17
	CH36X = 18
	CH36Y = 19
	CH38X = 20
	CH38Y = 21
	CH40X = 22
	CH40Y = 23
	CH42X = 24
	CH42Y = 25
	CH44X = 26
	CH44Y = 27
	CH46X = 28
	CH46Y = 29
	CH48X = 30
	CH48Y = 31
	CH50X = 32
	CH50Y = 33
	CH52X = 34
	CH52Y = 35
	CH54X = 36
	CH54Y = 37
	CH56X = 38
	CH56Y = 39


# noinspection SpellCheckingInspection
class AvionicIlsGsMode(Enum):
	"""3 Members, LLOBe ... ULOBe"""
	LLOBe = 0
	NORM = 1
	ULOBe = 2


# noinspection SpellCheckingInspection
class AvionicIlsDdmPol(Enum):
	"""2 Members, P150_90 ... P90_150"""
	P150_90 = 0
	P90_150 = 1


# noinspection SpellCheckingInspection
class AvionicIlsDdmCoup(Enum):
	"""2 Members, FIXed ... SDM"""
	FIXed = 0
	SDM = 1


# noinspection SpellCheckingInspection
class AvionicDmeUsedFact(Enum):
	"""2 Members, INTernal ... PSENsor"""
	INTernal = 0
	PSENsor = 1


# noinspection SpellCheckingInspection
class AvionicDmePulsShap(Enum):
	"""4 Members, COS ... LIN"""
	COS = 0
	COS2 = 1
	GAUSs = 2
	LIN = 3


# noinspection SpellCheckingInspection
class AvionicDmePulsInput(Enum):
	"""2 Members, EXTernal ... PSENsor"""
	EXTernal = 0
	PSENsor = 1


# noinspection SpellCheckingInspection
class AvionicDmeMode(Enum):
	"""2 Members, INTerrogation ... REPLy"""
	INTerrogation = 0
	REPLy = 1


# noinspection SpellCheckingInspection
class AvionicDmeIcaoChan(Enum):
	"""252 Members, CH100X ... CH9Y"""
	CH100X = 0
	CH100Y = 1
	CH101X = 2
	CH101Y = 3
	CH102X = 4
	CH102Y = 5
	CH103X = 6
	CH103Y = 7
	CH104X = 8
	CH104Y = 9
	CH105X = 10
	CH105Y = 11
	CH106X = 12
	CH106Y = 13
	CH107X = 14
	CH107Y = 15
	CH108X = 16
	CH108Y = 17
	CH109X = 18
	CH109Y = 19
	CH10X = 20
	CH10Y = 21
	CH110X = 22
	CH110Y = 23
	CH111X = 24
	CH111Y = 25
	CH112X = 26
	CH112Y = 27
	CH113X = 28
	CH113Y = 29
	CH114X = 30
	CH114Y = 31
	CH115X = 32
	CH115Y = 33
	CH116X = 34
	CH116Y = 35
	CH117X = 36
	CH117Y = 37
	CH118X = 38
	CH118Y = 39
	CH119X = 40
	CH119Y = 41
	CH11X = 42
	CH11Y = 43
	CH120X = 44
	CH120Y = 45
	CH121X = 46
	CH121Y = 47
	CH122X = 48
	CH122Y = 49
	CH123X = 50
	CH123Y = 51
	CH124X = 52
	CH124Y = 53
	CH125X = 54
	CH125Y = 55
	CH126X = 56
	CH126Y = 57
	CH12X = 58
	CH12Y = 59
	CH13X = 60
	CH13Y = 61
	CH14X = 62
	CH14Y = 63
	CH15X = 64
	CH15Y = 65
	CH16X = 66
	CH16Y = 67
	CH17X = 68
	CH17Y = 69
	CH18X = 70
	CH18Y = 71
	CH19X = 72
	CH19Y = 73
	CH1X = 74
	CH1Y = 75
	CH20X = 76
	CH20Y = 77
	CH21X = 78
	CH21Y = 79
	CH22X = 80
	CH22Y = 81
	CH23X = 82
	CH23Y = 83
	CH24X = 84
	CH24Y = 85
	CH25X = 86
	CH25Y = 87
	CH26X = 88
	CH26Y = 89
	CH27X = 90
	CH27Y = 91
	CH28X = 92
	CH28Y = 93
	CH29X = 94
	CH29Y = 95
	CH2X = 96
	CH2Y = 97
	CH30X = 98
	CH30Y = 99
	CH31X = 100
	CH31Y = 101
	CH32X = 102
	CH32Y = 103
	CH33X = 104
	CH33Y = 105
	CH34X = 106
	CH34Y = 107
	CH35X = 108
	CH35Y = 109
	CH36X = 110
	CH36Y = 111
	CH37X = 112
	CH37Y = 113
	CH38X = 114
	CH38Y = 115
	CH39X = 116
	CH39Y = 117
	CH3X = 118
	CH3Y = 119
	CH40X = 120
	CH40Y = 121
	CH41X = 122
	CH41Y = 123
	CH42X = 124
	CH42Y = 125
	CH43X = 126
	CH43Y = 127
	CH44X = 128
	CH44Y = 129
	CH45X = 130
	CH45Y = 131
	CH46X = 132
	CH46Y = 133
	CH47X = 134
	CH47Y = 135
	CH48X = 136
	CH48Y = 137
	CH49X = 138
	CH49Y = 139
	CH4X = 140
	CH4Y = 141
	CH50X = 142
	CH50Y = 143
	CH51X = 144
	CH51Y = 145
	CH52X = 146
	CH52Y = 147
	CH53X = 148
	CH53Y = 149
	CH54X = 150
	CH54Y = 151
	CH55X = 152
	CH55Y = 153
	CH56X = 154
	CH56Y = 155
	CH57X = 156
	CH57Y = 157
	CH58X = 158
	CH58Y = 159
	CH59X = 160
	CH59Y = 161
	CH5X = 162
	CH5Y = 163
	CH60X = 164
	CH60Y = 165
	CH61X = 166
	CH61Y = 167
	CH62X = 168
	CH62Y = 169
	CH63X = 170
	CH63Y = 171
	CH64X = 172
	CH64Y = 173
	CH65X = 174
	CH65Y = 175
	CH66X = 176
	CH66Y = 177
	CH67X = 178
	CH67Y = 179
	CH68X = 180
	CH68Y = 181
	CH69X = 182
	CH69Y = 183
	CH6X = 184
	CH6Y = 185
	CH70X = 186
	CH70Y = 187
	CH71X = 188
	CH71Y = 189
	CH72X = 190
	CH72Y = 191
	CH73X = 192
	CH73Y = 193
	CH74X = 194
	CH74Y = 195
	CH75X = 196
	CH75Y = 197
	CH76X = 198
	CH76Y = 199
	CH77X = 200
	CH77Y = 201
	CH78X = 202
	CH78Y = 203
	CH79X = 204
	CH79Y = 205
	CH7X = 206
	CH7Y = 207
	CH80X = 208
	CH80Y = 209
	CH81X = 210
	CH81Y = 211
	CH82X = 212
	CH82Y = 213
	CH83X = 214
	CH83Y = 215
	CH84X = 216
	CH84Y = 217
	CH85X = 218
	CH85Y = 219
	CH86X = 220
	CH86Y = 221
	CH87X = 222
	CH87Y = 223
	CH88X = 224
	CH88Y = 225
	CH89X = 226
	CH89Y = 227
	CH8X = 228
	CH8Y = 229
	CH90X = 230
	CH90Y = 231
	CH91X = 232
	CH91Y = 233
	CH92X = 234
	CH92Y = 235
	CH93X = 236
	CH93Y = 237
	CH94X = 238
	CH94Y = 239
	CH95X = 240
	CH95Y = 241
	CH96X = 242
	CH96Y = 243
	CH97X = 244
	CH97Y = 245
	CH98X = 246
	CH98Y = 247
	CH99X = 248
	CH99Y = 249
	CH9X = 250
	CH9Y = 251


# noinspection SpellCheckingInspection
class AvionicDmeChanSuff(Enum):
	"""3 Members, ICAO ... Y"""
	ICAO = 0
	X = 1
	Y = 2


# noinspection SpellCheckingInspection
class AvionicDdmStep(Enum):
	"""2 Members, DECimal ... PREDefined"""
	DECimal = 0
	PREDefined = 1


# noinspection SpellCheckingInspection
class AvionicComIdTimeSchem(Enum):
	"""2 Members, STD ... USER"""
	STD = 0
	USER = 1


# noinspection SpellCheckingInspection
class AvionicCarrFreqModeMrkBcn(Enum):
	"""2 Members, PREDefined ... USER"""
	PREDefined = 0
	USER = 1


# noinspection SpellCheckingInspection
class AvionicCarrFreqMode(Enum):
	"""3 Members, DECimal ... USER"""
	DECimal = 0
	ICAO = 1
	USER = 2


# noinspection SpellCheckingInspection
class AutoUser(Enum):
	"""2 Members, AUTO ... USER"""
	AUTO = 0
	USER = 1


# noinspection SpellCheckingInspection
class AutoStep(Enum):
	"""2 Members, AUTO ... STEP"""
	AUTO = 0
	STEP = 1


# noinspection SpellCheckingInspection
class AutoMode(Enum):
	"""3 Members, AUTO ... ON"""
	AUTO = 0
	OFF = 1
	ON = 2


# noinspection SpellCheckingInspection
class AutoManualMode(Enum):
	"""2 Members, AUTO ... MANual"""
	AUTO = 0
	MANual = 1


# noinspection SpellCheckingInspection
class AutoManStep(Enum):
	"""3 Members, AUTO ... STEP"""
	AUTO = 0
	MANual = 1
	STEP = 2


# noinspection SpellCheckingInspection
class AttitMode(Enum):
	"""5 Members, CONStant ... SPINning"""
	CONStant = 0
	FILE = 1
	MOTion = 2
	REMote = 3
	SPINning = 4


# noinspection SpellCheckingInspection
class ArbWaveSegmRest(Enum):
	"""5 Members, MRK1 ... OFF"""
	MRK1 = 0
	MRK2 = 1
	MRK3 = 2
	MRK4 = 3
	OFF = 4


# noinspection SpellCheckingInspection
class ArbWaveSegmPowMode(Enum):
	"""2 Members, ERMS ... UNCHanged"""
	ERMS = 0
	UNCHanged = 1


# noinspection SpellCheckingInspection
class ArbWaveSegmMarkMode(Enum):
	"""2 Members, IGNore ... TAKE"""
	IGNore = 0
	TAKE = 1


# noinspection SpellCheckingInspection
class ArbWaveSegmClocMode(Enum):
	"""3 Members, HIGHest ... USER"""
	HIGHest = 0
	UNCHanged = 1
	USER = 2


# noinspection SpellCheckingInspection
class ArbTrigSegmModeNoEhop(Enum):
	"""4 Members, NEXT ... SEQuencer"""
	NEXT = 0
	NSEam = 1
	SAME = 2
	SEQuencer = 3


# noinspection SpellCheckingInspection
class ArbSignType(Enum):
	"""4 Members, AWGN ... SINE"""
	AWGN = 0
	CIQ = 1
	RECT = 2
	SINE = 3


# noinspection SpellCheckingInspection
class ArbSegmNextSource(Enum):
	"""2 Members, INTernal ... NSEGM1"""
	INTernal = 0
	NSEGM1 = 1


# noinspection SpellCheckingInspection
class ArbMultCarrSpacMode(Enum):
	"""2 Members, ARBitrary ... EQUidistant"""
	ARBitrary = 0
	EQUidistant = 1


# noinspection SpellCheckingInspection
class ArbMultCarrSigDurMod(Enum):
	"""4 Members, LCM ... USER"""
	LCM = 0
	LONG = 1
	SHORt = 2
	USER = 3


# noinspection SpellCheckingInspection
class ArbMultCarrLevRef(Enum):
	"""2 Members, PEAK ... RMS"""
	PEAK = 0
	RMS = 1


# noinspection SpellCheckingInspection
class ArbMultCarrCresMode(Enum):
	"""3 Members, MAX ... OFF"""
	MAX = 0
	MIN = 1
	OFF = 2


# noinspection SpellCheckingInspection
class ArbLevMode(Enum):
	"""2 Members, HIGHest ... UNCHanged"""
	HIGHest = 0
	UNCHanged = 1


# noinspection SpellCheckingInspection
class AntViewType(Enum):
	"""4 Members, APHase ... POSition"""
	APHase = 0
	APOWer = 1
	BODY = 2
	POSition = 3


# noinspection SpellCheckingInspection
class AmFmSource(Enum):
	"""6 Members, EXT1 ... NOISe"""
	EXT1 = 0
	EXTernal = 1
	INTernal = 2
	LF1 = 3
	LF2 = 4
	NOISe = 5


# noinspection SpellCheckingInspection
class AllPxschSequenceGeneration(Enum):
	"""2 Members, CELLid ... DMRSid"""
	CELLid = 0
	DMRSid = 1


# noinspection SpellCheckingInspection
class AllPorts(Enum):
	"""8 Members, _1 ... _8"""
	_1 = 0
	_12 = 1
	_16 = 2
	_2 = 3
	_24 = 4
	_32 = 5
	_4 = 6
	_8 = 7


# noinspection SpellCheckingInspection
class AllPeriodicity(Enum):
	"""13 Members, _10 ... _80"""
	_10 = 0
	_16 = 1
	_160 = 2
	_20 = 3
	_32 = 4
	_320 = 5
	_4 = 6
	_40 = 7
	_5 = 8
	_64 = 9
	_640 = 10
	_8 = 11
	_80 = 12


# noinspection SpellCheckingInspection
class AllocPxschDcifmt(Enum):
	"""4 Members, F00 ... F11"""
	F00 = 0
	F01 = 1
	F10 = 2
	F11 = 3


# noinspection SpellCheckingInspection
class AllocDciuSage(Enum):
	"""16 Members, AI ... TSRS"""
	AI = 0
	C = 1
	CI = 2
	CS = 3
	INT = 4
	MCSC = 5
	P = 6
	PS = 7
	RA = 8
	SFI = 9
	SI = 10
	SPCS = 11
	TC = 12
	TPUC = 13
	TPUS = 14
	TSRS = 15


# noinspection SpellCheckingInspection
class AllocDcisEarchSpace(Enum):
	"""6 Members, CSS0 ... USS"""
	CSS0 = 0
	CSS0A = 1
	CSS1 = 2
	CSS2 = 3
	CSS3 = 4
	USS = 5


# noinspection SpellCheckingInspection
class AllocDcifMt(Enum):
	"""12 Members, CUSTom ... F26"""
	CUSTom = 0
	F00 = 1
	F01 = 2
	F10 = 3
	F11 = 4
	F20 = 5
	F21 = 6
	F22 = 7
	F23 = 8
	F24 = 9
	F25 = 10
	F26 = 11


# noinspection SpellCheckingInspection
class AllocDciaGgLvl(Enum):
	"""5 Members, AL1 ... AL8"""
	AL1 = 0
	AL16 = 1
	AL2 = 2
	AL4 = 3
	AL8 = 4


# noinspection SpellCheckingInspection
class AllHarqAckCodebook(Enum):
	"""2 Members, DYNamic ... SEMistatic"""
	DYNamic = 0
	SEMistatic = 1


# noinspection SpellCheckingInspection
class AllDensity(Enum):
	"""4 Members, DEN1 ... ODD5"""
	DEN1 = 0
	DEN3 = 1
	EVE5 = 2
	ODD5 = 3


# noinspection SpellCheckingInspection
class AllChannelRaster(Enum):
	"""3 Members, R100 ... R60"""
	R100 = 0
	R15 = 1
	R60 = 2


# noinspection SpellCheckingInspection
class AllCdmType(Enum):
	"""4 Members, CDM2 ... NOCDm"""
	CDM2 = 0
	CDM4 = 1
	CDM8 = 2
	NOCDm = 3


# noinspection SpellCheckingInspection
class AllCancellInd(Enum):
	"""10 Members, _1 ... _8"""
	_1 = 0
	_112 = 1
	_14 = 2
	_16 = 3
	_2 = 4
	_32 = 5
	_4 = 6
	_56 = 7
	_7 = 8
	_8 = 9


# noinspection SpellCheckingInspection
class All(Enum):
	"""18 Members, A141 ... A247"""
	A141 = 0
	A142 = 1
	A143 = 2
	A144 = 3
	A151 = 4
	A152 = 5
	A161 = 6
	A162 = 7
	A163 = 8
	A164 = 9
	A165 = 10
	A241 = 11
	A242 = 12
	A243 = 13
	A244 = 14
	A245 = 15
	A246 = 16
	A247 = 17


# noinspection SpellCheckingInspection
class AlcOnOffAuto(Enum):
	"""9 Members, _0 ... PRESet"""
	_0 = 0
	_1 = 1
	AUTO = 2
	OFF = 3
	OFFTable = 4
	ON = 5
	ONSample = 6
	ONTable = 7
	PRESet = 8


# noinspection SpellCheckingInspection
class AlcOffModeSmbv(Enum):
	"""3 Members, HIGHaccuracy ... TABLe"""
	HIGHaccuracy = 0
	SHOLd = 1
	TABLe = 2


# noinspection SpellCheckingInspection
class AichTranTim(Enum):
	"""3 Members, ATT0 ... VOID"""
	ATT0 = 0
	ATT1 = 1
	VOID = 2


# noinspection SpellCheckingInspection
class AcqDataFormatGlonass(Enum):
	"""2 Members, G3GPP ... GRS"""
	G3GPP = 0
	GRS = 1


# noinspection SpellCheckingInspection
class AcDc(Enum):
	"""2 Members, AC ... DC"""
	AC = 0
	DC = 1
