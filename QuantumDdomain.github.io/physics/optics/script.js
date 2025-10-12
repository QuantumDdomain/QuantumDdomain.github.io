//-------------------------------------------------------------
// Matrix & Gaussian Matrix Math
//-------------------------------------------------------------

class Matrix {
    constructor(a, b, c, d) {
        this.mat = [[a, b], [c, d]];
    }

    multiply(other) {
        const a = this.mat[0][0] * other.mat[0][0] + this.mat[0][1] * other.mat[1][0];
        const b = this.mat[0][0] * other.mat[0][1] + this.mat[0][1] * other.mat[1][1];
        const c = this.mat[1][0] * other.mat[0][0] + this.mat[1][1] * other.mat[1][0];
        const d = this.mat[1][0] * other.mat[0][1] + this.mat[1][1] * other.mat[1][1];
        return new Matrix(a, b, c, d);
    }

    toString() {
        return `[${this.mat[0][0].toFixed(3)}, ${this.mat[0][1].toFixed(3)}; ${this.mat[1][0].toFixed(3)}, ${this.mat[1][1].toFixed(3)}]`;
    }
}

function translationMatrix(d) {
    return new Matrix(1, d, 0, 1);
}

function thinLensMatrix(f) {
    return new Matrix(1, 0, -1 / f, 1);
}

function mirrorMatrix(f) {
    return new Matrix(1, 0, -1 / f, 1);
}

function calculateLensFocalLength(n, r1, r2) {
    return 1 / ((n - 1) * (1 / r1 - 1 / r2));
}

//-------------------------------------------------------------
// App State and DOM Elements
//-------------------------------------------------------------

let system = [];
let systemIdCounter = 0;

const lensFocalLengthInput = document.getElementById('lens-focal-length');
const mirrorFocalLengthInput = document.getElementById('mirror-focal-length');

const combinationLibrary = document.getElementById('combination-library');
const systemDisplay = document.getElementById('system-display');
const resultsPlaceholder = document.getElementById('results-placeholder');
const calculationResults = document.getElementById('calculation-results');
const imagePosEl = document.getElementById('image-pos-val');
const magnificationEl = document.getElementById('magnification-val');
const imageTypeEl = document.getElementById('image-type-val');
const imageOrientationEl = document.getElementById('image-orientation-val');
const matrixDisplayEl = document.getElementById('matrix-display');
const objectDistanceInput = document.getElementById('object-distance');

const combinationSystems = [
    {
        name: 'Newtonian Telescope',
        description: 'Concave mirror + flat mirror',
        components: [
            { type: 'mirror', name: 'Primary Mirror', f: 100 },
            { type: 'translation', name: 'Gap', d: 95 },
            { type: 'mirror', name: 'Secondary Mirror', f: 1e6 }
        ],
        icon: '🔭'
    },
    {
        name: 'Cassegrain Telescope',
        description: 'Concave + convex mirror',
        components: [
            { type: 'mirror', name: 'Primary Mirror', f: 100 },
            { type: 'translation', name: 'Gap', d: 80 },
            { type: 'mirror', name: 'Secondary Mirror', f: -25 }
        ],
        icon: '🌌'
    },
    {
        name: 'Compound Microscope',
        description: 'Objective + eyepiece lens',
        components: [
            { type: 'lens', name: 'Objective Lens', f: 2 },
            { type: 'translation', name: 'Tube Length', d: 16 },
            { type: 'lens', name: 'Eyepiece Lens', f: 5 }
        ],
        icon: '🔬'
    },
    {
        name: 'Galilean Telescope',
        description: 'Converging + diverging lens',
        components: [
            { type: 'lens', name: 'Objective Lens', f: 50 },
            { type: 'translation', name: 'Gap', d: 40 },
            { type: 'lens', name: 'Eyepiece Lens', f: -10 }
        ],
        icon: '🌠'
    },
    {
        name: 'Keplerian Telescope',
        description: 'Two converging lenses',
        components: [
            { type: 'lens', name: 'Objective Lens', f: 60 },
            { type: 'translation', name: 'Gap', d: 70 },
            { type: 'lens', name: 'Eyepiece Lens', f: 10 }
        ],
        icon: '🌟'
    },
    {
        name: 'Beam Expander',
        description: 'Diverging + converging lens',
        components: [
            { type: 'lens', name: 'Diverging Lens', f: -10 },
            { type: 'translation', name: 'Gap', d: 40 },
            { type: 'lens', name: 'Converging Lens', f: 30 }
        ],
        icon: '📡'
    }
];

