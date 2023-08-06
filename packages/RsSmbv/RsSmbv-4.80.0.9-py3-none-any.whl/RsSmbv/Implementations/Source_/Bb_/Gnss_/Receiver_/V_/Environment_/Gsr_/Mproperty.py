from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Mproperty:
	"""Mproperty commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("mproperty", core, parent)

	def set(self, material_propert: enums.MatProp, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:RECeiver:[V<ST>]:ENVironment:GSR:MPRoperty \n
		Specifies, if the material is defined by its permittivity/conductivity or by its power loss characteristic. \n
			:param material_propert: PLOSS| PERM
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')"""
		param = Conversions.enum_scalar_to_str(material_propert, enums.MatProp)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:RECeiver:V{stream_cmd_val}:ENVironment:GSR:MPRoperty {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.MatProp:
		"""[SOURce<HW>]:BB:GNSS:RECeiver:[V<ST>]:ENVironment:GSR:MPRoperty \n
		Specifies, if the material is defined by its permittivity/conductivity or by its power loss characteristic. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')
			:return: material_propert: PLOSS| PERM"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:RECeiver:V{stream_cmd_val}:ENVironment:GSR:MPRoperty?')
		return Conversions.str_to_scalar_enum(response, enums.MatProp)
