# Performance evaluation

Measurements were taken on 18 November 2026 using Python 3.12.3 and the dependency versions resolved from `requirements.txt`. App-server readiness, warm local HTTP responses, interactive filter updates, and public browser startup measure different stages of delivery and should not be treated as interchangeable.

| Measurement | Result | Method / interpretation |
|---|---:|---|
| Fresh local Streamlit process to health endpoint | 1.154 s | Started a new local Streamlit process on port 8880 and timed until `/_stcore/health` returned HTTP 200. |
| Warm local `/` response | 0.005 s | HTTP response only; it does not include a browser-rendered Streamlit session. |
| Warm local health response | 0.001 s | HTTP response only. |
| Local filter response | 638 ms (Country Divide year filter); 557 ms (Company Size year filter). | Measured in a real local browser from selection to updated finding/KPI, including the Streamlit rerun. The AppTest regression suite also exercises filter updates. |
| Public Streamlit Community Cloud | **Cold-start threshold not verified.** | A fresh browser tab showed the host's sleeping screen. After the wake request, it was still waking after 10 s and had rendered by the next 15 s check. A non-browser HTTP request redirected repeatedly and ended with HTTP 303 after 12.3 s; this is not a valid browser load-time measurement. |

The local measurements verify that the application server, warm HTTP responses, and tested filter interactions are fast. The application has no deliberate loading delay. Streamlit Community Cloud controls sleep and wake behaviour, so the observed public cold-start interval cannot be inferred from local measurements. The under-five-second public deployment criterion therefore remains **unverified**. Verifying it would require a controlled timing from a known sleeping state to the first fully rendered interactive page.
