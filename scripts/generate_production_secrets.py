#!/usr/bin/env python3
"""
Secure Production Secrets Generator for BFSI API
Generates cryptographically secure passwords and keys for production deployment.
"""

import secrets
import string
import hashlib
import base64
import os
import sys
import datetime
from pathlib import Path
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC


class ProductionSecretsGenerator:
    """Generate secure production secrets for BFSI API deployment."""
    
    def __init__(self):
        self.secrets = {}
    
    def generate_strong_password(self, length=32, include_symbols=True):
        """Generate a cryptographically secure password."""
        characters = string.ascii_letters + string.digits
        if include_symbols:
            characters += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        # Ensure at least one character from each category
        password = [
            secrets.choice(string.ascii_lowercase),
            secrets.choice(string.ascii_uppercase),
            secrets.choice(string.digits)
        ]
        
        if include_symbols:
            password.append(secrets.choice("!@#$%^&*()_+-=[]{}|;:,.<>?"))
        
        # Fill the rest randomly
        for _ in range(length - len(password)):
            password.append(secrets.choice(characters))
        
        # Shuffle the password
        secrets.SystemRandom().shuffle(password)
        return ''.join(password)
    
    def generate_secret_key(self, length=64):
        """Generate a secure secret key."""
        return secrets.token_urlsafe(length)
    
    def generate_encryption_key(self):
        """Generate a 32-byte encryption key for Fernet."""
        return Fernet.generate_key().decode()
    
    def generate_jwt_secret(self, length=64):
        """Generate a secure JWT secret key."""
        return secrets.token_urlsafe(length)
    
    def generate_api_key(self, length=32):
        """Generate a secure API key."""
        return secrets.token_urlsafe(length)
    
    def generate_all_secrets(self):
        """Generate all required production secrets."""
        print("🔐 Generating secure production secrets...")
        
        # Database credentials
        self.secrets['DB_PASSWORD'] = self.generate_strong_password(32)
        self.secrets['REDIS_PASSWORD'] = self.generate_strong_password(24)
        
        # Security keys
        self.secrets['SECRET_KEY'] = self.generate_secret_key(64)
        self.secrets['JWT_SECRET_KEY'] = self.generate_jwt_secret(64)
        self.secrets['ENCRYPTION_KEY'] = self.generate_encryption_key()
        self.secrets['API_KEY_MASTER'] = self.generate_api_key(32)
        
        # SMTP password
        self.secrets['SMTP_PASSWORD'] = self.generate_strong_password(24)
        
        print("✅ All secrets generated successfully!")
        return self.secrets
    
    def save_secrets_to_file(self, output_file="production_secrets.env"):
        """Save generated secrets to a file."""
        secrets_content = "# Generated Production Secrets - KEEP SECURE!\n"
        secrets_content += "# Generated on: {}\n".format(datetime.datetime.now().isoformat())
        secrets_content += "# DO NOT COMMIT THIS FILE TO VERSION CONTROL!\n\n"
        
        for key, value in self.secrets.items():
            secrets_content += f"{key}={value}\n"
        
        with open(output_file, 'w') as f:
            f.write(secrets_content)
        
        print(f"🔒 Secrets saved to {output_file}")
        print("⚠️  IMPORTANT: Keep this file secure and do not commit to version control!")
    
    def update_production_env(self, env_file_path="config/environment/production.env"):
        """Update the production.env file with generated secrets."""
        if not os.path.exists(env_file_path):
            print(f"❌ Environment file not found: {env_file_path}")
            return False
        
        # Read current file
        with open(env_file_path, 'r') as f:
            content = f.read()
        
        # Replace placeholder values
        replacements = {
            'secure_db_password_change_me': self.secrets['DB_PASSWORD'],
            'secure_redis_password_change_me': self.secrets['REDIS_PASSWORD'],
            'your_super_secret_key_change_me_in_production': self.secrets['SECRET_KEY'],
            'your_jwt_secret_key_change_me_in_production': self.secrets['JWT_SECRET_KEY'],
            'your_32_byte_encryption_key_change_me': self.secrets['ENCRYPTION_KEY'],
            'your_master_api_key_change_me': self.secrets['API_KEY_MASTER'],
            'your_smtp_password': self.secrets['SMTP_PASSWORD']
        }
        
        for placeholder, new_value in replacements.items():
            content = content.replace(placeholder, new_value)
        
        # Create backup
        backup_path = f"{env_file_path}.backup"
        with open(backup_path, 'w') as f:
            f.write(content)
        
        # Write updated content
        with open(env_file_path, 'w') as f:
            f.write(content)
        
        print(f"✅ Updated {env_file_path} with secure credentials")
        print(f"📋 Backup created at {backup_path}")
        return True


def main():
    """Main execution function."""
    print("🚀 BFSI Production Secrets Generator")
    print("=" * 50)
    
    generator = ProductionSecretsGenerator()
    
    # Generate all secrets
    generator.generate_all_secrets()
    
    # Save to secrets file
    generator.save_secrets_to_file()
    
    # Update production environment file
    env_file = "config/environment/production.env"
    if os.path.exists(env_file):
        generator.update_production_env(env_file)
    else:
        print(f"⚠️  Environment file not found: {env_file}")
        print("📋 Generated secrets are available in production_secrets.env")
    
    print("\n🔐 Security Recommendations:")
    print("1. Store secrets in a secure secrets management system (AWS Secrets Manager, HashiCorp Vault, etc.)")
    print("2. Use environment variables or secure configuration injection in production")
    print("3. Rotate secrets regularly")
    print("4. Never commit secrets to version control")
    print("5. Use least privilege access controls")
    
    print("\n✅ Secret generation complete!")


if __name__ == "__main__":
    main()
