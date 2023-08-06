from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Orate:
	"""Orate commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("orate", core, parent)

	def set(self, orate: enums.SymbRate, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:DPDCh:ORATe \n
		The command sets the overall symbol rate. The overall symbol rate determines the number of DPDCHs as well as their symbol
		rate and channelization codes. \n
			:param orate: D15K| D30K| D60K| D120k| D240k| D480k| D960k| D1920k| D2880k| D3840k| D4800k| D5760k D15K ... D5760K 15 ksps ... 6 x 960 ksps
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')"""
		param = Conversions.enum_scalar_to_str(orate, enums.SymbRate)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:DPDCh:ORATe {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.SymbRate:
		"""[SOURce<HW>]:BB:W3GPp:MSTation<ST>:DPDCh:ORATe \n
		The command sets the overall symbol rate. The overall symbol rate determines the number of DPDCHs as well as their symbol
		rate and channelization codes. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Mstation')
			:return: orate: D15K| D30K| D60K| D120k| D240k| D480k| D960k| D1920k| D2880k| D3840k| D4800k| D5760k D15K ... D5760K 15 ksps ... 6 x 960 ksps"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:MSTation{stream_cmd_val}:DPDCh:ORATe?')
		return Conversions.str_to_scalar_enum(response, enums.SymbRate)
