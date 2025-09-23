function cargarRuta() {
    console.log("Alias usado:", alias);
    fetch(`/empresa/${alias}/lecturas/ruta/`)
        .then(res => {
            if (!res.ok) {
                throw new Error(`Error HTTP: ${res.status}`);
            }
            return res.json();
        })
        .then(data => {
            console.log("Clientes recibidos:", data);
            const contenedor = document.getElementById('ruta');
            contenedor.innerHTML = ''; // limpiar antes de cargar

            if (!Array.isArray(data) || data.length === 0) {
                contenedor.innerHTML = '<p class="text-gray-500">No hay clientes disponibles para lectura.</p>';
                return;
            }

            data.forEach(cliente => {
                if (!cliente.id || !cliente.nombre || !cliente.direccion) {
                    console.warn("Cliente incompleto:", cliente);
                    return;
                }

                const div = document.createElement('div');
                div.className = 'bg-white p-4 rounded shadow';

                div.innerHTML = `
                    <strong>${cliente.nombre}</strong> (${cliente.direccion})<br>
                    <input type="number" placeholder="Lectura" id="lectura-${cliente.id}" class="border px-2 py-1 w-full mt-1">
                    <input type="text" placeholder="Observación" id="obs-${cliente.id}" class="border px-2 py-1 w-full mt-1">
                    <button onclick="guardarLectura(${cliente.id})" class="bg-blue-600 text-white px-3 py-1 mt-2 rounded">Guardar</button>
                `;
                contenedor.appendChild(div);
            });

            console.log("Renderizado completado");
        })
        .catch(err => {
            console.error('Error al cargar ruta:', err);
            document.getElementById('status').innerText = 'Error al cargar ruta';
        });
}
