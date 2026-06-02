# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

SERPTECH ERP with Full Accounting Integration (Version 35) — Django-based ERP system with double-entry bookkeeping (PSAK/IFRS compliant). This is the **+Accounting** variant that includes comprehensive financial accounting modules on top of operational ERP features.

**Tech Stack**: Django 6.0.3, Python 3.x, SQLite (dev) / PostgreSQL (prod), Redis (caching), Gunicorn, WhiteNoise

## Development Commands

### Setup & Running
```bash
# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver

# Run with Gunicorn (production-like)
gunicorn config.wsgi:application --config gunicorn.conf.py
```

### Database Operations
```bash
# Create migrations after model changes
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Reset database (SQLite only - DESTRUCTIVE)
rm db.sqlite3
python manage.py migrate
```

### Custom Management Commands

**Accounting & Financial**:
```bash
# Seed Chart of Accounts (CoA) - REQUIRED for new installations
python manage.py seed_coa

# Audit accounting integrity (detect missing journals)
python manage.py audit_accounting_integrity

# Audit financial integration between operational and accounting modules
python manage.py audit_integrasi_keuangan

# Backfill missing journals for existing transactions
python manage.py backfill_jurnal

# Validate payment method mappings to Kas/Bank accounts
python manage.py validate_metode_pembayaran

# Fix negative Kas/Bank balances
python manage.py fix_saldo_awal

# Auto-depreciate assets monthly
python manage.py auto_susutkan
```

**Data Seeding**:
```bash
# Seed permissions and roles
python manage.py seed_permissions

# Seed unit conversions (Satuan & KonversiSatuan)
python manage.py seed_konversi_satuan

# Seed operational test data (products, customers, suppliers)
python manage.py seed_operational_test_data

# Seed dashboard sample data
python manage.py seed_dashboard_data
```

**Other Utilities**:
```bash
# Normalize permissions across modules
python manage.py normalize_permissions

# Re-encode face recognition data (HR module)
python manage.py reencode_faces

# Run Telegram bot (automation module)
python manage.py run_telegram_bot

# Send weekly report (AI assistant)
python manage.py send_weekly_report
```

### Static Files
```bash
# Collect static files for production
python manage.py collectstatic --noinput
```

## Architecture Overview

### Double-Entry Accounting Flow

Every operational transaction automatically creates accounting journals via **signals → services → accounting layer**:

```
[Operational Transaction] 
    → Signal (post_save)
        → Service Layer (ensure_*_accounting)
            → akuntansi.services.create_jurnal()
                → JurnalEntry + JurnalLine (double-entry)
                → kas_bank.services.create_operational_mutation()
                    → KasBankTransaction (treasury tracking)
```

**Key Pattern**: All accounting integration is **idempotent** — services check for existing journals before creating new ones to prevent duplicates.

### Module Structure

**Core Operational Modules** (exist in both ID-34 and +Accounting-35):
- `apps/produk/` — Products, categories, units, stock
- `apps/inventory/` — Stock transfers, adjustments, warehouses
- `apps/penjualan/` — Customers, Sales Orders
- `apps/pembelian/` — Suppliers, Purchase Orders
- `apps/pos/` — Point of Sale transactions
- `apps/biaya/` — Operational expenses
- `apps/hr/` — Payroll, attendance, face recognition
- `apps/laporan/` — Reports (operational view)

**Accounting Modules** (exclusive to +Accounting-35):
- `apps/akuntansi/` — Chart of Accounts (CoA), Journal Entries, General Ledger, Financial Reports
- `apps/kas_bank/` — Treasury management (Kas/Bank accounts, transactions, transfers, reconciliation)
- `apps/piutang/` — Accounts Receivable (AR)
- `apps/hutang/` — Accounts Payable (AP)
- `apps/aset/` — Fixed Assets (depreciation, disposal)
- `apps/pajak/` — Tax engine (PPN/VAT, e-Faktur)

**System Modules**:
- `apps/core/` — Shared utilities, mixins, validators, finance metrics
- `apps/dashboard/` — Main dashboard with KPIs
- `apps/activity_log/` — Audit trail for all operations
- `apps/permission_management/` — Role-based access control (RBAC)
- `apps/user_management/` — User accounts
- `apps/pengaturan/` — Company settings
- `apps/automation/` — Telegram bot notifications
- `apps/ai_assistant/` — AI-powered insights
- `apps/fraud_detection/` — Anomaly detection

### Signal-Driven Accounting Integration

**Sales (POS - Cash)**:
```python
# pos/signals.py::create_pos_journal()
POS status='paid' → Jurnal: D:Kas/Bank K:Pendapatan+PPN
                  → Jurnal HPP: D:HPP K:Persediaan
                  → KasBankTransaction (masuk)
                  → FakturPajak (keluaran)
```

