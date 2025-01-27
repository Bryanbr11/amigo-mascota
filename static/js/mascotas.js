const RAZAS_POR_ESPECIE = {
    'PERRO': [
        ['LABRADOR', 'Labrador Retriever'],
        ['PASTOR_ALEMAN', 'Pastor Alemán'],
        ['BULLDOG', 'Bulldog'],
        ['GOLDEN', 'Golden Retriever'],
        ['CHIHUAHUA', 'Chihuahua'],
        ['POODLE', 'Poodle'],
        ['ROTTWEILER', 'Rottweiler'],
        ['YORKSHIRE', 'Yorkshire Terrier'],
        ['BOXER', 'Boxer'],
        ['OTRO', 'Otro'],
    ],
    'GATO': [
        ['PERSA', 'Persa'],
        ['SIAMES', 'Siamés'],
        ['ANGORA', 'Angora'],
        ['BENGALI', 'Bengalí'],
        ['MAINE_COON', 'Maine Coon'],
        ['BRITISH', 'British Shorthair'],
        ['SPHYNX', 'Sphynx'],
        ['RAGDOLL', 'Ragdoll'],
        ['OTRO', 'Otro'],
    ],
    'CONEJO': [
        ['HOLANDES', 'Holandés'],
        ['CABEZA_LEON', 'Cabeza de León'],
        ['ANGORA', 'Angora'],
        ['REX', 'Rex'],
        ['OTRO', 'Otro'],
    ],
    'HAMSTER': [
        ['SIRIO', 'Sirio'],
        ['RUSO', 'Ruso'],
        ['ROBOROVSKI', 'Roborovski'],
        ['CHINO', 'Chino'],
        ['OTRO', 'Otro'],
    ],
    'AVE': [
        ['CANARIO', 'Canario'],
        ['PERIQUITO', 'Periquito'],
        ['AGAPORNIS', 'Agapornis'],
        ['CACATUA', 'Cacatúa'],
        ['OTRO', 'Otro'],
    ],
    'PEZ': [
        ['BETA', 'Beta'],
        ['GOLDFISH', 'Goldfish'],
        ['GUPPY', 'Guppy'],
        ['TETRA', 'Tetra'],
        ['OTRO', 'Otro'],
    ],
    'REPTIL': [
        ['IGUANA', 'Iguana'],
        ['GECKO', 'Gecko'],
        ['TORTUGA', 'Tortuga'],
        ['DRAGON_BARBUDO', 'Dragón Barbudo'],
        ['OTRO', 'Otro'],
    ],
    'OTRO': [
        ['OTRO', 'Otro'],
    ],
};

function updateRazas(especie) {
    const razaSelect = document.getElementById('id_raza');
    const razas = RAZAS_POR_ESPECIE[especie] || [['OTRO', 'Otro']];
    
    // Limpiar opciones actuales
    razaSelect.innerHTML = '';
    
    // Agregar nuevas opciones
    razas.forEach(([value, label]) => {
        const option = new Option(label, value);
        razaSelect.add(option);
    });
}

// Función para validar la fecha de nacimiento
function validateFechaNacimiento() {
    const fechaNacimientoInput = document.getElementById('id_fecha_nacimiento');
    const today = new Date().toISOString().split('T')[0];
    
    // Establecer la fecha máxima
    fechaNacimientoInput.max = today;
    
    // Validar cuando cambie el valor
    fechaNacimientoInput.addEventListener('change', function() {
        if (this.value > today) {
            this.value = today;
            alert('La fecha de nacimiento no puede ser en el futuro.');
        }
    });
}

// Agregar la validación de fecha al DOMContentLoaded
document.addEventListener('DOMContentLoaded', function() {
    const especieSelect = document.getElementById('id_especie');
    if (especieSelect) {
        updateRazas(especieSelect.value);
    }
    
    // Inicializar validación de fecha
    validateFechaNacimiento();
}); 