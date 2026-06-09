import streamlit as st
import yfinance as yf
import plotly.express as px
import pandas as pd

# 1. 페이지 설정
st.set_page_config(page_title="Global Top 10 Stock Dashboard", page_icon="📈", layout="wide")

st.title("📈 글로벌 시가총액 TOP 10 주식 대시보드")
st.markdown("최근 1년간 글로벌 시가총액 상위 10개 기업의 주가 및 수익률 추이를 확인하세요.")

# 2. 글로벌 시가총액 TOP 10
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

# 3. 데이터 로딩 (안정성 강화 버전)
@st.cache_data(ttl=3600)
def load_data():
    tickers = list(TOP_10_STOCKS.keys())
    df_list = []
    
    # 🌟 수정 포인트: 한 번에 다운로드 시 발생하는 yfinance 구조 오류를 방지하기 위해 하나씩 호출
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            hist = stock.history(period="1y")
            
            if not hist.empty and 'Close' in hist.columns:
                close_series = hist['Close']
                close_series.name = ticker
                
                # 시간대(timezone) 차이로 인해 데이터가 어긋나는 것을 방지
                if close_series.index.tz is not None:
                    close_series.index = close_series.index.tz_localize(None)
                
                # 시간 정보 제거하고 날짜(Date)만 남김
                close_series.index = close_series.index.normalize()
                
                df_list.append(close_series)
        except Exception as e:
            # 특정 종목을 못 불러오더라도 대시보드가 멈추지 않도록 예외 처리
            continue
            
    if not df_list:
        return pd.DataFrame()
        
    # 수집한 데이터 하나로 병합
    df = pd.concat(df_list, axis=1)
    
    # 🌟 수정 포인트: dropna() 대신 ffill()과 bfill()을 사용하여
    # 단 하루라도 누락된 데이터 때문에 전체 차트가 사라지는 현상 방지
    df = df.ffill().bfill()
    return df

# 스피너와 함께 데이터 로딩
with st.spinner("야후 파이낸스에서 최신 주식 데이터를 불러오는 중입니다..."):
    raw_df = load_data()

# 🌟 수정 포인트: 데이터 로딩 실패 시 원인을 알려주는 메시지 출력
if raw_df.empty:
    st.error("🚨 주식 데이터를 불러오지 못했습니다. 야후 파이낸스 서버 접속이 지연되고 있거나, Streamlit Cloud 서버의 일시적인 네트워크 문제일 수 있습니다. 잠시 후 새로고침 해주세요.")
else:
    # 4. 사용자 선택 UI (사이드바)
    st.sidebar.header("설정")
    selected_tickers = st.sidebar.multiselect(
        "비교할 기업을 선택하세요",
        options=list(TOP_10_STOCKS.keys()),
        default=list(TOP_10_STOCKS.keys()),
        format_func=lambda x: f"{x} ({TOP_10_STOCKS[x]})"
    )

    if selected_tickers:
        # 선택된 기업만 필터링 (만에 하나 로드 실패한 기업이 있을 수 있으므로 교집합 확인)
        valid_tickers = [t for t in selected_tickers if t in raw_df.columns]
        
        if not valid_tickers:
            st.warning("선택한 기업의 데이터가 없습니다. 다른 기업을 선택해 주세요.")
        else:
            # --- 데이터 전처리 ---
            price_df = raw_df[valid_tickers].reset_index()
            # Date 컬럼 이름 명확화
            price_df.rename(columns={'index': 'Date', 'Date': 'Date'}, inplace=True)
            
            price_melted = price_df.melt(id_vars=["Date"], var_name="Ticker", value_name="Price(USD)")
            price_melted['Company'] = price_melted['Ticker'].map(TOP_10_STOCKS)

            # 수익률 계산: 1년 전 첫 데이터 대비 변동률
            first_prices = raw_df[valid_tickers].iloc[0]
            return_df = (raw_df[valid_tickers] / first_prices * 100) - 100
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
                fig_return.add_hline(y=0, line_dash="dash", line_color="white" if st.get_option("theme.base") == "dark" else "black", opacity=0.5)
                fig_return.update_layout(xaxis_title="날짜", yaxis_title="수익률 (%)", hovermode="x unified")
                st.plotly_chart(fig_return, use_container_width=True)

            # --- 요약 테이블 ---
            st.subheader("📊 최근 주가 요약")
            
            latest_prices = raw_df[valid_tickers].iloc[-1]
            
            summary_df = pd.DataFrame({
                "기업명": [TOP_10_STOCKS[t] for t in valid_tickers],
                "1년 전 주가($)": first_prices.values.round(2),
                "현재 주가($)": latest_prices.values.round(2)
            })
            
            summary_df['수익률(%)'] = (((summary_df['현재 주가($)'] - summary_df['1년 전 주가($)']) / summary_df['1년 전 주가($)']) * 100).round(2)
            summary_df.index = valid_tickers
            st.dataframe(summary_df, use_container_width=True)
            
    else:
        st.warning("👈 왼쪽 사이드바에서 최소 1개 이상의 기업을 선택해주세요.")
