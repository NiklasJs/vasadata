import streamlit as st
import pandas as pd
import seaborn as sns
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import plotly.io as pio

### KPI visualizations ###
def number_card(toptxt, subtext):
    st.markdown("""
    <style>
    .big-font {
        font-size:60px !important;
        line-height:45%;
        text-align:center;
        color:#CDE8E5;
    }
    .under-font {
        font-size:15px;
        text-align:center;
    }
    </style>
    """, unsafe_allow_html=True)
    st.markdown('<p class="big-font">' + str(toptxt) + '</p>', unsafe_allow_html=True)
    st.markdown('<p class="under-font">' + str(subtext) + '</p>', unsafe_allow_html=True)


def number_card_tworow(toptxt, infotext, subtext):
    st.markdown("""
    <style>
    .big-font-two-row {
        font-size:60px !important;
        line-height:45%;
        text-align:center;
        color:#CDE8E5;
    }
    .mid-font {
        font-size:20px;
        text-align:center;
        line-height:100%;
        color:#E4E6EB;
    }
    .under-font {
        font-size:15px;
        text-align:center;
        line-height:100%;
    }
    </style>
    """, unsafe_allow_html=True)
    st.markdown('<p class="big-font-two-row">' + str(toptxt) + '</p>', unsafe_allow_html=True)
    st.markdown('<p class="mid-font">' + str(infotext) + '</p>', unsafe_allow_html=True)
    st.markdown('<p class="under-font">' + str(subtext) + '</p>', unsafe_allow_html=True)


def number_card_tworow_seg_table(bigtext, smalltext):
    st.markdown("""
    <style>
    .big-font-two-seg {
        font-size:30px !important;
        line-height:45%;
        text-align:center;
        color:#202A44;
    }
    .small-font-two-seg {
        font-size:14px;
        text-align:center;
        line-height:100%;
        color:#A7A8A9;
    }
    </style>
    """, unsafe_allow_html=True)
    st.markdown('<p class="big-font-two-seg">' + str(bigtext) + '</p>', unsafe_allow_html=True)
    st.markdown('<p class="small-font-two-seg">' + str(smalltext) + '</p>', unsafe_allow_html=True)


### Segment summary cards ###
# Standard Discount
def segment_card_sd(data, auto_expand=True):
    if 'other' in data.segment.unique()[0].lower():
        segment_card_sd_other_seg(data, auto_expand=auto_expand)
    else:
        segment_card_sd_single_bucket(data)


