from .......Internal.Core import Core
from .......Internal.CommandsGroup import CommandsGroup
from .......Internal import Conversions
from ....... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Es:
	"""Es commands group definition. 7 total commands, 2 Sub-groups, 5 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("es", core, parent)

	def clone(self) -> 'Es':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Es(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def cs(self):
		"""cs commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_cs'):
			from .Es_.Cs import Cs
			self._cs = Cs(self._core, self._base)
		return self._cs

	@property
	def tp(self):
		"""tp commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_tp'):
			from .Es_.Tp import Tp
			self._tp = Tp(self._core, self._base)
		return self._tp

	def get_cs_length(self) -> int:
		"""[SOURce<HW>]:BB:NR5G:QCKSet:GENeral:ES:CSLength \n
		Sets the number of symbols in the CORESET. \n
			:return: qck_set_corset_len: integer Range: 1 to 3
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:QCKSet:GENeral:ES:CSLength?')
		return Conversions.str_to_int(response)

	def set_cs_length(self, qck_set_corset_len: int) -> None:
		"""[SOURce<HW>]:BB:NR5G:QCKSet:GENeral:ES:CSLength \n
		Sets the number of symbols in the CORESET. \n
			:param qck_set_corset_len: integer Range: 1 to 3
		"""
		param = Conversions.decimal_value_to_str(qck_set_corset_len)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:QCKSet:GENeral:ES:CSLength {param}')

	# noinspection PyTypeChecker
	def get_mod(self) -> enums.ModulationB:
		"""[SOURce<HW>]:BB:NR5G:QCKSet:GENeral:ES:MOD \n
		Sets the modulation scheme. \n
			:return: qck_set_mod_type: QPSK| QAM16| QAM64| QAM256
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:QCKSet:GENeral:ES:MOD?')
		return Conversions.str_to_scalar_enum(response, enums.ModulationB)

	def set_mod(self, qck_set_mod_type: enums.ModulationB) -> None:
		"""[SOURce<HW>]:BB:NR5G:QCKSet:GENeral:ES:MOD \n
		Sets the modulation scheme. \n
			:param qck_set_mod_type: QPSK| QAM16| QAM64| QAM256
		"""
		param = Conversions.enum_scalar_to_str(qck_set_mod_type, enums.ModulationB)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:QCKSet:GENeral:ES:MOD {param}')

	# noinspection PyTypeChecker
	def get_rb_config(self) -> enums.Config:
		"""[SOURce<HW>]:BB:NR5G:QCKSet:GENeral:ES:RBConfig \n
		Sets the configuration mode for the resource block configuration. \n
			:return: qck_set_rb_config: MAN| EFL| EFR| E1RL| E1RR| OUTF| INNF| I1RL| I1RR
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:QCKSet:GENeral:ES:RBConfig?')
		return Conversions.str_to_scalar_enum(response, enums.Config)

	def set_rb_config(self, qck_set_rb_config: enums.Config) -> None:
		"""[SOURce<HW>]:BB:NR5G:QCKSet:GENeral:ES:RBConfig \n
		Sets the configuration mode for the resource block configuration. \n
			:param qck_set_rb_config: MAN| EFL| EFR| E1RL| E1RR| OUTF| INNF| I1RL| I1RR
		"""
		param = Conversions.enum_scalar_to_str(qck_set_rb_config, enums.Config)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:QCKSet:GENeral:ES:RBConfig {param}')

	def get_rb_number(self) -> int:
		"""[SOURce<HW>]:BB:NR5G:QCKSet:GENeral:ES:RBNumber \n
		Sets the number of resource blocks. \n
			:return: qck_set_rb_num: integer Range: 1 to 273
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:QCKSet:GENeral:ES:RBNumber?')
		return Conversions.str_to_int(response)

	def set_rb_number(self, qck_set_rb_num: int) -> None:
		"""[SOURce<HW>]:BB:NR5G:QCKSet:GENeral:ES:RBNumber \n
		Sets the number of resource blocks. \n
			:param qck_set_rb_num: integer Range: 1 to 273
		"""
		param = Conversions.decimal_value_to_str(qck_set_rb_num)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:QCKSet:GENeral:ES:RBNumber {param}')

	def get_rb_offset(self) -> int:
		"""[SOURce<HW>]:BB:NR5G:QCKSet:GENeral:ES:RBOFfset \n
		Sets the resource block offset. \n
			:return: qck_set_rb_offset: integer Range: 0 to 272
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:QCKSet:GENeral:ES:RBOFfset?')
		return Conversions.str_to_int(response)

	def set_rb_offset(self, qck_set_rb_offset: int) -> None:
		"""[SOURce<HW>]:BB:NR5G:QCKSet:GENeral:ES:RBOFfset \n
		Sets the resource block offset. \n
			:param qck_set_rb_offset: integer Range: 0 to 272
		"""
		param = Conversions.decimal_value_to_str(qck_set_rb_offset)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:QCKSet:GENeral:ES:RBOFfset {param}')