**Sales (POS - Credit/Kasbon)**:
```python
# pos/signals.py → pos/services.py::ensure_pos_kasbon_accounting()
POS status='unpaid' → Jurnal: D:Piutang K:Pendapatan+PPN
                    → Jurnal HPP: D:HPP K:Persediaan
                    → Piutang record created
                    → On payment: PembayaranPiutang → D:Kas/Bank K:Piutang
```

**Sales Order (Cash/Credit)**:
```python
# penjualan/signals.py::create_so_journal_and_piutang()
SO status='confirmed' → Jurnal: D:Kas/Bank (or Piutang) K:Pendapatan+PPN
                      → Jurnal HPP: D:HPP K:Persediaan
                      → Piutang record (if credit)
                      → FakturPajak (keluaran)
```

**Purchase Order (Cash/Credit)**:
```python
# pembelian/signals.py::create_po_journal_and_hutang()
PO status='received' → Jurnal: D:Persediaan+PPN_Masukan K:Kas/Bank (or Hutang)
                     → Hutang record (if credit)
                     → FakturPajak (masukan)
```

**Expenses**:
```python
# biaya/signals.py → biaya/services.py::ensure_biaya_accounting()
TransaksiBiaya status='approved' → Jurnal: D:Beban K:Kas/Bank
                                  → KasBankTransaction (keluar)
# Cancellation: reversal journal (swap debit↔kredit)
```

**Payroll**:
```python
# hr/signals.py::create_penggajian_journal()
Penggajian status='dibayar' → Jurnal: D:Beban_Gaji K:Kas/Bank+Hutang_PPh21+Hutang_BPJS
                             → KasBankTransaction (keluar)
```

**Receivables/Payables Payment**:
```python
# piutang/models.py::PembayaranPiutang.save()
Payment → Jurnal: D:Kas/Bank K:Piutang
        → KasBankTransaction (masuk)
        → Reversal on delete (pre_delete signal)

# hutang/models.py::PembayaranHutang.save()
Payment → Jurnal: D:Hutang K:Kas/Bank
        → KasBankTransaction (keluar)
        → Reversal on delete (pre_delete signal)
```

### Service Layer Pattern

All accounting services follow this pattern:

```python
def ensure_*_accounting(transaction, user=None):
    """
    Idempotent: check existing journal before creating.
    Returns: JurnalEntry or None
    Raises: ValueError on validation failure
    """
    # 1. Idempotent check
    if JurnalEntry.objects.filter(sumber='X', sumber_id=transaction.pk).exists():
        return None
    
    # 2. Resolve accounts (CoA mapping)
    kas_bank_account, _, akun_kas_kode = resolve_kas_bank_mapping(metode_pembayaran)
    
    # 3. Build lines_data (double-entry)
    lines_data = [
        {'akun_kode': 'X-XXXX', 'debit': amount, 'kredit': 0, 'keterangan': '...'},
        {'akun_kode': 'Y-YYYY', 'debit': 0, 'kredit': amount, 'keterangan': '...'},
    ]
    
    # 4. Create journal
    with transaction.atomic():
        jurnal = create_jurnal(tanggal, deskripsi, lines_data, sumber='X', ...)
        create_operational_mutation(...)  # Treasury tracking
    
    return jurnal
```

### Chart of Accounts (CoA) Structure

Standard PSAK hierarchy:
- `1-xxxx` — Aset (Assets)
- `2-xxxx` — Kewajiban (Liabilities)
- `3-xxxx` — Modal (Equity)
- `4-xxxx` — Pendapatan (Revenue)
- `5-xxxx` — HPP (Cost of Goods Sold)
- `6-xxxx` — Beban (Expenses)

**Critical accounts**:
- `1-1000` — Kas (default cash account)
- `1-1100` — Bank BCA (default bank account)
- `1-2000` — Piutang Usaha (Accounts Receivable)
- `1-3000` — Persediaan Barang (Inventory)
- `2-1000` — Hutang Usaha (Accounts Payable)
- `2-2000` — PPN Keluaran (Output VAT)
- `1-1500` — PPN Masukan (Input VAT)
- `4-1000` — Pendapatan Penjualan (Sales Revenue)
- `4-1002` — Diskon Penjualan (Sales Discount - contra revenue)
- `5-1000` — HPP (COGS)
- `6-1000` — Beban Gaji (Payroll Expense)

### Financial Reconciliation

`apps/akuntansi/views.py::RekonsiliasiKeuanganView` performs **5 integrity checks**:

