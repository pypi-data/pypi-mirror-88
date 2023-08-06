from .....Internal.Core import Core
from .....Internal.CommandsGroup import CommandsGroup
from .....Internal import Conversions


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Ubwp:
	"""Ubwp commands group definition. 273 total commands, 2 Sub-groups, 1 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("ubwp", core, parent)

	def clone(self) -> 'Ubwp':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Ubwp(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def restart(self):
		"""restart commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_restart'):
			from .Ubwp_.Restart import Restart
			self._restart = Restart(self._core, self._base)
		return self._restart

	@property
	def user(self):
		"""user commands group. 7 Sub-classes, 0 commands."""
		if not hasattr(self, '_user'):
			from .Ubwp_.User import User
			self._user = User(self._core, self._base)
		return self._user

	def get_nuser(self) -> int:
		"""[SOURce<HW>]:BB:NR5G:UBWP:NUSer \n
		Sets the number of simulated users. \n
			:return: num_users: integer Range: 1 to 10
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:NR5G:UBWP:NUSer?')
		return Conversions.str_to_int(response)

	def set_nuser(self, num_users: int) -> None:
		"""[SOURce<HW>]:BB:NR5G:UBWP:NUSer \n
		Sets the number of simulated users. \n
			:param num_users: integer Range: 1 to 10
		"""
		param = Conversions.decimal_value_to_str(num_users)
		self._core.io.write(f'SOURce<HwInstance>:BB:NR5G:UBWP:NUSer {param}')
