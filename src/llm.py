import json
from llama_cpp import Llama, LlamaRAMCache, LlamaGrammar

class CerebroUR5:
    def __init__(self, model_path, routines_json_path):
        # 1. CARGA DEL MOTOR (Configuración de alto rendimiento para tu RTX 4060)
        self.llm = Llama(
            model_path=model_path,
            n_ctx=2048,           # Espacio para el contexto
            n_threads=8,          # Hilos de CPU para apoyo (8 es ideal para tu i9)
            n_gpu_layers=-1,      # ¡TODO a la tarjeta gráfica!
            n_batch=52,          # Procesamiento en paralelo de tokens
            verbose=False          # Limpieza total en terminal
        )

        # 2. SISTEMA DE CACHÉ (Memoria persistente)
        # Esto guarda el "pensamiento" del System Prompt en la RAM
        self.cache = LlamaRAMCache(capacity_bytes=2 << 30) 
        self.llm.set_cache(self.cache)

        # 3. CARGA DE CONTEXTO INDUSTRIAL
        with open(routines_json_path, 'r') as f:
            self.datos = json.load(f)
            self.nombres_rutinas = list(self.datos.get("routines", {}).keys())

        # 4. PROMPT MAESTRO (Definido como constante de clase)
        self.prompt_sistema = f"""Eres un sistema de control inteligente para un brazo robótico industrial.

Tu única función es interpretar la intención del operario y generar un JSON válido con la configuración de ejecución de la tarea.

No explicas nada. No añades texto. Solo generas JSON válido.

----------------------------------
REGLAS GENERALES
----------------------------------

- Debes seleccionar la tarea más adecuada según la intención del operario.
- Si la orden es ambigua, elige la opción más lógica y segura.
- Prioriza siempre: SEGURIDAD > INTEGRIDAD DEL OBJETO > VELOCIDAD > EFICIENCIA.

----------------------------------
CAMPOS DEL JSON
----------------------------------

1. "tarea":
   - Debe ser una de estas: {self.nombres_rutinas}
   - Selecciona la más adecuada según lo que pide el operario.

2. "ciclos":
   - Número de repeticiones.
   - Por defecto: 1
   - Si el usuario indica cantidad → usarla.
   - Si indica “varias”, “muchas”, etc → estima un valor razonable (>1).

3. "bucle_infinito":
   - true si el usuario indica producción continua, automatización o trabajo sin fin.
   - false en cualquier otro caso.

4. "velocidad_perfil":
   - "lenta", "normal", "rapida"
   - Decide según:
     • FRÁGIL / PRECISIÓN / PRUEBA → lenta
     • NORMAL → normal
     • PRODUCCIÓN / PRISA → rápida

5. "alcance_velocidad":
   - "global" o "solo_contacto"
   - "solo_contacto" si:
       • hay manipulación de objetos
       • el objeto puede ser frágil
       • requiere precisión en agarre/interacción
   - "global" si toda la tarea debe ir a esa velocidad sin restricciones.

6. "modo_simulacion":
   - true si el usuario quiere probar, ver, testear o simular.
   - En simulación:
       • velocidad_perfil SIEMPRE = "lenta"
       • alcance_velocidad = "global"

7. "comportamiento_error":
   - "abortar" por defecto
   - Puede ser:
       • "reintentar" si la tarea es repetitiva o de producción
       • "ignorar" si el fallo no es crítico

8. "persistente":
   - true si el usuario quiere guardar configuración o automatizar a futuro
   - false por defecto

----------------------------------
REGLAS DE INFERENCIA INTELIGENTE
----------------------------------

- Si detectas palabras como:
    "cristal", "cerámica", "frágil", "delicado"
    → velocidad_perfil = "lenta"
    → alcance_velocidad = "solo_contacto"

- Si detectas:
    "rápido", "urgente", "producción", "muchas piezas"
    → velocidad_perfil = "rapida"

- Si hay conflicto (ej: rápido + frágil):
    → velocidad_perfil = "rapida"
    → alcance_velocidad = "solo_contacto"

- Si el usuario quiere observar comportamiento:
    → modo_simulacion = true

- Si no se menciona velocidad:
    → inferir automáticamente según contexto

Regla de Cantidad Estricta: "Si el usuario no especifica un número exacto de piezas o no usa palabras de cantidad (varias, muchas), el valor de 'ciclos' debe ser SIEMPRE 1."

Regla de Prisa: "La palabra 'prisa' solo afecta a 'velocidad_perfil', NUNCA a la cantidad de 'ciclos'."

- Nunca dejes campos vacíos.

----------------------------------
FORMATO DE SALIDA
----------------------------------

Devuelve SOLO este JSON:

{{
  "tarea": "...",
  "ciclos": ...,
  "bucle_infinito": ...,
  "velocidad_perfil": "...",
  "alcance_velocidad": "...",
  "modo_simulacion": ...,
  "comportamiento_error": "...",
  "persistente": ...
}}"""

        # 5. GRAMÁTICA (El escudo de acero)
        self.gramatica = self._generar_gramatica_segura()

        # 6. CALENTAMIENTO (Warm-up)
        # Hacemos que la GPU procese el system prompt una vez para que se quede en caché
        print("🤖 Inicializando cerebro en GPU...")
        self.llm.create_chat_completion(
            messages=[{"role": "system", "content": self.prompt_sistema}],
            max_tokens=500
        )

    def _generar_gramatica_segura(self):
        """Genera el esquema JSON estricto"""
        esquema_json = {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "tarea": {"type": "string", "enum": self.nombres_rutinas},
                    "ciclos": {"type": "integer", "minimum": 1},
                    "bucle_infinito": {"type": "boolean"},
                    "velocidad_perfil": {"type": "string", "enum": ["lenta", "normal", "rapida"]},
                    "alcance_velocidad": {"type": "string", "enum": ["global", "solo_contacto", "solo_transito"]},
                    "modo_simulacion": {"type": "boolean"},
                    "comportamiento_error": {"type": "string", "enum": ["abortar", "reintentar", "ignorar"]},
                    "persistente": {"type": "boolean"}
                },
                "required": [
                    "tarea", "ciclos", "bucle_infinito", "velocidad_perfil", 
                    "alcance_velocidad", "modo_simulacion", "comportamiento_error", "persistente"
                ],
                "additionalProperties": False
            }
        }
        return LlamaGrammar.from_json_schema(json.dumps(esquema_json))

    def procesar_voz(self, comando_usuario):
        # Generación (La caché se activará sola al detectar el mismo sistema de mensajes)
        respuesta = self.llm.create_chat_completion(
            messages=[
                {"role": "system", "content": self.prompt_sistema},
                {"role": "user", "content": comando_usuario}
            ],
            grammar=self.gramatica,
            temperature=0.0,
            # Quitamos cache_prompt porque ahora es automático
            max_tokens=256,
            stop=["<|eot_id|>"]
        )

        resultado_texto = respuesta['choices'][0]['message']['content']
        return json.loads(resultado_texto)

def main():
    # Rutas (Asegúrate de que el nombre del archivo es el correcto)
    path_model = "/home/ivan/proyectos/ur5/models/Meta-Llama-3.1-8B-Instruct-Q5_K_M.gguf"
    path_json = "/home/ivan/proyectos/ur5/cobogen-ur5/docs/routines.json"
    
    try:
        model = CerebroUR5(path_model, path_json)
        print("✅ Sistema listo para recibir órdenes.")

        while True:
            print("-" * 30)
            orden = input("🎤 Orden para el UR5: ")
            if orden.lower() in ["salir", "exit", "quit"]:
                break
                
            try:
                resultado = model.procesar_voz(orden)
                print(f"📦 JSON GENERADO:\n{json.dumps(resultado, indent=4, ensure_ascii=False)}")
            except Exception as e:
                print(f"❌ Error al procesar: {e}")
                
    except Exception as e:
        print(f"🚫 Error al iniciar el modelo: {e}")

if __name__ == "__main__":
     main()