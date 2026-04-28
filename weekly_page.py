import streamlit as st


def render_weekly_config_page():
    st.markdown(
        '<div class="top-titlebar">Programmazione settimanale - Configurazione scenario</div>',
        unsafe_allow_html=True,
    )

    weekly_toolbar = st.container(key="weekly_top_toolbar", width="stretch")
    with weekly_toolbar:
        left_actions, right_chip = st.columns([6.2, 1.1], gap="small")

        with left_actions:
            btn_save_col, btn_new_col, btn_dup_col, btn_sim_col, btn_opt_col = st.columns(
                [1.25, 1.5, 1.4, 1.7, 2.0],
                gap="small",
            )
            with btn_save_col:
                if st.button("Salva scenario", width="stretch", key="weekly_btn_save"):
                    # TODO: implementare salvataggio scenario settimanale reale.
                    pass
            with btn_new_col:
                if st.button("Nuovo scenario v", width="stretch", key="weekly_btn_new"):
                    pass
            with btn_dup_col:
                if st.button("Duplica scenario", width="stretch", key="weekly_btn_duplicate"):
                    pass
            with btn_sim_col:
                if st.button("Esegui simulazione", width="stretch", type="primary", key="weekly_btn_run_simulation"):
                    # TODO: collegare la simulazione settimanale a logiche reali.
                    pass
            with btn_opt_col:
                if st.button(
                    "Esegui ottimizzazione",
                    width="stretch",
                    disabled=True,
                    key="weekly_btn_run_optimization",
                ):
                    # TODO: collegare l'ottimizzazione settimanale al solver.
                    pass

        with right_chip:
            st.markdown(
                '<div class="top-chip" style="margin-top:0; margin-right:-2px; float:right">Scenario A v</div>',
                unsafe_allow_html=True,
            )

    weekly_left_col, weekly_right_col = st.columns([0.82, 2.18], gap="medium")

    with weekly_left_col:
        with st.container(key="weekly_left_panel", width="stretch"):
            with st.container(key="weekly_import_panel", width="stretch"):
                st.markdown('<div class="weekly-panel-head">Import dati</div>', unsafe_allow_html=True)
                st.markdown('<div class="weekly-panel-body"></div>', unsafe_allow_html=True)
                st.markdown('<div class="weekly-field-label">File / dati base settimana</div>', unsafe_allow_html=True)
                file_col, upload_col = st.columns([2.95, 1.05], gap="small")
                with file_col:
                    st.markdown(
                        '<div class="weekly-file-chip">conferimenti_settimana_14.xlsx</div>',
                        unsafe_allow_html=True,
                    )
                with upload_col:
                    with st.container(key="weekly_upload_btn", width="stretch"):
                        if st.button("Upload", width="stretch", key="weekly_btn_upload"):
                            # TODO: integrare import dati reale da file e controlli formato.
                            pass
                st.markdown(
                    """
                    <div class="weekly-import-state">
                        <span>Stato import</span>
                        <span class="weekly-status-badge weekly-status-badge-ok">Completato</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with st.container(key="weekly_rules_panel", width="stretch"):
                st.markdown('<div class="weekly-panel-head">Vincoli giornalieri di scenario</div>', unsafe_allow_html=True)
                st.markdown(
                    """
                    <div class="weekly-panel-body">
                        <div class="weekly-rule-note">Default modificabile</div>
                        <div class="weekly-rule"><span class="weekly-rule-label">Numero max conferimenti/giorno</span><span class="weekly-rule-value">18</span></div>
                        <div class="weekly-rule-note">Default modificabile</div>
                        <div class="weekly-rule"><span class="weekly-rule-label">Volume max/giorno</span><span class="weekly-rule-value">420 t</span></div>
                        <div class="weekly-rule-note">Default modificabile</div>
                        <div class="weekly-rule"><span class="weekly-rule-label">Limite COD/giorno</span><span class="weekly-rule-value">12.500 kg</span></div>
                        <div class="weekly-rule"><span class="weekly-rule-label">Concentrazione COD uscita</span><span class="weekly-rule-value">0,85</span></div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                if st.button("Altre impostazioni...", width="stretch", key="weekly_btn_other_settings"):
                    pass

            with st.container(key="weekly_checks_panel", width="stretch"):
                st.markdown('<div class="weekly-panel-head">Controlli di coerenza</div>', unsafe_allow_html=True)
                st.markdown(
                    """
                    <div class="weekly-panel-body">
                        <span class="weekly-status-badge weekly-status-badge-alert">2 criticita</span>
                        <ul class="weekly-issues">
                            <li>Volume conferito mercoledi superiore al limite giornaliero</li>
                        </ul>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                if st.button("Apri dettaglio controlli", width="stretch", key="weekly_btn_open_checks"):
                    # TODO: aprire dettaglio completo dei controlli di coerenza.
                    pass

    with weekly_right_col:
        weekly_right_main_box = st.container(key="weekly_right_main_box", width="stretch")
        with weekly_right_main_box:
            with st.container(key="weekly_mode_tabs", width="stretch"):
                sim_col, opt_col, _ = st.columns([1.0, 1.0, 6.0], gap="small")
                with sim_col:
                    if st.button("Simulazione", width="stretch", type="primary", key="weekly_btn_tab_simulation"):
                        pass
                with opt_col:
                    if st.button("Ottimizzazione", width="stretch", key="weekly_btn_tab_optimization"):
                        pass

            st.markdown('<div class="weekly-subtitle">Rifiuti e vincoli settimanali</div>', unsafe_allow_html=True)

            weekly_rows = [
                ("Rif. A", "Cliente 01", "Bio", "780", "120", "120", "Lun"),
                ("Rif. B", "Cliente 02", "TOP", "650", "60", "45", "Mar"),
                ("Rif. C", "Cliente 03", "Bio", "820", "95", "95", "Mer"),
                ("Rif. D", "Cliente 04", "TOP", "540", "40", "25", "Ven"),
                ("Rif. E", "Cliente 05", "Bio", "760", "55", "55", "Gio"),
                ("Rif. F", "Cliente 06", "TOP", "610", "30", "20", "Mar"),
                ("Rif. G", "Cliente 07", "Bio", "790", "75", "60", "Ven"),
            ]
            weekly_table_rows = "".join(
                f"""
                <tr>
                    <td>{rifiuto}</td>
                    <td>{cliente}</td>
                    <td>{tipologia}</td>
                    <td>{cod}</td>
                    <td>{vol_req}</td>
                    <td>{vol_acc}</td>
                    <td><span class="weekly-day-pill">{giorno}</span></td>
                </tr>
                """
                for rifiuto, cliente, tipologia, cod, vol_req, vol_acc, giorno in weekly_rows
            )
            st.markdown(
                f"""
                <div class="weekly-table-wrap">
                    <table class="weekly-table">
                        <thead>
                            <tr>
                                <th>Rifiuto</th>
                                <th>Cliente</th>
                                <th>Tipologia</th>
                                <th>COD mg/kg</th>
                                <th>Vol. rich.</th>
                                <th>Volume accettato</th>
                                <th>Giorno</th>
                            </tr>
                        </thead>
                        <tbody>
                            {weekly_table_rows}
                        </tbody>
                    </table>
                </div>
                """,
                unsafe_allow_html=True,
            )

            summary_col, dayload_col = st.columns([1.0, 1.9], gap="small")
            with summary_col:
                with st.container(key="weekly_summary_box", width="stretch"):
                    st.markdown('<div class="weekly-box-head">Sintesi configurazione</div>', unsafe_allow_html=True)
                    st.markdown(
                        """
                        <div class="weekly-summary-grid">
                            <div class="weekly-summary-card">
                                <div class="weekly-summary-label">Rifiuti importati</div>
                                <div class="weekly-summary-value">184</div>
                            </div>
                            <div class="weekly-summary-card">
                                <div class="weekly-summary-label">Conferimenti obbligatori</div>
                                <div class="weekly-summary-value">2</div>
                            </div>
                            <div class="weekly-summary-card">
                                <div class="weekly-summary-label">Giorni con vincoli specifici</div>
                                <div class="weekly-summary-value">4</div>
                            </div>
                            <div class="weekly-summary-card">
                                <div class="weekly-summary-label">Volumi minimi impostati</div>
                                <div class="weekly-summary-value weekly-summary-value-strong">125 t</div>
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

            with dayload_col:
                with st.container(key="weekly_dayload_box", width="stretch"):
                    st.markdown('<div class="weekly-box-head">Carico preliminare per giorno</div>', unsafe_allow_html=True)
                    st.markdown(
                        """
                        <div class="weekly-dayload-row">
                            <div class="weekly-day-card"><div class="weekly-day-name">Lun</div><div class="weekly-day-metrics">14 conf.<span>380 t</span></div></div>
                            <div class="weekly-day-card"><div class="weekly-day-name">Mar</div><div class="weekly-day-metrics">11 conf.<span>250 t</span></div></div>
                            <div class="weekly-day-card"><div class="weekly-day-name">Mer</div><div class="weekly-day-metrics">17 conf.<span>410 t</span></div></div>
                            <div class="weekly-day-card"><div class="weekly-day-name">Gio</div><div class="weekly-day-metrics">13 conf.<span>300 t</span></div></div>
                            <div class="weekly-day-card"><div class="weekly-day-name">Ven</div><div class="weekly-day-metrics">9 conf.<span>220 t</span></div></div>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

            st.markdown(
                '<div class="weekly-footnote">Mockup di esempio - Programmazione settimanale / Configurazione scenario</div>',
                unsafe_allow_html=True,
            )
