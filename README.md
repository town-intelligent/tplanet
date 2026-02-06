# TPlanet Deploy

TPlanet 部署專用 Repo - Microservices 架構

## 目錄結構

```
town-intelligent/
├── tplanet-AI/           # Frontend repo (獨立)
├── tplanet-daemon/       # Backend repo (獨立)
├── LLMTwins/             # AI Service repo (獨立)
│
└── tplanet-deploy/       # 部署專用 (本 repo)
    ├── docker-compose.yml
    ├── docker-compose.beta.yml
    ├── docker-compose.stable.yml
    ├── docker-compose.multi-tenant.yml
    ├── nginx/
    └── packages/
        └── multi-tenant/  # 共用套件
```

## 前置作業

確保 sibling 目錄有以下 repos：

```bash
cd /path/to/town-intelligent
git clone git@github.com:town-intelligent-beta/tplanet-AI.git
git clone git@github.com:town-intelligent/tplanet-daemon.git
git clone git@github.com:towNingtek/LLMTwins.git
git clone git@github.com:town-intelligent/tplanet-deploy.git
```

## 部署指令

```bash
cd tplanet-deploy

# Beta 環境
docker compose -f docker-compose.yml -f docker-compose.beta.yml up -d

# Stable 環境
docker compose -f docker-compose.yml -f docker-compose.stable.yml up -d

# Multi-tenant 環境
docker compose -f docker-compose.yml -f docker-compose.multi-tenant.yml up -d
```

## Multi-tenant 測試網址

| 網址 | Tenant |
|------|--------|
| https://multi-tenant.4impact.cc | default |
| https://nantou.multi-tenant.4impact.cc | nantou-gov |

## 架構

```
                    ┌─────────────────┐
                    │     Nginx       │
                    │  (X-Tenant-ID)  │
                    └────────┬────────┘
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
         ▼                   ▼                   ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│    Frontend     │ │    Backend      │ │   LLMTwins      │
│   tplanet-AI    │ │ tplanet-daemon  │ │    Wrapper      │
│  (React/Vite)   │ │    (Django)     │ │   (FastAPI)     │
└─────────────────┘ └────────┬────────┘ └────────┬────────┘
                             │                   │
                    ┌────────┴────────┐          │
                    │   Databases     │          ▼
                    │  (per tenant)   │   ┌─────────────┐
                    └─────────────────┘   │  LLMTwins   │
                                          │  (RAG/AI)   │
                                          └─────────────┘
```

## 新增 Tenant

1. 編輯 `../tplanet-daemon/backend/config/tenants.yml`
2. 建立對應的資料庫
3. 設定 DNS + Nginx (`nginx/` 目錄)
4. 重啟服務
