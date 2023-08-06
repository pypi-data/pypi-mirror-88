from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class CfOffset:
	"""CfOffset commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("cfOffset", core, parent)

	def set(self, cf_offset: int, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:BTOoth:DTTest:TABLe:SHORt:SET<CH>:CFOFfset \n
		Sets a carrier frequency offset. The carrier frequency offset shows the deviation of the transmitted initial center
		frequency from carrier frequency. \n
			:param cf_offset: integer Range: -150 to 150, Unit: kHz
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Set')"""
		param = Conversions.decimal_value_to_str(cf_offset)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:BTOoth:DTTest:TABLe:SHORt:SET{channel_cmd_val}:CFOFfset {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""[SOURce<HW>]:BB:BTOoth:DTTest:TABLe:SHORt:SET<CH>:CFOFfset \n
		Sets a carrier frequency offset. The carrier frequency offset shows the deviation of the transmitted initial center
		frequency from carrier frequency. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Set')
			:return: cf_offset: integer Range: -150 to 150, Unit: kHz"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:BTOoth:DTTest:TABLe:SHORt:SET{channel_cmd_val}:CFOFfset?')
		return Conversions.str_to_int(response)
