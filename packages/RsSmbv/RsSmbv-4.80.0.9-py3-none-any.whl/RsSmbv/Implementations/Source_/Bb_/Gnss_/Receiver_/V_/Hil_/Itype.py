from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums
from ........ import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Itype:
	"""Itype commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("itype", core, parent)

	def set(self, interface_type: enums.HilIfc, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:RECeiver:[V<ST>]:HIL:ITYPe \n
		Set the interface type for the remote communication between R&S SMBV100B and the master application. \n
			:param interface_type: SCPI| UDP
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')"""
		param = Conversions.enum_scalar_to_str(interface_type, enums.HilIfc)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:RECeiver:V{stream_cmd_val}:HIL:ITYPe {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.HilIfc:
		"""[SOURce<HW>]:BB:GNSS:RECeiver:[V<ST>]:HIL:ITYPe \n
		Set the interface type for the remote communication between R&S SMBV100B and the master application. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')
			:return: interface_type: SCPI| UDP"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:RECeiver:V{stream_cmd_val}:HIL:ITYPe?')
		return Conversions.str_to_scalar_enum(response, enums.HilIfc)
