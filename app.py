import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter

st.set_page_config(page_title='Cuba NM | Gasoline Analysis', layout='wide')
NAVY='#1f385c'; BLUE='#4080c7'; RED='#e04f4d'; GREEN='#40a66b'; YELLOW='#f5b833'; PURPLE='#8c33bf'
prices=[3.949,4.399,4.339,4.339,4.599,4.979]
stations=['Conoco','Speedway','Circle K',"Daily’s Convenience Store",'Marathon','Buds Oil']
locations=['US-550 / NM-537 Junction','6475 Main St.','6401 Highway 550','6350 Hwy 550','6454 Main St.','Regina, NM']
price_cuba=4.45; price_nm=4.0163
barrels=21683000; population=2130256; total=barrels*42
commute_nm=23.5; commute_cuba=29
factor=commute_cuba/commute_nm
use_nm=total/population; use_cuba=use_nm*factor
income_cuba=24855; income_nm=36218; income_us=43289
expense_nm=use_nm*price_nm; expense_cuba=use_cuba*price_cuba
burden_nm=100*expense_nm/income_nm; burden_cuba=100*expense_cuba/income_cuba
burden_us=3.08

def chart(labels, values, colors, title, ylabel, fmt, ymax=None, width=.55):
    fig, ax=plt.subplots(figsize=(8,3.7), layout='constrained')
    bars=ax.bar(labels,values,color=colors,width=width)
    ax.set_title(title,color=NAVY,fontweight='bold',pad=14)
    ax.set_ylabel(ylabel)
    ax.set_ylim(0,ymax or max(values)*1.25)
    ax.grid(axis='y',alpha=.18); ax.set_axisbelow(True)
    ax.spines[['top','right']].set_visible(False)
    ax.bar_label(bars,labels=[fmt(v) for v in values],padding=4,color=NAVY,fontweight='bold')
    st.pyplot(fig); plt.close(fig)

st.title('Gasoline and Transportation in Cuba, New Mexico')
st.caption('ENG220 | Peace Engineering Project | Javas Maria')
st.write('Explore gasoline prices, fuel consumption and transportation affordability in Cuba, New Mexico.')
sections=['Gasoline prices','Quantity and cost','Gasoline consumption','Income and cost burden','Commute and expenses']
tabs=st.tabs(sections)
with tabs[0]:
    st.header('Gasoline prices – Cuba, New Mexico')
    a,b,c=st.columns(3)
    a.metric('Cuba area average',f'${price_cuba:.2f}/gal'); b.metric('New Mexico average',f'${price_nm:.4f}/gal'); c.metric('Difference',f'${price_cuba-price_nm:.2f}/gal')
    fig,ax=plt.subplots(figsize=(9,4.5),layout='constrained')
    bars=ax.barh(stations,prices,color=[GREEN if p<4.30 else YELLOW if p<=4.50 else RED for p in prices],height=.65)
    ax.invert_yaxis(); ax.set_xlim(0,5.8); ax.set_xlabel('Gasoline price ($/gallon)'); ax.set_title('Price comparison by gas station',color=NAVY,fontweight='bold')
    ax.axvline(price_cuba,color=NAVY,linestyle='--',label='Cuba average'); ax.axvline(price_nm,color=PURPLE,linestyle=':',label='NM average')
    ax.bar_label(bars,labels=[f'${p:.3f}' for p in prices],padding=4,fontweight='bold'); ax.grid(axis='x',alpha=.15); ax.set_axisbelow(True); ax.legend(loc='lower center',bbox_to_anchor=(.5,-.28),ncol=2)
    st.pyplot(fig); plt.close(fig)
    st.dataframe(pd.DataFrame({'Gas Station':stations,'Location':locations,'Price ($/gal)':[f'${p:.3f}' for p in prices]}),hide_index=True,use_container_width=True)
    st.info(f'Lowest: ${min(prices):.3f} | Highest: ${max(prices):.3f} | Station price spread: ${max(prices)-min(prices):.3f}')
    st.caption('Green: below $4.30 | Yellow: $4.30–$4.50 | Red: above $4.50. Prices are the project’s reported snapshot, not live prices.')
