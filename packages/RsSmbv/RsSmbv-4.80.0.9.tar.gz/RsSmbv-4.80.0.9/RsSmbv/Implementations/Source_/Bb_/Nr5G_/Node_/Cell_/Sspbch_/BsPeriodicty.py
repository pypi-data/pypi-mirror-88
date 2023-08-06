from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class BsPeriodicty:
	"""BsPeriodicty commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("bsPeriodicty", core, parent)

	def set(self, burst_set_per: enums.Nr5Gbsp, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:NR5G:NODE:CELL<CH>:SSPBch<ST>:BSPeriodicty \n
		Sets the burst set periodicity. \n
			:param burst_set_per: BS5| BS10| BS20| BS40| BS80| BS160
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sspbch')"""
		param = Conversions.enum_scalar_to_str(burst_set_per, enums.Nr5Gbsp)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{channel_cmd_val}:SSPBch{stream_cmd_val}:BSPeriodicty {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default, stream=repcap.Stream.Default) -> enums.Nr5Gbsp:
		"""[SOURce<HW>]:BB:NR5G:NODE:CELL<CH>:SSPBch<ST>:BSPeriodicty \n
		Sets the burst set periodicity. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sspbch')
			:return: burst_set_per: BS5| BS10| BS20| BS40| BS80| BS160"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{channel_cmd_val}:SSPBch{stream_cmd_val}:BSPeriodicty?')
		return Conversions.str_to_scalar_enum(response, enums.Nr5Gbsp)
