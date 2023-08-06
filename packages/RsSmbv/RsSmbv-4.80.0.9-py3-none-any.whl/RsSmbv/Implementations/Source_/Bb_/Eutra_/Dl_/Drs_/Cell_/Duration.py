from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Duration:
	"""Duration commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("duration", core, parent)

	def set(self, drs_duration: enums.EutraDrsDuration, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:DL:DRS:CELL<CH>:DURation \n
		Sets the DRS duration. \n
			:param drs_duration: DUR1| DUR2| DUR3| DUR4| DUR5 DUR1 For LAA SCells, the DRS is always 1 ms long DUR2|DUR3|DUR4|DUR5 In FDD mode, sets duration of 2 ms to 5 ms
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')"""
		param = Conversions.enum_scalar_to_str(drs_duration, enums.EutraDrsDuration)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:DL:DRS:CELL{channel_cmd_val}:DURation {param}')

	# noinspection PyTypeChecker
	def get(self, channel=repcap.Channel.Default) -> enums.EutraDrsDuration:
		"""[SOURce<HW>]:BB:EUTRa:DL:DRS:CELL<CH>:DURation \n
		Sets the DRS duration. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:return: drs_duration: DUR1| DUR2| DUR3| DUR4| DUR5 DUR1 For LAA SCells, the DRS is always 1 ms long DUR2|DUR3|DUR4|DUR5 In FDD mode, sets duration of 2 ms to 5 ms"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:DL:DRS:CELL{channel_cmd_val}:DURation?')
		return Conversions.str_to_scalar_enum(response, enums.EutraDrsDuration)
