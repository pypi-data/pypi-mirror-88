from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Pmodel:
	"""Pmodel commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("pmodel", core, parent)

	def set(self, model: enums.ObscPhysModel, stream=repcap.Stream.Default) -> None:
		"""[SOURce<HW>]:BB:GNSS:RECeiver:[V<ST>]:ENVironment:VOBS:PMODel \n
		Selects the physical effects to be simulated on the GNSS signal. \n
			:param model: OBSCuration| OMPath OBSCuration Simulates obscuration effects. OMPath Simulates obscuration and multipath propagation effects.
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')"""
		param = Conversions.enum_scalar_to_str(model, enums.ObscPhysModel)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		self._core.io.write(f'SOURce<HwInstance>:BB:GNSS:RECeiver:V{stream_cmd_val}:ENVironment:VOBS:PMODel {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default) -> enums.ObscPhysModel:
		"""[SOURce<HW>]:BB:GNSS:RECeiver:[V<ST>]:ENVironment:VOBS:PMODel \n
		Selects the physical effects to be simulated on the GNSS signal. \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'V')
			:return: model: No help available"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:GNSS:RECeiver:V{stream_cmd_val}:ENVironment:VOBS:PMODel?')
		return Conversions.str_to_scalar_enum(response, enums.ObscPhysModel)
