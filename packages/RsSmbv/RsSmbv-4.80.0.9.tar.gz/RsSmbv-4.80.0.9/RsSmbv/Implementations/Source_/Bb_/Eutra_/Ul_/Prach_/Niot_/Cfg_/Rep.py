from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Rep:
	"""Rep commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("rep", core, parent)

	def set(self, repetitions: enums.EutraIotRepetitions, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:PRACh:NIOT:CFG<CH>:REP \n
		Queries the number of NPRACH repetitions per preamble attempt. \n
			:param repetitions: R1| R2| R4| R8| R16| R32| R64| R128 | R192| R256| R384| R512| R768| R1024| R1536| R2048| R12| R24
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cfg')"""
		param = Conversions.enum_scalar_to_str(repetitions, enums.EutraIotRepetitions)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:PRACh:NIOT:CFG{channel_cmd_val}:REP {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.EutraIotRepetitions:
		"""[SOURce<HW>]:BB:EUTRa:UL:PRACh:NIOT:CFG<CH>:REP \n
		Queries the number of NPRACH repetitions per preamble attempt. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cfg')
			:return: repetitions: R1| R2| R4| R8| R16| R32| R64| R128 | R192| R256| R384| R512| R768| R1024| R1536| R2048| R12| R24"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:PRACh:NIOT:CFG{channel_cmd_val}:REP?')
		return Conversions.str_to_scalar_enum(response, enums.EutraIotRepetitions)
