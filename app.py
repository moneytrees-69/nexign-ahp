import streamlit as st
import pandas as pd
import plotly.express as px

# Настройка страницы
st.set_page_config(page_title="Nexign: Матрица позиционирования", layout="wide")

# Заголовок
st.title("Стратегический анализ B2B-вендоров (AHP)")
st.markdown("Изменяйте веса критериев в боковой панели, чтобы увидеть, как меняется лидер рынка в зависимости от приоритетов заказчика.")

# Данные нашей матрицы (сырые баллы от 1 до 5)
data = {
    'Вендор': ['Amdocs', 'Netcracker', 'Matrixx', 'Bercut', 'Nexign'],
    'Суверенитет и Безопасность': [1, 1, 1, 5, 5],
    'Highload-масштаб (Tier-1)': [5, 5, 3, 3, 5],
    'Agility (Time-to-Market)': [2, 4, 5, 3, 4],
    'Эффективность TCO': [1, 2, 3, 5, 4]
}
df = pd.DataFrame(data)

# Боковая панель для ползунков
st.sidebar.header("Веса критериев")
st.sidebar.markdown("Настройте важность каждого параметра для клиента:")

# Ползунки (пользователь может ставить любые значения от 0 до 100)
w1 = st.sidebar.slider('Суверенитет (On-premise)', 0, 100, 35)
w2 = st.sidebar.slider('Highload-масштаб', 0, 100, 30)
w3 = st.sidebar.slider('Agility (Time-to-Market)', 0, 100, 20)
w4 = st.sidebar.slider('Эффективность TCO', 0, 100, 15)

# Автоматическая математическая нормализация (чтобы сумма весов была 100%)
total_weight = w1 + w2 + w3 + w4
if total_weight == 0:
    st.warning("Пожалуйста, установите хотя бы один критерий больше 0.")
    st.stop()

nw1 = w1 / total_weight
nw2 = w2 / total_weight
nw3 = w3 / total_weight
nw4 = w4 / total_weight

# Показываем пользователю реальные проценты
st.sidebar.markdown("---")
st.sidebar.markdown("**Итоговые веса (нормализованные):**")
st.sidebar.markdown(f"🛡️ Суверенитет: **{nw1*100:.1f}%**")
st.sidebar.markdown(f"⚙️ Highload: **{nw2*100:.1f}%**")
st.sidebar.markdown(f"🚀 Agility: **{nw3*100:.1f}%**")
st.sidebar.markdown(f"💰 TCO: **{nw4*100:.1f}%**")

# Расчет средневзвешенного итогового балла
df['Итоговый балл'] = (
    df['Суверенитет и Безопасность'] * nw1 +
    df['Highload-масштаб (Tier-1)'] * nw2 +
    df['Agility (Time-to-Market)'] * nw3 +
    df['Эффективность TCO'] * nw4
)

# Округляем до двух знаков после запятой и сортируем
df['Итоговый балл'] = df['Итоговый балл'].round(2)
df = df.sort_values(by='Итоговый балл', ascending=False)

# Настраиваем цвета для графика (Выделяем Nexign их фирменным зеленым-неоновым цветом)
color_map = {
    'Nexign': '#CCFF00',  # Яркий неон
    'Amdocs': '#4A4A4A',  # Строгий серый для конкурентов
    'Netcracker': '#4A4A4A',
    'Matrixx': '#4A4A4A',
    'Bercut': '#4A4A4A'
}

# Строим красивый график
fig = px.bar(
    df,
    x='Итоговый балл',
    y='Вендор',
    orientation='h',
    color='Вендор',
    color_discrete_map=color_map,
    text='Итоговый балл'
)

fig.update_layout(
    showlegend=False, 
    yaxis={'categoryorder':'total ascending'},
    xaxis_title="Скор (макс. 5)",
    yaxis_title="",
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(size=14)
)

fig.update_traces(textposition='outside')

# Выводим график на страницу
st.plotly_chart(fig, use_container_width=True)

# Опционально: таблица с сырыми данными внизу
with st.expander("Посмотреть исходную матрицу баллов (1-5)"):
    st.dataframe(df.drop(columns=['Итоговый балл']), hide_index=True)
