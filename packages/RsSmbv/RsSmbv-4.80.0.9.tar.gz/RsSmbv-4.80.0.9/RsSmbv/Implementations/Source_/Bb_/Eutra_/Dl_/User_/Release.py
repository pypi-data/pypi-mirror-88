from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Release:
	"""Release commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("release", core, parent)

	def set(self, release: enums.EutraUeReleaseDl, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:USER<CH>:RELease \n
		Sets the 3GPP release version the UE supports. \n
			:param release: R89 | LADV | EM_A| NIOT| EM_B EM_A = eMTC CE: A and EM_B = eMTC CE: B
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')"""
		param = Conversions.enum_scalar_to_str(release, enums.EutraUeReleaseDl)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{channel_cmd_val}:RELease {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.EutraUeReleaseDl:
		"""[SOURce<HW>]:BB:EUTRa:DL:USER<CH>:RELease \n
		Sets the 3GPP release version the UE supports. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'User')
			:return: release: R89 | LADV | EM_A| NIOT| EM_B EM_A = eMTC CE: A and EM_B = eMTC CE: B"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:USER{channel_cmd_val}:RELease?')
		return Conversions.str_to_scalar_enum(response, enums.EutraUeReleaseDl)
