from ........Internal.Core import Core
from ........Internal.CommandsGroup import CommandsGroup
from ........Internal import Conversions
from ........ import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ccoding:
	"""Ccoding commands group definition. 6 total commands, 1 Sub-groups, 2 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ccoding", core, parent)

	def clone(self) -> 'Ccoding':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Ccoding(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def user(self):
		"""user commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_user'):
			from .Ccoding_.User import User
			self._user = User(self._core, self._base)
		return self._user

	def get_state(self) -> bool:
		"""[SOURce<HW>]:BB:W3GPp:MSTation:ENHanced:DPDCh:CCODing:STATe \n
		The command activates or deactivates channel coding for the enhanced channels. When channel coding is activated, the
		overall symbol rate (method RsSmbv.Source.Bb.W3Gpp.Mstation.Enhanced.Dpdch.orate) is set to the value predetermined by
		the selected channel coding type (method RsSmbv.Source.Bb.W3Gpp.Mstation.Enhanced.Dpdch.Ccoding.typePy) . \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:W3GPp:MSTation:ENHanced:DPDCh:CCODing:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""[SOURce<HW>]:BB:W3GPp:MSTation:ENHanced:DPDCh:CCODing:STATe \n
		The command activates or deactivates channel coding for the enhanced channels. When channel coding is activated, the
		overall symbol rate (method RsSmbv.Source.Bb.W3Gpp.Mstation.Enhanced.Dpdch.orate) is set to the value predetermined by
		the selected channel coding type (method RsSmbv.Source.Bb.W3Gpp.Mstation.Enhanced.Dpdch.Ccoding.typePy) . \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation:ENHanced:DPDCh:CCODing:STATe {param}')

	# noinspection PyTypeChecker
	def get_type_py(self) -> enums.ChanCodType:
		"""[SOURce<HW>]:BB:W3GPp:MSTation:ENHanced:DPDCh:CCODing:TYPE \n
		The command selects the channel coding scheme in accordance with the 3GPP specification. The channel coding scheme
		selected predetermines the overall symbol rate. When channel coding is activated (method RsSmbv.Source.Bb.W3Gpp.Mstation.
		Enhanced.Dpdch.Ccoding.state) the overall symbol rate (method RsSmbv.Source.Bb.W3Gpp.Mstation.Enhanced.Dpdch.orate) is
		set to the value predetermined by the selected channel coding type. \n
			:return: type_py: M12K2| M64K| M144k| M384k| AMR M12K2 Measurement channel with an input data bit rate of 12.2 ksps. M64K Measurement channel with an input data bit rate of 64 ksps. M144K Measurement channel with an input data bit rate of 144 ksps. M384K Measurement channel with an input data bit rate of 384 ksps. AMR Channel coding for the AMR Coder (coding a voice channel) . USER This parameter cannot be set. USER is returned whenever a user-defined channel coding is active, that is to say, after a channel coding parameter has been changed or a user coding file has been loaded. The file is loaded by the command method RsSmbv.Source.Bb.W3Gpp.Mstation.Enhanced.Dpdch.Ccoding.User.load.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:W3GPp:MSTation:ENHanced:DPDCh:CCODing:TYPE?')
		return Conversions.str_to_scalar_enum(response, enums.ChanCodType)

	def set_type_py(self, type_py: enums.ChanCodType) -> None:
		"""[SOURce<HW>]:BB:W3GPp:MSTation:ENHanced:DPDCh:CCODing:TYPE \n
		The command selects the channel coding scheme in accordance with the 3GPP specification. The channel coding scheme
		selected predetermines the overall symbol rate. When channel coding is activated (method RsSmbv.Source.Bb.W3Gpp.Mstation.
		Enhanced.Dpdch.Ccoding.state) the overall symbol rate (method RsSmbv.Source.Bb.W3Gpp.Mstation.Enhanced.Dpdch.orate) is
		set to the value predetermined by the selected channel coding type. \n
			:param type_py: M12K2| M64K| M144k| M384k| AMR M12K2 Measurement channel with an input data bit rate of 12.2 ksps. M64K Measurement channel with an input data bit rate of 64 ksps. M144K Measurement channel with an input data bit rate of 144 ksps. M384K Measurement channel with an input data bit rate of 384 ksps. AMR Channel coding for the AMR Coder (coding a voice channel) . USER This parameter cannot be set. USER is returned whenever a user-defined channel coding is active, that is to say, after a channel coding parameter has been changed or a user coding file has been loaded. The file is loaded by the command method RsSmbv.Source.Bb.W3Gpp.Mstation.Enhanced.Dpdch.Ccoding.User.load.
		"""
		param = Conversions.enum_scalar_to_str(type_py, enums.ChanCodType)
		self._core.io.write(f'SOURce<HwInstance>:BB:W3GPp:MSTation:ENHanced:DPDCh:CCODing:TYPE {param}')
