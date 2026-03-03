import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from typing import Optional

# Configuration - Loaded from environment variables for Render/Production
# BASE_URL must be the full public URL of your instance (e.g. https://capinvest.onrender.com)
SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com")
SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
SMTP_USER = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")
BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")

def send_verification_email(to_email: str, token: str, full_name: str):
    """Send welcome email with verification link."""
    subject = "Bienvenue sur CapInvest - Vérifiez votre compte"
    verify_url = f"{BASE_URL}/verify_status.html?token={token}"
    
    html = f"""
    <html>
        <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #1a1714; background-color: #f8fafc; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background: white; padding: 40px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
                <div style="text-align: center; margin-bottom: 30px;">
                    <h1 style="color: #4A90A4; margin: 0;">CapInvest</h1>
                    <p style="color: #64748b; font-size: 0.9rem;">Algorithmes avancés au service de votre patrimoine</p>
                </div>
                
                <h2 style="color: #1a1714;">Bienvenue {full_name} !</h2>
                <p>Merci de vous être inscrit sur <strong>CapInvest</strong>. Nous sommes ravis de vous accompagner dans votre stratégie d'investissement.</p>
                <p>Pour activer votre compte et accéder à toutes nos fonctionnalités Premium, veuillez vérifier votre adresse email en cliquant sur le bouton ci-dessous :</p>
                
                <div style="text-align: center; margin: 40px 0;">
                    <a href="{verify_url}" style="background-color: #4A90A4; color: white; padding: 14px 30px; text-decoration: none; border-radius: 8px; font-weight: 600; display: inline-block;">Activer mon compte</a>
                </div>
                
                <p style="font-size: 0.85rem; color: #64748b; text-align: center;">Ce lien expirera dans 24 heures.<br>Si le bouton ne fonctionne pas, copiez ce lien :<br><span style="color: #4A90A4;">{verify_url}</span></p>
                
                <hr style="border: 0; border-top: 1px solid #e2e8f0; margin: 30px 0;">
                <p style="font-size: 0.75rem; color: #94a3b8; text-align: center;">Si vous n'êtes pas à l'origine de cette inscription, vous pouvez ignorer cet email en toute sécurité.</p>
            </div>
        </body>
    </html>
    """
    _send_email(to_email, subject, html)

def send_reset_password_email(to_email: str, token: str):
    """Send password reset instructions."""
    subject = "CapInvest - Réinitialisation de votre mot de passe"
    reset_url = f"{BASE_URL}/reset_password.html?token={token}"
    
    html = f"""
    <html>
        <body style="font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; line-height: 1.6; color: #1a1714; background-color: #f8fafc; padding: 20px;">
            <div style="max-width: 600px; margin: 0 auto; background: white; padding: 40px; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.05);">
                <div style="text-align: center; margin-bottom: 30px;">
                    <h1 style="color: #4A90A4; margin: 0;">CapInvest</h1>
                </div>
                
                <h2 style="color: #1a1714;">Demande de réinitialisation</h2>
                <p>Nous avons reçu une demande de réinitialisation du mot de passe pour votre compte CapInvest.</p>
                <p>Cliquez sur le bouton ci-dessous pour choisir un nouveau mot de passe sécurisé :</p>
                
                <div style="text-align: center; margin: 40px 0;">
                    <a href="{reset_url}" style="background-color: #4A90A4; color: white; padding: 14px 30px; text-decoration: none; border-radius: 8px; font-weight: 600; display: inline-block;">Réinitialiser mon mot de passe</a>
                </div>
                
                <p style="font-size: 0.85rem; color: #64748b; text-align: center;">Ce lien expirera dans 1 heure.<br>Si vous n'avez pas demandé ce changement, votre compte est en sécurité et vous pouvez ignorer cet email.</p>
                
                <hr style="border: 0; border-top: 1px solid #e2e8f0; margin: 30px 0;">
                <p style="font-size: 0.75rem; color: #94a3b8; text-align: center;">&copy; 2026 CapInvest. Tous droits réservés.</p>
            </div>
        </body>
    </html>
    """
    _send_email(to_email, subject, html)

def _send_email(to_email: str, subject: str, html_content: str):
    """Internal helper to send email via SMTP."""
    if not SMTP_USER or not SMTP_PASSWORD:
        print(f"\n[STUB] EMAIL SENT TO: {to_email}")
        print(f"[STUB] SUBJECT: {subject}")
        print(f"[STUB] CONTENT PREVIEW: {html_content[:100]}...")
        return

    msg = MIMEMultipart()
    msg['From'] = f"CapInvest <{SMTP_USER}>"
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(html_content, 'html'))

    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.set_debuglevel(0)
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
            print(f"✓ Email sent successfully to {to_email}")
    except Exception as e:
        print(f"❌ Failed to send email to {to_email}: {e}")
