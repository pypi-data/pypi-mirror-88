from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class TypePy:
	"""TypePy commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("typePy", core, parent)

	def set(self, type_py: enums.EutraUlFrc, stream=repcap.Stream.Default, carrierComponent=repcap.CarrierComponent.Default) -> None:
		"""[SOURce<HW>]:BB:EUTRa:UL:UE<ST>:[CELL<CCIDX>]:FRC:TYPE \n
		Selects a predefined fixed reference channel according to and . \n
			:param type_py: A11| A12| A13| A14| A15| A21| A22| A23| A31| A32| A33| A34| A35| A36| A37| A41| A42| A43| A44| A45| A46| A47| A48| A51| A52| A53| A54| A55| A56| A57| A71| A72| A73| A74| A75| A76| A81| A82| A83| A84| A85| A86| UE11| UE12| UE21| UE22| UE3| A16| A17| A121| A122| A123| A124| A125| A126| A131| A132| A133| A134| A135| A136 | A171| A172| A173| A174| A175| A176| A181| A182| A183| A184| A185| A186| A191| A192| A193| A194| A195| A196
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')"""
		param = Conversions.enum_scalar_to_str(type_py, enums.EutraUlFrc)
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		carrierComponent_cmd_val = self._base.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		self._core.io.write(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:CELL{carrierComponent_cmd_val}:FRC:TYPE {param}')

	# noinspection PyTypeChecker
	def get(self, stream=repcap.Stream.Default, carrierComponent=repcap.CarrierComponent.Default) -> enums.EutraUlFrc:
		"""[SOURce<HW>]:BB:EUTRa:UL:UE<ST>:[CELL<CCIDX>]:FRC:TYPE \n
		Selects a predefined fixed reference channel according to and . \n
			:param stream: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Ue')
			:param carrierComponent: optional repeated capability selector. Default value: Nr1 (settable in the interface 'Cell')
			:return: type_py: A11| A12| A13| A14| A15| A21| A22| A23| A31| A32| A33| A34| A35| A36| A37| A41| A42| A43| A44| A45| A46| A47| A48| A51| A52| A53| A54| A55| A56| A57| A71| A72| A73| A74| A75| A76| A81| A82| A83| A84| A85| A86| UE11| UE12| UE21| UE22| UE3| A16| A17| A121| A122| A123| A124| A125| A126| A131| A132| A133| A134| A135| A136 | A171| A172| A173| A174| A175| A176| A181| A182| A183| A184| A185| A186| A191| A192| A193| A194| A195| A196"""
		stream_cmd_val = self._base.get_repcap_cmd_value(stream, repcap.Stream)
		carrierComponent_cmd_val = self._base.get_repcap_cmd_value(carrierComponent, repcap.CarrierComponent)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:EUTRa:UL:UE{stream_cmd_val}:CELL{carrierComponent_cmd_val}:FRC:TYPE?')
		return Conversions.str_to_scalar_enum(response, enums.EutraUlFrc)
