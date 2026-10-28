#!/usr/bin/env python3
"""
Monthly California city market data for theprestige.luxe city pages (no AI, free public data).

Downloads (inside GitHub Actions, which can reach them):
  - Zillow Home Value Index (ZHVI), city level, all homes, mid tier, smoothed + seasonally adjusted
  - Zillow Observed Rent Index (ZORI), city level
  - Redfin Data Center city market tracker (sales, days on market, inventory...)
Keeps only Memo's target areas and writes data/market/ca_cities.json (small, a few MB at most).

Run:  python tools/ca_city_market.py            (downloads)
      python tools/ca_city_market.py --local DIR (reads zhvi.csv, zori.csv, redfin.tsv.gz from DIR)
"""
import argparse, csv, datetime as dt, gzip, io, json, os, re, sys, urllib.request

ZHVI_URL = "https://files.zillowstatic.com/research/public_csvs/zhvi/City_zhvi_uc_sfrcondo_tier_0.33_0.67_sm_sa_month.csv"
ZORI_URL = "https://files.zillowstatic.com/research/public_csvs/zori/City_zori_uc_sfrcondomfr_sm_month.csv"
RDC_ZIP_URL = "https://econdata.s3-us-west-2.amazonaws.com/Reports/Core/RDC_Inventory_Core_Metrics_Zip.csv"
REDFIN_URL = "https://redfin-public-data.s3.us-west-2.amazonaws.com/redfin_market_tracker/city_market_tracker.tsv000.gz"

# Whole counties (every city / community Zillow tracks in them) ...
COUNTIES = ["Los Angeles County", "Orange County", "Riverside County", "San Bernardino County", "Alameda County"]
# ... plus these single cities (city name -> county)
EXTRA_CITIES = {"Bakersfield": "Kern County", "Fresno": "Fresno County", "San Jose": "Santa Clara County",
                "San Francisco": "San Francisco County", "Sacramento": "Sacramento County"}
OUT = os.path.join(os.path.dirname(__file__), "..", "data", "market", "ca_cities.json")
UA = {"User-Agent": "Mozilla/5.0 (memo-social-bot market data; github.com/memorialdinh/memo-social-bot)"}

def slugify(s): return re.sub(r"-+", "-", re.sub(r"[^a-z0-9]+", "-", s.lower())).strip("-")
def fnum(x):
    try:
        x = (x or "").strip().strip('"')
        return float(x) if x not in ("", "NA", "nan", "None") else None
    except ValueError: return None
def pct(new, old): return round((new / old - 1) * 100, 1) if new and old else None

