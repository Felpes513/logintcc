from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from app.core.use_cases.envia_emails import EnviaEmailUseCase
from app.adapters.email.smtp_email_remetente import SmtpEmailRemetente
from app.core.models.email_payload import EmailBase64Payload
import base64

router = APIRouter()

@router.post("/send-emails-base64")
def send_emails_base64(payload: EmailBase64Payload):
    try:
        arquivo_em_bytes = base64.b64decode(payload.arquivo_base64)

        use_case = EnviaEmailUseCase(email_sender=SmtpEmailRemetente())
        qtd_emails_enviados = use_case.execute(arquivo_em_bytes)

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "E-mails enviados com sucesso!",
                "data": {"quantidade_enviada": qtd_emails_enviados}
            }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro interno: {str(e)}")