//-------------------------------------------------------------
// Core Logic
//-------------------------------------------------------------

function calculate() {
    if (system.length === 0) {
        alert('Please add at least one component to the system.');
        return;
    }

    let systemMatrix = new Matrix(1, 0, 0, 1);

    for (let i = system.length - 1; i >= 0; i--) {
        const component = system[i];
        if (component.type === 'lens') {
            systemMatrix = systemMatrix.multiply(thinLensMatrix(component.f));
        } else if (component.type === 'mirror') {
            systemMatrix = systemMatrix.multiply(mirrorMatrix(component.f));
        } else if (component.type === 'translation') {
            systemMatrix = systemMatrix.multiply(translationMatrix(component.d));
        }
    }
    
    const s_o = parseFloat(objectDistanceInput.value);
    if (isNaN(s_o) || s_o <= 0) {
        alert('Object distance must be a positive number.');
        return;
    }

    const A = systemMatrix.mat[0][0];
    const B = systemMatrix.mat[0][1];
    const C = systemMatrix.mat[1][0];
    const D = systemMatrix.mat[1][1];

    const denominator = C * s_o + D;
    if (Math.abs(denominator) < 1e-9) {
        displayResults('∞ (Infinity)', '∞', 'Collimated beam', 'N/A', systemMatrix);
        return;
    }
    const s_i = -(A * s_o + B) / denominator;
    const m = 1 / denominator;

    const imageType = s_i > 0 ? 'Real' : 'Virtual';
    const imageOrientation = m > 0 ? 'Erect' : 'Inverted';
    
    displayResults(s_i.toFixed(2), m.toFixed(2), imageType, imageOrientation, systemMatrix);
}

function displayResults(pos, mag, type, orientation, matrix) {
    resultsPlaceholder.classList.add('hidden');
    calculationResults.classList.remove('hidden');
    imagePosEl.textContent = pos;
    magnificationEl.textContent = mag;
    imageTypeEl.textContent = type;
    imageOrientationEl.textContent = orientation;
    matrixDisplayEl.textContent = `System Matrix: ${matrix.toString()}`;
}

//-------------------------------------------------------------
// UI & Event Handlers
//-------------------------------------------------------------

function addCustomLensByF() {
    const f = parseFloat(lensFocalLengthInput.value);
    if (isNaN(f) || f === 0) {
        alert("Please enter a valid, non-zero number for the focal length.");
        return;
    }
    const name = f > 0 ? 'Converging Lens' : 'Diverging Lens';
    system.push({ type: 'lens', name: name, f: f, id: systemIdCounter++ });
    updateSystemDisplay();
    lensFocalLengthInput.value = ''; // Clear the input field
}

function addCustomMirrorByF() {
    const f = parseFloat(mirrorFocalLengthInput.value);
    if (isNaN(f) || f === 0) {
        alert("Please enter a valid, non-zero number for the focal length.");
        return;
    }
    const name = f > 0 ? 'Concave Mirror' : 'Convex Mirror';
    system.push({ type: 'mirror', name: name, f: f, id: systemIdCounter++ });
    updateSystemDisplay();
    mirrorFocalLengthInput.value = ''; // Clear the input field
}

function addCombination(systemName) {
    const combo = combinationSystems.find(c => c.name === systemName);
    if (combo) {
        combo.components.forEach(comp => {
            system.push({ ...comp, id: systemIdCounter++ });
        });
        updateSystemDisplay();
    }
}

function addTranslation() {
    const distance = parseFloat(document.getElementById('translation-distance').value);
    if (isNaN(distance) || distance <= 0) {
        alert('Distance must be a positive number.');
        return;
    }
    system.push({ type: 'translation', name: 'Gap', d: distance, id: systemIdCounter++ });
    document.getElementById('translation-distance').value = '';
    updateSystemDisplay();
}

function createCustomLens() {
    const n = parseFloat(document.getElementById('n-custom').value);
    const r1 = parseFloat(document.getElementById('r1-custom').value);
    const r2 = parseFloat(document.getElementById('r2-custom').value);

    if (isNaN(n) || isNaN(r1) || isNaN(r2)) {
        alert('Please enter valid numbers for all custom lens parameters.');
        return;
    }
    
    const f = calculateLensFocalLength(n, r1, r2);
    if (isNaN(f) || !isFinite(f)) {
         alert('Invalid lens parameters. Focal length cannot be calculated.');
         return;
    }
    
    system.push({ 
        type: 'lens', 
        name: `Custom Lens`, 
        f: f,
        id: systemIdCounter++
    });
    updateSystemDisplay();
}

