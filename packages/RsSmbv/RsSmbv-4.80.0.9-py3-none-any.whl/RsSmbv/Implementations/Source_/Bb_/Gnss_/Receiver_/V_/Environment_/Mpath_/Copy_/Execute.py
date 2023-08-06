from ..........Internal.Core import Core
from ..........Internal.CommandsGroup import CommandsGroup
from .......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Execute:
	"""Execute commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("execute", core, parent)

	def set(self, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:RECeiver:[V<ST>]:ENVironment:MPATh:COPY:EXECute \n
		Copies the multipath configuration of the source GNSS System and SV ID to the target SV ID and GNSS system or to all SV
		IDs from a system.
			INTRO_CMD_HELP: Set the source with: \n
			- BB:GNSS:ENVironment:MPATh:SYSTem
			- BB:GNSS:ENVironment:MPATh:SVID
			INTRO_CMD_HELP: Set the target with: \n
			- BB:GNSS:ENVironment:MPATh:COPY:SYSTem
			- BB:GNSS:ENVironment:MPATh:COPY:SVID \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:RECeiver:V{stream_cmd_val}:ENVironment:MPATh:COPY:EXECute')

	def set_with_opc(self, stream=repcap.Stream.Default) -> None:
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		"""[SOURce<HW>]:BB:GNSS:RECeiver:[V<ST>]:ENVironment:MPATh:COPY:EXECute \n
		Copies the multipath configuration of the source GNSS System and SV ID to the target SV ID and GNSS system or to all SV
		IDs from a system.
			INTRO_CMD_HELP: Set the source with: \n
			- BB:GNSS:ENVironment:MPATh:SYSTem
			- BB:GNSS:ENVironment:MPATh:SVID
			INTRO_CMD_HELP: Set the target with: \n
			- BB:GNSS:ENVironment:MPATh:COPY:SYSTem
			- BB:GNSS:ENVironment:MPATh:COPY:SVID \n
		Same as set, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:GNSS:RECeiver:V{stream_cmd_val}:ENVironment:MPATh:COPY:EXECute')
