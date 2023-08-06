from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Phase:
	"""Phase commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("phase", core, parent)

	def set(self, phase: float, channel=repcap.Channel.Default) -> None:
		"""[SOURce<HW>]:BB:ARBitrary:MCARrier:CARRier<CH>:PHASe \n
		Sets the start phase of the selected carrier. \n
			:param phase: float Range: 0 to 359.99, Unit: DEG
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Carrier')"""
		param = Conversions.decimal_value_to_str(phase)
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		self._core.io.write(f'SOURce<HwInstance>:BB:ARBitrary:MCARrier:CARRier{channel_cmd_val}:PHASe {param}')

	def get(self, channel=repcap.Channel.Default) -> float:
		"""[SOURce<HW>]:BB:ARBitrary:MCARrier:CARRier<CH>:PHASe \n
		Sets the start phase of the selected carrier. \n
			:param channel: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Carrier')
			:return: phase: float Range: 0 to 359.99, Unit: DEG"""
		channel_cmd_val = self._base.get_repcap_cmd_value(channel, repcap.Channel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:ARBitrary:MCARrier:CARRier{channel_cmd_val}:PHASe?')
		return Conversions.str_to_float(response)
