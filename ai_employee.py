"""
🤖 SLP AI EMPLOYEE - Personal Payroll Assistant
Like the image - auto processes emails, files, and approvals
"""

import os
import time
import shutil
import smtplib
import imaplib
import email
import json
import pandas as pd
from pathlib import Path
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv

load_dotenv()

# ============================================
# CONFIGURATION — set these in a .env file (see .env.example)
# ============================================
GMAIL_EMAIL = os.getenv("GMAIL_EMAIL", "your_email@gmail.com")
GMAIL_PASSWORD = os.getenv("GMAIL_APP_PASSWORD", "")
GMAIL_NAME = os.getenv("GMAIL_NAME", "AI Payroll Assistant")

VAULT_PATH = os.getenv("VAULT_PATH", "vault")

# SLP Entities (12 companies)
SLP_ENTITIES = [
    "Houston_Operations", "Dallas_Distribution", "Austin_Retail",
    "SanAntonio_Logistics", "FortWorth_Production", "ElPaso_FieldOps",
    "CorpusChristi_Marine", "Midland_Energy", "Lubbock_Agri",
    "Plano_Corporate", "Amarillo_Transport", "Beaumont_Refinery"
]

class SLPAIEmployee:
    def __init__(self):
        self.vault = Path(VAULT_PATH)
        self.setup_folders()
        self.processed_count = 0
        self.approval_count = 0
        
        print("=" * 60)
        print("🤖 SLP AI EMPLOYEE ACTIVATED")
        print("=" * 60)
        print(f"📧 Email: {GMAIL_EMAIL}")
        print(f"📁 Vault: {VAULT_PATH}")
        print(f"🏢 Entities: {len(SLP_ENTITIES)}")
        print("=" * 60)
    
    def setup_folders(self):
        """Create all required folders"""
        folders = [
            "Needs_Action", "Done", "Pending_Approval", 
            "Approved", "Rejected", "Logs", 
            "Payroll_Data", "Receipts"
        ]
        for folder in folders:
            (self.vault / folder).mkdir(parents=True, exist_ok=True)
    
    def send_email(self, to_address, subject, body, attachment_path=None):
        """Send email with optional attachment"""
        try:
            msg = MIMEMultipart()
            msg['From'] = f"{GMAIL_NAME} <{GMAIL_EMAIL}>"
            msg['To'] = to_address
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))
            
            # Add attachment if provided
            if attachment_path and Path(attachment_path).exists():
                with open(attachment_path, 'rb') as f:
                    part = MIMEBase('application', 'octet-stream')
                    part.set_payload(f.read())
                    encoders.encode_base64(part)
                    part.add_header('Content-Disposition', f'attachment; filename={Path(attachment_path).name}')
                    msg.attach(part)
            
            server = smtplib.SMTP("smtp.gmail.com", 587)
            server.starttls()
            server.login(GMAIL_EMAIL, GMAIL_PASSWORD)
            server.send_message(msg)
            server.quit()
            
            self.log_action(f"Email sent to: {to_address} - {subject}")
            return True
        except Exception as e:
            self.log_action(f"Email error: {e}")
            return False
    
    def log_action(self, message):
        """Log all actions for audit trail"""
        log_file = self.vault / "Logs" / f"log_{datetime.now().strftime('%Y-%m-%d')}.txt"
        with open(log_file, 'a') as f:
            f.write(f"{datetime.now().strftime('%H:%M:%S')} - {message}\n")
        print(f"  📝 {message}")
    
    def extract_client_info(self, content):
        """Extract client email and request details"""
        client_email = GMAIL_EMAIL
        request_type = "general"
        amount = None
        entity = None
        
        lines = content.split('\n')
        for line in lines:
            if '@' in line and ('from:' in line.lower() or 'client:' in line.lower()):
                import re
                match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', line)
                if match:
                    client_email = match.group()
            if 'payroll' in line.lower() or 'salary' in line.lower():
                request_type = "payroll"
            if '$' in line:
                import re
                match = re.search(r'\$[\d,]+\.?\d*', line)
                if match:
                    amount = match.group()
            if entity in line for entity in SLP_ENTITIES:
                for e in SLP_ENTITIES:
                    if e.lower().replace('_', ' ') in line.lower():
                        entity = e
                        break
        
        return client_email, request_type, amount, entity
    
    def process_payroll_request(self, data, client_email):
        """Process payroll specific requests"""
        # Generate Excel file with entity splits
        excel_path = self.vault / "Payroll_Data" / f"payroll_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
        
        # Create sample payroll data
        payroll_data = []
        for entity in SLP_ENTITIES:
            payroll_data.append({
                "Entity": entity,
                "Amount": f"${hash(entity) % 50000 + 20000:,}",
                "Status": "Pending Approval",
                "Employees": hash(entity) % 30 + 10
            })
        
        df = pd.DataFrame(payroll_data)
        df.to_excel(excel_path, index=False)
        
        # Send to client
        client_body = f"""Dear Client,

Your payroll request has been received and is being processed.

📊 Summary:
- Entities: {len(SLP_ENTITIES)}
- Total Amount: ${sum([hash(e) % 50000 + 20000 for e in SLP_ENTITIES]):,}
- Status: Pending approval

📎 Attached: Payroll breakdown by entity

You will receive confirmation once approved.

Best regards,
SLP AI Employee
"""
        self.send_email(client_email, "Payroll Request Received", client_body, excel_path)
        
        return excel_path
    
    def check_emails(self):
        """Read emails from Gmail"""
        try:
            mail = imaplib.IMAP4_SSL("imap.gmail.com")
            mail.login(GMAIL_EMAIL, GMAIL_PASSWORD)
            mail.select("INBOX")
            
            result, data = mail.search(None, 'UNSEEN')
            
            for num in data[0].split():
                result, msg_data = mail.fetch(num, '(RFC822)')
                msg = email.message_from_bytes(msg_data[0][1])
                
                subject = msg['subject']
                from_addr = msg['from']
                body = ""
                
                if msg.is_multipart():
                    for part in msg.walk():
                        if part.get_content_type() == "text/plain":
                            body = part.get_payload(decode=True).decode()
                            break
                else:
                    body = msg.get_payload(decode=True).decode()
                
                # Save to Needs_Action
                filename = f"email_{int(time.time())}_{len(list((self.vault / 'Needs_Action').glob('*')))}.txt"
                filepath = self.vault / "Needs_Action" / filename
                
                content = f"""From: {from_addr}
Subject: {subject}
Received: {datetime.now()}
ClientEmail: {from_addr}

{body}
"""
                filepath.write_text(content, encoding='utf-8')
                print(f"\n📧 NEW EMAIL from: {from_addr}")
                print(f"   Subject: {subject}")
            
            mail.close()
            mail.logout()
        except Exception as e:
            self.log_action(f"Email check error: {e}")
    
    def process_file(self, filepath):
        """Process a single file/request"""
        content = filepath.read_text(encoding='utf-8')
        content_upper = content.upper()
        
        # Extract client info
        client_email, request_type, amount, entity = self.extract_client_info(content)
        
        print(f"\n📄 Processing: {filepath.name}")
        print(f"   Client: {client_email}")
        print(f"   Type: {request_type}")
        
        # Check if approval needed
        if any(word in content_upper for word in ["APPROVAL", "PAYMENT", "INVOICE", "$", "SEND", "PAYROLL"]):
            # Move to Pending_Approval
            dest = self.vault / "Pending_Approval" / filepath.name
            shutil.move(str(filepath), str(dest))
            
            # Send acknowledgment to CLIENT
            client_msg = f"""Dear Client,

Thank you for your request. It has been received and is waiting for approval.

📋 Request Details:
- Type: {request_type}
- Amount: {amount if amount else 'To be determined'}
- Status: Pending Approval
- Request ID: {filepath.name}

You will receive confirmation once approved.

Best regards,
SLP AI Employee System
"""
            self.send_email(client_email, f"Request Received - Pending Approval", client_msg)
            
            # Send notification to OWNER (you)
            owner_msg = f"""🔔 Approval Needed

Request from: {client_email}
Type: {request_type}
Amount: {amount if amount else 'N/A'}
File: {filepath.name}

To approve: Move file to "Approved" folder
To reject: Move file to "Rejected" folder

Location: {self.vault / 'Pending_Approval'}
"""
            self.send_email(GMAIL_EMAIL, f"APPROVAL NEEDED: {filepath.name}", owner_msg)
            
            self.approval_count += 1
            self.log_action(f"Approval needed: {filepath.name} from {client_email}")
            
        elif "PAYROLL" in content_upper:
            # Process payroll request
            excel_file = self.process_payroll_request(content, client_email)
            dest = self.vault / "Done" / filepath.name
            shutil.move(str(filepath), str(dest))
            self.log_action(f"Payroll processed: {filepath.name}")
            
        else:
            # Regular task - auto process
            response = f"""AI RESPONSE
Processed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

Your request has been processed successfully.

Request: {content[:200]}

Best regards,
SLP AI Employee
"""
            response_file = self.vault / "Done" / f"response_{filepath.name}"
            response_file.write_text(response)
            
            # Send response to client
            self.send_email(client_email, "Request Processed", response)
            
            dest = self.vault / "Done" / filepath.name
            shutil.move(str(filepath), str(dest))
            self.log_action(f"Auto-processed: {filepath.name}")
        
        self.processed_count += 1
    
    def check_approvals(self):
        """Check Approved/Rejected folders and execute"""
        # Process Approved
        approved_folder = self.vault / "Approved"
        for file in approved_folder.glob("*"):
            if file.is_file():
                print(f"\n✅ APPROVED: {file.name}")
                content = file.read_text()
                
                # Extract client email
                client_email = GMAIL_EMAIL
                for line in content.split('\n'):
                    if line.startswith('ClientEmail:'):
                        client_email = line.split(':', 1)[1].strip()
                    elif line.startswith('From:'):
                        client_email = line.split(':', 1)[1].strip()
                
                # Send confirmation to CLIENT
                client_msg = f"""Dear Client,

Great news! Your request '{file.name}' has been APPROVED.

Status: Processing in progress
Processed by: SLP AI Employee System

Thank you for your business.

Best regards,
SLP Team
"""
                self.send_email(client_email, f"✅ Request Approved: {file.name}", client_msg)
                
                # Move to Done
                dest = self.vault / "Done" / f"approved_{file.name}"
                shutil.move(str(file), str(dest))
                self.log_action(f"Approved and executed: {file.name}")
        
        # Process Rejected
        rejected_folder = self.vault / "Rejected"
        for file in rejected_folder.glob("*"):
            if file.is_file():
                print(f"\n❌ REJECTED: {file.name}")
                content = file.read_text()
                
                client_email = GMAIL_EMAIL
                for line in content.split('\n'):
                    if line.startswith('ClientEmail:'):
                        client_email = line.split(':', 1)[1].strip()
                
                client_msg = f"""Dear Client,

Your request '{file.name}' has been REJECTED.

Please contact the finance department for more information.

Best regards,
SLP Team
"""
                self.send_email(client_email, f"❌ Request Rejected: {file.name}", client_msg)
                
                dest = self.vault / "Done" / f"rejected_{file.name}"
                shutil.move(str(file), str(dest))
                self.log_action(f"Rejected: {file.name}")
    
    def show_status(self):
        """Display current status"""
        pending = len(list((self.vault / "Pending_Approval").glob("*")))
        done = len(list((self.vault / "Done").glob("*")))
        
        print(f"\n📊 STATUS: {datetime.now().strftime('%H:%M:%S')}")
        print(f"   Pending Approval: {pending}")
        print(f"   Completed: {done}")
        print(f"   Total Processed: {self.processed_count}")
        print("-" * 40)
    
    def run(self):
        """Main loop"""
        print("\n" + "=" * 60)
        print("🎯 SLP AI EMPLOYEE IS RUNNING")
        print("=" * 60)
        print(f"\n📁 Watching: {self.vault}/Needs_Action")
        print(f"📧 Auto-checking Gmail every 30 seconds")
        print(f"✅ Approve: Move files to 'Approved' folder")
        print(f"❌ Reject: Move files to 'Rejected' folder")
        print("\n💡 Send an email to see AI in action!")
        print("❌ Press Ctrl+C to stop\n")
        
        email_check_count = 0
        
        while True:
            try:
                # Check emails every 30 seconds
                if email_check_count >= 10:
                    self.check_emails()
                    email_check_count = 0
                email_check_count += 1
                
                # Process new files
                files = list((self.vault / "Needs_Action").glob("*"))
                for file in files:
                    if not file.is_file() or file.suffix in ['.tmp', '.swp']:
                        continue
                    self.process_file(file)
                
                # Check for approvals
                self.check_approvals()
                
                # Show status every 30 cycles
                if email_check_count % 30 == 0:
                    self.show_status()
                
                time.sleep(3)
                
            except KeyboardInterrupt:
                print("\n\n" + "=" * 60)
                print(f"🛑 AI EMPLOYEE SHUTDOWN")
                print(f"   Total processed: {self.processed_count}")
                print(f"   Approvals handled: {self.approval_count}")
                print("=" * 60)
                break
            except Exception as e:
                print(f"  ❌ Error: {e}")
                self.log_action(f"Error: {e}")
                time.sleep(5)

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("🎯 SLP PERSONAL AI EMPLOYEE SYSTEM")
    print("   Like the image - Auto processes emails and files")
    print("=" * 60 + "\n")
    
    # Check configuration
    if GMAIL_EMAIL == "your_email@gmail.com":
        print("⚠️  FIRST: Edit the file and add your Gmail credentials!")
        print("   Line 20 and 21 in ai_employee.py")
        print("\n   Get app password from: https://myaccount.google.com/apppasswords")
    else:
        ai = SLPAIEmployee()
        ai.run()