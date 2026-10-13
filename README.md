# Shadow AI Sentinel

## AI Prompt Security & Data Loss Prevention

Shadow AI Sentinel is a lightweight security proxy designed to detect sensitive information in prompts before they are sent to an LLM API.

It helps prevent accidental exposure of credentials, personal information, and other sensitive data.

---

## Project Objective

The main objective of Shadow AI Sentinel is to provide a security layer between users/applications and AI services.

It analyzes prompts and makes a security decision:

- **ALLOW** → Safe prompt is allowed.
- **REDACT** → Sensitive information is removed before forwarding.
- **BLOCK** → High-risk sensitive information prevents the request from continuing.

---

## Architecture

```text
User / Application
        |
        v
 Shadow AI Proxy
        |
        v
 Sensitive Data Detector
        |
        v
    Risk Engine
        |
        v
   Policy Engine
        |
   +----+----+
   |    |    |
   v    v    v
 ALLOW REDACT BLOCK
   |    |    
   |    v
   |  Safe Prompt
   |    |
   +----+
        |
        v
     LLM API