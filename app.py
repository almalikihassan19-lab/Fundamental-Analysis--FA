import streamlit as st
import yfinance as yf

st.set_page_config(page_title="Fundamental Aktieanalys", layout="wide")

st.title("📊 Fundamentalanalys & Sektorscanner")
st.write("Skriv in en aktieticker nedan för att granska bolaget, dess risker och konkurrenter.")

ticker_input = st.text_input("Ticker (t.ex. AAPL, MSFT, TSLA, VOLV-B.ST):", "AAPL").upper().strip()

if ticker_input:
    try:
        stock = yf.Ticker(ticker_input)
        info = stock.info

        st.subheader(f"{info.get('longName', ticker_input)} ({info.get('currency', 'USD')})")
        col_m1, col_m2, col_m3 = st.columns(3)
        col_m1.write(f"**Sektor:** {info.get('sector', 'N/A')}")
        col_m2.write(f"**Bransch:** {info.get('industry', 'N/A')}")
        mcap = info.get('marketCap')
        col_m3.write(f"**Börsvärde:** {mcap:,}" if mcap else "**Börsvärde:** N/A")

        pe = info.get("trailingPE")
        fwd_pe = info.get("forwardPE")
        curr_ratio = info.get("currentRatio")
        margin = info.get("profitMargins")
        fcf = info.get("freeCashflow")

        st.markdown("---")
        st.subheader("1. Centrala Nyckeltal")
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("P/E (Historiskt)", f"{pe:.1f}" if pe else "N/A")
        c2.metric("Forward P/E (Prognos)", f"{fwd_pe:.1f}" if fwd_pe else "N/A")
        c3.metric("Balanslikviditet", f"{curr_ratio:.2f}" if curr_ratio else "N/A")
        c4.metric("Vinstmarginal", f"{margin * 100:.1f}%" if margin else "N/A")

        st.markdown("---")
        st.subheader("🚩 Identifierade Varningsflaggor")
        flags = []
        if curr_ratio and curr_ratio < 1.0:
            flags.append(f"Kortfristig likviditetsrisk: Balanslikviditeten är {curr_ratio:.2f} (< 1.0). Bolaget kan få svårt att betala kortfristiga skulder.")
        if margin and margin < 0:
            flags.append("Negativ vinstmarginal: Företaget går med förlust på sista raden.")
        if fcf and fcf < 0:
            flags.append("Negativt kassaflöde: Företagets verksamhet genererar inte positivt kassaflöde efter nödvändiga investeringar.")
        if pe and pe > 50:
            flags.append(f"Mycket hög värdering: P/E-talet ligger på {pe:.1f}, vilket ställer extrema krav på framtida vinsttillväxt.")

        if flags:
            for flag in flags:
                st.error(flag)
        else:
            st.success("Inga uppenbara primära varningsflaggor på grundläggande nyckeltal.")

        st.markdown("---")
        col_left, col_right = st.columns(2)
        sector = info.get("sector", "")

        with col_left:
            st.subheader("🏢 Konkurrenter & Sektor")
            st.write(f"Bolaget tillhör sektorn: **{sector}**")
            if "Technology" in sector:
                st.write("- **Konkurrenter:** Microsoft (MSFT), Alphabet/Google (GOOGL), Apple (AAPL)")
            elif "Consumer Cyclical" in sector:
                st.write("- **Konkurrenter:** Amazon (AMZN), Walmart (WMT), Tesla (TSLA)")
            elif "Energy" in sector:
                st.write("- **Konkurrenter:** ExxonMobil (XOM), Chevron (CVX), Equinor (EQNR)")
            elif "Industrials" in sector:
                st.write("- **Konkurrenter:** Caterpillar (CAT), Volvo (VOLV-B.ST), ABB (ABB.ST)")
            else:
                st.write("- Jämför nyckeltalen mot ledande aktörer inom samma delbransch.")

        with col_right:
            st.subheader("⚡ Kritiska Resursbehov")
            if "Technology" in sector:
                st.write("- **Humankapital:** Ingenjörer och mjukvaruutvecklare.")
                st.write("- **Infrastruktur:** Datacenter, molnkapacitet och mikrochips.")
                st.write("- **Energi:** Oavbruten elförsörjning till serverhallar.")
            elif "Energy" in sector:
                st.write("- **Naturresurser:** Oljefält, gasfyndigheter och utvinningslicenser.")
                st.write("- **Kapital & Utrustning:** Mycket höga investeringar i borriggar och raffinaderier.")
            elif "Industrials" in sector or "Consumer Cyclical" in sector:
                st.write("- **Råvaror:** Stål, metaller, batterimineraler och komponenter.")
                st.write("- **Logistik:** Globala fraktkedjor och distributionsnätverk.")
            else:
                st.write("- Rörelsekapital och säker tillgång till branschspecifika råvaror och arbetskraft.")

    except Exception:
        st.error(f"Kunde inte hitta eller analysera tickern '{ticker_input}'. Säkerställ att förkortningen stämmer.")
