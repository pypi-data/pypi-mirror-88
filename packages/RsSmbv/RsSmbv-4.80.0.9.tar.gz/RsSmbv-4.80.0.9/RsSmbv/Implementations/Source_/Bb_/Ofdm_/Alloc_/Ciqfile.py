from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ......Internal.Utilities import trim_str_response
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ciqfile:
	"""Ciqfile commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ciqfile", core, parent)

	def set(self, custom_iq_file: str, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:OFDM:ALLoc<CH>:CIQFile \n
		Selects an existing file wit hcustom I/Q data from the default directory or from the specific directory.
		Refer to 'Accessing Files in the Default or Specified Directory' for general information on file handling in the default
		and in a specific directory. \n
			:param custom_iq_file: string Filename incl. file extension or complete file path
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')"""
		param = Conversions.value_to_quoted_str(custom_iq_file)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:OFDM:ALLoc{channel_cmd_val}:CIQFile {param}')

	def get(self, channel=repcap.Channel.Default) -> str:
		"""[SOURce<HW>]:BB:OFDM:ALLoc<CH>:CIQFile \n
		Selects an existing file wit hcustom I/Q data from the default directory or from the specific directory.
		Refer to 'Accessing Files in the Default or Specified Directory' for general information on file handling in the default
		and in a specific directory. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')
			:return: custom_iq_file: string Filename incl. file extension or complete file path"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:OFDM:ALLoc{channel_cmd_val}:CIQFile?')
		return trim_str_response(response)
