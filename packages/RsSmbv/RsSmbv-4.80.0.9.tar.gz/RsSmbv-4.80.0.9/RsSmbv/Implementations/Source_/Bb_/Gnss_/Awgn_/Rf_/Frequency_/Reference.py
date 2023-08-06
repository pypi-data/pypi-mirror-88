from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Reference:
	"""Reference commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("reference", core, parent)

	def get(self, channel=repcap.Channel.Default) -> int:
		"""[SOURce<HW>]:BB:GNSS:AWGN:[RF<CH>]:FREQuency:REFerence \n
		Queries the reference frequency, that is the RF carrier frequency. Set the freqquency with the following remote command:
		SOURce1:FREQuency \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Rf')
			:return: reference_freque: integer Range: 1E9 to 2E9"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:AWGN:RF{channel_cmd_val}:FREQuency:REFerence?')
		return Conversions.str_to_int(response)
