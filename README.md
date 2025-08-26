# Atlas CP Proxy (FastAPI)

CryptoPanic developer API isteklerini güvenli veya anonimleştirilmiş şekilde geçirmek için hafif bir FastAPI servisi.

## Özellikler
- Header veya ortam değişkeni ile anahtar kullanımı
- Basit bellek içi cache (opsiyonel)
- CORS kontrolü
- Health endpoint
- OpenAPI şeması
- Docker / Render / Vercel deploy örnekleri
- Testler

## Kurulum (Lokal)

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
export CP_KEY=YOUR_TOKEN
uvicorn app.main:app --reload
```

Tarayıcı: http://127.0.0.1:8000/docs

Örnek istek:
```bash
curl -H "X-CP-KEY: $CP_KEY" "http://127.0.0.1:8000/posts?filter=hot&page=1"
```

## Docker

```bash
docker build -t cp-proxy .
docker run -p 8000:8000 -e CP_KEY=YOUR_TOKEN cp-proxy
```

## Render Deploy

1. Yeni repo push et
2. render.com -> New Web Service -> GitHub repo seç
3. Environment: Python
4. Build Command: `pip install -r requirements.txt`
5. Start Command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
6. Env Vars sekmesinde `CP_KEY` ekle
7. İstersen `render.yaml` kullanarak Infrastructure as Code

## Vercel Deploy

1. `vercel.json` dahil et
2. Vercel dashboard -> Project
3. Environment Variables: `CP_KEY`
4. Deploy
5. URL: `https://<project>.vercel.app/posts`

Not: Vercel serverless timeout limitlerine (genelde 10 sn) dikkat et. Gerekirse timeout'u düşür veya cache'i artır.

## OpenAPI

`openapi.yaml` dosyası manuel güncellenmiştir. FastAPI kendi `/openapi.json` endpoint'i üretir.
GitHub Action ile (isteğe göre) export edip commit edebilirsin.

## Test

```bash
pytest -q
```

## Ortam Değişkenleri

| Değişken | Açıklama | Varsayılan |
|----------|----------|------------|
| CP_KEY | CryptoPanic Auth Token | Yok |
| ALLOW_ORIGINS | CORS origin listesi (virgüllü) | * |
| ENABLE_HTTP_CACHE | Bellek içi cache toggle | true |
| CACHE_TTL_SECONDS | Cache TTL | 30 |

## Geliştirme Önerileri
- Rate limit eklemek için: slowapi veya basit sayaç
- Daha kalıcı cache: Redis
- Observability: Prometheus endpoint veya APM agent

## Güvenlik
- Public deploy ediyorsan CP_KEY'i sadece server env'de sakla, kullanıcıya header ile iletilmesini iste (daha fazla kontrol)
- Abuse engellemek için IP tabanlı rate limit veya API key layer (ikinci katman) ekleyebilirsin.

## Lisans
MIT