# LLMTwins Tenant Wrapper

Multi-tenant proxy for LLMTwins，不修改原始碼即可實現租戶隔離。

## 架構

```
┌─────────────┐     ┌─────────────────┐     ┌─────────────┐
│   Client    │────▶│  Tenant Wrapper │────▶│  LLMTwins   │
│             │     │    (port 8001)  │     │ (port 8000) │
│ X-Tenant-ID │     │                 │     │             │
└─────────────┘     └─────────────────┘     └─────────────┘
```

## 原理

**Session ID 改寫：**

```
# 請求進來
session_id: "sess_abc123"
X-Tenant-ID: "nantou-gov"

# 轉發給 LLMTwins
session_id: "nantou-gov__sess_abc123"

# 回應給 Client (還原)
session_id: "sess_abc123"
```

**檔案隔離效果：**

```
sessions/
├── default__sess_xxx/        # default 租戶
├── nantou-gov__sess_yyy/     # 南投縣政府
└── other-tenant__sess_zzz/   # 其他租戶
```

## 快速開始

### 本地執行

```bash
cd llmtwins_wrapper

# 安裝依賴
pip install -r requirements.txt

# 設定環境變數
export LLMTWINS_BASE_URL=http://localhost:8000
export DEFAULT_TENANT=default
export VALID_TENANTS=default,nantou-gov

# 啟動
python main.py
```

### Docker

```bash
docker build -t llmtwins-wrapper .
docker run -p 8001:8001 \
  -e LLMTWINS_BASE_URL=http://host.docker.internal:8000 \
  -e VALID_TENANTS=default,nantou-gov \
  llmtwins-wrapper
```

## 環境變數

| 變數 | 預設值 | 說明 |
|------|--------|------|
| `LLMTWINS_BASE_URL` | `http://localhost:8000` | LLMTwins 位址 |
| `DEFAULT_TENANT` | `default` | 無 header 時的預設租戶 |
| `TENANT_HEADER` | `X-Tenant-ID` | 租戶 header 名稱 |
| `VALID_TENANTS` | (空) | 允許的租戶列表，逗號分隔。空 = 允許全部 |
| `UPSTREAM_TIMEOUT` | `180` | 上游超時秒數 |
| `PORT` | `8001` | 服務埠號 |

## API 使用

所有 LLMTwins API 皆可透過 Wrapper 存取，只需加上 `X-Tenant-ID` header：

### 建立 Session

```bash
curl -X POST http://localhost:8001/api/sessions \
  -H "X-Tenant-ID: nantou-gov"
```

### Chat

```bash
curl -X POST http://localhost:8001/api/chat \
  -H "Content-Type: application/json" \
  -H "X-Tenant-ID: nantou-gov" \
  -d '{
    "model": "llama3:instruct",
    "messages": [{"role": "user", "content": "你好"}],
    "stream": false
  }'
```

### 上傳檔案

```bash
curl -X POST "http://localhost:8001/api/sessions/sess_xxx/upload" \
  -H "X-Tenant-ID: nantou-gov" \
  -F "file=@document.pdf"
```

## 健康檢查

```bash
# Wrapper 狀態
curl http://localhost:8001/health

# 回應
{
  "status": "ok",
  "upstream": "http://localhost:8000",
  "upstream_ok": true
}
```

## 整合到現有架構

在 Django 後端呼叫時加入 tenant header：

```python
import httpx

async def call_llmtwins(tenant_id: str, endpoint: str, data: dict):
    async with httpx.AsyncClient() as client:
        response = await client.post(
            f"http://llmtwins-wrapper:8001{endpoint}",
            json=data,
            headers={"X-Tenant-ID": tenant_id},
        )
        return response.json()
```
