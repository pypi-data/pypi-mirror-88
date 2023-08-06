from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Immediate:
	"""Immediate commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("immediate", core, parent)

	def set(self, channel=repcap.Channel.Default) -> None:
		"""OUTPut<HW>:USER<CH>:TRIGger:[IMMediate] \n
		Generates a short pulse signal and outputs it at the User connector. This signal can serve as a common external trigger
		signal for triggering of several R&S SMBV100B, see Example 'Triggering several R&S SMBV100B instruments simultaneously'. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'OUTPut<HwInstance>:USER{channel_cmd_val}:TRIGger:IMMediate')

	def set_with_opc(self, channel=repcap.Channel.Default) -> None:
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		"""OUTPut<HW>:USER<CH>:TRIGger:[IMMediate] \n
		Generates a short pulse signal and outputs it at the User connector. This signal can serve as a common external trigger
		signal for triggering of several R&S SMBV100B, see Example 'Triggering several R&S SMBV100B instruments simultaneously'. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')"""
		self._core.io.write_with_opc(f'OUTPut<HwInstance>:USER{channel_cmd_val}:TRIGger:IMMediate')
