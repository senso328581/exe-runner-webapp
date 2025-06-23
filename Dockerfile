# ベースイメージ
FROM ubuntu:20.04

# 環境変数設定
ENV DEBIAN_FRONTEND=noninteractive

# 必要パッケージのインストール
RUN apt-get update && apt-get install -y \
    wine64 \
    xvfb \
    nodejs \
    npm \
  && rm -rf /var/lib/apt/lists/*

# アプリケーションディレクトリ
WORKDIR /app

# アプリケーション依存関係をインストール
COPY package.json package-lock.json* ./
RUN npm install --production

# アプリケーションコードをコピー
COPY server.js ./
COPY public/ ./public/

# ポート公開
EXPOSE 3000

# アプリ起動
CMD ["node", "server.js"]
