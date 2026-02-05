# TPlanet Monorepo

LLM RAG & Agent CMS 系統 - Multi-tenant 架構

## 結構

```
tplanet/
├── apps/
│   ├── frontend/        # React + Vite 前端
│   ├── backend/         # Django 後端
│   └── llmtwins/        # AI Service (RAG & Agent)
│
├── packages/
│   └── multi-tenant/    # Multi-tenant 共用套件
│       ├── django/      # Django middleware + router
│       ├── react/       # React TenantProvider
│       └── llmtwins-wrapper/  # Session 隔離 proxy
│
├── deploy/
│   ├── docker-compose.beta.yml
│   ├── docker-compose.stable.yml
│   ├── docker-compose.multi-tenant.yml
│   └── nginx/
│
└── docker-compose.yml   # Base compose file
```

## 快速開始

### Beta 環境
```bash
docker compose -f docker-compose.yml -f deploy/docker-compose.beta.yml up -d
```

### Stable 環境
```bash
docker compose -f docker-compose.yml -f deploy/docker-compose.stable.yml up -d
```

### Multi-tenant 環境
```bash
docker compose -f docker-compose.yml -f deploy/docker-compose.multi-tenant.yml up -d
```

## Multi-tenant 測試網址

| 網址 | Tenant |
|------|--------|
| https://multi-tenant.4impact.cc | default |
| https://nantou.multi-tenant.4impact.cc | nantou-gov |

## 架構

```
Browser
    ↓
Nginx (X-Tenant-ID header)
    ↓
┌─────────────────────────────────────┐
│  Frontend (React)                   │
│  - TenantProvider                   │
│  - TenantThemeProvider              │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│  Backend (Django)                   │
│  - TenantMiddleware                 │
│  - TenantDatabaseRouter             │
│  - TenantAwareAuthBackend           │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│  LLMTwins Wrapper                   │
│  - Session ID prefixing             │
│  - Tenant isolation                 │
└─────────────────────────────────────┘
    ↓
┌─────────────────────────────────────┐
│  Databases                          │
│  - default DB                       │
│  - nantou-gov DB                    │
│  - ... (per tenant)                 │
└─────────────────────────────────────┘
```

## 新增 Tenant

1. 編輯 `apps/backend/backend/config/tenants.yml`
2. 建立對應的資料庫
3. 設定 DNS + Nginx
4. 重啟服務