with tabs[1]:
    st.header('Gasoline quantity and cost comparison')
    gallons=[5,10,15,20]; costs=[g*price_cuba for g in gallons]
    chart([str(g) for g in gallons],costs,['#a6d1f2','#66a6de',BLUE,'#1f4d8c'],'Cost of gasoline by quantity','Total cost ($)',lambda v:f'${v:.2f}',105)
    st.dataframe(pd.DataFrame({'Gasoline quantity':[f'{g} gallons' for g in gallons],'Price per gallon':[f'${price_cuba:.2f}']*4,'Total cost':[f'${v:.2f}' for v in costs]}),hide_index=True,use_container_width=True)
    st.info('Each additional 5 gallons costs $22.25 at $4.45 per gallon.')
    st.subheader('Interactive fuel calculator')
    quantity=st.slider('Gallons to purchase',0,40,15)
    price=st.number_input('Price per gallon ($)',min_value=0.0,max_value=20.0,value=price_cuba,step=.01)
    st.metric('Total fuel cost',f'${quantity*price:.2f}')
    st.caption('Calculator inputs do not change the baseline research graphs.')
with tabs[2]:
    st.header('Gasoline consumption and transportation')
    st.caption('New Mexico transportation sector | 2024 data')
    chart(['New Mexico'],[total/1e6],[BLUE],'Annual motor gasoline consumption','Million gallons',lambda v:f'{v:,.3f} million gallons',1100,.38)
    chart(['New Mexico','Cuba (Estimated)'],[use_nm,use_cuba],[BLUE,RED],'Estimated annual gasoline use per person','Gallons / person / year',lambda v:f'{v:.1f} gal',650)
    st.info(f'NM: {use_nm:.1f} gal/person/year | Cuba estimate: {use_cuba:.1f} gal/person/year')
    with st.expander('View calculation and assumptions'):
        st.write(f'New Mexico: {barrels:,} barrels × 42 = {total:,} gallons. Divide by {population:,} residents to obtain {use_nm:.2f} gallons per person.')
        st.write(f'Cuba estimate: {use_nm:.2f} × (29 / 23.5) = {use_cuba:.2f} gallons per person per year.')
        st.write('This model assumes fuel consumption scales with average commute time. It is not measured local fuel consumption and does not account for vehicle efficiency, non-work trips or differences in driving speed.')
with tabs[3]:
    st.header('Income and gasoline cost burden')
    chart(['Cuba','New Mexico','United States'],[income_cuba,income_nm,income_us],[RED,BLUE,GREEN],'Average annual per capita income','Annual income ($)',lambda v:f'${v:,.0f}',52000)
    chart(['Cuba (Est.)','NM (Est.)','USA (Reported)'],[burden_cuba,burden_nm,burden_us],[RED,BLUE,GREEN],'Annual income spent on gasoline','Percent of income (%)',lambda v:f'{v:.2f}%',12)
    st.info('Cuba and NM: calculated estimates | USA: supplied comparison')
    st.write(f'Estimated Cuba gasoline burden: {burden_cuba:.2f}% of per capita income, versus {burden_nm:.2f}% for New Mexico.')
    st.caption('The 3.08% national figure is supplied in the original project; its source and comparability with per-capita estimates have not been independently verified.')
with tabs[4]:
    st.header('Commute time and gasoline expenses')
    chart(['New Mexico','Cuba'],[commute_nm,commute_cuba],[BLUE,RED],'Average one-way commute time','Minutes',lambda v:f'{v:.1f} min',36)
    chart(['New Mexico (Est.)','Cuba (Est.)'],[expense_nm,expense_cuba],[BLUE,RED],'Estimated annual gasoline expenses per person','Annual gasoline cost ($)',lambda v:f'${v:,.2f}',2900)
    st.info(f'Cuba average commute: {(factor-1)*100:.1f}% longer than NM')
    st.subheader('Transportation energy analysis')
    st.dataframe(pd.DataFrame({'Metric':['NM total gallons','NM gallons/person','Cuba estimated gallons/person','Commute increase','Cuba annual gasoline expense','NM annual gasoline expense','Cuba income spent on gas','NM income spent on gas'],'Value':[f'{total:,}',f'{use_nm:.2f}',f'{use_cuba:.2f}',f'{(factor-1)*100:.2f}%',f'${expense_cuba:,.2f}',f'${expense_nm:,.2f}',f'{burden_cuba:.2f}%',f'{burden_nm:.2f}%']}),hide_index=True,use_container_width=True)
with st.expander('Project sources and limitations'):
    st.markdown('''Sources listed in the project slides (not independently verified here):
- iExit App, Gas Prices in Cuba, New Mexico; AAA Gas Prices, New Mexico Average Gas Prices (November 2026).
- U.S. EIA, SEDS Table F15: Motor Gasoline Consumption Estimates (2024).
- U.S. Census Bureau, State Population Totals: 2020–2025; New Mexico QuickFacts.
- Census Reporter, Cuba, NM Profile (ACS 2024 5-year data); U.S. Census Bureau, Income in the United States: 2024.

The Cuba fuel-use and expense figures are modeled estimates, not household survey results. The original MATLAB inputs and formulas are retained.''')
