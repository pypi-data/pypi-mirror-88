from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal.Utilities import trim_str_response
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class LogFile:
	"""LogFile commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("logFile", core, parent)

	def get(self, channel=repcap.Channel.Default) -> str:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:LOGFile \n
		Queries the fixed file path used for logging the contents of HE-SIG-A and HE-SIG-B fields, if method RsSmbv.Source.Bb.
		Wlnn.Fblock.Logging.set is set to ON. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:return: log_file: string"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:LOGFile?')
		return trim_str_response(response)
