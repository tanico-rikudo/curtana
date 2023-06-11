from fastapi import FastAPI
from routers import headline, sample, details
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.include_router(headline.router)
app.include_router(sample.router)
app.include_router(details.router)

# アクセスを許可するオリジン（URLのようなもの）を設定
origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    # 認証情報のアクセスを許可(今回は必要ない)
    allow_credentials=True,
    # 全てのリクエストメソッドを許可(["GET", "POST"]など個別指定も可能)
    allow_methods=["*"],
    # アクセス可能なレスポンスヘッダーを設定（今回は必要ない）
    allow_headers=["*"],
)

