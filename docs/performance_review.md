# Startup and response-time review

Measurements were taken on 18 November 2026 with Python 3.12.3, the versions resolved from `requirements.txt`, and the current project worktree. They distinguish app-server readiness, a warm local HTTP response and the public browser result; these are not interchangeable measures.

| Measurement | Result | Method / interpretation |
|---|---:|---|
| Fresh local Streamlit process to health endpoint | 1.154 s | Started a new local Streamlit process on port 8880 and timed until `/_stcore/health` returned HTTP 200. |
| Warm local `/` response | 0.005 s | HTTP response only; it does not include a browser-rendered Streamlit session. |
| Warm local health response | 0.001 s | HTTP response only. |
| Local filter response | 638 ms (Country Divide year filter); 557 ms (Company Size year filter). | Measured in a real local browser from selection to updated finding/KPI, including the Streamlit rerun. The AppTest regression suite also exercises filter updates. |
| Public Streamlit Community Cloud | **Cold-start threshold not verified.** | After publication, a fresh browser tab showed the app's explicit sleeping screen. Following the wake request it was still waking after 10 s and had rendered by the next 15 s check. This confirms the public deployment works, but the manually sampled interval is not a controlled exact benchmark. A non-browser HTTP request redirected repeatedly and ended with HTTP 303 after 12.3 s, so it is not a valid browser load-time measurement. |

The tested app has no deliberate loading delay. The local startup and warm responses are already fast, so this audit found no application-level delay that justified removing charts or changing data loading. Streamlit Community Cloud controls app sleeping and wake-up; the observed manual wake took more than 10 seconds and was rendered by the next 15-second check, but this is not an exact controlled timing. Therefore the under-five-second deployment requirement remains **unverified**. Do not infer it from the local timing. A verified test requires timing the public app from a known sleeping state to its first fully rendered interactive page; the host's cold-start behaviour may exceed five seconds even when the app itself is fast.
