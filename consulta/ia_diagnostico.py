import openai

def generar_diagnostico_ia(datos_consulta):
    openai.api_key = 'TU_API_KEY_DE_OPENAI'
    
    prompt = f"""
    Basándote en la siguiente información de una consulta veterinaria, proporciona un diagnóstico complementario, posibles causas y tratamientos sugeridos:
    
    Síntomas: {datos_consulta['sintomas']}
    Diagnóstico inicial del veterinario: {datos_consulta['diagnostico']}
    Peso: {datos_consulta['peso']} kg
    Edad: {datos_consulta['edad']} años
    Raza: {datos_consulta['raza']}
    
    Por favor, proporciona:
    1. Posibles enfermedades adicionales a considerar
    2. Tratamientos sugeridos
    3. Referencias adicionales o pruebas recomendadas
    """
    
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=500,
        n=1,
        stop=None,
        temperature=0.7,
    )
    
    return response.choices[0].text.strip()