function removeComponent(id) {
    system = system.filter(comp => comp.id !== id);
    updateSystemDisplay();
}

function updateSystemDisplay() {
    systemDisplay.innerHTML = '';
    
    // Object icon
    const objectIcon = document.createElement('div');
    objectIcon.className = 'component-container';
    objectIcon.innerHTML = `
        <div class="component-icon text-4xl">📍</div>
        <span class="text-sm font-medium">Object</span>
    `;
    systemDisplay.appendChild(objectIcon);
    
    system.forEach((comp, index) => {
        const container = document.createElement('div');
        container.className = 'component-container relative';
        
        let iconHTML;
        let nameToDisplay = comp.name;

        if (comp.type === 'lens') {
            if (comp.f > 0) { // Converging lens
                iconHTML = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 50 50">
                                <ellipse cx="25" cy="25" rx="10" ry="22" fill="#60a5fa" stroke="#1e40af" stroke-width="2"/>
                            </svg>`;
            } else { // Diverging lens
                iconHTML = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 50 50">
                                <path d="M15 3 Q25 25 15 47" fill="none" stroke="#1e40af" stroke-width="3"/>
                                <path d="M35 3 Q25 25 35 47" fill="none" stroke="#1e40af" stroke-width="3"/>
                            </svg>`;
            }
        } else if (comp.type === 'mirror') {
            if (comp.f > 0) { // Concave mirror
                iconHTML = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 50 50">
                                <path d="M20 5 Q10 25 20 45" fill="none" stroke="#9333ea" stroke-width="3"/>
                            </svg>`;
            } else { // Convex mirror
                iconHTML = `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 50 50">
                                <path d="M30 5 Q40 25 30 45" fill="none" stroke="#9333ea" stroke-width="3"/>
                            </svg>`;
            }
        } else if (comp.type === 'translation') {
            iconHTML = '↔️';
            nameToDisplay = `Gap (${comp.d}cm)`;
        }

        container.innerHTML = `
            <button class="remove-btn" onclick="removeComponent(${comp.id})" title="Remove component">×</button>
            <div class="component-icon text-2xl">${iconHTML}</div>
            <span class="text-xs text-center font-medium" style="max-width: 80px; word-wrap: break-word;">${nameToDisplay}</span>
            ${comp.type !== 'translation' ? `<span class="text-xs text-gray-500">f=${comp.f.toFixed(1)}cm</span>` : ''}
        `;
        
        systemDisplay.appendChild(container);
        
        // Add arrow after each component except the last
        if (index < system.length - 1) {
            const arrow = document.createElement('div');
            arrow.className = 'text-2xl text-gray-400';
            arrow.textContent = '➡️';
            systemDisplay.appendChild(arrow);
        }
    });

    // Image icon
    const finalIcon = document.createElement('div');
    finalIcon.className = 'component-container';
    finalIcon.innerHTML = `
        <div class="component-icon text-4xl">🖼️</div>
        <span class="text-sm font-medium">Image</span>
    `;
    systemDisplay.appendChild(finalIcon);
}

function resetSystem() {
    system = [];
    systemIdCounter = 0;
    updateSystemDisplay();
    resultsPlaceholder.classList.remove('hidden');
    calculationResults.classList.add('hidden');
}

// Initial setup
window.onload = function() {
    combinationSystems.forEach(combo => {
        addCombinationSystem(combo);
    });
    updateSystemDisplay();
};

function addCombinationSystem(combo) {
    const card = document.createElement('div');
    card.classList.add('component-button', 'flex-col', 'items-start', 'w-full');
    card.innerHTML = `
        <div class="flex items-center justify-between w-full mb-2">
            <h4 class="font-bold text-gray-800">${combo.icon} ${combo.name}</h4>
            <button onclick="addCombination('${combo.name}')" class="btn btn-primary btn-sm px-4 py-1">Add</button>
        </div>
        <p class="text-sm text-gray-600">${combo.description}</p>
    `;
    combinationLibrary.appendChild(card);
}