from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dl:
	"""Dl commands group definition. 616 total commands, 25 Sub-groups, 14 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dl", core, parent)

	def clone(self) -> 'Dl':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Dl(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def ca(self):
		"""ca commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_ca'):
			from .Dl_.Ca import Ca
			self._ca = Ca(self._core, self._base)
		return self._ca

	@property
	def carrier(self):
		"""carrier commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_carrier'):
			from .Dl_.Carrier import Carrier
			self._carrier = Carrier(self._core, self._base)
		return self._carrier

	@property
	def conf(self):
		"""conf commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_conf'):
			from .Dl_.Conf import Conf
			self._conf = Conf(self._core, self._base)
		return self._conf

	@property
	def csettings(self):
		"""csettings commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_csettings'):
			from .Dl_.Csettings import Csettings
			self._csettings = Csettings(self._core, self._base)
		return self._csettings

	@property
	def csis(self):
		"""csis commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_csis'):
			from .Dl_.Csis import Csis
			self._csis = Csis(self._core, self._base)
		return self._csis

	@property
	def drs(self):
		"""drs commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_drs'):
			from .Dl_.Drs import Drs
			self._drs = Drs(self._core, self._base)
		return self._drs

	@property
	def dumd(self):
		"""dumd commands group. 0 Sub-classes, 6 commands."""
		if not hasattr(self, '_dumd'):
			from .Dl_.Dumd import Dumd
			self._dumd = Dumd(self._core, self._base)
		return self._dumd

	@property
	def emtc(self):
		"""emtc commands group. 5 Sub-classes, 4 commands."""
		if not hasattr(self, '_emtc'):
			from .Dl_.Emtc import Emtc
			self._emtc = Emtc(self._core, self._base)
		return self._emtc

	@property
	def laa(self):
		"""laa commands group. 1 Sub-classes, 1 commands."""
		if not hasattr(self, '_laa'):
			from .Dl_.Laa import Laa
			self._laa = Laa(self._core, self._base)
		return self._laa

	@property
	def mbsfn(self):
		"""mbsfn commands group. 4 Sub-classes, 3 commands."""
		if not hasattr(self, '_mbsfn'):
			from .Dl_.Mbsfn import Mbsfn
			self._mbsfn = Mbsfn(self._core, self._base)
		return self._mbsfn

	@property
	def mimo(self):
		"""mimo commands group. 2 Sub-classes, 2 commands."""
		if not hasattr(self, '_mimo'):
			from .Dl_.Mimo import Mimo
			self._mimo = Mimo(self._core, self._base)
		return self._mimo

	@property
	def niot(self):
		"""niot commands group. 9 Sub-classes, 3 commands."""
		if not hasattr(self, '_niot'):
			from .Dl_.Niot import Niot
			self._niot = Niot(self._core, self._base)
		return self._niot

	@property
	def pbch(self):
		"""pbch commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_pbch'):
			from .Dl_.Pbch import Pbch
			self._pbch = Pbch(self._core, self._base)
		return self._pbch

	@property
	def pdcch(self):
		"""pdcch commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_pdcch'):
			from .Dl_.Pdcch import Pdcch
			self._pdcch = Pdcch(self._core, self._base)
		return self._pdcch

	@property
	def pdsch(self):
		"""pdsch commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_pdsch'):
			from .Dl_.Pdsch import Pdsch
			self._pdsch = Pdsch(self._core, self._base)
		return self._pdsch

	@property
	def phich(self):
		"""phich commands group. 2 Sub-classes, 0 commands."""
		if not hasattr(self, '_phich'):
			from .Dl_.Phich import Phich
			self._phich = Phich(self._core, self._base)
		return self._phich

	@property
	def prss(self):
		"""prss commands group. 1 Sub-classes, 7 commands."""
		if not hasattr(self, '_prss'):
			from .Dl_.Prss import Prss
			self._prss = Prss(self._core, self._base)
		return self._prss

	@property
	def refsig(self):
		"""refsig commands group. 1 Sub-classes, 6 commands."""
		if not hasattr(self, '_refsig'):
			from .Dl_.Refsig import Refsig
			self._refsig = Refsig(self._core, self._base)
		return self._refsig

	@property
	def rstFrame(self):
		"""rstFrame commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_rstFrame'):
			from .Dl_.RstFrame import RstFrame
			self._rstFrame = RstFrame(self._core, self._base)
		return self._rstFrame

	@property
	def sync(self):
		"""sync commands group. 1 Sub-classes, 7 commands."""
		if not hasattr(self, '_sync'):
			from .Dl_.Sync import Sync
			self._sync = Sync(self._core, self._base)
		return self._sync

	@property
	def user(self):
		"""user commands group. 25 Sub-classes, 0 commands."""
		if not hasattr(self, '_user'):
			from .Dl_.User import User
			self._user = User(self._core, self._base)
		return self._user

	@property
	def view(self):
		"""view commands group. 0 Sub-classes, 5 commands."""
		if not hasattr(self, '_view'):
			from .Dl_.View import View
			self._view = View(self._core, self._base)
		return self._view

	@property
	def cell(self):
		"""cell commands group. 1 Sub-classes, 0 commands."""
		if not hasattr(self, '_cell'):
			from .Dl_.Cell import Cell
			self._cell = Cell(self._core, self._base)
		return self._cell

	@property
	def plci(self):
		"""plci commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_plci'):
			from .Dl_.Plci import Plci
			self._plci = Plci(self._core, self._base)
		return self._plci

	@property
	def subf(self):
		"""subf commands group. 5 Sub-classes, 0 commands."""
		if not hasattr(self, '_subf'):
			from .Dl_.Subf import Subf
			self._subf = Subf(self._core, self._base)
		return self._subf

	# noinspection PyTypeChecker
	def get_bur(self) -> enums.EutraBehUnsSubframes:
		"""[SOURce<HW>]:BB:EUTRa:DL:BUR \n
		Selects either to fill unscheduled resource elements and subframes with dummy data or DTX. In 'Mode > eMTC/NB-IoT',
		unused resource elements are filled in with DTX. \n
			:return: bur: DUData| DTX
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:BUR?')
		return Conversions.str_to_scalar_enum(response, enums.EutraBehUnsSubframes)

	def set_bur(self, bur: enums.EutraBehUnsSubframes) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:BUR \n
		Selects either to fill unscheduled resource elements and subframes with dummy data or DTX. In 'Mode > eMTC/NB-IoT',
		unused resource elements are filled in with DTX. \n
			:param bur: DUData| DTX
		"""
		param = Conversions.enum_scalar_to_str(bur, enums.EutraBehUnsSubframes)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:BUR {param}')

	# noinspection PyTypeChecker
	def get_bw(self) -> enums.EutraChannelBandwidth:
		"""[SOURce<HW>]:BB:EUTRa:DL:BW \n
		Sets the DL channel bandwidth. \n
			:return: bw: BW1_40| BW3_00| BW5_00| BW10_00| BW15_00| BW20_00 | BW0_20 | USER
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:BW?')
		return Conversions.str_to_scalar_enum(response, enums.EutraChannelBandwidth)

	def set_bw(self, bw: enums.EutraChannelBandwidth) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:BW \n
		Sets the DL channel bandwidth. \n
			:param bw: BW1_40| BW3_00| BW5_00| BW10_00| BW15_00| BW20_00 | BW0_20 | USER
		"""
		param = Conversions.enum_scalar_to_str(bw, enums.EutraChannelBandwidth)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:BW {param}')

	def get_con_sub_frames(self) -> int:
		"""[SOURce<HW>]:BB:EUTRa:DL:CONSubframes \n
		Sets the number of configurable subframes. \n
			:return: con_sub_frames: integer Range: 1 to 40
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:CONSubframes?')
		return Conversions.str_to_int(response)

	def set_con_sub_frames(self, con_sub_frames: int) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:CONSubframes \n
		Sets the number of configurable subframes. \n
			:param con_sub_frames: integer Range: 1 to 40
		"""
		param = Conversions.decimal_value_to_str(con_sub_frames)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:CONSubframes {param}')

	# noinspection PyTypeChecker
	def get_cpc(self) -> enums.EutraCyclicPrefixGs:
		"""[SOURce<HW>]:BB:EUTRa:DL:CPC \n
		Sets the cyclic prefix length for all LTE subframes. \n
			:return: cyclic_prefix: NORMal| EXTended | USER
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:CPC?')
		return Conversions.str_to_scalar_enum(response, enums.EutraCyclicPrefixGs)

	def set_cpc(self, cyclic_prefix: enums.EutraCyclicPrefixGs) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:CPC \n
		Sets the cyclic prefix length for all LTE subframes. \n
			:param cyclic_prefix: NORMal| EXTended | USER
		"""
		param = Conversions.enum_scalar_to_str(cyclic_prefix, enums.EutraCyclicPrefixGs)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:CPC {param}')

	def get_fft(self) -> int:
		"""[SOURce<HW>]:BB:EUTRa:DL:FFT \n
		Sets the FFT size. \n
			:return: fft: integer Range: 64 to 2048
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:FFT?')
		return Conversions.str_to_int(response)

	def set_fft(self, fft: int) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:FFT \n
		Sets the FFT size. \n
			:param fft: integer Range: 64 to 2048
		"""
		param = Conversions.decimal_value_to_str(fft)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:FFT {param}')

	def get_lgs(self) -> int:
		"""[SOURce<HW>]:BB:EUTRa:DL:LGS \n
		Queries the number of left guard subcarriers. \n
			:return: lgs: integer Range: 28 to 364
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:LGS?')
		return Conversions.str_to_int(response)

	def get_norb(self) -> int:
		"""[SOURce<HW>]:BB:EUTRa:DL:NORB \n
		Selects the number of physical resource blocks per slot. \n
			:return: norb: integer Range: 6 to 110
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:NORB?')
		return Conversions.str_to_int(response)

	def set_norb(self, norb: int) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:NORB \n
		Selects the number of physical resource blocks per slot. \n
			:param norb: integer Range: 6 to 110
		"""
		param = Conversions.decimal_value_to_str(norb)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:NORB {param}')

	def get_occ_bandwidth(self) -> float:
		"""[SOURce<HW>]:BB:EUTRa:DL:OCCBandwidth \n
		Queries the occupied bandwidth. \n
			:return: occup_bandwidth: float
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:OCCBandwidth?')
		return Conversions.str_to_float(response)

	def get_occ_subcarriers(self) -> int:
		"""[SOURce<HW>]:BB:EUTRa:DL:OCCSubcarriers \n
		Queries the occupied subcarriers. \n
			:return: occup_subcarr: integer Range: 72 to 1321
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:OCCSubcarriers?')
		return Conversions.str_to_int(response)

	# noinspection PyTypeChecker
	def get_pum(self) -> enums.EutraPwrUpdMode:
		"""[SOURce<HW>]:BB:EUTRa:DL:PUM \n
		No command help available \n
			:return: power_update_mode: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:PUM?')
		return Conversions.str_to_scalar_enum(response, enums.EutraPwrUpdMode)

	def set_pum(self, power_update_mode: enums.EutraPwrUpdMode) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:PUM \n
		No command help available \n
			:param power_update_mode: No help available
		"""
		param = Conversions.enum_scalar_to_str(power_update_mode, enums.EutraPwrUpdMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:PUM {param}')

	def get_rgs(self) -> int:
		"""[SOURce<HW>]:BB:EUTRa:DL:RGS \n
		Queries the number of right guard subcarriers. \n
			:return: rgs: integer Range: 27 to 364
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:RGS?')
		return Conversions.str_to_int(response)

	def get_sf_selection(self) -> int:
		"""[SOURce<HW>]:BB:EUTRa:DL:SFSelection \n
		No command help available \n
			:return: sub_frame_sel: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:SFSelection?')
		return Conversions.str_to_int(response)

	def set_sf_selection(self, sub_frame_sel: int) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:SFSelection \n
		No command help available \n
			:param sub_frame_sel: No help available
		"""
		param = Conversions.decimal_value_to_str(sub_frame_sel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:SFSelection {param}')

	def get_symbol_rate(self) -> float:
		"""[SOURce<HW>]:BB:EUTRa:DL:SRATe \n
		Queries the sampling rate. \n
			:return: sample_rate: float Range: 192E4 to 3072E4
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:SRATe?')
		return Conversions.str_to_float(response)

	# noinspection PyTypeChecker
	def get_ulcpc(self) -> enums.EuTraDuration:
		"""[SOURce<HW>]:BB:EUTRa:DL:ULCPc \n
		In TDD duplexing mode, sets the cyclic prefix for the opposite direction. \n
			:return: gs_cpc_opp_dir: NORMal| EXTended
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:DL:ULCPc?')
		return Conversions.str_to_scalar_enum(response, enums.EuTraDuration)

	def set_ulcpc(self, gs_cpc_opp_dir: enums.EuTraDuration) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:ULCPc \n
		In TDD duplexing mode, sets the cyclic prefix for the opposite direction. \n
			:param gs_cpc_opp_dir: NORMal| EXTended
		"""
		param = Conversions.enum_scalar_to_str(gs_cpc_opp_dir, enums.EuTraDuration)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:ULCPc {param}')
