---
paths:
  - "api/**/*.py"
---
# API rules (load only when Claude touches api/)
- Return 409 on a repeated Idempotency-Key with a different body.
- Log the order_id on every error.
