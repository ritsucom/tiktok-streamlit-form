import streamlit as st
import requests
from datetime import date

# ✅ Notion連携用の秘密情報（Streamlit Cloud用にsecretsから読み込む）
NOTION_API_KEY = st.secrets["NOTION_API_KEY"]
DATABASE_ID = st.secrets["DATABASE_ID"]

st.set_page_config(page_title="📱 TikTok エンゲージメント送信フォーム", layout="centered")

st.title("📱 TikTok エンゲージメント送信フォーム")

with st.form("tiktok_form"):
    influencer = st.text_input("インフルエンサー名")
    genre = st.selectbox("ジャンル", [
        "ビューティー", "ファッション", "ライフスタイル", "グルメ・料理", "ダンス", "コメディ・ネタ",
        "ペット・動物", "教育・ハウツー", "フィットネス・筋トレ", "Vlog", "旅行・観光",
        "日常・ルーティン", "恋愛・人間関係", "ゲーム", "アニメ・漫画", "音楽・歌ってみた",
        "DIY・クラフト", "ビジネス・キャリア", "ニュース・時事", "ガジェット・サービス",
        "メンタル・自己啓発", "子育て・家族", "その他"
    ])
    post_date = st.date_input("投稿日", value=date.today())
    post_type = st.selectbox("投稿者タイプ", [
        "インフルエンサー（顔出し・世界観あり）",
        "一般ユーザー（素人感あり）",
        "ブランド・企業アカウント（公式っぽい）",
        "スタッフ・現場投稿（制服・職場内など）",
        "その他・判別不能"
    ])
    format_type = st.selectbox("投稿フォーマット", [
        "音楽中心（リップシンク／BGM映え）",
        "コメディ（おもしろ・笑わせ系）",
        "Vlog（日常の中で自然紹介）",
        "レビュー（使ってみた・感想）",
        "ハウツー（使い方／手順紹介）",
        "ドラマ（共感ストーリー型）",
        "エフェクト系（AI変換・編集テンポ・視覚演出）",
        "ASMR / 無音系",
        "ミーム・ネタ系（ネット流行り型）",
        "インタビュー・語り系（話を引き出す・答える形式）",
        "写真スライドショー・静止画中心",
        "ランキング / まとめ紹介",
        "文字メイン（字幕・テロップだけ）",
        "生成AI動画（外部ツールで作った高精度映像）",
        "その他"
    ])
    promo_type = st.selectbox("投稿種別", [
         "オーガニック投稿",
        "PR投稿（案件）",
        "不明・判別不能"
    ])
    scene = st.text_input("撮影シーン・場所（例：自宅 / 店舗内 / 屋外 / スタジオ など）")
    origin_type = st.radio("動画の種類", ["オリジナル", "リポスト"])
    url = st.text_input("TikTok動画URL")
    views = st.number_input("再生数", min_value=0)
    likes = st.number_input("いいね数", min_value=0)
    comments = st.number_input("コメント数", min_value=0)
    saves = st.number_input("保存数", min_value=0)
    shares = st.number_input("シェア数", min_value=0)
    submitted = st.form_submit_button("送信")

if submitted:
    engagement = likes + comments + saves + shares
    rate = round((engagement / views) * 100, 2) if views > 0 else 0

    payload = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "インフルエンサー名": {"title": [{"text": {"content": influencer}}]},
            "ジャンル": {"multi_select": [{"name": genre}]},
            "投稿日": {"date": {"start": str(post_date)}},
            "投稿者タイプ": {"select": {"name": post_type}},
            "投稿フォーマット": {"select": {"name": format_type}},
            "投稿種別": {"select": {"name": promo_type}},
            "撮影シーン・場所": {"rich_text": [{"text": {"content": scene}}]},
            "動画の種類": {"select": {"name": origin_type}},
            "動画URL": {"url": url},
            "再生数": {"number": views},
            "いいね数": {"number": likes},
            "コメント数": {"number": comments},
            "保存数": {"number": saves},
            "シェア数": {"number": shares},
            "エンゲージメント合計": {"number": engagement},
            "エンゲージメント率": {"number": rate}
        }
    }

    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    response = requests.post("https://api.notion.com/v1/pages", json=payload, headers=headers)

    if response.status_code == 200:
        st.success("✅ Notionに送信しました！")
    else:
        st.error(f"❌ エラーが発生しました: {response.text}")
