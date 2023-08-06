from ......Internal.Core import Core
from ......Internal.CommandsGroup import CommandsGroup
from ...... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Insert:
	"""Insert commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("insert", core, parent)

	def set(self, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:GBAS:VDB<CH>:INSert \n
		Inserts a new VDB before the selected one. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Vdb')"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:GBAS:VDB{channel_cmd_val}:INSert')

	def set_with_opc(self, channel=repcap.Channel.Default) -> None:
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		"""[SOURce<HW>]:BB:GBAS:VDB<CH>:INSert \n
		Inserts a new VDB before the selected one. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Vdb')"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:GBAS:VDB{channel_cmd_val}:INSert')
