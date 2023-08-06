from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from ..........Internal import Conversions
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dir:
	"""Dir commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dir", core, parent)

	def set(self, directory: str, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:ATMospheric:IONospheric:MOPS:IMPort<ST>:ADD:DIR \n
		Adds a set of files to the input files selection in one step. \n
			:param directory: string File path
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'ImportPy')"""
		param = Conversions.value_to_quoted_str(directory)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:ATMospheric:IONospheric:MOPS:IMPort{stream_cmd_val}:ADD:DIR {param}')
