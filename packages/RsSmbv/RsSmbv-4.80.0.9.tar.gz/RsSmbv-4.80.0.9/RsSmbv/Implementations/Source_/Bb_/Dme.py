from ....Internal.Core import Core
from ....Internal.CommandsGroup import CommandsGroup
from ....Internal import Conversions
from .... import enums


# noinspection PyPep8Naming,PyAttributeOutsideInit,SpellCheckingInspection
class Dme:
	"""Dme commands group definition. 76 total commands, 12 Sub-groups, 15 group commands"""

	def __init__(self, core: Core, parent):
		self._core = core
		self._base = CommandsGroup("dme", core, parent)

	def clone(self) -> 'Dme':
		"""Clones the group by creating new object from it and its whole existing sub-groups
		Also copies all the existing default Repeated Capabilities setting,
		which you can change independently without affecting the original group"""
		new_group = Dme(self._core, self._base.parent)
		self._base.synchronize_repcaps(new_group)
		return new_group

	@property
	def clock(self):
		"""clock commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_clock'):
			from .Dme_.Clock import Clock
			self._clock = Clock(self._core, self._base)
		return self._clock

	@property
	def ppst(self):
		"""ppst commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_ppst'):
			from .Dme_.Ppst import Ppst
			self._ppst = Ppst(self._core, self._base)
		return self._ppst

	@property
	def setting(self):
		"""setting commands group. 0 Sub-classes, 4 commands."""
		if not hasattr(self, '_setting'):
			from .Dme_.Setting import Setting
			self._setting = Setting(self._core, self._base)
		return self._setting

	@property
	def trigger(self):
		"""trigger commands group. 3 Sub-classes, 4 commands."""
		if not hasattr(self, '_trigger'):
			from .Dme_.Trigger import Trigger
			self._trigger = Trigger(self._core, self._base)
		return self._trigger

	@property
	def analysis(self):
		"""analysis commands group. 1 Sub-classes, 11 commands."""
		if not hasattr(self, '_analysis'):
			from .Dme_.Analysis import Analysis
			self._analysis = Analysis(self._core, self._base)
		return self._analysis

	@property
	def echo(self):
		"""echo commands group. 0 Sub-classes, 3 commands."""
		if not hasattr(self, '_echo'):
			from .Dme_.Echo import Echo
			self._echo = Echo(self._core, self._base)
		return self._echo

	@property
	def gaussian(self):
		"""gaussian commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_gaussian'):
			from .Dme_.Gaussian import Gaussian
			self._gaussian = Gaussian(self._core, self._base)
		return self._gaussian

	@property
	def icao(self):
		"""icao commands group. 0 Sub-classes, 1 commands."""
		if not hasattr(self, '_icao'):
			from .Dme_.Icao import Icao
			self._icao = Icao(self._core, self._base)
		return self._icao

	@property
	def id(self):
		"""id commands group. 2 Sub-classes, 11 commands."""
		if not hasattr(self, '_id'):
			from .Dme_.Id import Id
			self._id = Id(self._core, self._base)
		return self._id

	@property
	def marker(self):
		"""marker commands group. 4 Sub-classes, 0 commands."""
		if not hasattr(self, '_marker'):
			from .Dme_.Marker import Marker
			self._marker = Marker(self._core, self._base)
		return self._marker

	@property
	def pinput(self):
		"""pinput commands group. 1 Sub-classes, 2 commands."""
		if not hasattr(self, '_pinput'):
			from .Dme_.Pinput import Pinput
			self._pinput = Pinput(self._core, self._base)
		return self._pinput

	@property
	def rdistance(self):
		"""rdistance commands group. 0 Sub-classes, 2 commands."""
		if not hasattr(self, '_rdistance'):
			from .Dme_.Rdistance import Rdistance
			self._rdistance = Rdistance(self._core, self._base)
		return self._rdistance

	def preset(self) -> None:
		"""[SOURce<HW>]:BB:DME:PRESet \n
		Sets the parameters of the digital standard to their default values (*RST values specified for the commands) .
		Not affected is the state set with the command SOURce<hw>:BB:VOR|ILS|DME:STATe. \n
		"""
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:PRESet')

	def preset_with_opc(self) -> None:
		"""[SOURce<HW>]:BB:DME:PRESet \n
		Sets the parameters of the digital standard to their default values (*RST values specified for the commands) .
		Not affected is the state set with the command SOURce<hw>:BB:VOR|ILS|DME:STATe. \n
		Same as preset, but waits for the operation to complete before continuing further. Use the RsSmbv.utilities.opc_timeout_set() to set the timeout value. \n
		"""
		self._core.io.write_with_opc(f'SOURce<HwInstance>:BB:DME:PRESet')

	def get_state(self) -> bool:
		"""[SOURce<HW>]:BB:DME:STATe \n
		Activates/deactivates the avionic standard. \n
			:return: state: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:STATe?')
		return Conversions.str_to_bool(response)

	def set_state(self, state: bool) -> None:
		"""[SOURce<HW>]:BB:DME:STATe \n
		Activates/deactivates the avionic standard. \n
			:param state: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(state)
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:STATe {param}')

	# noinspection PyTypeChecker
	def get_csuffix(self) -> enums.AvionicDmeChanSuff:
		"""[SOURce<HW>]:[BB]:DME:CSUFfix \n
		Sets the channel that is simulated. Standard compliant X and Y channels differ in the spacing between the two pulses of
		the pulse pair and the delay of the ground station. \n
			:return: csuffix: X| Y| ICAO
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:CSUFfix?')
		return Conversions.str_to_scalar_enum(response, enums.AvionicDmeChanSuff)

	def set_csuffix(self, csuffix: enums.AvionicDmeChanSuff) -> None:
		"""[SOURce<HW>]:[BB]:DME:CSUFfix \n
		Sets the channel that is simulated. Standard compliant X and Y channels differ in the spacing between the two pulses of
		the pulse pair and the delay of the ground station. \n
			:param csuffix: X| Y| ICAO
		"""
		param = Conversions.enum_scalar_to_str(csuffix, enums.AvionicDmeChanSuff)
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:CSUFfix {param}')

	def get_efficiency(self) -> int:
		"""[SOURce<HW>]:[BB]:DME:EFFiciency \n
		Sets the relation between reply pulse pairs and received trigger signals, e.g. with a set efficiency of 50% only every
		second trigger event leads to the generation of a reply pulse pair. \n
			:return: efficiency: integer Range: 0 to 100
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:EFFiciency?')
		return Conversions.str_to_int(response)

	def set_efficiency(self, efficiency: int) -> None:
		"""[SOURce<HW>]:[BB]:DME:EFFiciency \n
		Sets the relation between reply pulse pairs and received trigger signals, e.g. with a set efficiency of 50% only every
		second trigger event leads to the generation of a reply pulse pair. \n
			:param efficiency: integer Range: 0 to 100
		"""
		param = Conversions.decimal_value_to_str(efficiency)
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:EFFiciency {param}')

	def get_fall(self) -> float:
		"""[SOURce<HW>]:[BB]:DME:FALL \n
		Sets the fall time of the pulse (90% to 10% of peak voltage) . \n
			:return: fall: float Range: 0.5E-6 to 10E-6
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:FALL?')
		return Conversions.str_to_float(response)

	def set_fall(self, fall: float) -> None:
		"""[SOURce<HW>]:[BB]:DME:FALL \n
		Sets the fall time of the pulse (90% to 10% of peak voltage) . \n
			:param fall: float Range: 0.5E-6 to 10E-6
		"""
		param = Conversions.decimal_value_to_str(fall)
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:FALL {param}')

	def get_frequency(self) -> float:
		"""[SOURce<HW>]:[BB]:DME:FREQuency \n
		Sets the carrier frequency of the signal. \n
			:return: carreier_freq: float Range: 100E3 to 6E9
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:FREQuency?')
		return Conversions.str_to_float(response)

	def set_frequency(self, carreier_freq: float) -> None:
		"""[SOURce<HW>]:[BB]:DME:FREQuency \n
		Sets the carrier frequency of the signal. \n
			:param carreier_freq: float Range: 100E3 to 6E9
		"""
		param = Conversions.decimal_value_to_str(carreier_freq)
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:FREQuency {param}')

	# noinspection PyTypeChecker
	def get_mode(self) -> enums.AvionicDmeMode:
		"""[SOURce<HW>]:[BB]:DME:MODE \n
		Selects the mode of the DME modulation. The mode determines the signal type that is simulated. The exact timing of the
		signal for each mode is determined by the channel selected withmethod RsSmbv.Source.Bb.Dme.csuffix. \n
			:return: mode: INTerrogation| REPLy INTerrogation The interrogation signal of the airborne transmitter is simulated. REPLy The reply signal of the ground based transponder is simulated. The trigger is automatically set to external and the default trigger delay either to 50 us (channel X) or 56 us (channel Y) depending on the selected channel (method RsSmbv.Source.Bb.Dme.csuffix) . The interval between the pulse pairs can be set to a fixed value (repetition rate, method RsSmbv.Source.Bb.Dme.rate) or to random generation (pulse squitter, method RsSmbv.Source.Bb.Dme.squitter) . The trigger signal is input via the Pulse Ext connector.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:MODE?')
		return Conversions.str_to_scalar_enum(response, enums.AvionicDmeMode)

	def set_mode(self, mode: enums.AvionicDmeMode) -> None:
		"""[SOURce<HW>]:[BB]:DME:MODE \n
		Selects the mode of the DME modulation. The mode determines the signal type that is simulated. The exact timing of the
		signal for each mode is determined by the channel selected withmethod RsSmbv.Source.Bb.Dme.csuffix. \n
			:param mode: INTerrogation| REPLy INTerrogation The interrogation signal of the airborne transmitter is simulated. REPLy The reply signal of the ground based transponder is simulated. The trigger is automatically set to external and the default trigger delay either to 50 us (channel X) or 56 us (channel Y) depending on the selected channel (method RsSmbv.Source.Bb.Dme.csuffix) . The interval between the pulse pairs can be set to a fixed value (repetition rate, method RsSmbv.Source.Bb.Dme.rate) or to random generation (pulse squitter, method RsSmbv.Source.Bb.Dme.squitter) . The trigger signal is input via the Pulse Ext connector.
		"""
		param = Conversions.enum_scalar_to_str(mode, enums.AvionicDmeMode)
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:MODE {param}')

	def get_pps(self) -> float:
		"""[SOURce<HW>]:[BB]:DME:PPS \n
		Sets the spacing between the first and second pulse of a pulse pair (time between halfvoltage points on the leading edge
		of each pulse) . Available only for method RsSmbv.Source.Bb.Dme.singleOFF \n
			:return: pps: float Range: 1E-6 to 200E-6
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:PPS?')
		return Conversions.str_to_float(response)

	def set_pps(self, pps: float) -> None:
		"""[SOURce<HW>]:[BB]:DME:PPS \n
		Sets the spacing between the first and second pulse of a pulse pair (time between halfvoltage points on the leading edge
		of each pulse) . Available only for method RsSmbv.Source.Bb.Dme.singleOFF \n
			:param pps: float Range: 1E-6 to 200E-6
		"""
		param = Conversions.decimal_value_to_str(pps)
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:PPS {param}')

	def get_rate(self) -> int:
		"""[SOURce<HW>]:[BB]:DME:RATE \n
		If method RsSmbv.Source.Bb.Dme.mode is set to INTerrogation, sets the pulse repetition rate. If method RsSmbv.Source.Bb.
		Dme.mode is set to REPLy, indicates the mean pulse repetition rate in squitter mode. \n
			:return: rate: integer Range: 10 to 6000
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:RATE?')
		return Conversions.str_to_int(response)

	def set_rate(self, rate: int) -> None:
		"""[SOURce<HW>]:[BB]:DME:RATE \n
		If method RsSmbv.Source.Bb.Dme.mode is set to INTerrogation, sets the pulse repetition rate. If method RsSmbv.Source.Bb.
		Dme.mode is set to REPLy, indicates the mean pulse repetition rate in squitter mode. \n
			:param rate: integer Range: 10 to 6000
		"""
		param = Conversions.decimal_value_to_str(rate)
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:RATE {param}')

	def get_rise(self) -> float:
		"""[SOURce<HW>]:[BB]:DME:RISE \n
		Sets the rise time of the pulse (10% to 90% of peak voltage) . \n
			:return: rise: float Range: 0.5E-6 to 10E-6
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:RISE?')
		return Conversions.str_to_float(response)

	def set_rise(self, rise: float) -> None:
		"""[SOURce<HW>]:[BB]:DME:RISE \n
		Sets the rise time of the pulse (10% to 90% of peak voltage) . \n
			:param rise: float Range: 0.5E-6 to 10E-6
		"""
		param = Conversions.decimal_value_to_str(rise)
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:RISE {param}')

	# noinspection PyTypeChecker
	def get_shape(self) -> enums.AvionicDmePulsShap:
		"""[SOURce<HW>]:[BB]:DME:SHAPe \n
		Sets the pulse shape. \n
			:return: shape: COS2| LIN| COS| GAUSs COS2| The rising edge is cos shaped and the falling edge is cos^2 shaped. LIN The falling and the rising edge of the pulse are shaped linear. COS The falling and the rising edge of the pulse are cos^2 shaped.
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:SHAPe?')
		return Conversions.str_to_scalar_enum(response, enums.AvionicDmePulsShap)

	def set_shape(self, shape: enums.AvionicDmePulsShap) -> None:
		"""[SOURce<HW>]:[BB]:DME:SHAPe \n
		Sets the pulse shape. \n
			:param shape: COS2| LIN| COS| GAUSs COS2| The rising edge is cos shaped and the falling edge is cos^2 shaped. LIN The falling and the rising edge of the pulse are shaped linear. COS The falling and the rising edge of the pulse are cos^2 shaped.
		"""
		param = Conversions.enum_scalar_to_str(shape, enums.AvionicDmePulsShap)
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:SHAPe {param}')

	def get_single(self) -> bool:
		"""[SOURce<HW>]:[BB]:DME:SINGle \n
		Activates/deactivates generation of a single test pulse. \n
			:return: single: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:SINGle?')
		return Conversions.str_to_bool(response)

	def set_single(self, single: bool) -> None:
		"""[SOURce<HW>]:[BB]:DME:SINGle \n
		Activates/deactivates generation of a single test pulse. \n
			:param single: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(single)
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:SINGle {param}')

	def get_squitter(self) -> bool:
		"""[SOURce<HW>]:[BB]:DME:SQUitter \n
		Activates/deactivates the random pulse repetition rate. The average repetition rate is 2700 pp/s. The pulse spacing is
		distributed randomly in the range of 60 μs to about 1500 μs according to EUROCAE EN-54 6.2.12. The squitter pulses are
		constantly sent by the ground station in order to ensure proper operation and in order to ease synchronization of the
		aircraft interrogator to the ground station. \n
			:return: squitter: 0| 1| OFF| ON
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:SQUitter?')
		return Conversions.str_to_bool(response)

	def set_squitter(self, squitter: bool) -> None:
		"""[SOURce<HW>]:[BB]:DME:SQUitter \n
		Activates/deactivates the random pulse repetition rate. The average repetition rate is 2700 pp/s. The pulse spacing is
		distributed randomly in the range of 60 μs to about 1500 μs according to EUROCAE EN-54 6.2.12. The squitter pulses are
		constantly sent by the ground station in order to ensure proper operation and in order to ease synchronization of the
		aircraft interrogator to the ground station. \n
			:param squitter: 0| 1| OFF| ON
		"""
		param = Conversions.bool_to_str(squitter)
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:SQUitter {param}')

	def get_velocity(self) -> float:
		"""[SOURce<HW>]:[BB]:DME:VELocity \n
		Sets the delay between the DME echo pulse signal and the original DME pulse signal. \n
			:return: dme_velocity: float Range: -1E4 to 1E4
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:VELocity?')
		return Conversions.str_to_float(response)

	def set_velocity(self, dme_velocity: float) -> None:
		"""[SOURce<HW>]:[BB]:DME:VELocity \n
		Sets the delay between the DME echo pulse signal and the original DME pulse signal. \n
			:param dme_velocity: float Range: -1E4 to 1E4
		"""
		param = Conversions.decimal_value_to_str(dme_velocity)
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:VELocity {param}')

	def get_width(self) -> float:
		"""[SOURce<HW>]:[BB]:DME:WIDTh \n
		Sets the pulse width (50% to 50% of peak voltage) . \n
			:return: width: float Range: 1E-6 to 100E-6
		"""
		response = self._core.io.query_str('SOURce<HwInstance>:BB:DME:WIDTh?')
		return Conversions.str_to_float(response)

	def set_width(self, width: float) -> None:
		"""[SOURce<HW>]:[BB]:DME:WIDTh \n
		Sets the pulse width (50% to 50% of peak voltage) . \n
			:param width: float Range: 1E-6 to 100E-6
		"""
		param = Conversions.decimal_value_to_str(width)
		self._core.io.write(f'SOURce<HwInstance>:BB:DME:WIDTh {param}')
