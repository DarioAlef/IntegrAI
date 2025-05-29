import io
import ffmpeg

# Função para converter áudio OPUS (WhatsApp) para WAV usando ffmpeg
def convert_opus_to_wav(audio_bytes):
    in_file = io.BytesIO(audio_bytes)  # Cria um arquivo em memória com os bytes do áudio OPUS
    out_file = io.BytesIO()  # Cria um arquivo em memória para saída WAV
    process = (
        ffmpeg
        .input('pipe:0')  # Entrada via pipe (stdin)
        .output('pipe:1', format='wav')  # Saída via pipe (stdout) no formato WAV
        .run_async(pipe_stdin=True, pipe_stdout=True, pipe_stderr=True)  # Executa ffmpeg de forma assíncrona
    )
    output, err = process.communicate(input=in_file.read())  # Envia os dados do áudio para ffmpeg e recebe a saída
    out_file.write(output)  # Escreve o áudio convertido no arquivo em memória
    out_file.seek(0)  # Volta o ponteiro para o início do arquivo
    out_file.name = "audio.wav"  # Define o nome do arquivo em memória (necessário para algumas APIs)
    # Não salva mais o arquivo em disco
    return out_file  # Retorna o arquivo WAV em memória
