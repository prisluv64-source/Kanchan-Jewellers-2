from pathlib import Path

path = Path("styles.css")
css = path.read_text(encoding="utf-8")
marker = "/* ===== SINGLE-LINE LEFT-ALIGNED DESKTOP NAV ===== */"

if marker in css:
    print("Desktop nav fix already present.")
    raise SystemExit(0)

fix = r'''

/* ===== SINGLE-LINE LEFT-ALIGNED DESKTOP NAV ===== */
@media (min-width: 769px) {
  .main-nav {
    max-width: none !important;
    width: 100% !important;
    margin: 0 !important;
    padding: 0 6px 12px !important;
    gap: 0 !important;
    flex-wrap: nowrap !important;
    justify-content: flex-start !important;
    align-items: center !important;
    font-size: 0.82rem !important;
    white-space: nowrap !important;
  }

  .main-nav > a,
  .main-nav > .nav-item {
    flex: 0 0 auto !important;
    white-space: nowrap !important;
    margin-right: 25px !important;
  }

  .main-nav > a:last-child,
  .main-nav > .nav-item:last-child {
    margin-right: 0 !important;
  }

  .main-nav .nav-link,
  .main-nav .nav-direct {
    white-space: nowrap !important;
  }
}
'''

path.write_text(css + fix, encoding="utf-8")
print("Desktop nav aligned left and forced to one line.")
