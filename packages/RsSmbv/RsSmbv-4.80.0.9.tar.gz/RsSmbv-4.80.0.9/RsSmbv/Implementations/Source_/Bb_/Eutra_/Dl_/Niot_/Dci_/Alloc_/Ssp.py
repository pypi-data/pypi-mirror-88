from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ssp:
	"""Ssp commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ssp", core, parent)

	def set(self, search_space: enums.EutraSearchSpaceNbIoT, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:NIOT:DCI:ALLoc<CH>:SSP \n
		Sets the search space for the selected DCI. \n
			:param search_space: UE| T1CM| T2CM
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')"""
		param = Conversions.enum_scalar_to_str(search_space, enums.EutraSearchSpaceNbIoT)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:NIOT:DCI:ALLoc{channel_cmd_val}:SSP {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.EutraSearchSpaceNbIoT:
		"""[SOURce<HW>]:BB:EUTRa:DL:NIOT:DCI:ALLoc<CH>:SSP \n
		Sets the search space for the selected DCI. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Alloc')
			:return: search_space: UE| T1CM| T2CM"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:NIOT:DCI:ALLoc{channel_cmd_val}:SSP?')
		return Conversions.str_to_scalar_enum(response, enums.EutraSearchSpaceNbIoT)
