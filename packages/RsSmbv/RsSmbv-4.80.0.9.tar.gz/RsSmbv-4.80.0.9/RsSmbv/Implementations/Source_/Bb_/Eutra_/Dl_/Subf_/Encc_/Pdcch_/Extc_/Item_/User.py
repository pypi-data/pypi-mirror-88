from ...........Internal.Core import Core
from ...........Internal.CommandsGroup import CommandsGroup
from ...........Internal import Conversions
from ........... import enums
from ........... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class User:
	"""User commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("user", core, parent)

	def set(self, user: enums.EutraPdcchCfg, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:[SUBF<ST>]:ENCC:PDCCh:EXTC:ITEM<CH>:USER \n
		Selects the User the DCI is dedicated to. The available DCI Formats depend on the value of this parameter. \n
			:param user: USER1| USER2| USER3| USER4| PRNTi| SIRNti| RARNti| NONE | U1E| U2E| U3E| UE4 | CCNRti
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Item')"""
		param = Conversions.enum_scalar_to_str(user, enums.EutraPdcchCfg)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:SUBF{stream_cmd_val}:ENCC:PDCCh:EXTC:ITEM{channel_cmd_val}:USER {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default, channel=repcap.Channel.Default) -> enums.EutraPdcchCfg:
		"""[SOURce<HW>]:BB:EUTRa:DL:[SUBF<ST>]:ENCC:PDCCh:EXTC:ITEM<CH>:USER \n
		Selects the User the DCI is dedicated to. The available DCI Formats depend on the value of this parameter. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Subf')
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Item')
			:return: user: USER1| USER2| USER3| USER4| PRNTi| SIRNti| RARNti| NONE | U1E| U2E| U3E| UE4 | CCNRti"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:SUBF{stream_cmd_val}:ENCC:PDCCh:EXTC:ITEM{channel_cmd_val}:USER?')
		return Conversions.str_to_scalar_enum(response, enums.EutraPdcchCfg)
