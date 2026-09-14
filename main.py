import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------------------------------------------------------
# 페이지 기본 설정
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="영화 데이터 그래프 도감 1 - 시간",
    layout="wide"
)

st.title("🎬 영화 데이터 그래프 도감 1 - 시간")
st.write("2023년 일별 박스오피스 데이터를 바탕으로 시간의 흐름에 따른 영화 관객수 변화를 살펴봅니다.")

# -----------------------------------------------------------------------------
# 데이터 불러오기 및 전처리
# -----------------------------------------------------------------------------
@st.cache_data
def load_data():
    url = "https://raw.githubusercontent.com/greatsong/modudata/main/data/kobis_daily.csv"
    df = pd.read_csv(url)
    
    # 8자리 숫자(YYYYMMDD)로 된 날짜 열을 실제 날짜(datetime) 형식으로 변환
    df['날짜'] = pd.to_datetime(df['날짜'].astype(str), format='%Y%m%d')
    
    return df

df = load_data()

# -----------------------------------------------------------------------------
# [구역 1] 영화별 일일 관객수 변화
# -----------------------------------------------------------------------------
st.divider()
st.header("1. 영화별 일일 관객수 변화")

# 영화 목록 추출 및 드롭다운 생성
movie_list = df['영화명'].unique()
selected_movie = st.selectbox("그래프를 확인할 영화를 선택하세요:", movie_list)

# 선택한 영화 데이터 필터링
filtered_df = df[df['영화명'] == selected_movie]

# 플롯리(Plotly) 선 그래프 그리기
fig1 = px.line(
    filtered_df, 
    x='날짜', 
    y='일관객',
    title=f"'{selected_movie}' 일별 관객수 추이",
    markers=True # 데이터 포인트 표시
)

# 마우스 호버(hover) 시 보여줄 정보 커스텀
fig1.update_traces(
    hovertemplate="<b>날짜:</b> %{x|%Y-%m-%d}<br><b>일관객:</b> %{y:,.0f}명<extra></extra>"
)

# 그래프 출력
st.plotly_chart(fig1, use_container_width=True)

# '이 그래프로 알 수 있는 것' 작성란
st.info("💡 **이 그래프로 알 수 있는 것:** (여기에 분석 내용을 작성해 주세요)")


# -----------------------------------------------------------------------------
# [구역 2] Top 5 영화의 일일 관객수 비교
# -----------------------------------------------------------------------------
st.divider()
st.header("2. 총 관객수 Top 5 영화의 관객수 추이 비교")

# 1. 전체 기간 동안 '일관객' 합계가 가장 큰 5개 영화 추출
top5_movies = df.groupby('영화명')['일관객'].sum().nlargest(5).index

# 2. Top 5 영화에 해당하는 데이터만 필터링
top5_df = df[df['영화명'].isin(top5_movies)]

# 3. 플롯리 선 그래프 그리기 (color 인자로 영화 구분)
fig2 = px.line(
    top5_df, 
    x='날짜', 
    y='일관객', 
    color='영화명',
    title="Top 5 영화의 일별 관객수 변화 (범례를 클릭해 켜고 끌 수 있습니다)"
)

# 마우스 호버(hover) 정보 커스텀
fig2.update_traces(
    hovertemplate="<b>%{data.name}</b><br><b>날짜:</b> %{x|%Y-%m-%d}<br><b>일관객:</b> %{y:,.0f}명<extra></extra>"
)

# 그래프 출력
st.plotly_chart(fig2, use_container_width=True)

# '이 그래프로 알 수 있는 것' 작성란
st.info("💡 **이 그래프로 알 수 있는 것:** (여기에 분석 내용을 작성해 주세요)")


# -----------------------------------------------------------------------------
# [구역 3] 10위권 일관객 총합 추이 (영역 그래프)
# -----------------------------------------------------------------------------
st.divider()
st.header("3. 날짜별 10위권 일관객 총합 추이")

# 1. 날짜별 일관객 합계 구하기
daily_sum = df.groupby('날짜')['일관객'].sum().reset_index()

# 2. 합계가 가장 컸던 날 3일 추출
top3_days = daily_sum.nlargest(3, '일관객')

# 3. 플롯리 영역 그래프 그리기
fig3 = px.area(
    daily_sum, 
    x='날짜', 
    y='일관객', 
    title="날짜별 박스오피스 상위 10편 관객수 총합"
)

# 4. 합계가 가장 큰 3일에 주석(Annotation) 달기
for index, row in top3_days.iterrows():
    date_str = row['날짜'].strftime('%Y-%m-%d')
    audience_cnt = row['일관객']
    
    fig3.add_annotation(
        x=row['날짜'],
        y=audience_cnt,
        text=f"Top: {date_str}", # 표시할 텍스트
        showarrow=True,
        arrowhead=2,
        arrowsize=1,
        arrowwidth=2,
        ax=0,
        ay=-40, # 화살표를 위로 띄우기
        font=dict(size=12, color="red")
    )

# 마우스 호버(hover) 정보 커스텀
fig3.update_traces(
    hovertemplate="<b>날짜:</b> %{x|%Y-%m-%d}<br><b>총 일관객:</b> %{y:,.0f}명<extra></extra>"
)

# 그래프 출력
st.plotly_chart(fig3, use_container_width=True)

# '이 그래프로 알 수 있는 것' 작성란
st.info("💡 **이 그래프로 알 수 있는 것:** (여기에 분석 내용을 작성해 주세요)")


# -----------------------------------------------------------------------------
# [구역 4] 추가 그래프를 위한 빈 공간
# -----------------------------------------------------------------------------
st.divider()
st.header("4. (여기에 네 번째 그래프 제목을 입력하세요)")
st.write("앞으로 추가될 그래프와 분석을 넣을 공간입니다.")
# TODO: 새로운 데이터 필터링 및 그래프 코드를 이곳에 추가하세요.
