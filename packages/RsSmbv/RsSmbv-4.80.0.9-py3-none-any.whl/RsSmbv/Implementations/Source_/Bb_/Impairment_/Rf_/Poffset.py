from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Poffset:
	"""Poffset commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("poffset", core, parent)

	def set(self, phase_offset: float, channel=repcap.Channel.Default) -> None:
		"""[SOURce]:BB:IMPairment:RF<CH>:POFFset \n
		Adds an additional phase offset after the stream mapper.
			INTRO_CMD_HELP: You can shift the phase at the different stages in the signal generation flow, see: \n
			- method RsSmbv.Source.Bb.poffset \n
			:param phase_offset: float Range: -999.99 to 999.99
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rf')"""
		param = Conversions.decimal_value_to_str(phase_offset)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce:BB:IMPairment:RF{channel_cmd_val}:POFFset {param}')

	def get(self, channel=repcap.Channel.Default) -> float:
		"""[SOURce]:BB:IMPairment:RF<CH>:POFFset \n
		Adds an additional phase offset after the stream mapper.
			INTRO_CMD_HELP: You can shift the phase at the different stages in the signal generation flow, see: \n
			- method RsSmbv.Source.Bb.poffset \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rf')
			:return: phase_offset: float Range: -999.99 to 999.99"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce:BB:IMPairment:RF{channel_cmd_val}:POFFset?')
		return Conversions.str_to_float(response)
