# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

# Collect all Python files
a = Analysis(
    ['launcher.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('models', 'models'),
        ('routes', 'routes'),
        ('utils', 'utils'),
        ('*.py', '.'),
    ],
    hiddenimports=[
        'flask',
        'flask_sqlalchemy',
        'sqlalchemy',
        'pymysql',
        'werkzeug',
        'dotenv',
        'jwt',
        'reportlab',
        'PIL',
        'PIL.Image',
        'tkinter',
        'threading',
        'json',
        'datetime',
        # All models
        'models.user',
        'models.agent_profile',
        'models.bank_fee',
        'models.cash_flow',
        'models.edc_machine',
        'models.service_fee',
        'models.service',
        'models.transaction',
        # All routes
        'routes.auth',
        'routes.agent',
        'routes.bank_fee',
        'routes.cash_flow',
        'routes.dashboard',
        'routes.edc',
        'routes.health',
        'routes.reports',
        'routes.service_fee',
        'routes.service',
        'routes.transaction',
        # Utils
        'utils.jwt_handler',
        'utils.response',
        'utils.validators',
        # Other dependencies
        'sqlalchemy.dialects.mysql',
        'sqlalchemy.sql.default_comparator',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        'matplotlib',
        'numpy',
        'pandas',
        'scipy',
        'IPython',
        'notebook',
    ],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='BrilinkBackend',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add your icon path here if you have one: 'icon.ico'
)
