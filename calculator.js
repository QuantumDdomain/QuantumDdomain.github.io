let currentInput = null;

// Track last focused input/textarea
document.addEventListener('focusin', (e) => {
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
        currentInput = e.target;
    }
});

// Insert symbol or function into focused input
function insertToInput(symbol) {
    if (!currentInput) return;

    const start = currentInput.selectionStart;
    const end = currentInput.selectionEnd;
    const original = currentInput.value;

    currentInput.value = original.substring(0, start) + symbol + original.substring(end);
    currentInput.selectionStart = currentInput.selectionEnd = start + symbol.length;
    currentInput.focus();
}

// Helper to get the visible and hidden calculator inputs
function getCalcInputs() {
    const visibleInput = document.getElementById('calc-expression-display');
    const hiddenInput = document.getElementById('calc-expression-hidden');
    const calcInput = document.getElementById('calc-expression-input'); // Standard input field for calc mode
    return { visibleInput, hiddenInput, calcInput };
}


// Insert into calculator's own expression field (handles both single and dual fields)
function insertToCalcInput(symbol, numValue) {
    const { visibleInput, hiddenInput, calcInput } = getCalcInputs();
    
    // Check if we are using the dual input system (for external use) or standard calc mode input
    const targetInput = currentInput && currentInput.id === 'calc-expression-input' ? currentInput : null;
    
    // Determine which string to insert
    const insertSymbol = symbol;
    const insertValue = numValue || symbol; // Use numeric value if provided (for constants), otherwise use the symbol

    if (targetInput) {
        // Standard calc input mode (user is editing the input field directly)
        const start = targetInput.selectionStart;
        const end = targetInput.selectionEnd;
        const original = targetInput.value;

        targetInput.value = original.substring(0, start) + insertSymbol + original.substring(end);
        targetInput.selectionStart = targetInput.selectionEnd = start + insertSymbol.length;
        targetInput.focus();
    } else if (visibleInput && hiddenInput) {
        // Dual input mode (for external input simulation)
        
        // Append to the VISIBLE (symbol) field
        visibleInput.textContent += insertSymbol;
        
        // Append to the HIDDEN (numeric) field
        hiddenInput.value += insertValue;
        
    } else if (calcInput) {
         // Fallback to single calc input if it exists
         const start = calcInput.selectionStart;
         const end = calcInput.selectionEnd;
         const original = calcInput.value;
 
         calcInput.value = original.substring(0, start) + insertSymbol + original.substring(end);
         calcInput.selectionStart = calcInput.selectionEnd = start + insertSymbol.length;
         calcInput.focus();
    }
}


