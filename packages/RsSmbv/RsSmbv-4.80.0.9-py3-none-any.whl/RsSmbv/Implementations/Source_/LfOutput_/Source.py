from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Source:
	"""Source commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("source", core, parent)

	def set(self, source: enums.LfSource, channel=repcap.Channel.Default) -> None:
		"""[SOURce]:LFOutput<CH>:SOURce \n
		Determines the LF signal to be synchronized, when monitoring is enabled. \n
			:param source: LF1| LF2| NOISe| AM| FMPM| EXT1 LF1|LF2 Selects an internally generated LF signal. NOISe Selects an internally generated noise signal. EXT1 Selects an externally supplied LF signal AM Selects the AM signal. FMPM Selects the signal also used by the frequency or phase modulations.
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'LfOutput')"""
		param = Conversions.enum_scalar_to_str(source, enums.LfSource)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce:LFOutput{channel_cmd_val}:SOURce {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.LfSource:
		"""[SOURce]:LFOutput<CH>:SOURce \n
		Determines the LF signal to be synchronized, when monitoring is enabled. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'LfOutput')
			:return: source: LF1| LF2| NOISe| AM| FMPM| EXT1 LF1|LF2 Selects an internally generated LF signal. NOISe Selects an internally generated noise signal. EXT1 Selects an externally supplied LF signal AM Selects the AM signal. FMPM Selects the signal also used by the frequency or phase modulations."""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce:LFOutput{channel_cmd_val}:SOURce?')
		return Conversions.str_to_scalar_enum(response, enums.LfSource)
