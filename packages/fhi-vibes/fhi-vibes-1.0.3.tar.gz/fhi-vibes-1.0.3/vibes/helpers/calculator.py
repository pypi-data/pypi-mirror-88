from .socketio import socket_stress_off, socket_stress_on


def virials_off(calculator):
    """Turn virials computation off

    Args:
        calculator: ase.calculators.calculator.Calculator
            calculator to turn off virials computation for
    """
    if "socketio" in calculator.name.lower():
        socket_stress_off(calculator)
    else:
        virials_to(calculator, False)


def virials_on(calculator):
    """Turn virials computation on

    Args:
        calculator: ase.calculators.calculator.Calculator
            calculator to turn on virials computation for
    """
    if "socketio" in calculator.name.lower():
        socket_stress_on(calculator)
    else:
        virials_to(calculator, True)


def virials_to(calculator, value):
    """Turn virials computation on/off

    Args:
        calculator: ase.calculators.calculator.Calculator
            calculator to turn on virials computation for
        value: bool, set virials computation to this
    """

    # preferred way
    if hasattr(calculator, "virials"):
        calculator.virials = value

    # legacy for ase aims calculator
    else:
        calculator.parameters["compute_heat_flux"] = value
        calculator.parameters["compute_analytical_stress"] = value
