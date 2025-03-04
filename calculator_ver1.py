# In[ ]:
import streamlit as st
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import io
import os

# === 📌 페이지 설정 ===
st.set_page_config(page_title="가계 재무 계산기", layout="wide")


# === 🔹 세션 상태 초기화 ===
if "selected_menu" not in st.session_state:
    st.session_state.selected_menu = "가계수지"
if "inputs" not in st.session_state:
    st.session_state.inputs = {key: {"value1": 0, "value2": 0, "result": "계산 불가"} for key in [
        "가계수지", "저축성향", "비상예비 자금", "보장성보험", "노후대비", "부채비율", "투자성향"
    ]}

# === 🔹 네비게이션 바 메뉴 설정 ===
menu_items = {
    "가계수지": "생활비 / 가계소득",
    "저축성향": "총 저축 / 총 소득",
    "비상예비 자금": "유동성 자산 / 총 지출",
    "보장성보험": "보장성 보험료 / 총 소득",
    "노후대비": "노후대비 저축 / 총 저축",
    "부채비율": "총 부채 / 총 자산",
    "투자성향": "투자 자산 / 총 자산"
}

# === 🔹 사이드바 설정 ===
with st.sidebar:
    # ✅ 로고 이미지 중앙 정렬 (CSS 적용)
    st.markdown(
        """
        <style>
            .sidebar-image-container {
                display: flex;
                justify-content: center;
                align-items: center;
            }
        </style>
        <div class="sidebar-image-container">
            <img src="https://raw.githubusercontent.com/Sunmi1814/public_ver1/main/Signature%20Vertical.png" width="200">
        </div>
        """,
        unsafe_allow_html=True
    )

    # 타이틀 중앙 정렬
    st.markdown("<h2 style='text-align: center;'>All in One Calculator</h2>", unsafe_allow_html=True)

    # 사용자 정보 입력
    st.write("### 사용자 정보 입력")
    name = st.text_input("성함")
    age = st.number_input("연령", min_value=0, max_value=120, step=1)
    gender = st.radio("성별", ["남성", "여성"])
    manager = st.selectbox("담당 관리자", ["강성현", "이동훈", "나희령", "최근민"])

    # 🔄 새로고침 버튼
    if st.button("🔄 새로고침"):
        st.session_state.clear()  # 모든 세션 데이터 초기화
        st.rerun()  # 최신 Streamlit에서 사용하는 새로고침 함수

    # 📄 PDF 다운로드 버튼 (사이드바)
    # === 🔹 PDF 다운로드 ===
    st.write("### 📄 PDF 다운로드")
    pdf_buffer = io.BytesIO()

    def generate_pdf():
        pdf = canvas.Canvas(pdf_buffer, pagesize=A4)
        pdf.setTitle("가계 재무 계산 결과")


        pdf.drawString(100, 800, "가계 재무 계산 결과")
        pdf.drawString(100, 780, f"사용자: {name}")
        pdf.drawString(100, 760, f"연령: {age}세")
        pdf.drawString(100, 740, f"성별: {gender}")
        pdf.drawString(100, 720, f"담당 관리자: {manager}")

        y_position = 680
        selected_menu = st.session_state.selected_menu
        pdf.drawString(100, y_position, f"선택한 계산기: {selected_menu}")
        y_position -= 20

        pdf.drawString(100, y_position, f"{menu_items[selected_menu].split('/')[0]}: ₩{st.session_state.inputs[selected_menu]['value1']:,}")
        y_position -= 20
        pdf.drawString(100, y_position, f"{menu_items[selected_menu].split('/')[1]}: ₩{st.session_state.inputs[selected_menu]['value2']:,}")
        y_position -= 20
        pdf.drawString(100, y_position, f"계산 결과: {st.session_state.inputs[selected_menu]['result']}")

        pdf.save()
        pdf_buffer.seek(0)

    generate_pdf()
    st.download_button(label="📥 PDF 다운로드", data=pdf_buffer, file_name="financial_report.pdf", mime="application/pdf")

    # 하단 텍스트 중앙 정렬
    st.markdown("<div style='text-align: center;'>Made by 인모스트투자자문</div>", unsafe_allow_html=True)

