from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CfgType:
	"""CfgType commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("cfgType", core, parent)

	def set(self, conf_type: enums.NfcConfigType, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:NFC:CBLock<CH>:CFGType \n
		Determines what platform or protocol the device in listen mode is configured for. \n
			:param conf_type: T2| T4A| NDEP| DT4A| OFF| 0| ON| 1
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')"""
		param = Conversions.enum_scalar_to_str(conf_type, enums.NfcConfigType)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:NFC:CBLock{channel_cmd_val}:CFGType {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.NfcConfigType:
		"""[SOURce<HW>]:BB:NFC:CBLock<CH>:CFGType \n
		Determines what platform or protocol the device in listen mode is configured for. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cblock')
			:return: conf_type: T2| T4A| NDEP| DT4A| OFF| 0| ON| 1"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NFC:CBLock{channel_cmd_val}:CFGType?')
		return Conversions.str_to_scalar_enum(response, enums.NfcConfigType)
