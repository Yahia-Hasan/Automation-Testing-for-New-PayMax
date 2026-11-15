# BayMax Patients API — Postman test guide

For testers. Two files:

- This guide (tables + comments)
- `BayMax-Patients-API.postman_collection.json` — import into Postman (**Import → File**)

Generated from API controllers. **625** endpoints in **21** modules.

## How to test in Postman

1. Local **base URL**: `http://localhost:5250`
2. Environment variables:
   - `baseUrl` = `http://localhost:5250`
   - `token` = empty until login
3. Login (no token):

```http
POST {{baseUrl}}/api/auth/login
Content-Type: application/json

{
  "userName": "YOUR_USERNAME",
  "password": "YOUR_PASSWORD"
}
```

4. Copy `data.token` from the response into `{{token}}`.
5. All other requests need:

```
Authorization: Bearer {{token}}
```

6. Replace `{id}` path values with real test-DB ids (`reservationId`, `visitCode`, `patientCode`, `emergencyId`).
7. POST/PUT/DELETE on invoices, payments, and discharge: use a **test** case only.
8. Optional: Swagger at `{{baseUrl}}/swagger`.

## Auth

| Endpoint | Auth |
|----------|------|
| `POST /api/auth/login` | Anonymous |
| `GET /api/auth/auto-login` | Anonymous (legacy cookies or `X-Legacy-UserId`) |
| `GET /api/auth/session-debug` | Anonymous |
| `GET /api/auth/computers` | Anonymous |
| Everything else | JWT Bearer |

## Suggested smoke test

1. `POST /api/auth/login`
2. `GET /api/auth/me`
3. `GET /api/reception/patients/search?query=...`
4. `GET /api/reception/patients/{patientCode}`
5. `GET /api/clinic/visits?date=YYYY-MM-DD`
6. `GET /api/clinic/visits/{visitCode}/services-page` — `treasuries` must not be `[]`
7. `GET /api/emergency/waiting-list`
8. `GET /api/invoice-details/{reservationId}`
9. `GET /api/dashboards/audit` (needs privilege)
