import plotly.express as px


def create_countries_plot(df_countries, feature, title):
    fig = px.choropleth(
        data_frame=df_countries,
        locations=df_countries.index,
        locationmode="USA-states",
        color=feature,
        scope="usa",
        hover_name=df_countries["state_name"],
        #                     hover_data =["text"],
        title=title,
        #                     projection = 'conic equidistant'
        color_continuous_scale=px.colors.sequential.BuGn,
        width=900,
        height=700,
    )
    fig.update_layout(template="plotly_dark")
    return fig


def create_category_plot(df_categories, feature, title):
    df_categories.sort_values(by=feature, ascending=False, inplace=True)
    fig = px.bar(
        df_categories,
        x=df_categories.index,
        y=feature,
        color=feature,
        title=title,
        color_continuous_scale=px.colors.sequential.BuGn,
        labels=dict(index="Categories"),
        width=800,
        height=600,
    )
    fig.update_layout(template="plotly_dark")
    return fig