# === 🔹 네비게이션 바 UI (입력 값 유지) ===
selected_menu = st.radio(
    "계산기 선택",
    options=list(menu_items.keys()),
    index=list(menu_items.keys()).index(st.session_state.selected_menu),
    horizontal=True,
    key="menu_selection"
)
st.session_state.selected_menu = selected_menu  # ✅ 새로고침 없이 즉시 반영

# === 🔹 메인 제목 ===
st.title(f"{selected_menu} 계산기")
st.write(f"이 계산기는 {menu_items[selected_menu]} 비율을 계산하는 도구입니다.")

# === 🔹 입력 필드 유지 (세션 상태 저장) ===
col1, col2 = st.columns(2)
with col1:
    value1 = st.number_input(
        f"{menu_items[selected_menu].split('/')[0]} (₩)",
        min_value=0,
        format="%d",
        value=st.session_state.inputs[selected_menu]["value1"],
        step=1000,
        key=f"{selected_menu}_value1"
    )
    st.session_state.inputs[selected_menu]["value1"] = value1
    st.write(f"**입력값:** ₩ {value1:,}")  # ✅ 입력값 표시

with col2:
    value2 = st.number_input(
        f"{menu_items[selected_menu].split('/')[1]} (₩)",
        min_value=0,
        format="%d",
        value=st.session_state.inputs[selected_menu]["value2"],
        step=1000,
        key=f"{selected_menu}_value2"
    )
    st.session_state.inputs[selected_menu]["value2"] = value2
    st.write(f"**입력값:** ₩ {value2:,}")  # ✅ 입력값 표시

# === 🔹 결과 계산 ===
if value2 > 0:
    if selected_menu == "비상예비 자금":
        result = value1 / value2  # ✅ 비상예비 자금은 배수 표시
    else:
        result = (value1 / value2) * 100  # ✅ 나머지는 %로 표시
else:
    result = None

# === 🔹 결과 표시 ===
st.write("### 결과 분석")
if result is not None:
    if selected_menu == "비상예비 자금":
        formatted_result = f"{result:,.2f}배"  # ✅ 배수로 표시
        st.write(f"**{selected_menu} 비율:** {formatted_result}")

        # ✅ 기준 적용 및 메시지 표시
        if result >= 3:
            st.success("✅ 양호: 유동성 자산이 총 지출의 3배 이상입니다.")
        elif 1 <= result < 3:
            st.warning("⚠️ 주의: 유동성 자산이 총 지출의 1~3배입니다.")
        else:
            st.error("❌ 위험: 유동성 자산이 총 지출의 1배 미만입니다.")
    else:
        formatted_result = f"{result:,.2f}%"
        st.write(f"**{selected_menu} 비율:** {formatted_result}")

        # ✅ 기준 적용 및 메시지 표시
        if selected_menu == "가계수지":
            if result < 80:
                st.success("✅ 양호: 생활비가 가계소득의 80% 미만입니다.")
            else:
                st.warning("⚠️ 주의: 생활비가 가계소득의 80% 이상입니다.")

        elif selected_menu == "저축성향":
            if result >= 30:
                st.success("✅ 양호: 저축률이 30% 이상입니다.")
            else:
                st.warning("⚠️ 주의: 저축률이 10~30% 미만입니다.")

        elif selected_menu == "보장성보험":
            if result >= 10:
                st.success("✅ 양호: 보장성 보험료가 총 소득의 10% 이상입니다.")
            else:
                st.warning("⚠️ 주의: 보장성 보험료가 총 소득의 10~20% 미만입니다.")

        elif selected_menu == "노후대비":
            if result >= 0.5:
                st.success("✅ 양호: 노후대비 저축 비율이 0.5 이상입니다.")
            else:
                st.warning("⚠️ 주의: 노후대비 저축 비율이 0~0.5 미만입니다.")

        elif selected_menu == "부채비율":
            if result < 40:
                st.success("✅ 양호: 부채비율이 40% 미만입니다.")
            else:
                st.warning("⚠️ 주의: 부채비율이 40~50% 미만입니다.")

        elif selected_menu == "투자성향":
            if result >= 0.2:
                st.success("✅ 양호: 투자 자산이 총 자산의 20% 이상입니다.")
            else:
                st.warning("⚠️ 주의: 투자 자산이 총 자산의 14~20% 미만입니다.")



# %%
