from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Cbw:
	"""Cbw commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("cbw", core, parent)

	def set(self, lte_carrier_bw: enums.LteCrsCarrierBwAll, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:NR5G:NODE:CELL<CH>:LTE:CBW \n
		Sets the LTE bandwidth. \n
			:param lte_carrier_bw: N6| N15| N25| N50| N75| N100
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')"""
		param = Conversions.enum_scalar_to_str(lte_carrier_bw, enums.LteCrsCarrierBwAll)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{channel_cmd_val}:LTE:CBW {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.LteCrsCarrierBwAll:
		"""[SOURce<HW>]:BB:NR5G:NODE:CELL<CH>:LTE:CBW \n
		Sets the LTE bandwidth. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:return: lte_carrier_bw: N6| N15| N25| N50| N75| N100"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{channel_cmd_val}:LTE:CBW?')
		return Conversions.str_to_scalar_enum(response, enums.LteCrsCarrierBwAll)
