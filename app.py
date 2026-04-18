import streamlit as st
import pandas as pd
import plotly.express as px

# Настройка страницы
st.set_page_config(page_title="Nexign: Матрица позиционирования", layout="wide")

st.title("Стратегический анализ B2B-вендоров (AHP)")

# ДОБАВЛЕН НОВЫЙ ТЕКСТ ПО ТВОЕМУ ЗАПРОСУ
st.markdown("""
Изменяйте веса критериев в боковой панели, чтобы увидеть, как меняется лидер рынка в зависимости от приоритетов заказчика. 

*Данная интерактивная визуализация представляет собой средневзвешенную стратегическую модель (фреймворк McKinsey), рассчитанную с помощью математического метода AHP (Метод анализа иерархий Томаса Саати).*
""")

# Сырые данные
data = {
    'Вендор': ['Amdocs', 'Netcracker', 'Matrixx', 'Bercut', 'Nexign'],
    'Суверенитет и Безопасность': [1, 1, 1, 5, 5],
    'Highload-масштаб (Tier-1)': [5, 5, 3, 3, 5],
    'Agility (Time-to-Market)': [2, 4, 5, 3, 4],
    'Эффективность TCO': [1, 2, 3, 5, 4]
}
df = pd.DataFrame(data)

st.sidebar.header("Веса критериев")
st.sidebar.markdown("Настройте важность каждого параметра для клиента:")

# Инициализация памяти для кнопки сброса
if 'w1' not in st.session_state: st.session_state.w1 = 35
if 'w2' not in st.session_state: st.session_state.w2 = 30
if 'w3' not in st.session_state: st.session_state.w3 = 20
if 'w4' not in st.session_state: st.session_state.w4 = 15

# Функция сброса
def reset_sliders():
    st.session_state.w1 = 35
    st.session_state.w2 = 30
    st.session_state.w3 = 20
    st.session_state.w4 = 15

# Кнопка сброса
st.sidebar.button("🔄 Сбросить по умолчанию", on_click=reset_sliders)

# Ползунки
w1 = st.sidebar.slider('Суверенитет (On-premise)', 0, 100, key='w1')
w2 = st.sidebar.slider('Highload-масштаб', 0, 100, key='w2')
w3 = st.sidebar.slider('Agility (Time-to-Market)', 0, 100, key='w3')
w4 = st.sidebar.slider('Эффективность TCO', 0, 100, key='w4')

# Нормализация
total_weight = w1 + w2 + w3 + w4
if total_weight == 0:
    st.warning("Пожалуйста, установите хотя бы один критерий больше 0.")
    st.stop()

nw1 = w1 / total_weight
nw2 = w2 / total_weight
nw3 = w3 / total_weight
nw4 = w4 / total_weight

st.sidebar.markdown("---")
st.sidebar.markdown("**Итоговые веса (нормализованные):**")
st.sidebar.markdown(f"🛡️ Суверенитет: **{nw1*100:.1f}%**")
st.sidebar.markdown(f"⚙️ Highload: **{nw2*100:.1f}%**")
st.sidebar.markdown(f"🚀 Agility: **{nw3*100:.1f}%**")
st.sidebar.markdown(f"💰 TCO: **{nw4*100:.1f}%**")

# Математика Саати
df['Итоговый балл'] = (
    df['Суверенитет и Безопасность'] * nw1 +
    df['Highload-масштаб (Tier-1)'] * nw2 +
    df['Agility (Time-to-Market)'] * nw3 +
    df['Эффективность TCO'] * nw4
)

df['Итоговый балл'] = df['Итоговый балл'].round(2)
df = df.sort_values(by='Итоговый балл', ascending=False)

color_map = {
    'Nexign': '#CCFF00',
    'Amdocs': '#4A4A4A',
    'Netcracker': '#4A4A4A',
    'Matrixx': '#4A4A4A',
    'Bercut': '#4A4A4A'
}

fig = px.bar(
    df,
    x='Итоговый балл',
    y='Вендор',
    orientation='h',
    color='Вендор',
    color_discrete_map=color_map,
    text='Итоговый балл'
)

# Настройка графика
fig.update_layout(
    showlegend=False, 
    yaxis={'categoryorder':'total ascending'},
    xaxis_title="Скор (макс. 5)",
    yaxis_title="",
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(size=14),
    transition_duration=500 
)

fig.update_traces(textposition='outside')

st.plotly_chart(fig, use_container_width=True)

with st.expander("Посмотреть исходную матрицу баллов (1-5)"):
    st.dataframe(df.drop(columns=['Итоговый балл']), hide_index=True)
