from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums
from ....... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Count:
	"""Count commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("count", core, parent)

	def set(self, numb_of_basebands: enums.NumbOfBasebands, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:STReam<ST>:BB:COUNt \n
		No command help available \n
			:param numb_of_basebands: No help available
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Stream')"""
		param = Conversions.enum_scalar_to_str(numb_of_basebands, enums.NumbOfBasebands)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:STReam{stream_cmd_val}:BB:COUNt {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.NumbOfBasebands:
		"""[SOURce<HW>]:BB:GNSS:STReam<ST>:BB:COUNt \n
		No command help available \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Stream')
			:return: numb_of_basebands: No help available"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:STReam{stream_cmd_val}:BB:COUNt?')
		return Conversions.str_to_scalar_enum(response, enums.NumbOfBasebands)
