from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Sonce:
	"""Sonce commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("sonce", core, parent)

	def set(self, channel=repcap.Channel.Default) -> None:
		"""SENSe<CH>:[POWer]:FILTer:SONCe \n
		Starts searching the optimum filter length for the current measurement conditions. You can check the result with command
		method RsSmbv.Sense.Power.FilterPy.Length.User.set in filter mode USER (FILTer:TYPE) . \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sense')"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SENSe{channel_cmd_val}:POWer:FILTer:SONCe')

	def set_with_opc(self, channel=repcap.Channel.Default) -> None:
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		"""SENSe<CH>:[POWer]:FILTer:SONCe \n
		Starts searching the optimum filter length for the current measurement conditions. You can check the result with command
		method RsSmbv.Sense.Power.FilterPy.Length.User.set in filter mode USER (FILTer:TYPE) . \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Sense')"""
		self._core.io.write_with_opc(f'SENSe{channel_cmd_val}:POWer:FILTer:SONCe')
