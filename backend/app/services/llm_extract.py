from typing import Any, Dict, List
import json
import re
from tenacity import retry, stop_after_attempt, wait_fixed
from .templates import get_template_field_order, get_all_template_fields
from ..settings import is_mock_llm_enabled, get_openai_api_key
import os


def _build_prompt(pdf_text: str, template: Dict[str, Any]) -> str:
    template_id = template.get("templateId", "template")
    
    if template.get("multiSheet", False) and "sheets" in template:
        # Multi-sheet template
        prompt = (
            "You are a data extraction expert for private equity fund data.\n"
            f"Extract data from this PDF text according to {template_id} template.\n\n"
            "The template has multiple sheets with the following structure:\n\n"
        )
        
        for i, sheet in enumerate(template.get("sheets", []), 1):
            sheet_name = sheet.get("name", f"Sheet {i}")
            description = sheet.get("description", "")
            fields = [field["key"] for field in sheet.get("fields", [])]
            
            prompt += f"{i}. {sheet_name}\n"
            prompt += f"   Description: {description}\n"
            prompt += f"   Fields: {', '.join(fields)}\n\n"
        
        prompt += (
            "Extract all relevant data and organize it by sheet. "
            "For each field, provide the extracted value or empty string if not found.\n"
            "Output only valid JSON with all field keys from all sheets.\n"
            "PDF Text:\n" + pdf_text[:15000]
        )
    else:
        # Single-sheet template (legacy)
        fields = get_template_field_order(template)
        field_list = "\n".join([f"- {k}" for k in fields])
        prompt = (
            "You are a data extraction expert.\n"
            f"Extract the following fields from this PDF text according to {template_id}:\n"
            f"{field_list}\n\n"
            "Output only valid JSON (no markdown), with keys matching the fields.\n"
            "If a field is missing, use an empty string.\n"
            "PDF Text:\n" + pdf_text[:15000]
        )
    
    return prompt


def _mock_extract(pdf_text: str, template: Dict[str, Any]) -> Dict[str, Any]:
    result: Dict[str, Any] = {}
    for key in get_template_field_order(template):
        result[key] = ""  # deterministic empty values for demo
    return result


@retry(stop=stop_after_attempt(3), wait=wait_fixed(1))
def _call_openai(prompt: str) -> str:
    # Minimal httpx call to OpenAI Chat Completions (gpt-4o-mini as example)
    import httpx

    api_key = get_openai_api_key()
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY not set")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }
    model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": "You output strict JSON only."},
            {"role": "user", "content": prompt},
        ],
        "temperature": 0.0,
    }
    with httpx.Client(timeout=60) as client:
        resp = client.post("https://api.openai.com/v1/chat/completions", headers=headers, json=body)
        resp.raise_for_status()
        data = resp.json()
        content = data["choices"][0]["message"]["content"]
        return content


def _clean_json_response(text: str) -> Dict[str, Any]:
    # Strip common wrappers and parse JSON
    s = text.strip()
    if s.startswith("```"):
        # remove markdown fences if present
        s = s.strip("`")
        # naive split to last json content
        if "{" in s and "}" in s:
            s = s[s.find("{") : s.rfind("}") + 1]
    # try parse
    try:
        return json.loads(s)
    except Exception:
        # last resort: empty dict
        return {}


def _coerce_to_template(data: Dict[str, Any], template: Dict[str, Any]) -> Dict[str, Any]:
    coerced: Dict[str, Any] = {}
    for key in get_template_field_order(template):
        value = data.get(key, "")
        if value is None:
            value = ""
        if not isinstance(value, (str, int, float)):
            value = str(value)
        coerced[key] = value
    return coerced


