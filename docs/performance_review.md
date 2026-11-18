# Startup and response-time review

Measurements were taken on 18 November 2026 with Python 3.12.3, the versions resolved from `requirements.txt`, and the current project worktree. They distinguish app-server readiness, a warm local HTTP response and the public browser result; these are not interchangeable measures.

| Measurement | Result | Method / interpretation |
|---|---:|---|
| Fresh local Streamlit process to health endpoint | 1.154 s | Started a new local Streamlit process on port 8880 and timed until `/_stcore/health` returned HTTP 200. |
| Warm local `/` response | 0.005 s | HTTP response only; it does not include a browser-rendered Streamlit session. |
| Warm local health response | 0.001 s | HTTP response only. |
| Local filter response | 638 ms (Country Divide year filter); 557 ms (Company Size year filter). | Measured in a real local browser from selection to updated finding/KPI, including the Streamlit rerun. The AppTest regression suite also exercises filter updates. |
| Public Streamlit Community Cloud | **Cold-start threshold not verified.** | A fresh browser-tab check initially showed “Loading” after the browser open call (4.6 s); after a further 5.0 s wait the six-page app was rendered. The deployment was also open in another browser tab, so its sleep/wake state was not controlled and this is not a clean cold-start benchmark. A non-browser HTTP request redirected repeatedly and ended with HTTP 303 after 12.3 s, so it is not a valid browser load-time measurement. |

The tested app has no deliberate loading delay. The local startup and warm responses are already fast, so this audit found no application-level delay that justified removing charts or changing data loading. Streamlit Community Cloud controls app sleeping and wake-up; the currently available session did not let us measure a controlled sleeping-to-interactive duration. Therefore the under-five-second deployment requirement remains **unverified**. Do not infer it from the local timing. A verified test requires timing the public app from a known sleeping state to its first fully rendered interactive page; the host's cold-start behaviour may exceed five seconds even when the app itself is fast.
