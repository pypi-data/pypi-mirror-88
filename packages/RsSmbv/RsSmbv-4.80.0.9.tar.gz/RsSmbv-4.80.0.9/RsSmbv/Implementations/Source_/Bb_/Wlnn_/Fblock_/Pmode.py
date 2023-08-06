from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ......Internal import Conversions
from ...... import enums
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pmode:
	"""Pmode commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pmode", core, parent)

	def set(self, pm_ode: enums.WlannFbPhyMode, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:PMODe \n
		Selects the preamble design. For physical type SOUNDING, only GREEN FIELD is available. \n
			:param pm_ode: LEGacy| MIXed| GFIeld LEGacy Compatible with 802.11 a/g OFDM devices. MIXed For High Throughput (HT) and 802.11a/g OFDM devices. GFIeld For HT only networks.
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')"""
		param = Conversions.enum_scalar_to_str(pm_ode, enums.WlannFbPhyMode)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:PMODe {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.WlannFbPhyMode:
		"""[SOURce<HW>]:BB:WLNN:FBLock<CH>:PMODe \n
		Selects the preamble design. For physical type SOUNDING, only GREEN FIELD is available. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Fblock')
			:return: pm_ode: LEGacy| MIXed| GFIeld LEGacy Compatible with 802.11 a/g OFDM devices. MIXed For High Throughput (HT) and 802.11a/g OFDM devices. GFIeld For HT only networks."""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:WLNN:FBLock{channel_cmd_val}:PMODe?')
		return Conversions.str_to_scalar_enum(response, enums.WlannFbPhyMode)
