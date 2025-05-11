let currentInput = null;

// Track last focused input/textarea
document.addEventListener('focusin', (e) => {
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
        currentInput = e.target;
    }
});

// Insert symbol into focused input
function insertToInput(symbol) {
    if (!currentInput) return;

    const insertMap = {
        'π': '3.14159265359',
        'e': '2.71828182846',
        'y0': 'y0',
        'y1': 'y1',
        'y2': 'y2',
        '√2': '1.41421356237',
        '√3': '1.73205080757',
        '√5': '2.2360679775',
        '√7': '2.64575131106',
        '√11': '3.31662479036',
        'ln(2)': '0.69314718056',
        'ln(10)': '2.30258509299'
    };

    const text = insertMap[symbol] || symbol;
    const start = currentInput.selectionStart;
    const end = currentInput.selectionEnd;
    const original = currentInput.value;

    currentInput.value = original.substring(0, start) + text + original.substring(end);
    currentInput.selectionStart = currentInput.selectionEnd = start + text.length;
    currentInput.focus();
}

// Create toggle button
function createToggleButton() {
    const btn = document.createElement('button');
    btn.id = 'toggle-calculator-btn';
    btn.textContent = '🧮';
    Object.assign(btn.style, {
        position: 'fixed',
        bottom: '80px', // Position above the calculator
        right: '20px',
        padding: '8px',
        borderRadius: '8px', // Rounded corners for a clean look
        backgroundColor: '#000000', // Light blue for a techy look, matching calculator
        color: '#fff',
        border: 'none',
        fontSize: '24px', // Adjusted to a more suitable size
        width: '50px', // Width matching calculator icon
        height: '50px', // Height matching calculator icon
        zIndex: 9998,
        cursor: 'pointer',
        boxShadow: '0 4px 8px rgba(0,0,0,0.2)',
        transition: 'background 0.3s ease', // Smooth hover effect
        outline: 'none', // Remove the focus outline
    });

    btn.onmouseenter = () => btn.style.backgroundColor = '#0056b3'; // Darker blue on hover
    btn.onmouseleave = () => btn.style.backgroundColor = '#007BFF'; // Reset to original color
    
    btn.onclick = toggleCalculator;
    document.body.appendChild(btn);
}

// Toggle visibility
function toggleCalculator() {
    const calc = document.getElementById('floating-calculator');
    if (calc) {
        calc.style.display = (calc.style.display === 'none') ? 'grid' : 'none';
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
        top: '20px', // Placed to the right at top corner
        right: '20px',
        background: '#ffffff',
        color: '#000000',
        border: '2px solid #444',
        padding: '10px',
        borderRadius: '12px',
        boxShadow: '0 4px 16px rgba(0, 0, 0, 0.2)',
        zIndex: 9999,
        maxHeight: '320px',
        maxWidth: '300px',
        overflowY: 'auto',
        overflowX: 'hidden',
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fill, minmax(60px, 1fr))',
        gap: '10px',
        fontFamily: 'Arial, sans-serif',
        cursor: 'default'
    });

    const title = document.createElement('div');
    title.id = 'calculator-header';
    Object.assign(title.style, {
        gridColumn: '1 / -1',
        textAlign: 'center',
        fontWeight: 'bold',
        marginBottom: '8px',
        fontSize: '16px',
        cursor: 'move',
        background: '#eee',
        padding: '4px',
        borderRadius: '6px'
    });
    calc.appendChild(title);

    const constants = [
        'π', 'e', 'y0' , 'y1' , 'y2' ,
        '√2', '√3', '√5', '√7', '√11',
        'ln(2)', 'ln(10)'
    ];

    constants.forEach(symbol => {
        const btn = document.createElement('button');
        btn.textContent = symbol;
        Object.assign(btn.style, {
            padding: '4px',
            fontSize: '14px',
            color: '#000000',
            backgroundColor: '#e6e6e6',
            border: '1px solid #aaa',
            borderRadius: '8px',
            cursor: 'pointer',
            transition: 'background 0.2s'
        });
        btn.onmouseenter = () => btn.style.backgroundColor = '#d0d0d0';
        btn.onmouseleave = () => btn.style.backgroundColor = '#e6e6e6';
        btn.onclick = () => insertToInput(symbol);
        calc.appendChild(btn);
    });

    document.body.appendChild(calc);
    makeDraggable(calc, title);
}

// Make a div draggable using header
function makeDraggable(elmnt, dragHandle) {
    let pos1 = 0, pos2 = 0, pos3 = 0, pos4 = 0;

    dragHandle.onmousedown = dragMouseDown;

    function dragMouseDown(e) {
        e.preventDefault();
        // Get initial mouse pos
        pos3 = e.clientX;
        pos4 = e.clientY;
        document.onmouseup = closeDragElement;
        document.onmousemove = elementDrag;
    }

    function elementDrag(e) {
        e.preventDefault();
        // New cursor pos
        pos1 = pos3 - e.clientX;
        pos2 = pos4 - e.clientY;
        pos3 = e.clientX;
        pos4 = e.clientY;
        // Set new position
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
