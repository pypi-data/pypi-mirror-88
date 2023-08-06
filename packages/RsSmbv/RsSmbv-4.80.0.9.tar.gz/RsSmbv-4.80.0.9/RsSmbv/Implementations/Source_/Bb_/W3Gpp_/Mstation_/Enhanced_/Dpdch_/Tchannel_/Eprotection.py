from .........Internal.Core import Core
from .........Internal.CommandsGroup import CommandsGroup
from .........Internal import Conversions
from ......... import enums
from ......... import repcap


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Eprotection:
	"""Eprotection commands group definition. 1 total commands, 0 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("eprotection", core, parent)

	def set(self, eprotection: enums.EnhTchErr, transportChannel=repcap.TransportChannel.Default) -> None:
		"""[SOURce<HW>]:BB:W3GPp:MSTation:ENHanced:DPDCh:TCHannel<DI>:EPRotection \n
		The command determines the error protection. \n
			:param eprotection: NONE| CON2| CON3| TURBo3 NONE No error protection. TURBo3 Turbo Coder of rate 1/3 in accordance with the 3GPP specifications. CON2 | CON3 Convolution Coder of rate ½ or 1/3 with generator polynomials defined by 3GPP.
			:param transportChannel: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Tchannel')"""
		param = Conversions.enum_scalar_to_str(eprotection, enums.EnhTchErr)
		transportChannel_cmd_val = self._base.get_repcap_cmd_value(transportChannel, repcap.TransportChannel)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation:ENHanced:DPDCh:TCHannel{transportChannel_cmd_val}:EPRotection {param}')

	# noinspection PyTypeChecker
	def get(self, transportChannel=repcap.TransportChannel.Default) -> enums.EnhTchErr:
		"""[SOURce<HW>]:BB:W3GPp:MSTation:ENHanced:DPDCh:TCHannel<DI>:EPRotection \n
		The command determines the error protection. \n
			:param transportChannel: optional repeated capability selector. Default value: Nr0 (settable in the interface 'Tchannel')
			:return: eprotection: NONE| CON2| CON3| TURBo3 NONE No error protection. TURBo3 Turbo Coder of rate 1/3 in accordance with the 3GPP specifications. CON2 | CON3 Convolution Coder of rate ½ or 1/3 with generator polynomials defined by 3GPP."""
		transportChannel_cmd_val = self._base.get_repcap_cmd_value(transportChannel, repcap.TransportChannel)
		response = self._core.io.query_str(f'SOURce<HwInstance>:BB:W3GPp:MSTation:ENHanced:DPDCh:TCHannel{transportChannel_cmd_val}:EPRotection?')
		return Conversions.str_to_scalar_enum(response, enums.EnhTchErr)
