from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dfreq:
	"""Dfreq commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dfreq", core, parent)

	def set(self, delta_fto_dc: float, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:NR5G:NODE:CELL<CH>:DFReq \n
		Shifts the signal relative to the center output frequency. Use different frequency offsets to separate the channels of
		the configured and enabled cells. \n
			:param delta_fto_dc: float Range: -40E6 to 40E6
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')"""
		param = Conversions.decimal_value_to_str(delta_fto_dc)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{channel_cmd_val}:DFReq {param}')

	def get(self, channel=repcap.Channel.Default) -> float:
		"""[SOURce<HW>]:BB:NR5G:NODE:CELL<CH>:DFReq \n
		Shifts the signal relative to the center output frequency. Use different frequency offsets to separate the channels of
		the configured and enabled cells. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:return: delta_fto_dc: float Range: -40E6 to 40E6"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{channel_cmd_val}:DFReq?')
		return Conversions.str_to_float(response)
