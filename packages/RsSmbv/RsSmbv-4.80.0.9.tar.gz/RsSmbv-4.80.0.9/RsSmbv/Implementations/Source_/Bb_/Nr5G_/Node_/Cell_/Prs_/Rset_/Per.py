from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Per:
	"""Per commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("per", core, parent)

	def set(self, prs_rs_period: enums.PrsPeriodicity, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:NR5G:NODE:CELL<CH>:PRS:RSET<ST>:PER \n
		Sets the periodicity of the DL PRS allocation in slots for the given resource set. \n
			:param prs_rs_period: SL10240| SL5120| SL2560| SL1280| SL640| SL320| SL160| SL64| SL64| SL40| SL32| SL20| SL16| SL10| SL8| SL5| SL4
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rset')"""
		param = Conversions.enum_scalar_to_str(prs_rs_period, enums.PrsPeriodicity)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{channel_cmd_val}:PRS:RSET{stream_cmd_val}:PER {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> enums.PrsPeriodicity:
		"""[SOURce<HW>]:BB:NR5G:NODE:CELL<CH>:PRS:RSET<ST>:PER \n
		Sets the periodicity of the DL PRS allocation in slots for the given resource set. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rset')
			:return: prs_rs_period: SL10240| SL5120| SL2560| SL1280| SL640| SL320| SL160| SL64| SL64| SL40| SL32| SL20| SL16| SL10| SL8| SL5| SL4"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{channel_cmd_val}:PRS:RSET{stream_cmd_val}:PER?')
		return Conversions.str_to_scalar_enum(response, enums.PrsPeriodicity)
