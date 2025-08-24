import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional

class EmailService:
    """Serviço para envio de emails"""
    
    def __init__(self):
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', '587'))
        self.smtp_username = os.getenv('SMTP_USERNAME', '')
        self.smtp_password = os.getenv('SMTP_PASSWORD', '')
        self.from_email = os.getenv('FROM_EMAIL', self.smtp_username)
        self.base_url = os.getenv('BASE_URL', 'http://localhost:5000')
    
    def send_email(self, to_email: str, subject: str, body: str, is_html: bool = False) -> bool:
        """Envia um email"""
        try:
            # Criar mensagem
            msg = MIMEMultipart()
            msg['From'] = self.from_email
            msg['To'] = to_email
            msg['Subject'] = subject
            
            # Adicionar corpo
            msg.attach(MIMEText(body, 'html' if is_html else 'plain'))
            
            # Conectar ao servidor SMTP
            server = smtplib.SMTP(self.smtp_server, self.smtp_port)
            server.starttls()
            server.login(self.smtp_username, self.smtp_password)
            
            # Enviar email
            text = msg.as_string()
            server.sendmail(self.from_email, to_email, text)
            server.quit()
            
            return True
            
        except Exception as e:
            print(f"Erro ao enviar email: {e}")
            return False
    
    def send_password_reset_email(self, to_email: str, username: str, reset_token: str) -> bool:
        """Envia email de recuperação de senha"""
        reset_url = f"{self.base_url}/reset-password?token={reset_token}"
        
        subject = "Recuperação de Senha - Ecommerce"
        
        # Template HTML do email
        html_body = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <title>Recuperação de Senha</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .container {{
                    background-color: #f9f9f9;
                    padding: 30px;
                    border-radius: 10px;
                    border: 1px solid #ddd;
                }}
                .header {{
                    text-align: center;
                    color: #2c3e50;
                    margin-bottom: 30px;
                }}
                .content {{
                    background-color: white;
                    padding: 25px;
                    border-radius: 8px;
                    margin-bottom: 20px;
                }}
                .button {{
                    display: inline-block;
                    background-color: #3498db;
                    color: white;
                    padding: 12px 30px;
                    text-decoration: none;
                    border-radius: 5px;
                    font-weight: bold;
                    margin: 20px 0;
                }}
                .button:hover {{
                    background-color: #2980b9;
                }}
                .warning {{
                    background-color: #fff3cd;
                    border: 1px solid #ffeaa7;
                    color: #856404;
                    padding: 15px;
                    border-radius: 5px;
                    margin: 20px 0;
                }}
                .footer {{
                    text-align: center;
                    color: #666;
                    font-size: 12px;
                    margin-top: 30px;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>🔐 Recuperação de Senha</h1>
                </div>
                
                <div class="content">
                    <p>Olá <strong>{username}</strong>,</p>
                    
                    <p>Recebemos uma solicitação para redefinir a senha da sua conta. Se você fez esta solicitação, clique no botão abaixo para criar uma nova senha:</p>
                    
                    <div style="text-align: center;">
                        <a href="{reset_url}" class="button">Redefinir Senha</a>
                    </div>
                    
                    <p>Ou copie e cole este link no seu navegador:</p>
                    <p style="word-break: break-all; background-color: #f8f9fa; padding: 10px; border-radius: 4px;">
                        {reset_url}
                    </p>
                    
                    <div class="warning">
                        <strong>⚠️ Importante:</strong>
                        <ul>
                            <li>Este link expira em <strong>1 hora</strong></li>
                            <li>Você não poderá usar a mesma senha anterior</li>
                            <li>Se você não solicitou esta redefinição, ignore este email</li>
                        </ul>
                    </div>
                </div>
                
                <div class="footer">
                    <p>Este é um email automático, não responda a esta mensagem.</p>
                    <p>© 2024 Ecommerce - Todos os direitos reservados</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        # Template de texto simples (fallback)
        text_body = f"""
        Recuperação de Senha - Ecommerce
        
        Olá {username},
        
        Recebemos uma solicitação para redefinir a senha da sua conta.
        
        Para redefinir sua senha, acesse o link abaixo:
        {reset_url}
        
        IMPORTANTE:
        - Este link expira em 1 hora
        - Você não poderá usar a mesma senha anterior
        - Se você não solicitou esta redefinição, ignore este email
        
        Este é um email automático, não responda a esta mensagem.
        """
        
        # Tentar enviar HTML primeiro, se falhar, enviar texto simples
        if not self.send_email(to_email, subject, html_body, is_html=True):
            return self.send_email(to_email, subject, text_body, is_html=False)
        
        return True
    
    def is_configured(self) -> bool:
        """Verifica se o serviço de email está configurado"""
        return bool(self.smtp_username and self.smtp_password)

# Instância global do serviço
email_service = EmailService()

