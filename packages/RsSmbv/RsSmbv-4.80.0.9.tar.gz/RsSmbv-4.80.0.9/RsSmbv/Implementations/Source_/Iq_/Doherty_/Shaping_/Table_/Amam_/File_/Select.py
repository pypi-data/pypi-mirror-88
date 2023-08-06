from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from .........Internal.Utilities import trim_str_response
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Select:
	"""Select commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("select", core, parent)

	def set(self, filename: str, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:IQ:DOHerty<ST>:SHAPing:TABLe:AMAM:FILE:[SELect] \n
		No command help available \n
			:param filename: No help available
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Doherty')"""
		param = Conversions.value_to_quoted_str(filename)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:IQ:DOHerty{stream_cmd_val}:SHAPing:TABLe:AMAM:FILE:SELect {param}')

	def get(self, stream=repcap.Stream.Default) -> str:
		"""[SOURce<HW>]:IQ:DOHerty<ST>:SHAPing:TABLe:AMAM:FILE:[SELect] \n
		No command help available \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Doherty')
			:return: filename: No help available"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:IQ:DOHerty{stream_cmd_val}:SHAPing:TABLe:AMAM:FILE:SELect?')
		return trim_str_response(response)