def _rule_based_extract(pdf_text: str, template: Dict[str, Any]) -> Dict[str, Any]:
    # For template1, we need to create the specific template structure rows
    template_id = template.get("templateId", "")
    
    if template_id == "template1":
        # Create the template structure as shown in the image
        template_rows = [
            {
                "number": "1",
                "tab": "Fund and Investment Vehicle Information",
                "description": "Standard details about the Fund, Fund Partnership, and Investment Vehicle. While much of this data may be static, updates might be needed during fundraising or if the fund's term is extended."
            },
            {
                "number": "2", 
                "tab": "Fund Manager",
                "description": "Standard details about the Manager (GP) who is running the fund. Much of this data is static"
            },
            {
                "number": "3",
                "tab": "Fund Investment Vehicle Financial Position", 
                "description": "Investment Vehicle is the last layer in the financial structure that is used to deploy the funds into a company or investment. Current cumulative financial position of the Investment Vehicle as of the reporting date. Requires quarterly updates."
            },
            {
                "number": "4",
                "tab": "LP Investor cashflows",
                "description": "Comprehensive list of transactions between the Investment Vehicle and its investors, including quarterly Net Asset Values post carried interest deduction."
            },
            {
                "number": "5",
                "tab": "Fund Companies",
                "description": "Key details of the companies in which the fund has invested. Include realized investments. Updates required for new investments."
            },
            {
                "number": "6",
                "tab": "Initial Investments",
                "description": "Positions of the Investment Vehicle in invested companies as of the investment date. Must include all realized investments with data as of the reporting date. Updates required for new investments."
            },
            {
                "number": "7",
                "tab": "Company Investment Positions",
                "description": "Current positions in invested companies as of the reporting date. Include realized investments with relevant data. Requires quarterly updates."
            },
            {
                "number": "8",
                "tab": "Company Valuation",
                "description": "Valuation details of companies at the current reporting or exit date."
            },
            {
                "number": "9",
                "tab": "Company Financials",
                "description": "Most recent profit & loss, balance sheet, and debt maturity information."
            },
            {
                "number": "10",
                "tab": "Investment History",
                "description": "Full list of historical transactions between the Investment Vehicle and portfolio companies, including investment amounts, distributions, and valuations. Further transaction-level details are encouraged."
            },
            {
                "number": "14",
                "tab": "Reference Values",
                "description": "List of accepted values for dropdown fields (e.g., countries, currencies)."
            }
        ]
        
        # Return the first row (we'll handle multiple rows in the main extraction function)
        return template_rows[0]
    
    # For other templates, use the original logic
    text = pdf_text or ""
    lower = text.lower()
    result: Dict[str, Any] = {}

    # Common regexes
    email_match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", text)
    currency_match = re.search(r"\b(USD|EUR|GBP|INR|AED|JPY|CHF|CNY|AUD|CAD)\b", text, re.IGNORECASE)
    symbol_match = re.search(r"[€£$]", text)
    # Amount candidates (pick the largest-looking number)
    amount_candidates = [m.group(0) for m in re.finditer(r"\b\$?\s?(\d{1,3}(,\d{3})+|\d+)(\.\d+)?\b", text)]
    amount_value = next(iter(amount_candidates), "")

    # Date candidates
    date_patterns = [
        r"\b\d{4}-\d{2}-\d{2}\b",  # 2025-10-13
        r"\b\d{2}/\d{2}/\d{4}\b",  # 13/10/2025
        r"\b\d{2}-\d{2}-\d{4}\b",
        r"\b(?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2},\s+\d{4}\b",
    ]
    date_value = ""
    for p in date_patterns:
        m = re.search(p, text, re.IGNORECASE)
        if m:
            date_value = m.group(0)
            break

    # Heuristics for names
    fund_line = next((ln for ln in text.splitlines() if re.search(r"\bFund\b", ln)), "")
    manager_line = next((ln for ln in text.splitlines() if re.search(r"\bManager\b|General Partner|Investment Manager", ln, re.IGNORECASE)), "")
    investor_line = next((ln for ln in text.splitlines() if re.search(r"\bInvestor\b|Limited Partner|LP\b", ln, re.IGNORECASE)), "")

    # Template-driven population
    for key in get_template_field_order(template):
        v = ""
        if key in ("contact_email", "email", "manager_email") and email_match:
            v = email_match.group(0)
        elif key in ("currency",):
            v = (currency_match.group(0).upper() if currency_match else ("USD" if symbol_match and symbol_match.group(0) == "$" else ""))
        elif key in ("total_commitment", "commitment_amount", "call_amount", "amount"):
            v = amount_value
        elif key in ("report_date", "date", "statement_date"):
            v = date_value
        elif key in ("fund_name",):
            v = fund_line.strip()[:120]
        elif key in ("manager",):
            v = re.sub(r".*?:\s*", "", manager_line).strip()[:120] if manager_line else ""
        elif key in ("investor_name",):
            v = re.sub(r".*?:\s*", "", investor_line).strip()[:120] if investor_line else ""
        result[key] = v
    return result


