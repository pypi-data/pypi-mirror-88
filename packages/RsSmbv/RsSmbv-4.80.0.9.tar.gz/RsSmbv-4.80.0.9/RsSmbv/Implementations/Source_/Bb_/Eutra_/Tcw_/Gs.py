from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Gs:
	"""Gs commands group definition. 14 total commands, 0 Sub-groups, 14 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("gs", core, parent)

	# noinspection PyTypeChecker
	def get_ant_subset(self) -> enums.EutraTcwaNtSubset:
		"""[SOURce<HW>]:BB:EUTRa:TCW:GS:ANTSubset \n
		No command help available \n
			:return: antenna_subset: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:TCW:GS:ANTSubset?')
		return Conversions.str_to_scalar_enum(response, enums.EutraTcwaNtSubset)

	def set_ant_subset(self, antenna_subset: enums.EutraTcwaNtSubset) -> None:
		"""[SOURce<HW>]:BB:EUTRa:TCW:GS:ANTSubset \n
		No command help available \n
			:param antenna_subset: No help available
		"""
		param = Conversions.enum_scalar_to_str(antenna_subset, enums.EutraTcwaNtSubset)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:TCW:GS:ANTSubset {param}')

	# noinspection PyTypeChecker
	def get_bs_class(self) -> enums.UtraTcwbSclass:
		"""[SOURce<HW>]:BB:EUTRa:TCW:GS:BSCLass \n
		Sets the base station class. \n
			:return: bs_class: WIDE| LOCal| HOME| MEDium
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:TCW:GS:BSCLass?')
		return Conversions.str_to_scalar_enum(response, enums.UtraTcwbSclass)

	def set_bs_class(self, bs_class: enums.UtraTcwbSclass) -> None:
		"""[SOURce<HW>]:BB:EUTRa:TCW:GS:BSCLass \n
		Sets the base station class. \n
			:param bs_class: WIDE| LOCal| HOME| MEDium
		"""
		param = Conversions.enum_scalar_to_str(bs_class, enums.UtraTcwbSclass)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:TCW:GS:BSCLass {param}')

	# noinspection PyTypeChecker
	def get_gen_signals(self) -> enums.EutraTcwGeneratedSig:
		"""[SOURce<HW>]:BB:EUTRa:TCW:GS:GENSignals \n
		No command help available \n
			:return: generated_signal: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:TCW:GS:GENSignals?')
		return Conversions.str_to_scalar_enum(response, enums.EutraTcwGeneratedSig)

	def set_gen_signals(self, generated_signal: enums.EutraTcwGeneratedSig) -> None:
		"""[SOURce<HW>]:BB:EUTRa:TCW:GS:GENSignals \n
		No command help available \n
			:param generated_signal: No help available
		"""
		param = Conversions.enum_scalar_to_str(generated_signal, enums.EutraTcwGeneratedSig)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:TCW:GS:GENSignals {param}')

	# noinspection PyTypeChecker
	def get_inst_setup(self) -> enums.EutraTcwiNstSetup:
		"""[SOURce<HW>]:BB:EUTRa:TCW:GS:INSTsetup \n
		No command help available \n
			:return: instrument_setup: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:TCW:GS:INSTsetup?')
		return Conversions.str_to_scalar_enum(response, enums.EutraTcwiNstSetup)

	def set_inst_setup(self, instrument_setup: enums.EutraTcwiNstSetup) -> None:
		"""[SOURce<HW>]:BB:EUTRa:TCW:GS:INSTsetup \n
		No command help available \n
			:param instrument_setup: No help available
		"""
		param = Conversions.enum_scalar_to_str(instrument_setup, enums.EutraTcwiNstSetup)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:TCW:GS:INSTsetup {param}')

	# noinspection PyTypeChecker
	def get_marker_config(self) -> enums.EutraTcwMarkConf:
		"""[SOURce<HW>]:BB:EUTRa:TCW:GS:MARKerconfig \n
		Selects the marker configuration. The marker can be used to synchronize the measuring equipment to the signal generator. \n
			:return: marker_config: UNCHanged| FRAMe FRAMe The marker settings are customized for the selected test case. 'Radio Frame Start' markers are output; the marker delays are set equal to zero. UNCHanged The current marker settings of the signal generator are retained unchanged.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:TCW:GS:MARKerconfig?')
		return Conversions.str_to_scalar_enum(response, enums.EutraTcwMarkConf)

	def set_marker_config(self, marker_config: enums.EutraTcwMarkConf) -> None:
		"""[SOURce<HW>]:BB:EUTRa:TCW:GS:MARKerconfig \n
		Selects the marker configuration. The marker can be used to synchronize the measuring equipment to the signal generator. \n
			:param marker_config: UNCHanged| FRAMe FRAMe The marker settings are customized for the selected test case. 'Radio Frame Start' markers are output; the marker delays are set equal to zero. UNCHanged The current marker settings of the signal generator are retained unchanged.
		"""
		param = Conversions.enum_scalar_to_str(marker_config, enums.EutraTcwMarkConf)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:TCW:GS:MARKerconfig {param}')

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.EutraTcwGsModeDefaultRange:
		"""[SOURce<HW>]:BB:EUTRa:TCW:GS:MODE \n
		No command help available \n
			:return: mode: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:TCW:GS:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.EutraTcwGsModeDefaultRange)

	def set_mode(self, mode: enums.EutraTcwGsModeDefaultRange) -> None:
		"""[SOURce<HW>]:BB:EUTRa:TCW:GS:MODE \n
		No command help available \n
			:param mode: No help available
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.EutraTcwGsModeDefaultRange)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:TCW:GS:MODE {param}')

	# noinspection PyTypeChecker
	def get_option(self) -> enums.UtraTcwgsoPtion:
		"""[SOURce<HW>]:BB:EUTRa:TCW:GS:OPTion \n
		No command help available \n
			:return: option: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:TCW:GS:OPTion?')
		return Conversions.str_to_scalar_enum(response, enums.UtraTcwgsoPtion)

	def set_option(self, option: enums.UtraTcwgsoPtion) -> None:
		"""[SOURce<HW>]:BB:EUTRa:TCW:GS:OPTion \n
		No command help available \n
			:param option: No help available
		"""
		param = Conversions.enum_scalar_to_str(option, enums.UtraTcwgsoPtion)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:TCW:GS:OPTion {param}')

	# noinspection PyTypeChecker
	def get_release(self) -> enums.EutraTcwRelease:
		"""[SOURce<HW>]:BB:EUTRa:TCW:GS:RELease \n
		Sets the 3GPP test specification used as a guideline for the test cases. \n
			:return: release: REL8| REL9| REL10| REL11
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:TCW:GS:RELease?')
		return Conversions.str_to_scalar_enum(response, enums.EutraTcwRelease)

	def set_release(self, release: enums.EutraTcwRelease) -> None:
		"""[SOURce<HW>]:BB:EUTRa:TCW:GS:RELease \n
		Sets the 3GPP test specification used as a guideline for the test cases. \n
			:param release: REL8| REL9| REL10| REL11
		"""
		param = Conversions.enum_scalar_to_str(release, enums.EutraTcwRelease)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:TCW:GS:RELease {param}')

	# noinspection PyTypeChecker
	def get_rx_antennas(self) -> enums.EutraTcwNumOfRxAnt:
		"""[SOURce<HW>]:BB:EUTRa:TCW:GS:RXANtennas \n
		No command help available \n
			:return: num_of_rx_antennas: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:TCW:GS:RXANtennas?')
		return Conversions.str_to_scalar_enum(response, enums.EutraTcwNumOfRxAnt)

	def set_rx_antennas(self, num_of_rx_antennas: enums.EutraTcwNumOfRxAnt) -> None:
		"""[SOURce<HW>]:BB:EUTRa:TCW:GS:RXANtennas \n
		No command help available \n
			:param num_of_rx_antennas: No help available
		"""
		param = Conversions.enum_scalar_to_str(num_of_rx_antennas, enums.EutraTcwNumOfRxAnt)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:TCW:GS:RXANtennas {param}')

	# noinspection PyTypeChecker
	def get_sig_rout(self) -> enums.EutraTcwSignalRout:
		"""[SOURce<HW>]:BB:EUTRa:TCW:GS:SIGRout \n
		Selects the signal routing for baseband A signal which usually represents the wanted signal. \n
			:return: signal_routing: PORTA
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:TCW:GS:SIGRout?')
		return Conversions.str_to_scalar_enum(response, enums.EutraTcwSignalRout)

	def set_sig_rout(self, signal_routing: enums.EutraTcwSignalRout) -> None:
		"""[SOURce<HW>]:BB:EUTRa:TCW:GS:SIGRout \n
		Selects the signal routing for baseband A signal which usually represents the wanted signal. \n
			:param signal_routing: PORTA
		"""
		param = Conversions.enum_scalar_to_str(signal_routing, enums.EutraTcwSignalRout)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:TCW:GS:SIGRout {param}')

	# noinspection PyTypeChecker
	def get_spec(self) -> enums.UtraTcwsPec:
		"""[SOURce<HW>]:BB:EUTRa:TCW:GS:SPEC \n
		Selects the 3GPP test specification used as a guideline for the test cases. \n
			:return: gs_spec: TS36141
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:TCW:GS:SPEC?')
		return Conversions.str_to_scalar_enum(response, enums.UtraTcwsPec)

	def set_spec(self, gs_spec: enums.UtraTcwsPec) -> None:
		"""[SOURce<HW>]:BB:EUTRa:TCW:GS:SPEC \n
		Selects the 3GPP test specification used as a guideline for the test cases. \n
			:param gs_spec: TS36141
		"""
		param = Conversions.enum_scalar_to_str(gs_spec, enums.UtraTcwsPec)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:TCW:GS:SPEC {param}')

	# noinspection PyTypeChecker
	def get_stc(self) -> enums.UtraTcwgssUbtest:
		"""[SOURce<HW>]:BB:EUTRa:TCW:GS:STC \n
		No command help available \n
			:return: subtest_case: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:TCW:GS:STC?')
		return Conversions.str_to_scalar_enum(response, enums.UtraTcwgssUbtest)

	def set_stc(self, subtest_case: enums.UtraTcwgssUbtest) -> None:
		"""[SOURce<HW>]:BB:EUTRa:TCW:GS:STC \n
		No command help available \n
			:param subtest_case: No help available
		"""
		param = Conversions.enum_scalar_to_str(subtest_case, enums.UtraTcwgssUbtest)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:TCW:GS:STC {param}')

	# noinspection PyTypeChecker
	def get_trigger_config(self) -> enums.EutraTcwtRigConf:
		"""[SOURce<HW>]:BB:EUTRa:TCW:GS:TRIGgerconfig \n
		Selects the trigger configuration. The trigger is used to synchronize the signal generator to the other equipment. \n
			:return: trigger_config: UNCHanged| AAUTo UNCHanged The current trigger settings of the signal generator are retained unchanged. AAUTo The trigger settings are customized for the selected test case. The trigger setting 'Armed Auto' with external trigger source is used; the trigger delay is set to zero. Thus, the base station frame timing is able to synchronize the signal generator by a periodic trigger.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:TCW:GS:TRIGgerconfig?')
		return Conversions.str_to_scalar_enum(response, enums.EutraTcwtRigConf)

	def set_trigger_config(self, trigger_config: enums.EutraTcwtRigConf) -> None:
		"""[SOURce<HW>]:BB:EUTRa:TCW:GS:TRIGgerconfig \n
		Selects the trigger configuration. The trigger is used to synchronize the signal generator to the other equipment. \n
			:param trigger_config: UNCHanged| AAUTo UNCHanged The current trigger settings of the signal generator are retained unchanged. AAUTo The trigger settings are customized for the selected test case. The trigger setting 'Armed Auto' with external trigger source is used; the trigger delay is set to zero. Thus, the base station frame timing is able to synchronize the signal generator by a periodic trigger.
		"""
		param = Conversions.enum_scalar_to_str(trigger_config, enums.EutraTcwtRigConf)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:TCW:GS:TRIGgerconfig {param}')

	# noinspection PyTypeChecker
	def get_tx_antennas(self) -> enums.TxAntenna:
		"""[SOURce<HW>]:BB:EUTRa:TCW:GS:TXANtennas \n
		No command help available \n
			:return: num_of_tx_antennas: No help available
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:EUTRa:TCW:GS:TXANtennas?')
		return Conversions.str_to_scalar_enum(response, enums.TxAntenna)

	def set_tx_antennas(self, num_of_tx_antennas: enums.TxAntenna) -> None:
		"""[SOURce<HW>]:BB:EUTRa:TCW:GS:TXANtennas \n
		No command help available \n
			:param num_of_tx_antennas: No help available
		"""
		param = Conversions.enum_scalar_to_str(num_of_tx_antennas, enums.TxAntenna)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:TCW:GS:TXANtennas {param}')