// Evaluate mathematical expression
function evaluateExpression() {
    // We must use the content of the standard input for evaluation in calc mode
    const input = document.getElementById('calc-expression-input');
    const output = document.getElementById('calc-result-output');
    
    if (!input || !output) return;
    
    try {
        let expr = input.value.trim();
        if (!expr) {
            output.textContent = 'Enter an expression';
            output.style.color = '#666';
            return;
        }

        // Replace mathematical notation with JavaScript equivalents
        expr = expr
            // Constants
            .replace(/π/g, 'Math.PI')
            .replace(/\bphi\b|φ/g, '((1 + Math.sqrt(5)) / 2)')
            .replace(/\be\b/g, 'Math.E')
            
            // Trigonometric
            .replace(/sin\(/g, 'Math.sin(')
            .replace(/cos\(/g, 'Math.cos(')
            .replace(/tan\(/g, 'Math.tan(')
            .replace(/csc\(/g, '(1/Math.sin(')
            .replace(/sec\(/g, '(1/Math.cos(')
            .replace(/cot\(/g, '(1/Math.tan(')
            
            // Inverse trigonometric
            .replace(/arcsin\(/g, 'Math.asin(')
            .replace(/arccos\(/g, 'Math.acos(')
            .replace(/arctan\(/g, 'Math.atan(')
            .replace(/arccsc\(/g, 'Math.asin(1/')
            .replace(/arcsec\(/g, 'Math.acos(1/')
            .replace(/arccot\(/g, '(Math.PI/2-Math.atan(')
            
            // Hyperbolic
            .replace(/sinh\(/g, 'Math.sinh(')
            .replace(/cosh\(/g, 'Math.cosh(')
            .replace(/tanh\(/g, 'Math.tanh(')
            .replace(/csch\(/g, '(1/Math.sinh(')
            .replace(/sech\(/g, '(1/Math.cosh(')
            .replace(/coth\(/g, '(1/Math.tanh(')
            
            // Inverse hyperbolic
            .replace(/arcsinh\(/g, 'Math.asinh(')
            .replace(/arccosh\(/g, 'Math.acosh(')
            .replace(/arctanh\(/g, 'Math.atanh(')
            .replace(/arccsch\(/g, 'Math.asinh(1/')
            .replace(/arcsech\(/g, 'Math.acosh(1/')
            .replace(/arccoth\(/g, 'Math.atanh(1/')
            
            // Logarithmic
            .replace(/\bln\(/g, 'Math.log(')
            .replace(/log10\(/g, 'Math.log10(')
            .replace(/log2\(/g, 'Math.log2(')
            .replace(/\blog\(/g, 'Math.log10(')
            .replace(/exp\(/g, 'Math.exp(')
            
            // Roots
            .replace(/√\(/g, 'Math.sqrt(')
            .replace(/∛\(/g, 'Math.cbrt(')
            .replace(/∜\(/g, 'Math.pow(')
            .replace(/root\(/g, 'Math.pow(')
            
            // Special functions
            .replace(/abs\(/g, 'Math.abs(')
            .replace(/floor\(/g, 'Math.floor(')
            .replace(/ceil\(/g, 'Math.ceil(')
            .replace(/round\(/g, 'Math.round(')
            .replace(/sgn\(/g, 'Math.sign(')
            .replace(/mod\(/g, '(')
            
            // Power notation
            .replace(/\^/g, '**');

        const result = eval(expr);
        
        if (isNaN(result)) {
            output.textContent = 'Invalid result';
            output.style.color = '#e74c3c';
        } else if (!isFinite(result)) {
            output.textContent = result > 0 ? '∞' : '-∞';
            output.style.color = '#f39c12';
        } else {
            output.textContent = result;
            output.style.color = '#27ae60';
        }
    } catch (error) {
        output.textContent = 'Error: ' + error.message;
        output.style.color = '#e74c3c';
    }
}
// Create toggle button
function createToggleButton() {
    const btn = document.createElement('button');
    btn.id = 'toggle-calculator-btn';
    btn.innerHTML = `
        <svg width="28" height="28" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
            <rect x="3" y="3" width="18" height="18" rx="2" fill="white" opacity="0.9"/>
            <rect x="5" y="5" width="6" height="3" rx="0.5" fill="#007BFF"/>
            <rect x="13" y="5" width="6" height="3" rx="0.5" fill="#007BFF"/>
            <line x1="8" y1="12" x2="8" y2="15" stroke="#007BFF" stroke-width="1.5" stroke-linecap="round"/>
            <line x1="6.5" y1="13.5" x2="9.5" y2="13.5" stroke="#007BFF" stroke-width="1.5" stroke-linecap="round"/>
            <line x1="15" y1="11" x2="18" y2="14" stroke="#007BFF" stroke-width="1.5" stroke-linecap="round"/>
            <line x1="18" y1="11" x2="15" y2="14" stroke="#007BFF" stroke-width="1.5" stroke-linecap="round"/>
            <line x1="6.5" y1="18.5" x2="9.5" y2="18.5" stroke="#007BFF" stroke-width="1.5" stroke-linecap="round"/>
            <line x1="15" y1="18.5" x2="18" y2="18.5" stroke="#007BFF" stroke-width="1.8" stroke-linecap="round"/>
            <line x1="15" y1="17" x2="18" y2="17" stroke="#007BFF" stroke-width="1.8" stroke-linecap="round"/>
        </svg>
    `;
    Object.assign(btn.style, {
        position: 'fixed',
        bottom: '80px',
        right: '20px',
        padding: '11px',
        borderRadius: '12px',
        backgroundColor: '#007BFF',
        color: '#fff',
        border: 'none',
        width: '50px',
        height: '50px',
        zIndex: 9998,
        cursor: 'pointer',
        boxShadow: '0 4px 12px rgba(0,123,255,0.3)',
        transition: 'all 0.3s ease',
        outline: 'none',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center'
    });

    btn.onmouseenter = () => {
        btn.style.backgroundColor = '#0056b3';
        btn.style.transform = 'translateY(-2px)';
        btn.style.boxShadow = '0 6px 16px rgba(0,123,255,0.4)';
    };
    btn.onmouseleave = () => {
        btn.style.backgroundColor = '#007BFF';
        btn.style.transform = 'translateY(0)';
        btn.style.boxShadow = '0 4px 12px rgba(0,123,255,0.3)';
    };
    
    btn.onclick = toggleCalculator;
    document.body.appendChild(btn);
}

// Toggle visibility
function toggleCalculator() {
    const calc = document.getElementById('floating-calculator');
    if (calc) {
        calc.style.display = (calc.style.display === 'none') ? 'block' : 'none';
    } else {
        showCalculator();
    }
}

// Build calculator panel
function showCalculator() {
    const calc = document.createElement('div');
    calc.id = 'floating-calculator';
    Object.assign(calc.style, {
        position: 'fixed',
        top: '20px',
        right: '20px',
        background: '#ffffff',
        color: '#000000',
        border: '2px solid #444',
        padding: '15px',
        borderRadius: '12px',
        boxShadow: '0 4px 16px rgba(0, 0, 0, 0.3)',
        zIndex: 9999,
        maxHeight: '85vh',
        width: '420px',
        overflowY: 'auto',
        overflowX: 'hidden',
        fontFamily: 'Arial, sans-serif',
        cursor: 'default'
    });

    // Header
    const header = document.createElement('div');
    header.id = 'calculator-header';
    Object.assign(header.style, {
        textAlign: 'center',
        fontWeight: 'bold',
        marginBottom: '15px',
        fontSize: '18px',
        cursor: 'move',
        background: '#007BFF',
        color: '#fff',
        padding: '8px',
        borderRadius: '6px'
    });
    header.textContent = '📐 Math Functions Calculator';
    calc.appendChild(header);

    // Evaluation Section
    const evalSection = document.createElement('div');
    Object.assign(evalSection.style, {
        marginBottom: '20px',
        padding: '15px',
        background: '#f8f9fa',
        borderRadius: '8px',
        border: '2px solid #007BFF'
    });

    const evalTitle = document.createElement('div');
    Object.assign(evalTitle.style, {
        fontSize: '14px',
        fontWeight: 'bold',
        color: '#007BFF',
        marginBottom: '10px'
    });
    evalTitle.textContent = '🧪 Evaluate Expression';
    evalSection.appendChild(evalTitle);

    // --- DUAL INPUT SETUP (Replacing calc-expression-input) ---
    const inputContainer = document.createElement('div');
    inputContainer.style.marginBottom = '10px';

    const calcInput = document.createElement('input');
    calcInput.id = 'calc-expression-input';
    calcInput.type = 'text';
    calcInput.placeholder = 'e.g., sin(π/2) or sqrt(16)';
    Object.assign(calcInput.style, {
        width: '100%',
        padding: '10px',
        fontSize: '14px',
        borderRadius: '6px',
        border: '1px solid #ccc',
        boxSizing: 'border-box',
        fontFamily: 'monospace'
    });
    calcInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') evaluateExpression();
    });

    // Dual Input Elements (Visible Display and Hidden Value)
    const visibleDisplay = document.createElement('div');
    visibleDisplay.id = 'calc-expression-display';
    Object.assign(visibleDisplay.style, {
        width: '100%',
        padding: '10px',
        fontSize: '14px',
        borderRadius: '6px',
        border: '1px solid #ccc',
        boxSizing: 'border-box',
        minHeight: '40px',
        backgroundColor: '#fff',
        fontFamily: 'monospace',
        whiteSpace: 'nowrap',
        overflowX: 'auto',
        cursor: 'text'
    });
    visibleDisplay.textContent = '';

    const hiddenInput = document.createElement('input');
    hiddenInput.id = 'calc-expression-hidden';
    hiddenInput.type = 'hidden';
    hiddenInput.value = '';

    inputContainer.appendChild(calcInput);
    inputContainer.appendChild(visibleDisplay);
    inputContainer.appendChild(hiddenInput);

    // --- END DUAL INPUT SETUP ---
    
    evalSection.appendChild(inputContainer);

    const buttonContainer = document.createElement('div');
    Object.assign(buttonContainer.style, {
        display: 'flex',
        gap: '8px',
        marginBottom: '10px'
    });

    const evalBtn = document.createElement('button');
    evalBtn.textContent = '= Calculate';
    Object.assign(evalBtn.style, {
        flex: '1',
        padding: '10px',
        fontSize: '14px',
        fontWeight: 'bold',
        backgroundColor: '#28a745',
        color: '#fff',
        border: 'none',
        borderRadius: '6px',
        cursor: 'pointer',
        transition: 'background 0.2s'
    });
    evalBtn.onmouseenter = () => evalBtn.style.backgroundColor = '#218838';
    evalBtn.onmouseleave = () => evalBtn.style.backgroundColor = '#28a745';
    evalBtn.onclick = evaluateExpression;
    buttonContainer.appendChild(evalBtn);

    const clearBtn = document.createElement('button');
    clearBtn.textContent = 'Clear';
    Object.assign(clearBtn.style, {
        padding: '10px 15px',
        fontSize: '14px',
        backgroundColor: '#dc3545',
        color: '#fff',
        border: 'none',
        borderRadius: '6px',
        cursor: 'pointer',
        transition: 'background 0.2s'
    });
    clearBtn.onmouseenter = () => clearBtn.style.backgroundColor = '#c82333';
    clearBtn.onmouseleave = () => clearBtn.style.backgroundColor = '#dc3545';
    clearBtn.onclick = () => {
        calcInput.value = '';
        visibleDisplay.textContent = '';
        hiddenInput.value = '';
        document.getElementById('calc-result-output').textContent = '0';
        document.getElementById('calc-result-output').style.color = '#666';
    };
    buttonContainer.appendChild(clearBtn);
    evalSection.appendChild(buttonContainer);

    const resultLabel = document.createElement('div');
    resultLabel.textContent = 'Result:';
    Object.assign(resultLabel.style, {
        fontSize: '12px',
        color: '#666',
        marginBottom: '5px'
    });
    evalSection.appendChild(resultLabel);

    const resultOutput = document.createElement('div');
    resultOutput.id = 'calc-result-output';
    resultOutput.textContent = '0';
    Object.assign(resultOutput.style, {
        padding: '12px',
        fontSize: '18px',
        fontWeight: 'bold',
        backgroundColor: '#fff',
        borderRadius: '6px',
        border: '1px solid #ddd',
        textAlign: 'right',
        fontFamily: 'monospace',
        color: '#666',
        minHeight: '24px'
    });
    evalSection.appendChild(resultOutput);

    calc.appendChild(evalSection);

    // Mode selector
    const modeSection = document.createElement('div');
    Object.assign(modeSection.style, {
        marginBottom: '15px',
        padding: '10px',
        background: '#e9ecef',
        borderRadius: '6px',
        textAlign: 'center'
    });

    const modeLabel = document.createElement('span');
    modeLabel.textContent = 'Insert to: ';
    Object.assign(modeLabel.style, {
        fontSize: '13px',
        fontWeight: 'bold',
        marginRight: '10px'
    });
    modeSection.appendChild(modeLabel);

    const calcModeBtn = document.createElement('button');
    calcModeBtn.id = 'mode-calc';
    calcModeBtn.textContent = 'Calculator';
    Object.assign(calcModeBtn.style, {
        padding: '6px 12px',
        fontSize: '12px',
        backgroundColor: '#007BFF',
        color: '#fff',
        border: 'none',
        borderRadius: '4px',
        cursor: 'pointer',
        marginRight: '5px',
        transition: 'background 0.2s'
    });

    const inputModeBtn = document.createElement('button');
    inputModeBtn.id = 'mode-input';
    inputModeBtn.textContent = 'External Input';
    Object.assign(inputModeBtn.style, {
        padding: '6px 12px',
        fontSize: '12px',
        backgroundColor: '#6c757d',
        color: '#fff',
        border: 'none',
        borderRadius: '4px',
        cursor: 'pointer',
        transition: 'background 0.2s'
    });

    let insertMode = 'calc'; // 'calc' or 'input'
    
    // --- NEW: Update Display Visibility based on mode ---
    const updateInputVisibility = () => {
        if (insertMode === 'calc') {
            calcInput.style.display = 'block';
            visibleDisplay.style.display = 'none';
            hiddenInput.style.display = 'none';
        } else {
            calcInput.style.display = 'none';
            visibleDisplay.style.display = 'block';
            // The hidden input should always be hidden, but its value is what we insert externally
            hiddenInput.style.display = 'none'; 
        }
    };
    
    const updateModeButtons = () => {
        if (insertMode === 'calc') {
            calcModeBtn.style.backgroundColor = '#007BFF';
            inputModeBtn.style.backgroundColor = '#6c757d';
        } else {
            calcModeBtn.style.backgroundColor = '#6c757d';
            inputModeBtn.style.backgroundColor = '#007BFF';
        }
        updateInputVisibility();
    };

    calcModeBtn.onclick = () => {
        insertMode = 'calc';
        updateModeButtons();
        // Set currentInput to the actual input field for standard editing
        currentInput = calcInput; 
    };

    inputModeBtn.onclick = () => {
        insertMode = 'input';
        updateModeButtons();
        // Clear currentInput so button clicks go to dual input handler
        currentInput = null; 
    };
    // Initialize correct display
    updateInputVisibility();
    currentInput = calcInput; // Default focus on the actual input

    modeSection.appendChild(calcModeBtn);
    modeSection.appendChild(inputModeBtn);
    calc.appendChild(modeSection);

    // Categories with their functions
    const categories = [
        {
            name: 'Constants',
            items: [
                { display: 'π', value: 'π', numValue: '3.141592653589793' },
                { display: 'e', value: 'e', numValue: '2.71828182846' },
                { display: '√2', value: '√2', numValue: '1.41421356237' },
                { display: '√3', value: '√3', numValue: '1.73205080757' },
                { display: '√5', value: '√5', numValue: '2.23606797750' },
                { display: 'φ (golden)', value: 'φ', numValue: '1.61803398875' }
            ]
        },
        {
            name: 'Trigonometric',
            items: [
                { display: 'sin(x)', value: 'sin(' },
                { display: 'cos(x)', value: 'cos(' },
                { display: 'tan(x)', value: 'tan(' },
                { display: 'csc(x)', value: 'csc(' },
                { display: 'sec(x)', value: 'sec(' },
                { display: 'cot(x)', value: 'cot(' }
            ]
        },
        {
            name: 'Inverse Trigonometric',
            items: [
                { display: 'arcsin(x)', value: 'arcsin(' },
                { display: 'arccos(x)', value: 'arccos(' },
                { display: 'arctan(x)', value: 'arctan(' },
                { display: 'arccsc(x)', value: 'arccsc(' },
                { display: 'arcsec(x)', value: 'arcsec(' },
                { display: 'arccot(x)', value: 'arccot(' }
            ]
        },
        {
            name: 'Hyperbolic',
            items: [
                { display: 'sinh(x)', value: 'sinh(' },
                { display: 'cosh(x)', value: 'cosh(' },
                { display: 'tanh(x)', value: 'tanh(' },
                { display: 'csch(x)', value: 'csch(' },
                { display: 'sech(x)', value: 'sech(' },
                { display: 'coth(x)', value: 'coth(' }
            ]
        },
        {
            name: 'Inverse Hyperbolic',
            items: [
                { display: 'arcsinh(x)', value: 'arcsinh(' },
                { display: 'arccosh(x)', value: 'arccosh(' },
                { display: 'arctanh(x)', value: 'arctanh(' },
                { display: 'arccsch(x)', value: 'arccsch(' },
                { display: 'arcsech(x)', value: 'arcsech(' },
                { display: 'arccoth(x)', value: 'arccoth(' }
            ]
        },
        {
            name: 'Logarithmic',
            items: [
                { display: 'ln(x)', value: 'ln(' },
                { display: 'log(x)', value: 'log(' },
                { display: 'log₂(x)', value: 'log2(' },
                { display: 'log₁₀(x)', value: 'log10(' },
                { display: 'exp(x)', value: 'exp(' }
            ]
        },
        {
            name: 'Root Functions',
            items: [
                { display: '√(x)', value: '√(' },
                { display: '∛(x)', value: '∛(' },
                { display: '∜(x)', value: '∜(' },
                { display: 'x²', value: '^2' },
                { display: 'xⁿ', value: '^' },
                { display: '( )', value: '()' }
            ]
        },
        {
            name: 'Special Functions',
            items: [
                { display: '|x|', value: 'abs(' },
                { display: 'floor(x)', value: 'floor(' },
                { display: 'ceil(x)', value: 'ceil(' },
                { display: 'round(x)', value: 'round(' },
                { display: 'sgn(x)', value: 'sgn(' },
                { display: 'mod(x,y)', value: 'mod(' }
            ]
        },
        {
            name: 'Variables & Operators',
            items: [
                { display: 'x', value: 'x' },
                { display: 'y', value: 'y' },
                { display: 't', value: 't' },
                { display: '+', value: '+' },
                { display: '-', value: '-' },
                { display: '*', value: '*' },
                { display: '/', value: '/' }
            ]
        }
    ];

    // Create sections for each category
    categories.forEach(category => {
        const section = document.createElement('div');
        section.style.marginBottom = '15px';

        const categoryTitle = document.createElement('div');
        Object.assign(categoryTitle.style, {
            fontSize: '14px',
            fontWeight: 'bold',
            color: '#007BFF',
            marginBottom: '8px',
            borderBottom: '2px solid #007BFF',
            paddingBottom: '4px'
        });
        categoryTitle.textContent = category.name;
        section.appendChild(categoryTitle);

        const grid = document.createElement('div');
        Object.assign(grid.style, {
            display: 'grid',
            gridTemplateColumns: 'repeat(3, 1fr)',
            gap: '8px'
        });

        category.items.forEach(item => {
            const btn = document.createElement('button');
            btn.textContent = item.display;
            
            // Add a data attribute for the numeric value if it exists (for constants)
            if (item.numValue) {
                btn.setAttribute('data-numeric-value', item.numValue);
            }
            
            Object.assign(btn.style, {
                padding: '8px 4px',
                fontSize: '13px',
                color: '#000000',
                backgroundColor: '#f0f0f0',
                border: '1px solid #aaa',
                borderRadius: '6px',
                cursor: 'pointer',
                transition: 'all 0.2s',
                fontWeight: '500'
            });
            btn.onmouseenter = () => {
                btn.style.backgroundColor = '#007BFF';
                btn.style.color = '#fff';
                btn.style.transform = 'translateY(-2px)';
            };
            btn.onmouseleave = () => {
                btn.style.backgroundColor = '#f0f0f0';
                btn.style.color = '#000';
                btn.style.transform = 'translateY(0)';
            };
            btn.onclick = () => {
                if (insertMode === 'calc') {
                    // Use standard calc input, passing the symbol. JS evaluation handles conversion.
                    insertToCalcInput(item.value);
                } else {
                    // Use external input mode (dual fields) or the last focused external input.
                    
                    // Case 1: External Input (Last Focused Input/Textarea)
                    if (currentInput) {
                        // To guarantee the Python backend works, insert the numeric value for constants.
                        // For functions/variables, insert the symbol.
                         const valueToInsert = item.numValue || item.value;
                         insertToInput(valueToInsert);
                        
                    } 
                    // Case 2: Using the Calculator's Dual Input Display (Simulating the external input with symbol view)
                    else {
                        // Insert the symbol for the visible display, and the numeric value for the hidden field.
                        insertToCalcInput(item.value, item.numValue);
                    }
                }
            };
            grid.appendChild(btn);
        });

        section.appendChild(grid);
        calc.appendChild(section);
    });

    // Info section
    const info = document.createElement('div');
    Object.assign(info.style, {
        marginTop: '15px',
        padding: '10px',
        background: '#f9f9f9',
        borderRadius: '6px',
        fontSize: '11px',
        color: '#666',
        borderLeft: '3px solid #007BFF'
    });
    info.innerHTML = '<b>Usage:</b> Click functions. In **Calculator Mode**, type or click (symbols are auto-converted for evaluation). In **External Input Mode**, For direct external input (not the calculator panel\'s display), the actual numeric value must be inserted** for compatibility with backends.';
    calc.appendChild(info);

    document.body.appendChild(calc);
    makeDraggable(calc, header);
}

// Make a div draggable using header
function makeDraggable(elmnt, dragHandle) {
    let pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;

    dragHandle.onmousedown = dragMouseDown;

    function dragMouseDown(e) {
        e.preventDefault();
        pos3 = e.clientX;
        pos4 = e.clientY;
        document.onmouseup = closeDragElement;
        document.onmousemove = elementDrag;
    }

    function elementDrag(e) {
        e.preventDefault();
        pos1 = pos3 - e.clientX;
        pos2 = pos4 - e.clientY;
        pos3 = e.clientX;
        pos4 = e.clientY;
        elmnt.style.top = (elmnt.offsetTop - pos2) + "px";
        elmnt.style.left = (elmnt.offsetLeft - pos1) + "px";
        elmnt.style.bottom = 'auto';
        elmnt.style.right = 'auto';
    }

    function closeDragElement() {
        document.onmouseup = null;
        document.onmousemove = null;
    }
}

// Init
window.addEventListener('DOMContentLoaded', () => {
    createToggleButton();
});