from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Slength:
	"""Slength commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("slength", core, parent)

	def set(self, slot_length: enums.QuickSetSlotLenAll, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:NR5G:TRIGger:OUTPut<CH>:SLENgth \n
		Sets the duration of a UL/DL pattern containing a marker. \n
			:param slot_length: S5| S10 S5 Sets the duration of the UL/DL pattern to 5 slots. S10 Sets the duration of the UL/DL pattern to 10 slots.
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')"""
		param = Conversions.enum_scalar_to_str(slot_length, enums.QuickSetSlotLenAll)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:TRIGger:OUTPut{channel_cmd_val}:SLENgth {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.QuickSetSlotLenAll:
		"""[SOURce<HW>]:BB:NR5G:TRIGger:OUTPut<CH>:SLENgth \n
		Sets the duration of a UL/DL pattern containing a marker. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Output')
			:return: slot_length: S5| S10 S5 Sets the duration of the UL/DL pattern to 5 slots. S10 Sets the duration of the UL/DL pattern to 10 slots."""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:NR5G:TRIGger:OUTPut{channel_cmd_val}:SLENgth?')
		return Conversions.str_to_scalar_enum(response, enums.QuickSetSlotLenAll)
