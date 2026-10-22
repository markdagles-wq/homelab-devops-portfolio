#!/usr/bin/env python3
import pandas as pd
import os
import json

# Cesty k souborům vzhledem ke kořenu projektu (/app/)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
EXCEL_PATH = os.path.join(BASE_DIR, 'finance.xlsx')
CACHE_SUMMARY_PATH = os.path.join(BASE_DIR, 'core', 'ai_financial_context.txt')
METRICS_JSON_PATH = os.path.join(BASE_DIR, 'core', 'finance_metrics.json')

def analyze_finances():
    metrics = {"cashflow": "Zatím bez dat", "ico_income": 0, "assets": 0, "expenses": 0}
    
    if not os.path.exists(EXCEL_PATH) or os.path.getsize(EXCEL_PATH) == 0:
        print(f"[INFO] Soubor {EXCEL_PATH} nebyl nalezen nebo je prázdný.")
        os.makedirs(os.path.dirname(METRICS_JSON_PATH), exist_ok=True)
        with open(METRICS_JSON_PATH, 'w', encoding='utf-8') as jf:
            json.dump(metrics, jf, ensure_ascii=False)
        return

    try:
        xls = pd.ExcelFile(EXCEL_PATH)
        sheet_names = xls.sheet_names
        
        target_sheet = 'Osobni_CashFlow' if 'Osobni_CashFlow' in sheet_names else sheet_names[0]
        df = pd.read_excel(EXCEL_PATH, sheet_name=target_sheet)
        df.columns = df.columns.str.strip()
        df = df.dropna(subset=[df.columns[0]])

        monthly_details = []
        for index, row in df.iterrows():
            datum = str(row.iloc[0])
            row_str = f"Měsíc: {datum}"
            for col in df.columns:
                val = row[col]
                if pd.notna(val) and col.lower() in ['euro', 'status', 'hlav. příjem', 'vedl.příj.', 'rozdíl', 'czkbank']:
                    row_str += f" | {col}: {val}"
            monthly_details.append(row_str)

        total_ico = 0
        if 'ICO_Prijmy' in sheet_names:
            df_prijmy = pd.read_excel(EXCEL_PATH, sheet_name='ICO_Prijmy')
            df_prijmy.columns = df_prijmy.columns.str.strip()
            if 'Castka_CZK' in df_prijmy.columns:
                total_ico = float(pd.to_numeric(df_prijmy['Castka_CZK'], errors='coerce').fillna(0).sum())

        posledni_euro = "Neznámé"
        posledni_status = "Neznámý"
        
        euro_cols = [c for c in df.columns if 'euro' in c.lower()]
        status_cols = [c for c in df.columns if 'status' in c.lower()]
        
        if euro_cols and not df.empty:
            posledni_euro = str(df[euro_cols[0]].iloc[-1])
        if status_cols and not df.empty:
            posledni_status = str(df[status_cols[0]].iloc[-1])

        # Uložení metrik s čistými Python typy
        metrics = {
            "cashflow": str(posledni_status),
            "ico_income": float(total_ico),
            "assets": 0,
            "expenses": 0
        }
        
        os.makedirs(os.path.dirname(METRICS_JSON_PATH), exist_ok=True)
        with open(METRICS_JSON_PATH, 'w', encoding='utf-8') as jf:
            json.dump(metrics, jf, ensure_ascii=False)

        context_text = f"""[FINANČNÍ MATICE Z EXCELU]
- Poslední stav EUREK: {posledni_euro}
- Poslední STATUS účtu: {posledni_status}
- Celkové IČO příjmy: {total_ico:,.2f} Kč

[MĚSÍČNÍ ČASOVÁ ŘADA]:
""" + "\n".join(monthly_details)

        os.makedirs(os.path.dirname(CACHE_SUMMARY_PATH), exist_ok=True)
        with open(CACHE_SUMMARY_PATH, 'w', encoding='utf-8') as f:
            f.write(context_text)
            
        print("[OK] Data z Excelu úspěšně zpracována a uložena.")

    except Exception as e:
        print(f"[CHYBA při čtení Excelu]: {e}")

if __name__ == "__main__":
    analyze_finances()
