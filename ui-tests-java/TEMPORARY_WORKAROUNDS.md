# Temporary Workarounds & Follow-ups

Track everything marked **TEMPORARY** in the automation suite so we can replace it
once product / frontend behaviour is confirmed. Delete items as they get fixed.

---

## 1. Legacy login bridge (new system has no login page yet)

**Status:** Temporary  
**Where:**
- `helpers/LoginHelper.java`
- `BaseTest.loginAndNavigateToNewSystem()`
- Temporary keys in `config.properties` (`legacy.*`, `new.system.url`)

**What it does:** Logs into the old ASP.NET system, selects branch "Ad Doqi", then opens the new system on HTTPS `:4040`.

**Replace with:** Native new-system login page when developers finish it. Then delete `LoginHelper` and the temporary config keys.

---

## 2. Reception navigation reset between tests

**Status:** Hardened — each test hard-reloads exact `/reception`  
**Where:** `PatientAdmissionPage.prepareIsolatedTestState()` → `reloadReceptionFresh()`

**Why:** After a successful Save the URL becomes `/reception/patient/{patientCode}` and the form keeps that patient's data. Navbar-only navigation was also slow (~10s) and left the dropdown open over toolbar buttons (click intercepted).

**Current strategy (per test):**
1. Dismiss modal / nav dropdown / toasts
2. `driver.get(.../reception)` — hard reload of the blank admission page
3. Click **جديد** and assert name/mobile are empty

**Speed / stability notes:**
- Each test hard-reloads `/reception` (~0.7–1.5s) instead of navbar clicks (~10s) that also left the dropdown open
- Removed fixed `Thread.sleep(3000)` in toast wait
- Dropped `implicit.wait` from 10 → 0 (explicit waits only)
- **Never wipe** `toast-stack` via `innerHTML = ''` — that breaks Angular's toaster so later tests see Save succeed (URL changes) but **no toast appears**. Dismiss via close buttons or rely on the hard reload.

**Follow-up:** Confirm whether product wants an explicit "new patient" route, or if Save should stay on a blank form without changing the URL.

---

## 3. Patient search field behaviour (CURRENT PRIORITY)

**Status:** Temporary — needs product confirmation  
**Where:**
- `PatientAdmissionPage.searchForPatientAndSubmit()`
- `PatientAdmissionPage.selectFirstSearchResult()`
- `PatientAdmissionTests.searchPopulatesExistingPatientData()`

**Observed behaviour:**
- Typing a patient **code** (or name) into `patient-data-search-input` and pressing **ENTER does nothing**.
- A dropdown appears with **one result** (the matching patient).
- Selecting that row populates the form.

**Current workaround:** After typing the query, click the single dropdown result (flexible locators until we get the real HTML / `data-test-id`). Prefer searching by **patient code** captured after happy-path Save.

**Replace with:** The real intended UX once confirmed, e.g.:
- ENTER should select the first/only result, or
- Dedicated search button / `data-test-id` on result rows, or
- Debounced auto-select when only one match exists.

**Ask frontend for:** HTML of the search results dropdown + `data-test-id` on each row.

---

## 4. Toast / alert assertions by type only (not text)

**Status:** Updated — frontend added `data-test-id="global-toast-stack"`  
**Where:** `PatientAdmissionPage.isSystemMessageDisplayed(success|error|warning)`

**Why:** Hundreds of Arabic message texts are hard to maintain.

**Selectors used (preferred first):**
- Stack: `[data-test-id='global-toast-stack']`
- Items (confirmed from live DOM):
  - `toast-warning-{n}` / `toast-success-{n}` / `toast-error-{n}`
  - message: `toast-*-{n}-message`, close: `toast-*-{n}-close-btn`
- Fallback classes: `div.toast-item.warning|success|error`

**Flaky short-name warning:** arm `armToastTypeLatch()` (MutationObserver + sessionStorage) **before** Save so a toast that flashes during navigation is still recorded.

---

## 5. Identity type dropdown exact label

**Status:** Fixed (watch for copy changes)  
**Where:** `PatientAdmissionTests.ID_TYPE_NATIONAL_ID = "رقم قومي"`

**Note:** Was incorrectly `"الرقم القومي"` — search inside ng-select failed. Keep the exact option text from the UI.

---

## 6. Credit company (جهة آجل) exact label

**Status:** Fixed (watch for copy changes)  
**Where:** `PatientAdmissionTests.CREDIT_COMPANY_NAME = "#@ اليكو"`

**Note:** Must match the dropdown option text exactly (including `#@ `). If the credit company lives only under **الشركة الفرعية** for some clients, update the test to select parent جهة then sub-company.

---

## 7. HTTPS + self-signed certificate for new system

**Status:** Environment constraint  
**Where:** `config.properties` (`https://196.218.246.250:4040`), Chrome options in `BaseTest`

**Notes:**
- Plain `http://` hangs / connection resets; the app serves **HTTPS**.
- Certificate is self-signed → `acceptInsecureCerts` + `--ignore-certificate-errors` are required.
- Chrome HTTPS-First upgrades are disabled in ChromeOptions.

---

## 8. Shared browser session per test class

**Status:** Intentional  
**Where:** `BaseTest` `@BeforeClass` / `@AfterClass`, `PatientAdmissionTests` `@BeforeMethod` reset

**What:** One login for the whole class; each test re-opens a clean reception form (see item 2).

---

## 9. Patient Arabic-name word-count rules

**Status:** Covered by TC8 / TC9 / TC10  
**Rules under test:**
- 1 word → **error** on Save
- 2–3 words → **warning + success** on Save (name is still accepted)
- 4 words (`يحيى تيست اوتوميشن {n}`) → **success**

**Note:** Blur/TAB warning alone was flaky in automation; TC9 asserts both messages after Save.

**Follow-up:** Confirm exact word-count thresholds with business if copy changes.

---

## 10. Unknown patient (مريض غير معروف) modal

**Status:** Automated (TC-ADM-022 → TC-ADM-024)  
**Where:** `PatientAdmissionPage.openUnknownPatientModal()` and friends

**Confirmed `data-test-id` values:**
- `patient-data-unknown-patient-btn` (open)
- `patient-data-unknown-modal`, `patient-data-unknown-modal-backdrop`
- `patient-data-unknown-modal-close-btn`
- `patient-data-unknown-code-input` (readonly)
- `patient-data-unknown-gender-male-radio`, `patient-data-unknown-gender-female-radio`
- `patient-data-unknown-visit-date-input`, `patient-data-unknown-visit-time-input`
- `patient-data-unknown-notes-textarea`
- `patient-data-save-unknown-btn`
- Table rows: `patient-data-unknown-row`, `patient-data-select-unknown-btn`, `patient-data-print-unknown-barcode-btn`

**Note:** The open button sits under the navbar dropdown that `navigateToReception()` leaves expanded, so clicks are routed through `clickThroughOverlays()` (native click, JS fallback).

**Not covered yet:** selecting an existing unknown patient from the table, and barcode printing.

---

## Quick checklist (next cleanup pass)

- [ ] Replace legacy login bridge with new-system login
- [ ] Confirm / harden patient search UX + stable `data-test-id` on results
- [x] Add `data-test-id` on toast/alert containers (`global-toast-stack` — item-level IDs still TBD)
- [ ] Confirm credit-company selection path (جهة vs شركة فرعية)
- [ ] Confirm whether Save should leave URL on `/reception` or `/reception/{code}`
- [ ] Remove TEMPORARY comments once each item above is resolved
