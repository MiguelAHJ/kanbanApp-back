"""
Prueba manual de /build-minuta sin pasar por la interfaz de /docs (evita
problemas de pegar JSON largo en un campo de formulario web).

Uso:
    python tests/manual_test_build_minuta.py

Requiere que el servicio este corriendo (uvicorn app.main:app --port 8420).
"""
import json

import httpx

TRANSCRIPT = (
    "Hablamos sobre como implementar los seeders y factories del modulo de "
    "cursos, revisando el comando para generarlos y como conectarlos al "
    "DatabaseSeeder."
)

# Texto tal cual lo devolvio /read-photo para la foto de notas de Seeders/Factories
NOTES_TEXT = """Seeders

php artisan db:seed -> correr seeders
php artisan make:seeder CursoSeeder -> crear seeder
$this -> call (CursoSeeder::class); -> incluir seeder en DatabaseSeeder

public function run(){
    $this -> call (CursoSeeder::class);
}

Factories

php artisan make:factory CursoFactory --model=Curso
-> crear factory asociado a un modelo

| FACTORY | AÑADIR EN SEED |
| --- | --- |
| public function definition(){ return [ 'name' => $this -> faker -> sentence(), 'descript' => $this -> faker -> paragraph(), 'categoria' => $this -> faker -> randomElement (['opcion 1', 'opcion 2']) [ | Curso::factory(50)->create(); NOTA: se puede añadir en un seeder específico o en el DatabaseSeeder |"""

response = httpx.post(
    "http://localhost:8420/build-minuta",
    data={
        "transcript": TRANSCRIPT,
        "notes_texts": json.dumps([NOTES_TEXT]),
    },
    timeout=60,
)

print("Status:", response.status_code)
print(json.dumps(response.json(), indent=2, ensure_ascii=False))