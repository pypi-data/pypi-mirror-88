from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class All:
	"""All commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("all", core, parent)

	def set(self, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:ATMospheric:IONospheric:MOPS:IMPort<ST>:REMove:ALL \n
		Remove all or one particular file at the n-th position from an import file list. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'ImportPy')"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:ATMospheric:IONospheric:MOPS:IMPort{stream_cmd_val}:REMove:ALL')

	def set_with_opc(self, stream=repcap.Stream.Default) -> None:
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		"""[SOURce<HW>]:BB:GNSS:ATMospheric:IONospheric:MOPS:IMPort<ST>:REMove:ALL \n
		Remove all or one particular file at the n-th position from an import file list. \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'ImportPy')"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:GNSS:ATMospheric:IONospheric:MOPS:IMPort{stream_cmd_val}:REMove:ALL')
