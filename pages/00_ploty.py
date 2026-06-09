
import streamlit as st
import yfinance as yf
import plotly.express as px
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="Global Top 10 Stock Dashboard", page_icon="📈", layout="wide")

st.title("📈 글로벌 시가총액 TOP 10 주식 대시보드")
st.markdown("최근 1년간 글로벌 시가총액 상위 10개 기업의 주가 및 수익률 추이를 확인하세요.")

# 2. 글로벌 시가총액 TOP 10 (2025~2026년 기준 대표 종목)
TOP_10_STOCKS = {
    "NVDA": "NVIDIA",
    "AAPL": "Apple",
    "MSFT": "Microsoft",
    "GOOGL": "Alphabet (Google)",
    "AMZN": "Amazon",
    "META": "Meta",
    "TSM": "TSMC",
    "BRK-B": "Berkshire Hathaway",
    "LLY": "Eli Lilly",
    "AVGO": "Broadcom"
}

# 3. 데이터 로딩 (캐싱을 통해 재로딩 속도 개선)
@st.cache_data(ttl=3600) # 1시간마다 캐시 갱신
def load_data():
    tickers = list(TOP_10_STOCKS.keys())
    # yfinance를 통해 최근 1년('1y') 종가 데이터 가져오기
    df = yf.download(tickers, period="1y")['Close']
    
    # 결측치 처리 (이전 값으로 채움)
    df = df.ffill().dropna()
    return df

with st.spinner("데이터를 불러오는 중입니다... 잠시만 기다려주세요."):
    raw_df = load_data()

if not raw_df.empty:
    # 4. 사용자 선택 UI (사이드바 또는 메인 화면)
    st.sidebar.header("설정")
    selected_tickers = st.sidebar.multiselect(
        "비교할 기업을 선택하세요",
        options=list(TOP_10_STOCKS.keys()),
        default=list(TOP_10_STOCKS.keys()),
        format_func=lambda x: f"{x} ({TOP_10_STOCKS[x]})"
    )

    if selected_tickers:
        # --- 데이터 전처리 ---
        # 1) 단순 주가 데이터
        price_df = raw_df[selected_tickers].reset_index()
        price_melted = price_df.melt(id_vars=["Date"], var_name="Ticker", value_name="Price(USD)")
        price_melted['Company'] = price_melted['Ticker'].map(TOP_10_STOCKS)

        # 2) 수익률 데이터 (기준일=0%)
        # 1년 전 첫 번째 날의 주가를 기준으로 현재 몇 % 올랐는지 계산
        return_df = (raw_df[selected_tickers] / raw_df[selected_tickers].iloc[0] * 100) - 100
        return_df = return_df.reset_index()
        return_melted = return_df.melt(id_vars=["Date"], var_name="Ticker", value_name="Return(%)")
        return_melted['Company'] = return_melted['Ticker'].map(TOP_10_STOCKS)

        # --- 차트 그리기 ---
        tab1, tab2 = st.tabs(["💰 주가 추이 (USD)", "📈 누적 수익률 비교 (%)"])

        with tab1:
            fig_price = px.line(
                price_melted, 
                x="Date", y="Price(USD)", color="Company",
                title="최근 1년 주가 변동 추이 (USD)"
            )
            fig_price.update_layout(xaxis_title="날짜", yaxis_title="종가 (달러)", hovermode="x unified")
            st.plotly_chart(fig_price, use_container_width=True)

        with tab2:
            fig_return = px.line(
                return_melted, 
                x="Date", y="Return(%)", color="Company",
                title="최근 1년 누적 수익률 (%)"
            )
            # 0% 기준선 추가
            fig_return.add_hline(y=0, line_dash="dash", line_color="white", opacity=0.5)
            fig_return.update_layout(xaxis_title="날짜", yaxis_title="수익률 (%)", hovermode="x unified")
            st.plotly_chart(fig_return, use_container_width=True)

        # --- 요약 테이블 ---
        st.subheader("📊 최근 주가 요약")
        
        # 첫날(1년전)과 마지막 날(현재) 데이터 추출
        first_prices = raw_df[selected_tickers].iloc[0]
        latest_prices = raw_df[selected_tickers].iloc[-1]
        
        summary_df = pd.DataFrame({
            "기업명": [TOP_10_STOCKS[t] for t in selected_tickers],
            "1년 전 주가($)": first_prices.values.round(2),
            "현재 주가($)": latest_prices.values.round(2)
        })
        
        # 수익률 계산
        summary_df['수익률(%)'] = (((summary_df['현재 주가($)'] - summary_df['1년 전 주가($)']) / summary_df['1년 전 주가($)']) * 100).round(2)
        
        # 인덱스를 티커(Ticker)로 설정하여 출력
        summary_df.index = selected_tickers
        st.dataframe(summary_df, use_container_width=True)
        
    else:
        st.warning("왼쪽 사이드바에서 최소 1개 이상의 기업을 선택해주세요.")