1. **Operasional vs Akuntansi** — Compare SUM(operational tables) vs CoA balances
2. **Treasury vs Accounting** — Compare `KasBankAccount.saldo_terhitung` vs `get_saldo_akun(coa)`
3. **Orphan Detection** — Find posted transactions without journals & journals without treasury mutations
4. **Trial Balance** — Validate SUM(Debit) == SUM(Kredit) across all posted journals
5. **Jurnal Failure Log** — Detect failed auto-journal attempts from Activity Log (`[JURNAL GAGAL]`)

### Error Handling Pattern

When auto-journal creation fails:
1. **Log error** to Python logger
2. **Record to Activity Log** with prefix `[JURNAL GAGAL]`
3. **Transaction continues** (operational data not rolled back)
4. **Detected in Reconciliation** as discrepancy + failure log

### Database Isolation

This is the **Isolated Database** variant — each tenant has a separate database instance (vs Isolated Schema which uses PostgreSQL schemas). The `DATABASES` setting in `config/settings.py` determines the connection.

### Permission System

Role-based access control (RBAC) with module + sub-module granularity:
- Permissions checked via mixins: `ReadPermissionMixin`, `CreatePermissionMixin`, `UpdatePermissionMixin`, `DeletePermissionMixin`
- Permission format: `{module}.{sub_module}.can_{action}`
- Example: `akuntansi.coa.can_view`, `penjualan.sales_order.can_create`

### Template System

Uses custom template layout system from `config/template.py`:
- `TemplateLayout.init(self, context)` — Initialize layout context in views
- Theme variables and layout configuration centralized
- Templates in `templates/` directory

## Important Patterns

### When Adding New Operational Transactions

1. **Create model** in appropriate app
2. **Add signal** in `{app}/signals.py` to trigger on `post_save`
3. **Create service** in `{app}/services.py` with `ensure_*_accounting()` pattern
4. **Map to CoA** — determine which accounts (debit/kredit) for the transaction
5. **Test idempotency** — ensure duplicate journals aren't created
6. **Handle reversal** — implement cancellation via `create_reversal_jurnal()`

### When Modifying Accounting Logic

1. **Check existing journals** — accounting changes may require data migration
2. **Update reconciliation** — ensure `RekonsiliasiKeuanganView` still validates correctly
3. **Test trial balance** — SUM(Debit) must always equal SUM(Kredit)
4. **Verify treasury sync** — `KasBankTransaction` must match journal entries

### When Working with Financial Reports

Reports are generated from **CoA balances**, not operational tables:
- `get_neraca()` — Balance Sheet
- `get_laba_rugi()` — Income Statement
- `get_buku_besar()` — General Ledger
- All use `get_saldo_akun()` which aggregates from `JurnalLine` where `jurnal.is_posted=True`

## Environment Variables

Key variables in `.env`:
- `DEBUG` — Enable debug mode (default: True)
- `SECRET_KEY` — Django secret key (required in production)
- `ALLOWED_HOSTS` — Comma-separated allowed hosts
- `DATABASE_URL` — Database connection string (optional, defaults to SQLite)
- `REDIS_URL` — Redis connection for caching (optional)
- `DJANGO_ENVIRONMENT` — Environment name (local/staging/production)

## Testing & Validation

```bash
# Check for configuration errors
python manage.py check

# Validate accounting integrity
python manage.py audit_accounting_integrity

# Validate financial integration
python manage.py audit_integrasi_keuangan

# Check trial balance (should always be balanced)
# Visit: /akuntansi/trial-balance/

# Run reconciliation report
# Visit: /akuntansi/rekonsiliasi-keuangan/
```

## Key Files to Understand

- `apps/akuntansi/services.py` — Core accounting functions (create_jurnal, get_saldo_akun, get_neraca, get_laba_rugi)
- `apps/kas_bank/services.py` — Treasury functions (resolve_kas_bank_mapping, create_operational_mutation)
- `apps/core/finance_metrics.py` — Financial calculation utilities
- `config/settings.py` — Django configuration
- `config/urls.py` — URL routing master

## Common Gotchas

1. **Always run `seed_coa` first** on new installations — accounting modules require CoA to exist
2. **Journals are immutable** — use reversal journals for corrections, not deletion
3. **Idempotency is critical** — always check for existing journals before creating
4. **Treasury must sync** — every journal touching Kas/Bank accounts needs a corresponding `KasBankTransaction`
5. **Trial balance must balance** — if SUM(Debit) ≠ SUM(Kredit), something is broken
6. **Signals fire on save** — be careful with bulk operations that bypass signals
7. **Credit method detection** — `metode_is_credit()` checks if payment method code is in `CREDIT_METHOD_CODES`