def extract_structured_data(pdf_text: str, template: Dict[str, Any]) -> List[Dict[str, Any]]:
    template_id = template.get("templateId", "")
    
    # Special handling for template1 - return multiple rows for the template structure
    if template_id == "template1":
        template_rows = [
            {
                "number": "1",
                "tab": "Fund and Investment Vehicle Information",
                "description": "Standard details about the Fund, Fund Partnership, and Investment Vehicle. While much of this data may be static, updates might be needed during fundraising or if the fund's term is extended."
            },
            {
                "number": "2", 
                "tab": "Fund Manager",
                "description": "Standard details about the Manager (GP) who is running the fund. Much of this data is static"
            },
            {
                "number": "3",
                "tab": "Fund Investment Vehicle Financial Position", 
                "description": "Investment Vehicle is the last layer in the financial structure that is used to deploy the funds into a company or investment. Current cumulative financial position of the Investment Vehicle as of the reporting date. Requires quarterly updates."
            },
            {
                "number": "4",
                "tab": "LP Investor cashflows",
                "description": "Comprehensive list of transactions between the Investment Vehicle and its investors, including quarterly Net Asset Values post carried interest deduction."
            },
            {
                "number": "5",
                "tab": "Fund Companies",
                "description": "Key details of the companies in which the fund has invested. Include realized investments. Updates required for new investments."
            },
            {
                "number": "6",
                "tab": "Initial Investments",
                "description": "Positions of the Investment Vehicle in invested companies as of the investment date. Must include all realized investments with data as of the reporting date. Updates required for new investments."
            },
            {
                "number": "7",
                "tab": "Company Investment Positions",
                "description": "Current positions in invested companies as of the reporting date. Include realized investments with relevant data. Requires quarterly updates."
            },
            {
                "number": "8",
                "tab": "Company Valuation",
                "description": "Valuation details of companies at the current reporting or exit date."
            },
            {
                "number": "9",
                "tab": "Company Financials",
                "description": "Most recent profit & loss, balance sheet, and debt maturity information."
            },
            {
                "number": "10",
                "tab": "Investment History",
                "description": "Full list of historical transactions between the Investment Vehicle and portfolio companies, including investment amounts, distributions, and valuations. Further transaction-level details are encouraged."
            },
            {
                "number": "14",
                "tab": "Reference Values",
                "description": "List of accepted values for dropdown fields (e.g., countries, currencies)."
            }
        ]
        return template_rows
    
    # Special handling for template2 - return multiple rows for the template structure
    if template_id == "template2":
        template_rows = [
            {
                "number": "1",
                "tab": "Executive Portfolio Summary",
                "description": ""
            },
            {
                "number": "2",
                "tab": "Schedule of Investments",
                "description": "The schedule of investments allows"
            },
            {
                "number": "3",
                "tab": "Statement of Operations",
                "description": ""
            },
            {
                "number": "4",
                "tab": "Statements of Cashflows",
                "description": ""
            },
            {
                "number": "5",
                "tab": "PCAP Statements",
                "description": ""
            },
            {
                "number": "6",
                "tab": "Portfolio Companies Profile",
                "description": ""
            },
            {
                "number": "7",
                "tab": "Portfolio Companies Financials",
                "description": ""
            },
            {
                "number": "8",
                "tab": "FootNotes",
                "description": "To fully support the balance sheet and other reporting schedules, a complete and"
            },
            {
                "number": "9",
                "tab": "Reference Values",
                "description": ""
            }
        ]
        return template_rows
    
    # For other templates, return single row as before
    if is_mock_llm_enabled():
        # Use deterministic rule-based extraction in mock mode for more useful outputs
        data = _rule_based_extract(pdf_text, template)
        return [_coerce_to_template(data, template)]

    prompt = _build_prompt(pdf_text, template)
    try:
        raw = _call_openai(prompt)
        parsed = _clean_json_response(raw)
        # If model returns nothing or missing keys, fall back
        if not isinstance(parsed, dict) or not parsed:
            raise ValueError("LLM returned empty/invalid JSON")
        coerced = _coerce_to_template(parsed, template)
        if all(v == "" for v in coerced.values()):
            raise ValueError("LLM returned empty fields")
        return [coerced]
    except Exception:
        # Try Gemini if key provided
        try:
            import google.generativeai as genai  # type: ignore
            gemini_key = os.getenv("GEMINI_API_KEY")
            if gemini_key:
                genai.configure(api_key=gemini_key)
                model_name = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
                model = genai.GenerativeModel(model_name)
                resp = model.generate_content(prompt)
                content = resp.text or "{}"
                parsed = _clean_json_response(content)
                coerced = _coerce_to_template(parsed, template)
                if any(v for v in coerced.values()):
                    return [coerced]
        except Exception:
            pass

        rb = _rule_based_extract(pdf_text, template)
        return [_coerce_to_template(rb, template)]


