from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions
from ..... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Set:
	"""Set commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("set", core, parent)

	def set(self, ecount: int, channel=repcap.Channel.Default) -> None:
		"""DIAGnostic:INFO:ECOunt<CH>:SET \n
		No command help available \n
			:param ecount: No help available
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ecount')"""
		param = Conversions.decimal_value_to_str(ecount)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'DIAGnostic:INFO:ECOunt{channel_cmd_val}:SET {param}')
