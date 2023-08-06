from .............Internal.Core import Core
from .............Internal.CommandsGroup import CommandsGroup
from .............Internal import Conversions
from ............. import enums
from ............. import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Usage:
	"""Usage commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("usage", core, parent)

	def set(self, usage: enums.AllocDciuSage, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:NR5G:SCHed:CELL<CH>:SUBF<ST>:USER:BWPart:ALLoc:CS:DCI:USAGe \n
		Sets the RNTI type used to scramble the CRC. \n
			:param usage: C| CS| P| SI| RA| TC| SPCS| SFI| INT| TPUS| TPUC| TSRS| MCSC| CI The RNTI type is defined as follows: C Cell CS Configured scheduling P Paging SI System information RA Random access TC Temporary cell SPCS Semi-persistent scheduling cell SFI Slot format indication INT Interruption TPUS Transmit power control-PUSCH TPUC Transmit power control-PUCCH TSRS Transmit power control-SRS MCSC Modulation coding scheme cell CI Cancellation indication
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')"""
		param = Conversions.enum_scalar_to_str(usage, enums.AllocDciuSage)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:SCHed:CELL{channel_cmd_val}:SUBF{stream_cmd_val}:USER:BWPart:ALLoc:CS:DCI:USAGe {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> enums.AllocDciuSage:
		"""[SOURce<HW>]:BB:NR5G:SCHed:CELL<CH>:SUBF<ST>:USER:BWPart:ALLoc:CS:DCI:USAGe \n
		Sets the RNTI type used to scramble the CRC. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:return: usage: C| CS| P| SI| RA| TC| SPCS| SFI| INT| TPUS| TPUC| TSRS| MCSC| CI The RNTI type is defined as follows: C Cell CS Configured scheduling P Paging SI System information RA Random access TC Temporary cell SPCS Semi-persistent scheduling cell SFI Slot format indication INT Interruption TPUS Transmit power control-PUSCH TPUC Transmit power control-PUCCH TSRS Transmit power control-SRS MCSC Modulation coding scheme cell CI Cancellation indication"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:SCHed:CELL{channel_cmd_val}:SUBF{stream_cmd_val}:USER:BWPart:ALLoc:CS:DCI:USAGe?')
		return Conversions.str_to_scalar_enum(response, enums.AllocDciuSage)
