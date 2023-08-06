from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Store:
	"""Store commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("store", core, parent)

	def set(self, filename: str, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:IQ:DOHerty<ST>:SHAPing:NORMalized:DATA:STORe \n
		No command help available \n
			:param filename: No help available
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Doherty')"""
		param = Conversions.value_to_quoted_str(filename)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:IQ:DOHerty{stream_cmd_val}:SHAPing:NORMalized:DATA:STORe {param}')
