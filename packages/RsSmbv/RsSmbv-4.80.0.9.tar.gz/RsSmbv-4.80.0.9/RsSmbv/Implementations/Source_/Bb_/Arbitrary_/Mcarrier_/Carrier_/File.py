from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.Utilities import trim_str_response
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class File:
	"""File commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("file", core, parent)

	def set(self, file: str, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:ARBitrary:MCARrier:CARRier<CH>:FILE \n
		Selects the file with I/Q data to be modulated onto the selected carrier. \n
			:param file: file name
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Carrier')"""
		param = Conversions.value_to_quoted_str(file)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:MCARrier:CARRier{channel_cmd_val}:FILE {param}')

	def get(self, channel=repcap.Channel.Default) -> str:
		"""[SOURce<HW>]:BB:ARBitrary:MCARrier:CARRier<CH>:FILE \n
		Selects the file with I/Q data to be modulated onto the selected carrier. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Carrier')
			:return: file: file name"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:ARBitrary:MCARrier:CARRier{channel_cmd_val}:FILE?')
		return trim_str_response(response)
