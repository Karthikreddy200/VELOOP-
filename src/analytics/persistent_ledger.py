"""
VELOOP Rewards - Persistent Double-Entry Financial Ledger Engine (Work Package D)
Implements true multi-line double-entry bookkeeping with distinct debit and credit lines,
strict duplicate prevention, integer cent precision, and SQL-derived reconciliation.

Notice: SIMULATED DATA & MODEL — CREATED FOR ANALYTICAL TESTING & ARCHITECTURAL SPECIFICATION
"""

import sqlite3
import os
import threading
from datetime import datetime, timezone
from decimal import Decimal, ROUND_HALF_UP
from typing import Dict, Any, List, Tuple, Optional

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data", "wallet_ledger.db")
_LOCK = threading.Lock()

class LedgerError(Exception):
    """Base exception for financial ledger operations."""
    pass

class DuplicateTransactionError(LedgerError):
    """Raised when an attempt is made to insert an existing transaction ID."""
    pass

class UnbalancedJournalEntryError(LedgerError):
    """Raised when debit and credit lines do not mathematically balance."""
    pass

class InvalidPrecisionError(LedgerError):
    """Raised when a monetary amount cannot be accurately represented in integer subunits."""
    pass


def get_db_connection(timeout: float = 30.0) -> sqlite3.Connection:
    """Initializes and returns a SQLite connection with WAL mode and row factory."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH, timeout=timeout)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode=WAL;")
    conn.execute("PRAGMA foreign_keys=ON;")
    return conn


def init_persistent_ledger():
    """
    Initializes the relational double-entry schema:
    1. journal_entries: Master header tracking atomic transactions.
    2. journal_entry_lines: Individual debit and credit line items.
    3. fact_wallet_transactions: Backward-compatible analytical view.
    """
    with _LOCK:
        conn = get_db_connection()
        with conn:
            # 1. Master Journal Header
            conn.execute("""
                CREATE TABLE IF NOT EXISTS journal_entries (
                    entry_id TEXT PRIMARY KEY,
                    transaction_id TEXT NOT NULL UNIQUE,
                    user_id TEXT NOT NULL,
                    event_type TEXT NOT NULL,
                    description TEXT NOT NULL,
                    currency_unit TEXT NOT NULL DEFAULT 'USD',
                    status TEXT NOT NULL DEFAULT 'POSTED',
                    created_at TEXT NOT NULL
                );
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_je_user_id ON journal_entries(user_id);")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_je_tx_id ON journal_entries(transaction_id);")

            # 2. Relational Double-Entry Line Items (Separate Debit and Credit Rows)
            conn.execute("""
                CREATE TABLE IF NOT EXISTS journal_entry_lines (
                    line_id TEXT PRIMARY KEY,
                    entry_id TEXT NOT NULL,
                    account_number TEXT NOT NULL,
                    entry_type TEXT NOT NULL CHECK(entry_type IN ('DEBIT', 'CREDIT')),
                    amount_cents INTEGER NOT NULL CHECK(amount_cents > 0),
                    amount_usd TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    FOREIGN KEY (entry_id) REFERENCES journal_entries(entry_id) ON DELETE RESTRICT
                );
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_jel_entry_id ON journal_entry_lines(entry_id);")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_jel_account ON journal_entry_lines(account_number);")

            # 3. Cleanly migrate legacy table/view for unified reporting
            cursor = conn.execute("SELECT type FROM sqlite_master WHERE name='fact_wallet_transactions';")
            row = cursor.fetchone()
            if row:
                if row["type"] == "view":
                    conn.execute("DROP VIEW fact_wallet_transactions;")
                else:
                    conn.execute("DROP TABLE fact_wallet_transactions;")

            conn.execute("""
                CREATE VIEW fact_wallet_transactions AS
                SELECT 
                    je.transaction_id,
                    je.user_id,
                    je.event_type,
                    CASE 
                        WHEN je.event_type = 'REWARD_EARNED' THEN 'CREDIT' 
                        ELSE 'DEBIT' 
                    END AS direction,
                    je.currency_unit,
                    (SELECT amount_usd FROM journal_entry_lines WHERE entry_id = je.entry_id LIMIT 1) AS gross_amount,
                    CAST((SELECT amount_cents FROM journal_entry_lines WHERE entry_id = je.entry_id LIMIT 1) AS REAL) / 100.0 AS equivalent_usd,
                    0.0 AS running_balance_after,
                    (SELECT account_number FROM journal_entry_lines WHERE entry_id = je.entry_id AND entry_type = 'DEBIT' LIMIT 1) AS debit_account,
                    (SELECT account_number FROM journal_entry_lines WHERE entry_id = je.entry_id AND entry_type = 'CREDIT' LIMIT 1) AS credit_account,
                    0.0000 AS reconciliation_variance,
                    je.status,
                    je.created_at
                FROM journal_entries je;
            """)
        conn.close()


def to_cents(amount_usd: float | Decimal | str) -> int:
    """Converts a USD amount to exact integer cents using Decimal arithmetic."""
    d = Decimal(str(amount_usd)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    return int(d * 100)


def record_double_entry_transaction(
    transaction_id: str,
    user_id: str,
    event_type: str,
    description: str,
    debit_lines: List[Tuple[str, float | Decimal | int]],  # [(account_num, amount_usd_or_cents)]
    credit_lines: List[Tuple[str, float | Decimal | int]], # [(account_num, amount_usd_or_cents)]
    currency_unit: str = "USD"
) -> Dict[str, Any]:
    """
    Atomically posts a balanced double-entry journal entry with distinct debit and credit lines.
    Enforces strict mathematical balance: Sum(Debits) - Sum(Credits) == 0.
    Rejects duplicate transaction IDs with DuplicateTransactionError (no silent overwrite).
    """
    init_persistent_ledger()
    if not debit_lines or not credit_lines:
        raise UnbalancedJournalEntryError("A double-entry transaction must contain at least one debit and one credit line.")

    # Calculate exact integer cents using Decimal precision
    debit_cents_total = 0
    parsed_debit_lines = []
    for acc, amt in debit_lines:
        cents = amt if isinstance(amt, int) else to_cents(amt)
        if cents <= 0:
            raise InvalidPrecisionError(f"Monetary line amounts must be strictly positive: {acc} = {amt}")
        debit_cents_total += cents
        parsed_debit_lines.append((acc, cents, f"{Decimal(cents)/100:.2f}"))

    credit_cents_total = 0
    parsed_credit_lines = []
    for acc, amt in credit_lines:
        cents = amt if isinstance(amt, int) else to_cents(amt)
        if cents <= 0:
            raise InvalidPrecisionError(f"Monetary line amounts must be strictly positive: {acc} = {amt}")
        credit_cents_total += cents
        parsed_credit_lines.append((acc, cents, f"{Decimal(cents)/100:.2f}"))

    # Enforce zero variance between debits and credits
    variance_cents = debit_cents_total - credit_cents_total
    if variance_cents != 0:
        raise UnbalancedJournalEntryError(
            f"Unbalanced journal entry: Total Debits ({debit_cents_total} cents) "
            f"!= Total Credits ({credit_cents_total} cents). Variance: {variance_cents} cents."
        )

    entry_id = f"je_{abs(hash(transaction_id)) % 10000000:07d}"
    ts = datetime.now(timezone.utc).isoformat()

    with _LOCK:
        conn = get_db_connection()
        try:
            with conn:
                # 1. Insert Master Header (Will fail with sqlite3.IntegrityError on duplicate transaction_id)
                try:
                    conn.execute("""
                        INSERT INTO journal_entries (
                            entry_id, transaction_id, user_id, event_type, description, currency_unit, status, created_at
                        ) VALUES (?, ?, ?, ?, ?, ?, 'POSTED', ?)
                    """, (entry_id, transaction_id, user_id, event_type, description, currency_unit, ts))
                except sqlite3.IntegrityError as ie:
                    if "UNIQUE constraint failed" in str(ie) or "transaction_id" in str(ie):
                        raise DuplicateTransactionError(f"Transaction ID '{transaction_id}' already exists in the ledger. Silent replacement is prohibited.") from ie
                    raise

                # 2. Insert Debit Lines
                for i, (acc, cents, usd_str) in enumerate(parsed_debit_lines, 1):
                    line_id = f"{entry_id}_D{i}"
                    conn.execute("""
                        INSERT INTO journal_entry_lines (
                            line_id, entry_id, account_number, entry_type, amount_cents, amount_usd, created_at
                        ) VALUES (?, ?, ?, 'DEBIT', ?, ?, ?)
                    """, (line_id, entry_id, acc, cents, usd_str, ts))

                # 3. Insert Credit Lines
                for i, (acc, cents, usd_str) in enumerate(parsed_credit_lines, 1):
                    line_id = f"{entry_id}_C{i}"
                    conn.execute("""
                        INSERT INTO journal_entry_lines (
                            line_id, entry_id, account_number, entry_type, amount_cents, amount_usd, created_at
                        ) VALUES (?, ?, ?, 'CREDIT', ?, ?, ?)
                    """, (line_id, entry_id, acc, cents, usd_str, ts))

            return {
                "success": True,
                "entry_id": entry_id,
                "transaction_id": transaction_id,
                "total_amount_cents": debit_cents_total,
                "total_amount_usd": f"{Decimal(debit_cents_total)/100:.2f}",
                "debit_lines_count": len(parsed_debit_lines),
                "credit_lines_count": len(parsed_credit_lines),
                "reconciliation_variance_cents": 0,
                "status": "POSTED",
                "timestamp": ts
            }
        finally:
            conn.close()


def record_persistent_transaction(
    transaction_id: str,
    user_id: str,
    event_type: str,
    direction: str,
    currency_unit: str,
    gross_amount: float | Decimal,
    equivalent_usd: float | Decimal,
    running_balance_after: float | Decimal,
    debit_account: str,
    credit_account: str,
    variance: Optional[float] = None, # Deprecated; calculated automatically
    status: str = "SETTLED"
) -> bool:
    """
    High-level transaction recording adapter maintaining backward compatibility.
    Maps parameters to true double-entry journal entries with separate debit and credit lines.
    """
    cents = to_cents(equivalent_usd)
    try:
        record_double_entry_transaction(
            transaction_id=transaction_id,
            user_id=user_id,
            event_type=event_type,
            description=f"{event_type} - {currency_unit} {gross_amount}",
            debit_lines=[(debit_account, cents)],
            credit_lines=[(credit_account, cents)],
            currency_unit="USD"
        )
        return True
    except DuplicateTransactionError:
        raise
    except Exception as e:
        print(f"Ledger persistence error: {e}")
        return False


def fetch_persisted_ledger(limit: int = 50) -> List[Dict[str, Any]]:
    """Retrieves recent posted journal entries and their double-entry accounting lines."""
    init_persistent_ledger()
    conn = get_db_connection()
    try:
        cursor = conn.execute("""
            SELECT 
                je.transaction_id,
                je.entry_id,
                je.user_id,
                je.event_type,
                je.description,
                je.status,
                je.created_at,
                (SELECT GROUP_CONCAT(account_number || ': $' || amount_usd, ', ') 
                 FROM journal_entry_lines 
                 WHERE entry_id = je.entry_id AND entry_type = 'DEBIT') AS debit_breakdown,
                (SELECT GROUP_CONCAT(account_number || ': $' || amount_usd, ', ') 
                 FROM journal_entry_lines 
                 WHERE entry_id = je.entry_id AND entry_type = 'CREDIT') AS credit_breakdown,
                (SELECT SUM(amount_cents) FROM journal_entry_lines WHERE entry_id = je.entry_id AND entry_type = 'DEBIT') AS total_cents
            FROM journal_entries je
            ORDER BY je.created_at DESC
            LIMIT ?
        """, (limit,))
        rows = [dict(row) for row in cursor.fetchall()]
        for r in rows:
            if r["total_cents"]:
                r["equivalent_usd"] = float(Decimal(r["total_cents"]) / 100)
            else:
                r["equivalent_usd"] = 0.0
        return rows
    finally:
        conn.close()


def compute_persisted_account_balances() -> Dict[str, Any]:
    """
    Calculates ledger reconciliation strictly from actual accounting entries in SQL.
    Mathematically computes: Sum(Debits) - Sum(Credits) across all lines.
    Zero variance is mathematically proven from accounting records, not accepted from user input.
    """
    init_persistent_ledger()
    conn = get_db_connection()
    try:
        cursor = conn.execute("""
            SELECT 
                COUNT(DISTINCT entry_id) AS total_entries,
                COUNT(*) AS total_lines,
                COALESCE(SUM(CASE WHEN entry_type = 'DEBIT' THEN amount_cents ELSE 0 END), 0) AS total_debits_cents,
                COALESCE(SUM(CASE WHEN entry_type = 'CREDIT' THEN amount_cents ELSE 0 END), 0) AS total_credits_cents,
                COALESCE(SUM(CASE WHEN entry_type = 'DEBIT' THEN amount_cents ELSE -amount_cents END), 0) AS net_variance_cents
            FROM journal_entry_lines;
        """)
        row = cursor.fetchone()
        
        debits_cents = row["total_debits_cents"]
        credits_cents = row["total_credits_cents"]
        variance_cents = row["net_variance_cents"]

        # Account balances
        acc_cursor = conn.execute("""
            SELECT 
                account_number,
                SUM(CASE WHEN entry_type = 'DEBIT' THEN amount_cents ELSE 0 END) AS debit_cents,
                SUM(CASE WHEN entry_type = 'CREDIT' THEN amount_cents ELSE 0 END) AS credit_cents,
                SUM(CASE 
                    WHEN account_number LIKE '1%' THEN 
                        (CASE WHEN entry_type = 'DEBIT' THEN amount_cents ELSE -amount_cents END)
                    ELSE 
                        (CASE WHEN entry_type = 'CREDIT' THEN amount_cents ELSE -amount_cents END)
                END) AS ending_balance_cents
            FROM journal_entry_lines
            GROUP BY account_number
            ORDER BY account_number;
        """)
        account_summary = {}
        for acc_row in acc_cursor.fetchall():
            account_summary[acc_row["account_number"]] = {
                "debit_usd": f"{Decimal(acc_row['debit_cents'])/100:.2f}",
                "credit_usd": f"{Decimal(acc_row['credit_cents'])/100:.2f}",
                "net_balance_usd": f"{Decimal(acc_row['ending_balance_cents'])/100:.2f}"
            }

        return {
            "total_transactions": row["total_entries"],
            "total_ledger_lines": row["total_lines"],
            "total_debits_usd": round(float(Decimal(debits_cents) / 100), 2),
            "total_credits_usd": round(float(Decimal(credits_cents) / 100), 2),
            "net_variance_cents": variance_cents,
            "cumulative_variance_usd": round(float(Decimal(variance_cents) / 100), 4),
            "is_balanced": variance_cents == 0,
            "account_summary": account_summary
        }
    finally:
        conn.close()
