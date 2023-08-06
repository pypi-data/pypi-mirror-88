from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Fconfig:
	"""Fconfig commands group definition. 14 total commands, 3 Sub-groups, 9 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("fconfig", core, parent)

	def clone(self) -> 'Fconfig':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Fconfig(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def data(self):
		"""data commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_data'):
			from .Fconfig_.Data import Data
			self._data = Data(self._core, self._base)
		return self._data

	@property
	def dlength(self):
		"""dlength commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_dlength'):
			from .Fconfig_.Dlength import Dlength
			self._dlength = Dlength(self._core, self._base)
		return self._dlength

	@property
	def mcs(self):
		"""mcs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_mcs'):
			from .Fconfig_.Mcs import Mcs
			self._mcs = Mcs(self._core, self._base)
		return self._mcs

	# noinspection PyTypeChecker
	def get_cindex(self) -> enums.HrpUwbCodeIndex:
		"""[SOURce<HW>]:BB:HUWB:FCONfig:CINDex \n
		Sets the code index. \n
			:return: code_index: CI_1| CI_2| CI_3| CI_4| CI_5| CI_6| CI_7| CI_8| CI_9| CI_10| CI_11| CI_12| CI_13| CI_14| CI_15| CI_16| CI_17| CI_19| CI_18| CI_20| CI_21| CI_22| CI_23| CI_24
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:FCONfig:CINDex?')
		return Conversions.str_to_scalar_enum(response, enums.HrpUwbCodeIndex)

	def set_cindex(self, code_index: enums.HrpUwbCodeIndex) -> None:
		"""[SOURce<HW>]:BB:HUWB:FCONfig:CINDex \n
		Sets the code index. \n
			:param code_index: CI_1| CI_2| CI_3| CI_4| CI_5| CI_6| CI_7| CI_8| CI_9| CI_10| CI_11| CI_12| CI_13| CI_14| CI_15| CI_16| CI_17| CI_19| CI_18| CI_20| CI_21| CI_22| CI_23| CI_24
		"""
		param = Conversions.enum_scalar_to_str(code_index, enums.HrpUwbCodeIndex)
		self._core.io.write(f'SOURce<HwInstance>:BB:HUWB:FCONfig:CINDex {param}')

	# noinspection PyTypeChecker
	def get_cp_burst(self) -> enums.HrpUwbChipsPerBurst:
		"""[SOURce<HW>]:BB:HUWB:FCONfig:CPBurst \n
		Sets the chips per burst. \n
			:return: chips_per_burst: CPB_1| CPB_2| CPB_4| CPB_16| CPB_8| CPB_32| CPB_64| CPB_128| CPB_512
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:FCONfig:CPBurst?')
		return Conversions.str_to_scalar_enum(response, enums.HrpUwbChipsPerBurst)

	def set_cp_burst(self, chips_per_burst: enums.HrpUwbChipsPerBurst) -> None:
		"""[SOURce<HW>]:BB:HUWB:FCONfig:CPBurst \n
		Sets the chips per burst. \n
			:param chips_per_burst: CPB_1| CPB_2| CPB_4| CPB_16| CPB_8| CPB_32| CPB_64| CPB_128| CPB_512
		"""
		param = Conversions.enum_scalar_to_str(chips_per_burst, enums.HrpUwbChipsPerBurst)
		self._core.io.write(f'SOURce<HwInstance>:BB:HUWB:FCONfig:CPBurst {param}')

	def get_dr(self) -> float:
		"""[SOURce<HW>]:BB:HUWB:FCONfig:DR \n
		Queries the data rate. \n
			:return: data_rate: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:FCONfig:DR?')
		return Conversions.str_to_float(response)

	# noinspection PyTypeChecker
	def get_hop_burst(self) -> enums.HrpUwbHopBurst:
		"""[SOURce<HW>]:BB:HUWB:FCONfig:HOPBurst \n
		Sets the number of hop bursts. \n
			:return: hop_burst: HB_2| HB_8| HB_32
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:FCONfig:HOPBurst?')
		return Conversions.str_to_scalar_enum(response, enums.HrpUwbHopBurst)

	def set_hop_burst(self, hop_burst: enums.HrpUwbHopBurst) -> None:
		"""[SOURce<HW>]:BB:HUWB:FCONfig:HOPBurst \n
		Sets the number of hop bursts. \n
			:param hop_burst: HB_2| HB_8| HB_32
		"""
		param = Conversions.enum_scalar_to_str(hop_burst, enums.HrpUwbHopBurst)
		self._core.io.write(f'SOURce<HwInstance>:BB:HUWB:FCONfig:HOPBurst {param}')

	def get_mprf(self) -> float:
		"""[SOURce<HW>]:BB:HUWB:FCONfig:MPRF \n
		Queries the mean pulse repetition frequency (PRF) . \n
			:return: mean_prf: float
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:FCONfig:MPRF?')
		return Conversions.str_to_float(response)

	def get_phrb_rate(self) -> float:
		"""[SOURce<HW>]:BB:HUWB:FCONfig:PHRBrate \n
		Queries the physical header bit rate. \n
			:return: hrp_uwb_phr_bit_rate: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:FCONfig:PHRBrate?')
		return Conversions.str_to_float(response)

	# noinspection PyTypeChecker
	def get_sfd_length(self) -> enums.HrpUwbSfdlEngth:
		"""[SOURce<HW>]:BB:HUWB:FCONfig:SFDLength \n
		Queries the length of the start-of-frame delimiter (SFD) . \n
			:return: sfd_length: SFDL_8| SFDL_64
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:FCONfig:SFDLength?')
		return Conversions.str_to_scalar_enum(response, enums.HrpUwbSfdlEngth)

	def set_sfd_length(self, sfd_length: enums.HrpUwbSfdlEngth) -> None:
		"""[SOURce<HW>]:BB:HUWB:FCONfig:SFDLength \n
		Queries the length of the start-of-frame delimiter (SFD) . \n
			:param sfd_length: SFDL_8| SFDL_64
		"""
		param = Conversions.enum_scalar_to_str(sfd_length, enums.HrpUwbSfdlEngth)
		self._core.io.write(f'SOURce<HwInstance>:BB:HUWB:FCONfig:SFDLength {param}')

	# noinspection PyTypeChecker
	def get_syn_length(self) -> enums.HrpUwbSyncLength:
		"""[SOURce<HW>]:BB:HUWB:FCONfig:SYNLength \n
		Sets the sync length. \n
			:return: sync_length: SL_16| SL_1024| SL_64| SL_4096
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:FCONfig:SYNLength?')
		return Conversions.str_to_scalar_enum(response, enums.HrpUwbSyncLength)

	def set_syn_length(self, sync_length: enums.HrpUwbSyncLength) -> None:
		"""[SOURce<HW>]:BB:HUWB:FCONfig:SYNLength \n
		Sets the sync length. \n
			:param sync_length: SL_16| SL_1024| SL_64| SL_4096
		"""
		param = Conversions.enum_scalar_to_str(sync_length, enums.HrpUwbSyncLength)
		self._core.io.write(f'SOURce<HwInstance>:BB:HUWB:FCONfig:SYNLength {param}')

	# noinspection PyTypeChecker
	def get_vrate(self) -> enums.HrpUwbViterbiRate:
		"""[SOURce<HW>]:BB:HUWB:FCONfig:VRATe \n
		Queries the viterbi rate for convolutional coding. \n
			:return: hrp_uwb_viterbi_rate: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:HUWB:FCONfig:VRATe?')
		return Conversions.str_to_scalar_enum(response, enums.HrpUwbViterbiRate)
