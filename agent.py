"""Recalculate invoice lines and compare them with caller-stated totals."""
import math

def _num(value, name, low=0, high=1e12):
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(float(value)):
        raise ValueError(name + " must be a finite number")
    value=float(value)
    if value < low or value > high: raise ValueError(name + " is outside bounds")
    return value

def analyze(payload: dict) -> dict:
    if not isinstance(payload, dict): raise ValueError("payload must be an object")
    lines=payload.get("lines")
    if not isinstance(lines,list) or not lines or len(lines)>1000: raise ValueError("lines must be a non-empty bounded list")
    stated=_num(payload.get("stated_total"),"stated_total")
    tolerance=_num(payload.get("tolerance",.01),"tolerance",0,1000)
    seen=set(); details=[]; subtotal=0.0; tax=0.0
    for line in lines:
        if not isinstance(line,dict) or set(line)!={"id","quantity","unit_price","tax_rate"}: raise ValueError("invalid invoice line shape")
        ident=line["id"]
        if not isinstance(ident,str) or not ident.strip() or ident in seen: raise ValueError("line ids must be unique non-empty strings")
        seen.add(ident); qty=_num(line["quantity"],"quantity"); price=_num(line["unit_price"],"unit_price"); rate=_num(line["tax_rate"],"tax_rate",0,1)
        base=qty*price; line_tax=base*rate; subtotal+=base; tax+=line_tax
        details.append({"id":ident,"subtotal":round(base,2),"tax":round(line_tax,2),"total":round(base+line_tax,2)})
    calculated=round(subtotal+tax,2); difference=round(stated-calculated,2); matches=abs(difference)<=tolerance
    return {"status":"match" if matches else "mismatch","calculated_subtotal":round(subtotal,2),"calculated_tax":round(tax,2),
            "calculated_total":calculated,"stated_total":stated,"difference":difference,"within_tolerance":matches,
            "lines":details,"basis":"sum(quantity * unit_price * (1 + tax_rate)), rounded to two decimals at invoice total"}
