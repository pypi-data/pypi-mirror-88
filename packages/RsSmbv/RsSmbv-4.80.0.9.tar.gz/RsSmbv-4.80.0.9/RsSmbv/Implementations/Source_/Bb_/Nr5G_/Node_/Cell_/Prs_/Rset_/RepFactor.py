from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RepFactor:
	"""RepFactor commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("repFactor", core, parent)

	def set(self, prs_rs_rep_factor: enums.PrsRepFactor, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:NR5G:NODE:CELL<CH>:PRS:RSET<ST>:REPFactor \n
		Sets the number of repetitions of each resource for a single instance of the resource set. \n
			:param prs_rs_rep_factor: REP32| REP16| REP8| REP4| REP1| REP2
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rset')"""
		param = Conversions.enum_scalar_to_str(prs_rs_rep_factor, enums.PrsRepFactor)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{channel_cmd_val}:PRS:RSET{stream_cmd_val}:REPFactor {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> enums.PrsRepFactor:
		"""[SOURce<HW>]:BB:NR5G:NODE:CELL<CH>:PRS:RSET<ST>:REPFactor \n
		Sets the number of repetitions of each resource for a single instance of the resource set. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rset')
			:return: prs_rs_rep_factor: REP32| REP16| REP8| REP4| REP1| REP2"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{channel_cmd_val}:PRS:RSET{stream_cmd_val}:REPFactor?')
		return Conversions.str_to_scalar_enum(response, enums.PrsRepFactor)
