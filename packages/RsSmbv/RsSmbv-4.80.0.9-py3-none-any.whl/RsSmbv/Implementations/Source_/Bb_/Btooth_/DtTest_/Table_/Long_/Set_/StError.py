from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class StError:
	"""StError commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("stError", core, parent)

	def set(self, st_error: int, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:BTOoth:DTTest:TABLe:LONG:SET<CH>:STERror \n
		Sets a symbol timing error in ppm. This parameter modifies the symbol clock frequency by the set value. \n
			:param st_error: integer Range: -150 to 150, Unit: ppm
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Set')"""
		param = Conversions.decimal_value_to_str(st_error)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:DTTest:TABLe:LONG:SET{channel_cmd_val}:STERror {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""[SOURce<HW>]:BB:BTOoth:DTTest:TABLe:LONG:SET<CH>:STERror \n
		Sets a symbol timing error in ppm. This parameter modifies the symbol clock frequency by the set value. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Set')
			:return: st_error: integer Range: -150 to 150, Unit: ppm"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:BTOoth:DTTest:TABLe:LONG:SET{channel_cmd_val}:STERror?')
		return Conversions.str_to_int(response)
