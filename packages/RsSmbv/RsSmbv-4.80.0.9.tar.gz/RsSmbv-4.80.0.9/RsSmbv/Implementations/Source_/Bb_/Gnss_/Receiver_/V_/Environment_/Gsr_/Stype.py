from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Stype:
	"""Stype commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("stype", core, parent)

	def set(self, surface_type: enums.ReflMaterial, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:RECeiver:[V<ST>]:ENVironment:GSR:STYPe \n
		Defines the type of surface. \n
			:param surface_type: SEA| WATER| WET| MDRY| DRY| USER
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')"""
		param = Conversions.enum_scalar_to_str(surface_type, enums.ReflMaterial)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:RECeiver:V{stream_cmd_val}:ENVironment:GSR:STYPe {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.ReflMaterial:
		"""[SOURce<HW>]:BB:GNSS:RECeiver:[V<ST>]:ENVironment:GSR:STYPe \n
		Defines the type of surface. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')
			:return: surface_type: SEA| WATER| WET| MDRY| DRY| USER"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:RECeiver:V{stream_cmd_val}:ENVironment:GSR:STYPe?')
		return Conversions.str_to_scalar_enum(response, enums.ReflMaterial)
