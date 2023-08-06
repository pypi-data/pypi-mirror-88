from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Source:
	"""Source commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("source", core, parent)

	def set(self, source: enums.BboutClocSour, channel=repcap.Channel.Default) -> None:
		"""[SOURce]:IQ:OUTPut:DIGital:BBMM<CH>:SRATe:SOURce \n
		No command help available \n
			:param source: No help available
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bbmm')"""
		param = Conversions.enum_scalar_to_str(source, enums.BboutClocSour)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce:IQ:OUTPut:DIGital:BBMM{channel_cmd_val}:SRATe:SOURce {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.BboutClocSour:
		"""[SOURce]:IQ:OUTPut:DIGital:BBMM<CH>:SRATe:SOURce \n
		No command help available \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Bbmm')
			:return: source: No help available"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce:IQ:OUTPut:DIGital:BBMM{channel_cmd_val}:SRATe:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.BboutClocSour)
