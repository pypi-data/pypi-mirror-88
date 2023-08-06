from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from ....Internal.Types import DataType
from ....Internal.ArgSingleList import ArgSingleList
from ....Internal.ArgSingle import ArgSingle
from .... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class State:
	"""State commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("state", core, parent)

	def set(self, state: bool, key: int = None, channel=repcap.Channel.Default) -> None:
		"""SYSTem:PROTect<CH>:[STATe] \n
		Activates and deactivates the specified protection level. \n
			:param state: 0| 1| OFF| ON
			:param key: integer The respective functions are disabled when the protection level is activated. No password is required for activation of a level. A password must be entered to deactivate the protection level. The default password for the first level is 123456. This protection level is required to unlock internal adjustments for example.
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Protect')"""
		param = ArgSingleList().compose_cmd_string(ArgSingle('state', state, DataType.Boolean), ArgSingle('key', key, DataType.Integer, True))
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SYSTem:PROTect{channel_cmd_val}:STATe {param}'.rstrip())

	def get(self, channel=repcap.Channel.Default) -> bool:
		"""SYSTem:PROTect<CH>:[STATe] \n
		Activates and deactivates the specified protection level. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Protect')
			:return: state: 0| 1| OFF| ON"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SYSTem:PROTect{channel_cmd_val}:STATe?')
		return Conversions.str_to_bool(response)
