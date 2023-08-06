from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Nap:
	"""Nap commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("nap", core, parent)

	def set(self, lte_antenna_ports: enums.NumberOfPorts, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:NR5G:NODE:CELL<CH>:LTE:NAP \n
		Sets the number of antenna ports used for LTE-CRS. \n
			:param lte_antenna_ports: AP1| AP2| AP4
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')"""
		param = Conversions.enum_scalar_to_str(lte_antenna_ports, enums.NumberOfPorts)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{channel_cmd_val}:LTE:NAP {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.NumberOfPorts:
		"""[SOURce<HW>]:BB:NR5G:NODE:CELL<CH>:LTE:NAP \n
		Sets the number of antenna ports used for LTE-CRS. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:return: lte_antenna_ports: AP1| AP2| AP4"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:NODE:CELL{channel_cmd_val}:LTE:NAP?')
		return Conversions.str_to_scalar_enum(response, enums.NumberOfPorts)
