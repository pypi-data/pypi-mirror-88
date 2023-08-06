from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import enums
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Rmc:
	"""Rmc commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rmc", core, parent)

	def set(self, rmc: enums.TdscdmaEnhHsRmcMode, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:TDSCdma:DOWN:CELL<ST>:ENH:DCH:HSDPA:RMC \n
		Enables a predefined set of RMC channels or fully configurable user mode. \n
			:param rmc: HRMC_0M5_QPSK| HRMC_1M1_QPSK| HRMC_1M1_16QAM| HRMC_1M6_QPSK| HRMC_1M6_16QAM| HRMC_2M2_QPSK| HRMC_2M2_16QAM| HRMC_2M8_QPSK| HRMC_2M8_16QAM| HRMC_64QAM_16UE| HRMC_64QAM_19UE| HRMC_64QAM_22UE| USER
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')"""
		param = Conversions.enum_scalar_to_str(rmc, enums.TdscdmaEnhHsRmcMode)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:TDSCdma:DOWN:CELL{stream_cmd_val}:ENH:DCH:HSDPA:RMC {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.TdscdmaEnhHsRmcMode:
		"""[SOURce<HW>]:BB:TDSCdma:DOWN:CELL<ST>:ENH:DCH:HSDPA:RMC \n
		Enables a predefined set of RMC channels or fully configurable user mode. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:return: rmc: HRMC_0M5_QPSK| HRMC_1M1_QPSK| HRMC_1M1_16QAM| HRMC_1M6_QPSK| HRMC_1M6_16QAM| HRMC_2M2_QPSK| HRMC_2M2_16QAM| HRMC_2M8_QPSK| HRMC_2M8_16QAM| HRMC_64QAM_16UE| HRMC_64QAM_19UE| HRMC_64QAM_22UE| USER"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:TDSCdma:DOWN:CELL{stream_cmd_val}:ENH:DCH:HSDPA:RMC?')
		return Conversions.str_to_scalar_enum(response, enums.TdscdmaEnhHsRmcMode)
