from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TpState:
	"""TpState commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("tpState", core, parent)

	def set(self, tr_prec_state: bool, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:NR5G:NODE:CELL<CH>:DUMRes:TPSTate \n
		In uplink, enables using the optional DFT-S scheme. \n
			:param tr_prec_state: 0| 1| OFF| ON
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')"""
		param = Conversions.bool_to_str(tr_prec_state)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{channel_cmd_val}:DUMRes:TPSTate {param}')

	def get(self, channel=repcap.Channel.Default) -> bool:
		"""[SOURce<HW>]:BB:NR5G:NODE:CELL<CH>:DUMRes:TPSTate \n
		In uplink, enables using the optional DFT-S scheme. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:return: tr_prec_state: 0| 1| OFF| ON"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{channel_cmd_val}:DUMRes:TPSTate?')
		return Conversions.str_to_bool(response)