def segment_card_sd_single_bucket(data):
    st.markdown("""
    <style>
    .seg-header {
        font-size:20px !important;
        text-align:center;
        color:#FFFFFF;
        background-color:#396976;
    }
    </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown('<p class="seg-header">' + str(data.segment.unique()[0]) + '</p>', unsafe_allow_html=True)
    # Info Panel
    tot_veh = len(data)
    med_lp = int(round(data['new_model_lp'].median() / 1000, 0))
    min_lp = int(round(data['new_model_lp'].min() / 1000, 0))
    max_lp = int(round(data['new_model_lp'].max() / 1000, 0))
    model_sd_dec_share = 100 * round(sum(data['new_model_sd_pct'] >= data['model_sd_pct']) / tot_veh, 2)
    only_sd_frac_new = (len(data[data.new_ad >= 0]) / tot_veh) * 100
    only_sd_frac_old = (len(data[data.ad >= 0]) / tot_veh) * 100

    st.code(f'''
Vehicles: {tot_veh}
Model LP k Median (Min/Max): {med_lp} ({min_lp},{max_lp})
SD Model % (Old): {-round(data.new_model_sd_pct.median(), 2)} ({-round(100 * data.model_sd.sum() / data.model_lp.sum(), 2)})
SD Options % (Old): {-round(data.new_options_sd_pct.median(), 2)} ({-round(100 * data.options_sd.sum() / data.options_lp.sum(), 2)})
SD Total % (Old) {-round(100 * data.new_sd.sum() / data.new_tlp.sum(), 2)} ({-round(100 * data.sd.sum() / data.tlp.sum(), 2)})
Deals at SD only % (Old): {round(only_sd_frac_new, 1)} ({round(only_sd_frac_old, 1)})
    ''')

    with st.expander('Show Detailed Plot'):
        # st.pyplot(plot_option_net_scatter(data))
        st.plotly_chart(plot_option_net_scatter_plotly(data), use_container_width=True)
        st.info(
            'Lines show new (filled) and old (dashed) SD level.\n The Dots above the line indicate deals that will sell to SD only')


def segment_card_sd_other_seg(data, auto_expand=True):
    st.markdown("""
        <style>
        .seg-other-header {
            font-size:20px !important;
            text-align:center;
            color:#FFFFFF;
            background-color:#53565A;
        }
        </style>
        """, unsafe_allow_html=True)

    # Header
    st.markdown('<p class="seg-other-header">' + data.segment.unique()[0] + '</p>', unsafe_allow_html=True)
    # Info Panel
    st.code(f'''
Vehicles: {len(data)}
Buckets: {len(data.model_name.unique())}
SD Model New: {-round(data.new_model_sd_pct.median(), 2)}%
    ''')

    # Bucket Expander
    if auto_expand:
        expand_buckets = len(data.model_name.unique()) < 4
    else:
        expand_buckets = False

    with st.expander('Show Included Models', expand_buckets):
        # TODO Create groupby object and sort on counts before printing
        for bucket in data.model_name.unique():
            st.write(f'{bucket}, {len(data[data.model_name == bucket])} vehicles')


### TARGET CARDS ###
def result_card(result, target, subtext):
    st.markdown("""
    <style>
    .big-font-two-row-neg {
        font-size:60px !important;
        line-height:45%;
        text-align:center;
        color:#C4001A;
    }
    .big-font-two-row-pos {
        font-size:60px !important;
        line-height:45%;
        text-align:center;
        color:#47962D;
    }
    .mid-font {
        font-size:20px;
        text-align:center;
        line-height:100%;
        color:#A7A8A9;
    }
    .under-font {
        font-size:15px;
        text-align:center;
        line-height:100%;
    }
    </style>
    """, unsafe_allow_html=True)
    if result > 0:
        st.markdown('<p class="big-font-two-row-pos">' + str(result) + '</p>', unsafe_allow_html=True)
    else:
        st.markdown('<p class="big-font-two-row-neg">' + str(result) + '</p>', unsafe_allow_html=True)
    st.markdown('<p class="mid-font">' + str(target) + '</p>',
                unsafe_allow_html=True)
    st.markdown('<p class="under-font">' + str(subtext) + '</p>', unsafe_allow_html=True)


def option_rule_card(rule):
    st.markdown("""
        <style>
        .rule-header {
            font-size:20px !important;
            text-align:center;
            color:#FFFFFF;
            background-color:#396976;
        }
        </style>
        """, unsafe_allow_html=True)

    # Header
    st.markdown('<p class="rule-header">' + rule['desc'] + '</p>', unsafe_allow_html=True)
    # Info Panel
    st.code(f'''
    Models: {rule['segments']}
    Value: {rule['value']}
    Take Rate%: {rule['take_rate']} 
        ''')


def res_card_model(name, new_tlp, old_tlp, new_tns, old_tns, new_tsr, old_tsr):
    st.markdown("""
        <style>
        .res_card-header {
            font-size:20px !important;
            text-align:center;
            color:#FFFFFF;
            background-color:#396976;
        }
        </style>
        """, unsafe_allow_html=True)

    # Header
    st.markdown('<p class="res_card-header">' + name + '</p>', unsafe_allow_html=True)
    # Info Panel
    st.code(f'''
    List Price: {new_tlp} ({old_tlp})
    TSR %: {new_tsr} ({old_tsr})
    Net Sales: {new_tns} ({old_tns}) 
        ''')


def volume_card(data, tpin):
    st.markdown("""
        <style>
        .seg-header {
            font-size:20px !important;
            text-align:center;
            color:#FFFFFF;
            background-color:#396976;
        }
        .sub-header-volcard {
            font-size:15px !important;
            text-align:center;
            color:#FFFFFF;
            background-color:#96B0B6;
        }
        </style>
        """, unsafe_allow_html=True)

    # Header
    seg = data.segment.unique()[0]
    st.markdown('<p class="seg-header">' + str(seg) + '</p>', unsafe_allow_html=True)
    units = {}
    with st.expander(f'Edit Volumes, current units: {data.units.sum():.0f}', False):
        for i, cust_size in enumerate(data.deals_size_basket.unique()):
            tmp = data[data.deals_size_basket == cust_size].copy()
            st.markdown('<p class="sub-header-volcard">'+f'Customer Segment: {cust_size}'+'</p>', unsafe_allow_html=True)
            units[cust_size] = st.number_input(f'Units: {tmp.units.sum()} | NS: {tmp.new_tns.sum():.0f} | TSR%%: {-tmp.new_tsr_pct.sum():.1f}:',
                                               value=int(tpin.loc[tpin.deals_size_basket==cust_size, 'units'].sum()))

    return units


### Heatmaps & Graphs
# Heatmap
def plot_pp_ecp_heatmap(dd,
                        sort_order_axles=['42 Tractor', '42 Rigid', '62 Tractor', '62 Rigid', '82 Rigid', '44 Tractor',
                                          '44 Rigid', '64 Tractor', '64 Rigid', '84 Tractor', '84 Rigid', '104 Rigid',
                                          '66 Tractor', '66 Rigid', '86 Rigid', '106 Rigid'],
                        sort_order_models=['FL', 'FE', 'FM', 'FMX', 'FH13', 'FH16'],
                        threshold=40):
    def custom_round(x, base=500, divider=1):
        if math.isnan(x): return np.nan
        if divider != 1: return round(((base * round(float(x) / base)) / divider), 1)
        return int(base * round(float(x) / base))

    def plot_heatmap_axis(data, ax, title, show_yaxis=True, fmt='.0f', cmap='Blues'):
        sns.heatmap(data, ax=ax, cmap=cmap, annot=True, annot_kws={"fontsize": 15}, fmt=fmt, cbar=False,
                    linewidths=0.05,
                    linecolor='#d8d7d5', robust=True)
        ax.set_title(title, fontsize=15)
        ax.set_xlabel('')
        ax.set_ylabel('')
        ax.xaxis.set_tick_params(labelsize=15)
        if show_yaxis:
            ax.yaxis.set_tick_params(labelsize=15, rotation=0)
        else:
            ax.set_yticks([])

    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(25, 8))

    # Only include items that are in the dataset
    sort_order_models = [x for x in sort_order_models if x in dd.model.unique()]

    # Filters all with amount less than threshold
    fltr = dd.pivot_table(index='model_axles_type', values='market_pp', aggfunc='count').reindex(
        sort_order_axles).market_pp > threshold

    # Make the tables required for the heatmap
    d1 = dd.pivot_table(index='model_axles_type', columns='model', values='market_pp', aggfunc='mean').reindex(
        sort_order_axles)[sort_order_models].applymap(lambda x: custom_round(x, base=500, divider=1000))[fltr]
    d2 = dd.pivot_table(index='model_axles_type', columns='model', values='market_ecp', aggfunc='mean').reindex(
        sort_order_axles)[sort_order_models].applymap(lambda x: custom_round(x, base=500, divider=1000))[fltr]
    d3 = dd.pivot_table(index='model_axles_type', columns='model', values='market_ecp', aggfunc='count').reindex(
        sort_order_axles)[sort_order_models][fltr]

    plot_heatmap_axis(d1, ax1, 'Avg. Market Pricepoint (thousands)', fmt='.1f', cmap='Blues')
    plot_heatmap_axis(d2, ax2, 'Avg. Invoiced Price (thousands)', show_yaxis=False, fmt='.1f', cmap='Greens')
    plot_heatmap_axis(d3, ax3, 'Sold Units', show_yaxis=False, cmap='Oranges')

    return fig


def plot_option_net_scatter(data, figsize=(5, 4)):
    fig, ax = plt.subplots(figsize=figsize)

    dd = pd.DataFrame()
    # Add datapoints
    dd['net_sales'] = data.market_ecp / 1000
    dd['option_content'] = (data.options_lp + data.pca_lp + data.services_lp) / 1000

    sns.scatterplot(data=dd, x='option_content', y='net_sales', ax=ax)

    # self.data.to_csv(self.name+'.csv')

    # Add lineplot for SD New
    xlim = ax.get_xlim()
    model_net = (data.new_model_lp.median() / 1000) * (
            1 + (data.new_model_sd_pct.median() / 100))
    start = xlim[0] * (1 + (data.new_options_sd_pct.median() / 100)) + model_net
    end = xlim[1] * (1 + (data.new_options_sd_pct.median() / 100)) + model_net
    plt.plot(xlim, [start, end], linewidth=2)

    # Add lineplot for SD old
    xlim = ax.get_xlim()
    model_net = (data.model_lp.median() / 1000) * (1 + (data.model_sd_pct.median() / 100))
    start = xlim[0] * (1 + (data.options_sd_pct.median() / 100)) + model_net
    end = xlim[1] * (1 + (data.options_sd_pct.median() / 100)) + model_net
    plt.plot(xlim, [start, end], linewidth=1, linestyle='--', color='grey')

    plt.xlabel('Options Content (k)')
    plt.ylabel('Net Sales (k)')

    return fig


def plot_option_net_scatter_plotly(data):
    dd = pd.DataFrame()

    # Should be changed to be global

    # deals_size_basket_min = deals_size_basket.str.split(pat="-|\+").str[0].astype(float)

    # Add datapoints
    dd['net_sales'] = (data.new_tlp + data.new_tsr) / 1000
    dd['option_content'] = (data.new_options_lp + data.new_pca_lp + data.new_services_lp) / 1000
    dd['Customer Name'] = data.end_customer_name
    dd['Order Number'] = data.order_number
    dd['TSR%'] = -data.new_tsr_pct / 100
    dd['Customer Size'] = data.deals_size_basket

    dd['net_sales'] = (data.tlp + data.tsr) / 1000
    dd['option_content'] = (data.options_lp + data.pca_lp + data.services_lp) / 1000
    dd['TSR%'] = -data.tsr_pct / 100

    # st.write(dd.head())

    # Reorder data based on deals_size_basket (mainly for the legend order in plotly)
    active_basket = [basket for basket in ['-0', '1-2', '3-5', '6-10', '11-30', '31-99', '100+', 'Private dealer stock order', 'Unknown'] if
                     basket in dd['Customer Size'].unique()]
    # st.write(active_basket)
    # st.write(dd['Customer Size'].unique())
    dd['Customer Size'] = dd['Customer Size'].astype('category').cat.reorder_categories(active_basket, ordered=True)
    dd = dd.sort_values('Customer Size')
    xmin = dd['option_content'].min() * 0.85
    xmax = dd['option_content'].max() / 0.85
    ymin = dd['net_sales'].min() * 0.85
    ymax = dd['net_sales'].max() / 0.85

    # fig = px.scatter(dd, x="option_content", y="net_sales", color='Customer Size',
    #                  hover_data={'option_content': False,
    #                              'net_sales': False,
    #                              'Customer Size': False,
    #                              'Customer Name': True,
    #                              'Order Number': True,
    #                              'TSR%': ':.2%'})
    color_discrete_map_dict_keys = ['-0', '1-2', '3-5', '6-10', '11-30', '31-99', '100+']
    color_discrete_map_dict_values = px.colors.qualitative.Plotly
    pio.templates[pio.templates.default].layout.colorway = ['#E1DFDD', '#396976', '#96B0B6', '#B8DeD8', '#50A294',
                                                            '#C8E691', '#78B833']

    # color_discrete_map_dict_values = px.colors.diverging.Portland()

    # st.write(color_discrete_map_dict_values)
    color_discrete_map_dict = dict(zip(color_discrete_map_dict_keys, color_discrete_map_dict_values))

    fig = px.scatter(dd, x="option_content", y="net_sales", color='Customer Size',
                     #  color_discrete_map = color_discrete_map_dict,
                     hover_data={'option_content': False,
                                 'net_sales': False,
                                 'Customer Size': False,
                                 'Customer Name': True,
                                 'Order Number': True,
                                 #'TSR%': ':.2%' removed due to not beeing true TSR, it is excluding CA/EII
                                 })

    # Prettify the markers
    # # Fix the color of markers
    # fig.update_traces(marker=dict(size=9, color='#1f77b4',
    #                               line=dict(width=1, color='white')),
    #                   selector=dict(mode='markers'))

    fig.update_traces(marker=dict(size=9, line=dict(width=1, color='white')),
                      selector=dict(mode='markers'))

    # Add button
    fig.update_layout(
        updatemenus=[
            dict(
                type="buttons",
                direction="up",
                buttons=list([
                    dict(
                        # args=['color_discrete_map', color_discrete_map_dict],
                        args=[{'marker.color': color_discrete_map_dict}],
                        label="Yes",
                        method="update"
                    ),
                    dict(
                        args=[{'marker.color': "#1f77b4"}],
                        label="No",
                        method="update"
                    )
                ]),
                pad={"l": 20, "r": 0, "t": 0},
                showactive=True,
                # x=0.13,
                # xanchor="left",
                # y=1.11,
                # yanchor="middle",
                x=1,
                xanchor="left",
                y=0.2,
                yanchor="middle",
            ),
        ],
        font=dict(
            size=16
        )
    )

    # Add annotation
    fig.add_annotation(x=1, y=0.2,
                       font=dict(
                           size=16
                       ),
                       text="Color",
                       showarrow=False,
                       xshift=20,
                       yshift=50,
                       xref="paper", xanchor="left",
                       yref="paper", yanchor="middle")

    fig.update_layout(
        plot_bgcolor="white",
        margin=dict(
            l=0,
            r=10,
            b=0,
            t=40,
            pad=4),
    )

    fig.update_xaxes(range=[xmin, xmax],
                     title_text="Options Content (k)",
                     title_font=dict(size=20),
                     tickfont=dict(size=18),
                     ticks='outside',
                     showline=True,
                     linecolor='black',
                     mirror=True,
                     linewidth=1.5)

    fig.update_yaxes(range=[ymin, ymax],
                     title_text="Net Sales (k)",
                     title_font=dict(size=20),
                     tickfont=dict(size=18),
                     mirror=True,
                     ticks='outside',
                     showline=True,
                     linecolor='black',
                     linewidth=1.5)

    # Add lineplot for SD New
    shrinkage_factor = 0.9  # Shorten the solid line to avoid overlap with dashed line
    model_net = (data.new_model_lp.median() / 1000) * (
            1 + (data.new_model_sd_pct.median() / 100))
    start = xmin / shrinkage_factor * (1 + (data.new_options_sd_pct.median() / 100)) + model_net
    end = xmax * shrinkage_factor * (1 + (data.new_options_sd_pct.median() / 100)) + model_net
    fig.add_shape(type="line",
                  xref="x", yref="y",
                  x0=xmin / shrinkage_factor, y0=start, x1=xmax * shrinkage_factor, y1=end,
                  line=dict(
                      color="#1f77b4",
                      width=3
                  ),
                  )

    # Add lineplot for SD old

    model_net = (data.model_lp.median() / 1000) * (1 + (data.model_sd_pct.median() / 100))
    start = xmin * (1 + (data.options_sd_pct.median() / 100)) + model_net
    end = xmax * (1 + (data.options_sd_pct.median() / 100)) + model_net
    fig.add_shape(type="line",
                  xref="x", yref="y",
                  x0=xmin, y0=start, x1=xmax, y1=end,
                  line=dict(
                      dash="dash",
                      width=1.5
                  ),
                  )

    return fig