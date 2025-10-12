import sympy as sp

def recognize_symbolic_value(value, tolerance=1e-6):
    """
    Intelligently recognizes common mathematical constants and expressions.
    Converts floats to symbolic forms like √2, π, e, fractions, etc.
    """
    # Handle near-zero values FIRST (before any operations)
    if abs(value) < tolerance:
        return sp.Integer(0)
    
    # Check for exact integers
    if abs(value - round(value)) < tolerance:
        return sp.Integer(round(value))
    
    # Check for multiples of π (very common for trig functions)
    try:
        pi_val = float(sp.pi.evalf())
        ratio = value / pi_val
        
        # Check if it's close to an integer multiple of π
        if abs(ratio - round(ratio)) < tolerance * 10:
            n = round(ratio)
            if n == 0:
                return sp.Integer(0)
            elif n == 1:
                return sp.pi
            elif n == -1:
                return -sp.pi
            else:
                return n * sp.pi
        
        # Check if it's close to a simple rational multiple of π (like π/2, 2π/3, etc.)
        for denom in range(2, 13):  # Check denominators up to 12
            for numer in range(-20, 21):  # Check reasonable numerators
                if numer == 0:
                    continue
                test_val = (numer / denom) * pi_val
                if abs(value - test_val) < tolerance * 10:
                    if numer == 1:
                        return sp.pi / denom
                    elif numer == -1:
                        return -sp.pi / denom
                    else:
                        return (numer * sp.pi) / denom
    except (ZeroDivisionError, ValueError, OverflowError):
        pass
    
    # Check for multiples of e
    try:
        e_val = float(sp.E.evalf())
        e_ratio = value / e_val
        if abs(e_ratio - round(e_ratio)) < tolerance * 10:
            n = round(e_ratio)
            if n == 1:
                return sp.E
            elif n == -1:
                return -sp.E
            elif n != 0:
                return n * sp.E
    except (ZeroDivisionError, ValueError, OverflowError):
        pass
    
    # Check for common square roots (√2, √3, √5, etc.)
    try:
        for n in range(2, 21):  # Check sqrt(2) through sqrt(20)
            sqrt_val = float(sp.sqrt(n).evalf())
            if abs(value - sqrt_val) < tolerance:
                return sp.sqrt(n)
            if abs(value + sqrt_val) < tolerance:
                return -sp.sqrt(n)
            # Check for rational multiples of square roots (like 2√3)
            for mult in range(2, 6):
                if abs(value - mult * sqrt_val) < tolerance:
                    return mult * sp.sqrt(n)
                if abs(value + mult * sqrt_val) < tolerance:
                    return -mult * sp.sqrt(n)
    except (ValueError, OverflowError):
        pass
    
    # Check for cube roots, 4th roots, 5th roots, etc.
    try:
        for root_degree in range(3, 7):  # Check cube roots through 6th roots
            for n in range(2, 21):  # Check various radicands
                nth_root_val = float(n**(1/root_degree))
                if abs(value - nth_root_val) < tolerance:
                    return n**(sp.Rational(1, root_degree))
                if abs(value + nth_root_val) < tolerance:
                    return -n**(sp.Rational(1, root_degree))
                # Check for rational multiples
                for mult in range(2, 4):
                    if abs(value - mult * nth_root_val) < tolerance:
                        return mult * n**(sp.Rational(1, root_degree))
                    if abs(value + mult * nth_root_val) < tolerance:
                        return -mult * n**(sp.Rational(1, root_degree))
    except (ValueError, OverflowError):
        pass
    
    # Try with rational=False first to get radicals (WRAPPED IN TRY-EXCEPT)
    try:
        symbolic = sp.nsimplify(value, 
                               tolerance=tolerance,
                               rational=False,
                               full=True)
        
        # Verify the symbolic form is accurate and not too complex
        if symbolic is not None and abs(float(symbolic.evalf()) - value) < tolerance:
            # Reject if it contains complex nested expressions
            symbolic_str = str(symbolic)
            # Count complexity - if too many operations, reject it
            complexity = symbolic_str.count('+') + symbolic_str.count('*') + symbolic_str.count('/')
            if complexity <= 3:  # Allow only reasonably simple expressions
                return symbolic
    except (ZeroDivisionError, ValueError, OverflowError, TypeError):
        # If nsimplify fails, continue to other methods
        pass
    
    # Try simple fractions only (WRAPPED IN TRY-EXCEPT)
    try:
        rational = sp.nsimplify(value, rational=True, tolerance=tolerance)
        if rational is not None and abs(float(rational.evalf()) - value) < tolerance:
            if rational.is_rational and abs(rational.q) <= 20:  # Very simple fractions only
                return rational
    except (ZeroDivisionError, ValueError, OverflowError, TypeError):
        # If this fails too, fall back to float
        pass
    
    # If nothing works, return the rounded float
    return sp.Float(value, 6)


def recognize_complex_symbolic(complex_value, tolerance=1e-6):
    """
    Recognizes complex numbers symbolically.
    """
    real_part = complex_value.real
    imag_part = complex_value.imag
    
    # Clean up very small values (numerical noise)
    if abs(real_part) < tolerance:
        real_part = 0.0
    if abs(imag_part) < tolerance:
        imag_part = 0.0
    
    real_symbolic = recognize_symbolic_value(real_part, tolerance)
    imag_symbolic = recognize_symbolic_value(imag_part, tolerance)
    
    # Purely real
    if abs(imag_part) < tolerance:
        return real_symbolic
    
    # Purely imaginary
    if abs(real_part) < tolerance:
        if imag_symbolic == 1:
            return sp.I
        elif imag_symbolic == -1:
            return -sp.I
        else:
            return imag_symbolic * sp.I
    
    # Complex number
    return real_symbolic + imag_symbolic * sp.I


def format_symbolic(symbolic_expr):
    """
    Formats a symbolic expression as a clean string.
    """
    return str(symbolic_expr)


def numeric_to_symbolic(value, tolerance=1e-6):
    """
    Main function: Converts any numeric value to symbolic form.
    Handles real numbers, complex numbers, and lists/arrays.
    
    """
    # Handle lists/arrays
    if isinstance(value, (list, tuple)):
        return [numeric_to_symbolic(v, tolerance) for v in value]
    
    # Handle complex numbers
    if isinstance(value, complex):
        result = recognize_complex_symbolic(value, tolerance)
        return format_symbolic(result)
    
    # Handle real numbers
    if isinstance(value, (int, float)):
        result = recognize_symbolic_value(value, tolerance)
        return format_symbolic(result)
    
    # Unknown type
    return str(value)

