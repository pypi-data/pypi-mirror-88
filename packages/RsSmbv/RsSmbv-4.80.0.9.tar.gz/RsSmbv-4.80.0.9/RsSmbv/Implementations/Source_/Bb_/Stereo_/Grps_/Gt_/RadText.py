from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from .......Internal.Utilities import trim_str_response
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class RadText:
	"""RadText commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("radText", core, parent)

	def set(self, rad_text: str, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:STEReo:GRPS:GT<ST>:RADText \n
		No command help available \n
			:param rad_text: No help available
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gt')"""
		param = Conversions.value_to_quoted_str(rad_text)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:STEReo:GRPS:GT{stream_cmd_val}:RADText {param}')

	def get(self, stream=repcap.Stream.Default) -> str:
		"""[SOURce<HW>]:BB:STEReo:GRPS:GT<ST>:RADText \n
		No command help available \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Gt')
			:return: rad_text: No help available"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:STEReo:GRPS:GT{stream_cmd_val}:RADText?')
		return trim_str_response(response)
