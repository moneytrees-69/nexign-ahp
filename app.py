import streamlit as st
import pandas as pd
import plotly.express as px

# Íàñòðîéêà ñòðàíèöû
st.set_page_config(page_title="Nexign: Ìàòðèöà ïîçèöèîíèðîâàíèÿ", layout="wide")

# Çàãîëîâîê
st.title("Ñòðàòåãè÷åñêèé àíàëèç B2B-âåíäîðîâ (AHP)")
st.markdown("Èçìåíÿéòå âåñà êðèòåðèåâ â áîêîâîé ïàíåëè, ÷òîáû óâèäåòü, êàê ìåíÿåòñÿ ëèäåð ðûíêà â çàâèñèìîñòè îò ïðèîðèòåòîâ çàêàç÷èêà.")

# Äàííûå íàøåé ìàòðèöû (ñûðûå áàëëû îò 1 äî 5)
data = {
    'Âåíäîð': ['Amdocs', 'Netcracker', 'Matrixx', 'Bercut', 'Nexign'],
    'Ñóâåðåíèòåò è Áåçîïàñíîñòü': [1, 1, 1, 5, 5],
    'Highload-ìàñøòàá (Tier-1)': [5, 5, 3, 3, 5],
    'Agility (Time-to-Market)': [2, 4, 5, 3, 4],
    'Ýôôåêòèâíîñòü TCO': [1, 2, 3, 5, 4]
}
df = pd.DataFrame(data)

# Áîêîâàÿ ïàíåëü äëÿ ïîëçóíêîâ
st.sidebar.header("Âåñà êðèòåðèåâ")
st.sidebar.markdown("Íàñòðîéòå âàæíîñòü êàæäîãî ïàðàìåòðà äëÿ êëèåíòà:")

# Ïîëçóíêè (ïîëüçîâàòåëü ìîæåò ñòàâèòü ëþáûå çíà÷åíèÿ îò 0 äî 100)
w1 = st.sidebar.slider('Ñóâåðåíèòåò (On-premise)', 0, 100, 35)
w2 = st.sidebar.slider('Highload-ìàñøòàá', 0, 100, 30)
w3 = st.sidebar.slider('Agility (Time-to-Market)', 0, 100, 20)
w4 = st.sidebar.slider('Ýôôåêòèâíîñòü TCO', 0, 100, 15)

# Àâòîìàòè÷åñêàÿ ìàòåìàòè÷åñêàÿ íîðìàëèçàöèÿ (÷òîáû ñóììà âåñîâ áûëà 100%)
total_weight = w1 + w2 + w3 + w4
if total_weight == 0:
    st.warning("Ïîæàëóéñòà, óñòàíîâèòå õîòÿ áû îäèí êðèòåðèé áîëüøå 0.")
    st.stop()

nw1 = w1 / total_weight
nw2 = w2 / total_weight
nw3 = w3 / total_weight
nw4 = w4 / total_weight

# Ïîêàçûâàåì ïîëüçîâàòåëþ ðåàëüíûå ïðîöåíòû
st.sidebar.markdown("---")
st.sidebar.markdown("**Èòîãîâûå âåñà (íîðìàëèçîâàííûå):**")
st.sidebar.markdown(f"??? Ñóâåðåíèòåò: **{nw1*100:.1f}%**")
st.sidebar.markdown(f"?? Highload: **{nw2*100:.1f}%**")
st.sidebar.markdown(f"?? Agility: **{nw3*100:.1f}%**")
st.sidebar.markdown(f"?? TCO: **{nw4*100:.1f}%**")

# Ðàñ÷åò ñðåäíåâçâåøåííîãî èòîãîâîãî áàëëà
df['Èòîãîâûé áàëë'] = (
    df['Ñóâåðåíèòåò è Áåçîïàñíîñòü'] * nw1 +
    df['Highload-ìàñøòàá (Tier-1)'] * nw2 +
    df['Agility (Time-to-Market)'] * nw3 +
    df['Ýôôåêòèâíîñòü TCO'] * nw4
)

# Îêðóãëÿåì äî äâóõ çíàêîâ ïîñëå çàïÿòîé è ñîðòèðóåì
df['Èòîãîâûé áàëë'] = df['Èòîãîâûé áàëë'].round(2)
df = df.sort_values(by='Èòîãîâûé áàëë', ascending=False)

# Íàñòðàèâàåì öâåòà äëÿ ãðàôèêà (Âûäåëÿåì Nexign èõ ôèðìåííûì çåëåíûì-íåîíîâûì öâåòîì)
color_map = {
    'Nexign': '#CCFF00',  # ßðêèé íåîí
    'Amdocs': '#4A4A4A',  # Ñòðîãèé ñåðûé äëÿ êîíêóðåíòîâ
    'Netcracker': '#4A4A4A',
    'Matrixx': '#4A4A4A',
    'Bercut': '#4A4A4A'
}

# Ñòðîèì êðàñèâûé ãðàôèê
fig = px.bar(
    df,
    x='Èòîãîâûé áàëë',
    y='Âåíäîð',
    orientation='h',
    color='Âåíäîð',
    color_discrete_map=color_map,
    text='Èòîãîâûé áàëë'
)

fig.update_layout(
    showlegend=False, 
    yaxis={'categoryorder':'total ascending'},
    xaxis_title="Ñêîð (ìàêñ. 5)",
    yaxis_title="",
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(size=14)
)

fig.update_traces(textposition='outside')

# Âûâîäèì ãðàôèê íà ñòðàíèöó
st.plotly_chart(fig, use_container_width=True)

# Îïöèîíàëüíî: òàáëèöà ñ ñûðûìè äàííûìè âíèçó
with st.expander("Ïîñìîòðåòü èñõîäíóþ ìàòðèöó áàëëîâ (1-5)"):
    st.dataframe(df.drop(columns=['Èòîãîâûé áàëë']), hide_index=True)