def fetch(url, path):
    if os.path.exists(path) and os.path.getsize(path) > 1000: return path
    print("downloading", url, flush=True)
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=600) as r, open(path, "wb") as f:
        while True:
            b = r.read(1 << 20)
            if not b: break
            f.write(b)
    print("  ->", path, os.path.getsize(path) // 1_000_000, "MB", flush=True)
    return path

def zillow(path, kind):
    """Returns {(city, county): {...}} for target areas."""
    out = {}
    with open(path, newline="", encoding="utf-8") as f:
        rd = csv.reader(f)
        head = next(rd)
        idx = {h: i for i, h in enumerate(head)}
        dates = [(i, h) for i, h in enumerate(head) if re.fullmatch(r"\d{4}-\d{2}-\d{2}", h)]
        for row in rd:
            if row[idx["State"]] != "CA": continue
            city, county = row[idx["RegionName"]], row[idx["CountyName"]]
            if county not in COUNTIES and EXTRA_CITIES.get(city) != county: continue
            series = [(h, fnum(row[i])) for i, h in dates]
            series = [(h, v) for h, v in series if v]
            if len(series) < 13: continue
            last_d, last_v = series[-1]
            def ago(months):
                return series[-1 - months][1] if len(series) > months else None
            rec = {"date": last_d, "value": round(last_v), "yoy_pct": pct(last_v, ago(12)),
                   "series": [[h, round(v)] for h, v in series[-25:]]}
            if kind == "zhvi":
                rec["five_yr_pct"] = pct(last_v, ago(60))
                rec["metro"] = row[idx["Metro"]]
                rec["size_rank"] = int(fnum(row[idx["SizeRank"]]) or 99999)
            out[(city, county)] = rec
    return out

def redfin(path, wanted_cities):
    """Latest 13 months of 'All Residential' rows for target CA cities from the Redfin city tracker."""
    rows = {}
    with gzip.open(path, "rt", encoding="utf-8", newline="") as f:
        head = [h.strip().strip('"').lower() for h in f.readline().rstrip("\n").split("\t")]
        ix = {h: i for i, h in enumerate(head)}
        need = ["period_begin", "period_end", "city", "state_code", "property_type", "median_sale_price"]
        miss = [n for n in need if n not in ix]
        if miss: sys.exit(f"Redfin columns missing: {miss}. Header: {head[:40]}")
        n = 0
        for line in f:
            if "\tCA\t" not in line and '"CA"' not in line: continue
            c = [x.strip().strip('"') for x in line.rstrip("\n").split("\t")]
            if len(c) < len(head) or c[ix["state_code"]] != "CA": continue
            if c[ix["property_type"]] != "All Residential": continue
            if "is_seasonally_adjusted" in ix and c[ix["is_seasonally_adjusted"]].lower() in ("true", "t", "1"): continue
            city = c[ix["city"]]
            if city not in wanted_cities: continue
            n += 1
            metro = c[ix["parent_metro_region"]] if "parent_metro_region" in ix else ""
            rows.setdefault((city, metro), []).append({h: c[i] for h, i in ix.items()})
        print("redfin CA rows kept:", n, "cities:", len(rows), flush=True)
    out = {}
    for (city, metro), rs in rows.items():
        rs.sort(key=lambda r: r["period_end"])
        dur = max({r.get("period_duration", "") for r in rs}, key=lambda d: sum(1 for r in rs if r.get("period_duration", "") == d))
        rs = [r for r in rs if r.get("period_duration", "") == dur]
        last = rs[-1]
        g = lambda k: fnum(last.get(k))
        yoy_row = next((r for r in rs if r["period_end"][:7] == f"{int(last['period_end'][:4]) - 1}{last['period_end'][4:7]}"), None)
        rec = {"period_begin": last["period_begin"], "period_end": last["period_end"], "period_days": dur,
               "metro": last.get("parent_metro_region", ""),
               "median_sale_price": g("median_sale_price"), "median_sale_price_yoy": g("median_sale_price_yoy"),
               "median_list_price": g("median_list_price"), "median_ppsf": g("median_ppsf"),
               "homes_sold": g("homes_sold"), "homes_sold_yoy": g("homes_sold_yoy"),
               "pending_sales": g("pending_sales"), "new_listings": g("new_listings"),
               "inventory": g("inventory"), "inventory_yoy": g("inventory_yoy"), "months_of_supply": g("months_of_supply"),
               "median_dom": g("median_dom"), "median_dom_yoy": g("median_dom_yoy"),
               "avg_sale_to_list": g("avg_sale_to_list"), "sold_above_list": g("sold_above_list"),
               "price_drops": g("price_drops"), "off_market_in_two_weeks": g("off_market_in_two_weeks"),
               "last_updated": last.get("last_updated", ""),
               "price_series": [[r["period_end"], fnum(r.get("median_sale_price"))] for r in rs[-13:]]}
        if yoy_row: rec["median_dom_year_ago"] = fnum(yoy_row.get("median_dom"))
        out.setdefault(city, []).append(rec)
    return out

# ZIPs whose USPS postal name is a neighboring city but that cover a whole city of their own
ZIP_CITY = {"92880": "Eastvale", "92587": "Canyon Lake"}
# Realtor.com postal names spelled differently from the Zillow place name
ZIP_NAME_ALIAS = {"whitewater": "White Water"}

def realtor_zip(path, wanted_cities):
    """Realtor.com monthly inventory by ZIP, grouped by the ZIP's postal city ("long beach, ca")."""
    out = {}
    low = {c.lower(): c for c in wanted_cities}
    with open(path, newline="", encoding="utf-8", errors="replace") as f:
        rd = csv.DictReader(f)
        for r in rd:
            zn = (r.get("zip_name") or "").strip().lower()
            if not zn.endswith(", ca"): continue
            pc = (r.get("postal_code") or "").zfill(5)
            city = ZIP_CITY.get(pc) or ZIP_NAME_ALIAS.get(zn[:-4].strip()) or low.get(zn[:-4].strip())
            if city not in wanted_cities: continue
            if not city: continue
            # quality_flag=1: Realtor.com says this ZIP's year-over-year change is unreliable (source or method change).
            # Keep the current-month figures, drop only the year-over-year comparisons.
            flagged = (r.get("quality_flag") or "0").strip() not in ("0", "", "0.0")
            g = lambda k: None if flagged and k.endswith("_yy") else fnum(r.get(k))
            out.setdefault(city, []).append({"q": flagged,
                "zip": (r.get("postal_code") or "").zfill(5), "month": r.get("month_date_yyyymm"),
                "median_listing_price": g("median_listing_price"), "median_listing_price_yy": g("median_listing_price_yy"),
                "active": g("active_listing_count"), "active_yy": g("active_listing_count_yy"),
                "median_dom": g("median_days_on_market"), "median_dom_yy": g("median_days_on_market_yy"),
                "new": g("new_listing_count"), "price_reduced": g("price_reduced_count"), "pending": g("pending_listing_count"),
                "ppsf": g("median_listing_price_per_square_foot"), "sqft": g("median_square_feet")})
    res = {}
    for city, zs in out.items():
        zs.sort(key=lambda z: -(z["active"] or 0))
        act = sum(z["active"] or 0 for z in zs)
        def tot(k): return sum(z[k] or 0 for z in zs)
        # last year's active count from each ZIP's own year-over-year change (exact sum)
        # (only over ZIPs with a reliable comparison, so a flagged ZIP never skews the city's change)
        cmp = [z for z in zs if z["active"] and z["active_yy"] is not None and z["active_yy"] > -1]
        prev = sum(z["active"] / (1 + z["active_yy"]) for z in cmp)
        act_cmp = sum(z["active"] for z in cmp)
        res[city] = {"month": zs[0]["month"], "zip_count": len(zs), "active": round(act), "new": round(tot("new")),
                     "pending": round(tot("pending")), "price_reduced": round(tot("price_reduced")),
                     "price_reduced_share": round(tot("price_reduced") / act * 100, 1) if act else None,
                     "active_yoy_pct": round((act_cmp / prev - 1) * 100, 1) if prev and act_cmp >= act / 2 else None, "zips": zs}
    return res

# ---------- U.S. Census Bureau, American Community Survey (keyless summary files on www2.census.gov) ----------
ACS_BASE = "https://www2.census.gov/programs-surveys/acs/summary_file/{y}/table-based-SF/data/5YRData/acsdt5y{y}-{t}.dat"
PLACE_COUNTY_URL = "https://www2.census.gov/geo/docs/reference/codes2020/place_by_cou/st06_ca_place_by_county2020.txt"
ACS_TABLES = ["b25077", "b25064", "b25003", "b25035", "b25001"]

def norm(s):
    import unicodedata
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", " ", s).strip()

def acs_places(d):
    """{(normalized place name, county): {...}} for California places, latest ACS 5-year release available."""
    year = None
    for y in range(dt.date.today().year - 1, dt.date.today().year - 4, -1):
        try:
            fetch(ACS_BASE.format(y=y, t="b25077"), os.path.join(d, f"acs{y}-b25077.dat")); year = y; break
        except Exception as e:
            print(f"ACS {y} not available: {e}", flush=True)
    if not year: return None, {}
    vals = {}
    for t in ACS_TABLES:
        p = fetch(ACS_BASE.format(y=year, t=t), os.path.join(d, f"acs{year}-{t}.dat"))
        with open(p, encoding="utf-8", errors="replace") as f:
            head = f.readline().rstrip("\n").split("|")
            for line in f:
                if not line.startswith("1600000US06"): continue
                c = line.rstrip("\n").split("|")
                vals.setdefault(c[0], {}).update({h: c[i] for i, h in enumerate(head) if i})
    pc = fetch(PLACE_COUNTY_URL, os.path.join(d, "place_by_county.txt"))
    out = {}
    with open(pc, encoding="utf-8", errors="replace") as f:
        rd = csv.DictReader(f, delimiter="|")
        for r in rd:
            gid = "1600000US06" + r["PLACEFP"]
            v = vals.get(gid)
            if not v: continue
            full = r["PLACENAME"]
            short = re.sub(r"\s+(city|town|CDP)$", "", full)
            def num(k):
                x = fnum(v.get(k))
                return None if x is None or x < 0 else x
            def moe(k):
                x = fnum(v.get(k))
                return None if x is None or x < 0 else x
            occ, own = num("B25003_E001"), num("B25003_E002")
            rec = {"geo_id": gid, "name": full, "year": year, "range": f"{year - 4}-{year}",
                   "median_value": num("B25077_E001"), "median_value_moe": moe("B25077_M001"), "median_value_topcoded": v.get("B25077_E001") == "2000001",
                   "median_rent": num("B25064_E001"), "median_rent_moe": moe("B25064_M001"), "median_rent_topcoded": v.get("B25064_E001") == "3501",
                   "occupied_units": occ, "owner_units": own, "renter_units": num("B25003_E003"),
                   "owner_share": round(own / occ * 100, 1) if occ and own is not None else None,
                   "median_year_built": num("B25035_E001"), "housing_units": num("B25001_E001")}
            out[(norm(short), r["COUNTYNAME"])] = rec
    print(f"ACS {year} 5-year: {len(out)} California place/county pairs", flush=True)
    return year, out

# ---------- California Association of REALTORS monthly Home Sales and Price Report (county table) ----------
CAR_LIST = "https://www.car.org/aboutus/mediacenter/newsreleases"
BROWSER_UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36"}

def get_html(url):
    req = urllib.request.Request(url, headers=BROWSER_UA)
    with urllib.request.urlopen(req, timeout=90) as r: return r.read().decode("utf-8", "replace")

def car_counties(counties):
    """Latest C.A.R. monthly report: county median sold price (existing single-family), sales change, UII, days on market."""
    from html.parser import HTMLParser
    class T(HTMLParser):
        def __init__(s): super().__init__(); s.tables, s.row, s.cell, s.inrow, s.incell = [], None, "", False, False
        def handle_starttag(s, tag, a):
            if tag == "table": s.tables.append([])
            elif tag == "tr" and s.tables: s.row = []
            elif tag in ("td", "th") and s.row is not None: s.incell, s.cell = True, ""
        def handle_endtag(s, tag):
            if tag in ("td", "th") and s.incell: s.row.append(re.sub(r"\s+", " ", s.cell).strip()); s.incell = False
            elif tag == "tr" and s.row is not None and s.tables: s.tables[-1].append(s.row); s.row = None
        def handle_data(s, d):
            if s.incell: s.cell += d
    lst = get_html(CAR_LIST)
    links = re.findall(r'href="([^"]*/newsreleases/20\d\dreleases/[^"]*sales[^"]*)"', lst, re.I)
    links = [l for l in dict.fromkeys(links) if not re.search(r"forecast|qtr|hai", l, re.I)]
    if not links: raise RuntimeError("no C.A.R. sales release link found")
    url = links[0] if links[0].startswith("http") else "https://www.car.org" + links[0]
    url = url.replace("/en/aboutus", "/aboutus")
    p = T(); p.feed(get_html(url))
    if len(p.tables) < 2: raise RuntimeError(f"C.A.R. release has {len(p.tables)} tables")
    price, pace = p.tables[0], p.tables[1]
    month = (price[0][0] if price and price[0] else "").strip()
    if not re.fullmatch(r"[A-Z][a-z]+ 20\d\d", month): raise RuntimeError(f"unexpected C.A.R. table header {price[0][:2]}")
    money = lambda x: fnum(re.sub(r"[$,]", "", x or ""))
    pc = lambda x: fnum((x or "").replace("%", ""))
    def find(tab, name):
        return next((r for r in tab if r and r[0] == name and len(r) > 5 and r[1]), None)
    out = {}
    for county in counties:
        short = county.replace(" County", "")
        a, b = find(price, short), find(pace, short)
        if not a: continue
        rec = {"median": money(a[1]), "median_prev_month": money(a[2]), "median_year_ago": money(a[4]),
               "price_mtm_pct": pc(a[-4]), "price_yoy_pct": pc(a[-3]), "sales_mtm_pct": pc(a[-2]), "sales_yoy_pct": pc(a[-1])}
        if b:
            nums = [fnum(x) for x in b[1:] if x not in ("", "r")]
            if len(nums) >= 6:
                rec.update({"uii": nums[0], "uii_year_ago": nums[2], "dom": nums[3], "dom_year_ago": nums[5]})
        out[county] = rec
    state = find(price, "Calif. Single-family home")
    print(f"C.A.R. {month}: {len(out)} counties from {url}", flush=True)
    return {"month": month, "url": url, "name": f"California Association of REALTORS®, {month} Home Sales and Price Report",
            "property": "existing single-family homes", "state_median": money(state[1]) if state else None,
            "state_yoy_pct": pc(state[-3]) if state else None, "counties": out}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--local"); ap.add_argument("--work", default="/tmp/ca-market")
    a = ap.parse_args()
    d = a.local or a.work; os.makedirs(d, exist_ok=True)
    kp = os.path.join(d, "rdc_zip.csv"); zp = os.path.join(d, "zhvi.csv"); rp = os.path.join(d, "zori.csv"); fp = os.path.join(d, "redfin.tsv.gz")
    if not a.local:
        fetch(ZHVI_URL, zp); fetch(ZORI_URL, rp); fetch(RDC_ZIP_URL, kp)
        try: fetch(REDFIN_URL, fp)
        except Exception as e: print("redfin download failed (optional):", e)
    zhvi = zillow(zp, "zhvi")
    zori = zillow(rp, "zori") if os.path.exists(rp) else {}
    print("zillow target places:", len(zhvi), flush=True)
    if len(zhvi) < 100: sys.exit(f"Only {len(zhvi)} places matched; Zillow file format may have changed. Not overwriting data.")
    names = {c for c, _ in zhvi}
    rf = redfin(fp, names) if os.path.exists(fp) else {}
    rdc = realtor_zip(kp, names) if os.path.exists(kp) else {}
    print("realtor.com cities matched:", len(rdc), flush=True)
    all_counties = COUNTIES + sorted(set(EXTRA_CITIES.values()))
    prev = {}
    try: prev = json.load(open(OUT))
    except Exception: pass
    try: acs_year, acs = acs_places(d)
    except Exception as e:
        print("::warning::Census ACS download failed; keeping last month's Census figures:", e, flush=True)
        acs_year, acs = None, {}
    prev_acs = {c["slug"]: c.get("acs") for c in prev.get("cities", []) if c.get("acs")}
    try: car = car_counties(all_counties)
    except Exception as e:
        print("::warning::C.A.R. report not parsed; keeping the last one:", e, flush=True)
        car = prev.get("car")
    today = dt.date.today()
    cities = []
    for (city, county), z in zhvi.items():
        cands = rf.get(city) or []
        r = None
        if len(cands) == 1: r = cands[0]
        elif cands:
            hint = (z.get("metro", "") + " " + county).lower()
            r = next((x for x in cands if x.get("metro") and x["metro"].split(",")[0].split("-")[0].lower() in hint), None)
        cities.append({"name": city, "slug": slugify(city), "county": county, "metro": z.get("metro", ""),
                       "size_rank": z.get("size_rank"), "zhvi": z, "zori": zori.get((city, county)), "redfin": r,
                       "realtor": rdc.get(city)})
        if r: r["stale"] = (today - dt.date.fromisoformat(r["period_end"][:10])).days > 120
    # duplicate city names in different target counties get the county in the slug
    seen = {}
    for c in cities: seen[c["slug"]] = seen.get(c["slug"], 0) + 1
    for c in cities:
        if seen[c["slug"]] > 1: c["slug"] = slugify(c["name"] + " " + c["county"].replace(" County", ""))
    for c in cities:
        c["acs"] = acs.get((norm(c["name"]), c["county"])) if acs else prev_acs.get(c["slug"])
    print("places with Census ACS data:", sum(1 for c in cities if c.get("acs")), flush=True)
    cities.sort(key=lambda c: (c["county"], c["name"]))
    zdate = max(c["zhvi"]["date"] for c in cities)
    rdate = max((c["redfin"]["period_end"] for c in cities if c["redfin"]), default="")
    data = {"generated_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
            "sources": {"realtor": {"name": "Realtor.com Residential Data, monthly inventory by ZIP code", "url": "https://www.realtor.com/research/data/",
                                    "through": max((c["realtor"]["month"] for c in cities if c.get("realtor")), default="")},
                        "zhvi": {"name": "Zillow Home Value Index (ZHVI), all homes, mid-tier, smoothed & seasonally adjusted", "url": "https://www.zillow.com/research/data/", "through": zdate},
                        "zori": {"name": "Zillow Observed Rent Index (ZORI), all homes", "url": "https://www.zillow.com/research/data/"},
                        "redfin": {"name": "Redfin Data Center, city market tracker (all residential)", "url": "https://www.redfin.com/news/data-center/", "through": rdate},
                        "acs": {"name": "U.S. Census Bureau, American Community Survey 5-year estimates", "url": "https://data.census.gov/",
                                "range": next((c["acs"]["range"] for c in cities if c.get("acs")), "")},
                        "car": {"name": (car or {}).get("name", ""), "url": (car or {}).get("url", "")}},
            "car": car, "counties": all_counties, "cities": cities}
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(data, open(OUT, "w"), separators=(",", ":"))
    print(f"wrote {OUT}: {len(cities)} places, {sum(1 for c in cities if c['redfin'])} with Redfin sales data; ZHVI through {zdate}, Redfin through {rdate}")

if __name__ == "__main__":
    main()
