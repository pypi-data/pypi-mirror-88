from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Slot:
	"""Slot commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("slot", core, parent)

	def set(self, slot: int, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:GSM:TRIGger:OUTPut<CH>:PERiod:SLOT \n
		Sets the repetition rate for the slot clock at the marker outputs. \n
			:param slot: integer Range: 1 to 8
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')"""
		param = Conversions.decimal_value_to_str(slot)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:GSM:TRIGger:OUTPut{channel_cmd_val}:PERiod:SLOT {param}')

	def get(self, channel=repcap.Channel.Default) -> int:
		"""[SOURce<HW>]:BB:GSM:TRIGger:OUTPut<CH>:PERiod:SLOT \n
		Sets the repetition rate for the slot clock at the marker outputs. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')
			:return: slot: integer Range: 1 to 8"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GSM:TRIGger:OUTPut{channel_cmd_val}:PERiod:SLOT?')
		return Conversions.str_to_int(response)
