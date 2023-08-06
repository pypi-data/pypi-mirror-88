from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TypePy:
	"""TypePy commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("typePy", core, parent)

	def set(self, type_py: enums.ChanTypeDn, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:BSTation<ST>:CHANnel<CH>:TYPE \n
		Sets the channel type. \n
			:param type_py: PCPich| SCPich| PSCH| SSCH| PCCPch| SCCPch| PICH| APAich| AICH| PDSCh| DPCCh| DPCH| HSSCch| HSQPsk| HSQam| HS64Qam| HSMimo| EAGCh| ERGCh| EHICh| FDPCh| HS16Qam The channels types of CHANnel0 to CHANnel8 are predefined. For the remaining channels, you can select a channel type from the relevant standard channels and the high-speed channels
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')"""
		param = Conversions.enum_scalar_to_str(type_py, enums.ChanTypeDn)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:BSTation{stream_cmd_val}:CHANnel{channel_cmd_val}:TYPE {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> enums.ChanTypeDn:
		"""[SOURce<HW>]:BB:W3GPp:BSTation<ST>:CHANnel<CH>:TYPE \n
		Sets the channel type. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bstation')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Channel')
			:return: type_py: PCPich| SCPich| PSCH| SSCH| PCCPch| SCCPch| PICH| APAich| AICH| PDSCh| DPCCh| DPCH| HSSCch| HSQPsk| HSQam| HS64Qam| HSMimo| EAGCh| ERGCh| EHICh| FDPCh| HS16Qam The channels types of CHANnel0 to CHANnel8 are predefined. For the remaining channels, you can select a channel type from the relevant standard channels and the high-speed channels"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:BSTation{stream_cmd_val}:CHANnel{channel_cmd_val}:TYPE?')
		return Conversions.str_to_scalar_enum(response, enums.ChanTypeDn)
