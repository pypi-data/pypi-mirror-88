from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sonce:
	"""Sonce commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sonce", core, parent)

	def set(self, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:CORRection:CSET:DATA:[SENSor<CH>]:[POWer]:SONCe \n
		Fills the selected user correction table with the level values measured by the power sensor for the given frequencies. To
		select the used power sensor set the suffix in key word SENSe. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Data')"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:CORRection:CSET:DATA:SENSor{channel_cmd_val}:POWer:SONCe')

	def set_with_opc(self, channel=repcap.Channel.Default) -> None:
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		"""[SOURce<HW>]:CORRection:CSET:DATA:[SENSor<CH>]:[POWer]:SONCe \n
		Fills the selected user correction table with the level values measured by the power sensor for the given frequencies. To
		select the used power sensor set the suffix in key word SENSe. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Data')"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:CORRection:CSET:DATA:SENSor{channel_cmd_val}:POWer:SONCe')
